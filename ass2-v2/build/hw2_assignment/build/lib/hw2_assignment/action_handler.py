import rclpy
from rclpy.action.client import ActionClient

class ActionHandler(rclpy.node.Node):
    def __init__(self, nodeName):
        super().__init__(nodeName)
        self.done, self.accepted = False, False

    def _response_callback(self, future):
        goal_handle = future.result()
        self.accepted = goal_handle.accepted
        
        newFuture = goal_handle.get_result_async()
        newFuture.add_done_callback(self._result_callback)
    
    def _result_callback(self, future):
        self.done = True


    def do(self, *args, **kwargs):
        # must define self._do() yourself, which returns a goal_msg
        # must also define self._client which is a client for that action type
        goal_msg = self._do(*args, **kwargs)

        self.done, self.accepted = False, False
        self._client.wait_for_server()
        future = self._client.send_goal_async(goal_msg)
        future.add_done_callback(self._response_callback)

        while not self.done:
            rclpy.spin_once(self)
        return (self.done, self.accepted)