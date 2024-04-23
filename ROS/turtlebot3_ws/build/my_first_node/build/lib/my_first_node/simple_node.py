# simple_node.py
import rclpy
# importamos el modulo Node de la librería ROS2 de python
from rclpy.node import Node

#definimos una funcion basica

def main(args=None):
    #inicializamos la comunicacion ROS
    rclpy.init(args=args)
    #creamos un nodo
    my_node = Node('my_node')
    try:
        #imprimimos un mensaje por el terminal
        my_node.get_logger().info('Los miembros de mi equipo son:')
        # Aqui tienes que poner tu propio codigo
        # crea un diccionario con los nombres de los integrantes
        # de tu equipo y luego crea un iterador para ir imprimiendo estos nombres
        nombres_integrantes = {"Integrante1": "Carlos Martínez", "Integrante2": "Alberto Alonso", "Integrante3": "Pablo Perello", "Integrante4": "Diego Pascual", "Integrante5": "Alejandro Codoñer"}
        for clave, valor in nombres_integrantes.items():
            print(clave, ":", valor)
        # Dejamos abierto el nodo hasta pulsar ctrl+c
        rclpy.spin(my_node)
    except KeyboardInterrupt:
        my_node.get_logger().info('Cerrando el nodo')
    finally:
        #destruimos el nodo
        my_node.destroy_node()
        #cerramos la comunicacion
        rclpy.shutdown()

#definimos el ejecutable
if __name__=='__main__':
  main() # llamada a la funcion
  
