from rclpy.action.client import ActionClient
from irobot_create_msgs.action import AudioNoteSequence
from hw1_assignment.action_handler import ActionHandler
from irobot_create_msgs.msg import AudioNoteVector, AudioNote

class NoiseNode(ActionHandler):
    def __init__(self, robotName):
        super().__init__("hw1_noise_node")
        self._client = ActionClient(self, AudioNoteSequence, f'/{robotName}/audio_note_sequence')

    def _do(self):
        frequencies = [200, 300, 2000, 1000, 2000]
        notes = [AudioNote() for x in frequencies]
        for i in range(len(notes)):
            notes[i].frequency = frequencies[i]
        note_sequence = AudioNoteVector()
        note_sequence.notes = notes


        goal_msg = AudioNoteSequence.Goal()
        goal_msg.iterations = 5
        goal_msg.note_sequence = note_sequence
        return goal_msg
