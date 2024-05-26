import sys
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from nav2_msgs.action import FollowWaypoints
from geometry_msgs.msg import PoseStamped


class WaypointNavigator(Node):
    def __init__(self):
        super().__init__('my_waypoint_follower')
        self.follow_waypoints_client = ActionClient(self, FollowWaypoints, 'follow_waypoints')
       
    def define_waypoints_route_1(self):
        # Define los puntos de ruta (waypoints) para la ruta 1
        waypoints = [
            self.create_pose_stamped(1.0, 0.0, 1.0),
            self.create_pose_stamped(2.0, 0.0, 1.0),
            self.create_pose_stamped(3.0, 0.0, 1.0)
        ]
        return waypoints

    def define_waypoints_route_2(self):
        # Define los puntos de ruta (waypoints) para la ruta 2
        waypoints = [
            self.create_pose_stamped(4.0, 0.0, 1.0),
            self.create_pose_stamped(4.0, -5.0, 1.0),
            self.create_pose_stamped(2.0, -3.0, 1.0)
        ]
        return waypoints

    def define_waypoints_route_3(self):
        # Define los puntos de ruta (waypoints) para la ruta 3
        waypoints = [
            self.create_pose_stamped(1.0, 0.0, 1.0),
            self.create_pose_stamped(2.0, 1.0, 1.0),
            self.create_pose_stamped(3.0, 3.0, 1.0)
        ]
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
        waypoints_goal.poses = waypoints  # Pasar la lista directamente
        self.follow_waypoints_client.wait_for_server()
        self.goal_future = self.follow_waypoints_client.send_goal_async(waypoints_goal, feedback_callback=self.feedback_callback)
        self.goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result}')
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Received feedback: {feedback}')

def main(args=None):
    rclpy.init(args=args)
    waypoint_navigator = WaypointNavigator()

    if len(sys.argv) < 2:
        print("Usage: ros2 run clothy_nav2_system my_waypoint_follower 'ruta 1'|'ruta 2'|'ruta 3'")
        rclpy.shutdown()
        return

    route = sys.argv[1].strip().lower()
    if route == 'ruta 1':
        waypoints = waypoint_navigator.define_waypoints_route_1()
    elif route == 'ruta 2':
        waypoints = waypoint_navigator.define_waypoints_route_2()
    elif route == 'ruta 3':
        waypoints = waypoint_navigator.define_waypoints_route_3()
    else:
        print("Invalid route")
        rclpy.shutdown()
        return

    waypoint_navigator.send_waypoints(waypoints)
    rclpy.spin(waypoint_navigator)

if __name__ == '__main__':
    main()