document.addEventListener('DOMContentLoaded', event => {
    console.log("entro en la pagina")
    
    document.getElementById("btn_con").addEventListener("click", connect)
    document.getElementById("btn_dis").addEventListener("click", disconnect)
    document.getElementById("btn_move").addEventListener("click", move)
    document.getElementById("btn_forward").addEventListener("click", moveForward)
    document.getElementById("btn_backward").addEventListener("click", moveBackward)
    document.getElementById("btn_right").addEventListener("click", moveRight)
    document.getElementById("btn_left").addEventListener("click", moveLeft)
    document.getElementById("btn_stop").addEventListener("click", stop)



    data = {
        // ros connection
        ros: null,
        rosbridge_address: 'ws://127.0.0.1:9090/',
        connected: false,
    }

    function connect(){
	      console.log("Clic en connect")
	
	      data.ros = new ROSLIB.Ros({
                url: data.rosbridge_address
        })

        // Define callbacks
        data.ros.on("connection", () => {
            data.connected = true
            console.log("Conexion con ROSBridge correcta")
        })
        data.ros.on("error", (error) => {
            console.log("Se ha producido algun error mientras se intentaba realizar la conexion")
            console.log(error)
        })
        data.ros.on("close", () => {
            data.connected = false
            console.log("Conexion con ROSBridge cerrada")	    	 
        })
    }

    function disconnect(){
	      data.ros.close()        
	      data.connected = false
        console.log('Clic en botón de desconexión')
    }    

    function move() {
        let topic = new ROSLIB.Topic({
            ros: data.ros,
            name: '/cmd_vel',
            messageType: 'geometry_msgs/msg/Twist'
        })
        let message = new ROSLIB.Message({
            linear: {x: 0.1, y: 0, z: 0, },
            angular: {x: 0, y: 0, z: -0.2, },
        })
        topic.publish(message)
    }

    function moveForward() {
        let topic = new ROSLIB.Topic({
            ros: data.ros,
            name: '/cmd_vel',
            messageType: 'geometry_msgs/msg/Twist'
        });
        let message = new ROSLIB.Message({
            linear: {x: 0.1, y: 0, z: 0},
            angular: {x: 0, y: 0, z: 0}
        });
        topic.publish(message);
    }
    function moveBackward() {
        let topic = new ROSLIB.Topic({
            ros: data.ros,
            name: '/cmd_vel',
            messageType: 'geometry_msgs/msg/Twist'
        });
        let message = new ROSLIB.Message({
            linear: {x: -0.1, y: 0, z: 0},
            angular: {x: 0, y: 0, z: 0}
        });
        topic.publish(message);
    }
    
    
    function moveRight() {
        let topic = new ROSLIB.Topic({
            ros: data.ros,
            name: '/cmd_vel',
            messageType: 'geometry_msgs/msg/Twist'
        });
        let message = new ROSLIB.Message({
            linear: {x: 0, y: 0, z: 0},
            angular: {x: 0, y: 0, z: -0.2}
        });
        topic.publish(message);
    }
    
    
    function moveLeft() {
        let topic = new ROSLIB.Topic({
            ros: data.ros,
            name: '/cmd_vel',
            messageType: 'geometry_msgs/msg/Twist'
        });
        let message = new ROSLIB.Message({
            linear: {x: 0, y: 0, z: 0},
            angular: {x: 0, y: 0, z: 0.2}
        });
        topic.publish(message);
    }
    function stop() {
        let topic = new ROSLIB.Topic({
            ros: data.ros,
            name: '/cmd_vel',
            messageType: 'geometry_msgs/msg/Twist'
        });
        let message = new ROSLIB.Message({
            linear: {x: 0, y: 0, z: 0},
            angular: {x: 0, y: 0, z: 0}
        });
        topic.publish(message);
    }
    
    
});