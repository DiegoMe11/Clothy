# Importar mensajes
from nav2_msgs.action import FollowWaypoints
from geometry_msgs.msg import PoseStamped
from clothy_interface.srv import MyWavpointMsg

# Importar biblioteca Python ROS2
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

class WaypointService(Node):
    def __init__(self):
        super().__init__('waypoint_service')
        self.follow_waypoints_client = ActionClient(self, FollowWaypoints, 'follow_waypoints')
        self.srv = self.create_service(MyWavpointMsg, 'waypoints', self.waypoint_service_callback)

    def waypoint_service_callback(self, request, response):
        waypoints = self.define_waypoints()
        self.send_waypoints(waypoints)
        response.success = True
        return response

    def define_waypoints(self):
        waypoints = [self.create_pose_stamped(1.0, 1.0, 1.0), self.create_pose_stamped(2.0, 0.0, 1.0), self.create_pose_stamped(4.0, 0.0, 1.0)]
        return waypoints

    def create_pose_stamped(self, x, y, z):
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.orientation.w = z
        return pose

    def send_waypoints(self, waypoints):
        waypoints_goal = FollowWaypoints.Goal()
        waypoints_goal.poses = waypoints
        self.follow_waypoints_client.wait_for_server()
        self.goal_future = self.follow_waypoints_client.send_goal_async(waypoints_goal)

def main(args=None):
    rclpy.init(args=args)
    waypoint_service = WaypointService()
    try:
        rclpy.spin(waypoint_service)
    except KeyboardInterrupt:
        waypoint_service.get_logger().info('Cerrando el nodo waypoint_service')
    finally:
        waypoint_service.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
