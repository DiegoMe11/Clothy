document.addEventListener('DOMContentLoaded', event => {
    console.log("entro en la pagina")
    
    document.getElementById("btn_con").addEventListener("click", connect)
    document.getElementById("btn_dis").addEventListener("click", disconnect)

    document.getElementById("btn_forward").addEventListener("click", () => {
        call_delante_service("delante")
    })

    document.getElementById("btn_backward").addEventListener("click", () => {
        call_delante_service("atras")
    })

    document.getElementById("btn_stop").addEventListener("click", () => {
        call_delante_service("parar")
    })

    document.getElementById("btn_right").addEventListener("click", () => {
        call_delante_service("derecha")
    })

    document.getElementById("btn_left").addEventListener("click", () => {
        call_delante_service("izquierda")
    })

    document.getElementById("btn_publish_initial_pose").addEventListener("click", () => {
        // Obtener las coordenadas de la posición inicial del robot
        let x = parseFloat(document.getElementById('input_x').value);
        let y = parseFloat(document.getElementById('input_y').value);
        let z = parseFloat(document.getElementById('input_z').value);
    
        // Llamar a la función para publicar la posición inicial del robot
        publishInitialPose(x, y, z);
    });

    data = {
        // ros connection
        ros: null,
        rosbridge_address: 'ws://127.0.0.1:9090/',
        connected: false,
        // service information 
          service_busy: false, 
          service_response: ''
        }

    function call_delante_service(valor){
        data.service_busy = true
        data.service_response = ''	
        
        //definimos los datos del servicio
        let service = new ROSLIB.Service({
            ros: data.ros,
            name: '/movement',
            serviceType: 'custom_interface/srv/MyMoveMsg'
        })
        
        let request = new ROSLIB.ServiceRequest({
            move: valor
        })
        
        service.callService(request, (result) => {
            data.service_busy = false
            data.service_response = JSON.stringify(result)
        }, (error) => {
            data.service_busy = false
            console.error(error)
        })	
    }

    function getRobotPositionInGazebo() {
        let modelStateTopic = new ROSLIB.Topic({
            ros: data.ros,
            name: '/gazebo/model_states',
            messageType: 'gazebo_msgs/ModelStates'
        });
    
        modelStateTopic.subscribe(function (message) {
            // Suponiendo que el robot que te interesa es 'turtlebot3'
            let modelName = 'turtlebot3';
            let modelIndex = message.name.indexOf(modelName);
            
            if (modelIndex !== -1) {
                let modelPose = message.pose[modelIndex];
                let modelPosition = modelPose.position;
    
                // Hacer algo con la posición del modelo
                console.log("Posición del robot en Gazebo:");
                console.log("X:", modelPosition.x);
                console.log("Y:", modelPosition.y);
                console.log("Z:", modelPosition.z);
            }
            // Después de obtener la posición, dejamos de suscribirnos para evitar obtener múltiples posiciones.
            modelStateTopic.unsubscribe();
        });
    }
    

    function connect() {
        console.log("Clic en connect");
    
        data.ros = new ROSLIB.Ros({
            url: data.rosbridge_address
        });
    
        // Define callbacks
        data.ros.on("connection", () => {
            data.connected = true;
            console.log("Conexion con ROSBridge correcta");
            
            // Obtener la posición del robot en Gazebo y publicarla en RViz al conectar
            getRobotPositionInGazebo();
        });
    
        data.ros.on("error", (error) => {
            console.log("Se ha producido algún error mientras se intentaba realizar la conexión");
            console.log(error);
        });
    
        data.ros.on("close", () => {
            data.connected = false;
            console.log("Conexion con ROSBridge cerrada");
        });
    }

    function publishInitialPose(x, y, z, linearVelocity, angularVelocity) {
        // Publicar en RViz
        let rvizTopic = new ROSLIB.Topic({
            ros: data.ros,
            name: '/initialpose',
            messageType: 'geometry_msgs/PoseWithCovarianceStamped'
        });
    
        let rvizMessage = new ROSLIB.Message({
            header: {
                stamp: { sec: 0 },
                frame_id: 'map'
            },
            pose: {
                pose: {
                    position: { x: x, y: y, z: z },
                    orientation: { x: 0, y: 0, z: 0, w: 1 }
                }
            }
        });
    
        // Publicar en Gazebo
        let gazeboTopic = new ROSLIB.Topic({
            ros: data.ros,
            name: '/gazebo/set_model_state',
            messageType: 'gazebo_msgs/msg/ModelState'
        });
    
        let gazeboMessage = new ROSLIB.Message({
            model_name: 'turtlebot3',
            pose: {
                position: { x: x, y: y, z: z },
                orientation: { x: 0, y: 0, z: 0, w: 1 }
            },
            twist: {
                linear: { x: linearVelocity, y: 0, z: 0 },
                angular: { x: 0, y: 0, z: angularVelocity }
            }
        });
    
        gazeboTopic.publish(gazeboMessage);
        rvizTopic.publish(rvizMessage);
    }

    function disconnect(){
	      data.ros.close()        
	      data.connected = false
        console.log('Clic en botón de desconexión')
    }    
});