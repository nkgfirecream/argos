import time
import unittest

from parameterized import parameterized

from configs.config_patterns import door_movement
from configs.config_patterns.door_movement import MovementPatterns
from detection.pattern_detector import PatternMatch, PatternDetector
from detection.state_managers.door_state_manager import DoorStates
from detection.state_managers.motion_state_manager import MotionStates
from detection.state_managers.object_state_manager import ObjectStates
from detection.states import StateHistoryStep, NotState


class TestDoorDetect(unittest.TestCase):

    def _real_state_history(self, raw_state_history):
        total_delay = sum([d for (r, d) in raw_state_history])
        real_state_history = []
        t = int(round(time.time())) - total_delay
        for (raw_state, delay) in raw_state_history:
            t += delay
            real_state_history.append(StateHistoryStep(raw_state, ts=t))
        return real_state_history

    @parameterized.expand([
        [[MotionStates.MOTION_OUTSIDE_MASK, DoorStates.DOOR_OPEN, DoorStates.DOOR_CLOSED],
         [(MotionStates.MOTION_INSIDE_MASK, 1),
          (MotionStates.MOTION_INSIDE_MASK, 1),
          (MotionStates.MOTION_OUTSIDE_MASK, 1),
          (MotionStates.MOTION_INSIDE_MASK, 1),
          (DoorStates.DOOR_OPEN, 1),
          (MotionStates.MOTION_INSIDE_MASK, 1),
          (DoorStates.DOOR_CLOSED, 1),
          (MotionStates.MOTION_INSIDE_MASK, 1)],
         PatternMatch.MATCHED
         ],
        [[DoorStates.DOOR_OPEN, MotionStates.MOTION_INSIDE_MASK],
         [(ObjectStates.OBJECT_DETECTED, 1), (DoorStates.DOOR_OPEN, 1), (ObjectStates.OBJECT_DETECTED, 1),
          (DoorStates.DOOR_CLOSED, 1)],
         PatternMatch.PARTIAL_MATCH],
        [[NotState(ObjectStates.OBJECT_DETECTED), DoorStates.DOOR_OPEN, ObjectStates.OBJECT_DETECTED],
         [(MotionStates.MOTION_INSIDE_MASK, 1), (DoorStates.DOOR_OPEN, 1), (ObjectStates.OBJECT_DETECTED, 1),
          (DoorStates.DOOR_CLOSED, 1)],
         PatternMatch.MATCHED],
        [[NotState(ObjectStates.OBJECT_DETECTED), DoorStates.DOOR_OPEN, ObjectStates.OBJECT_DETECTED],
         [(ObjectStates.OBJECT_DETECTED, 1), (DoorStates.DOOR_OPEN, 1), (ObjectStates.OBJECT_DETECTED, 1),
          (DoorStates.DOOR_CLOSED, 1)],
         PatternMatch.NOT_MATCHED],
        [[DoorStates.DOOR_OPEN, NotState(ObjectStates.OBJECT_DETECTED), DoorStates.DOOR_CLOSED],
         [(DoorStates.DOOR_OPEN, 1), (ObjectStates.OBJECT_DETECTED, 1), (DoorStates.DOOR_CLOSED, 1)],
         PatternMatch.NOT_MATCHED],
        [[DoorStates.DOOR_OPEN, NotState(ObjectStates.OBJECT_DETECTED), DoorStates.DOOR_CLOSED],
         [(ObjectStates.OBJECT_DETECTED, 1), (DoorStates.DOOR_OPEN, 1), (MotionStates.MOTION_INSIDE_MASK, 1),
          (DoorStates.DOOR_CLOSED, 1)],
         PatternMatch.MATCHED],
        [[DoorStates.DOOR_OPEN, NotState(ObjectStates.OBJECT_DETECTED), DoorStates.DOOR_CLOSED],
         [(DoorStates.DOOR_OPEN, 1), (ObjectStates.OBJECT_DETECTED, 1), (DoorStates.DOOR_CLOSED, 1),
          (DoorStates.DOOR_OPEN, 1), (MotionStates.MOTION_INSIDE_MASK, 1), (DoorStates.DOOR_CLOSED, 1)],
         PatternMatch.MATCHED],
        [[DoorStates.DOOR_OPEN, DoorStates.DOOR_CLOSED, NotState(ObjectStates.OBJECT_DETECTED)],
         [(DoorStates.DOOR_OPEN, 1), (MotionStates.MOTION_INSIDE_MASK, 1),
          (DoorStates.DOOR_CLOSED, 1), (MotionStates.MOTION_INSIDE_MASK, 1)],
         PatternMatch.MATCHED],
        [[DoorStates.DOOR_OPEN, DoorStates.DOOR_CLOSED, NotState(ObjectStates.OBJECT_DETECTED)],
         [(DoorStates.DOOR_OPEN, 1), (MotionStates.MOTION_INSIDE_MASK, 1),
          (DoorStates.DOOR_CLOSED, 1), (MotionStates.MOTION_INSIDE_MASK, 1), (ObjectStates.OBJECT_DETECTED, 1)],
         PatternMatch.NOT_MATCHED],
        [door_movement.pattern_steps[MovementPatterns.PERSON_ENTERING_DOOR],
         [(ObjectStates.OBJECT_DETECTED, 1), (DoorStates.DOOR_OPEN, 1), (ObjectStates.OBJECT_DETECTED, 1),
          (DoorStates.DOOR_CLOSED, 1)],
         PatternMatch.NOT_MATCHED],
        [door_movement.pattern_steps[MovementPatterns.PERSON_ENTERING_DOOR],
         [(DoorStates.DOOR_OPEN, 1), (ObjectStates.OBJECT_DETECTED, 1), (DoorStates.DOOR_CLOSED, 1)],
         PatternMatch.MATCHED],
        [[NotState(ObjectStates.OBJECT_DETECTED, 2), DoorStates.DOOR_OPEN, ObjectStates.OBJECT_DETECTED],
         [(ObjectStates.OBJECT_DETECTED, 0), (DoorStates.DOOR_OPEN, 1), (ObjectStates.OBJECT_DETECTED, 1),
          (DoorStates.DOOR_CLOSED, 1)],
         PatternMatch.NOT_MATCHED],
        [[NotState(ObjectStates.OBJECT_DETECTED, 1), DoorStates.DOOR_OPEN, ObjectStates.OBJECT_DETECTED],
         [(ObjectStates.OBJECT_DETECTED, 0), (DoorStates.DOOR_OPEN, 4), (ObjectStates.OBJECT_DETECTED, 1),
          (DoorStates.DOOR_CLOSED, 1)],
         PatternMatch.MATCHED],
        [[DoorStates.DOOR_OPEN, DoorStates.DOOR_CLOSED, NotState(ObjectStates.OBJECT_DETECTED, 2)],
         [(DoorStates.DOOR_OPEN, 1), (MotionStates.MOTION_INSIDE_MASK, 1),
          (DoorStates.DOOR_CLOSED, 1), (MotionStates.MOTION_INSIDE_MASK, 1), (ObjectStates.OBJECT_DETECTED, 3)],
         PatternMatch.MATCHED],
        [[DoorStates.DOOR_OPEN, NotState(ObjectStates.OBJECT_DETECTED, 2), DoorStates.DOOR_CLOSED],
         [(DoorStates.DOOR_OPEN, 1), (ObjectStates.OBJECT_DETECTED, 1), (DoorStates.DOOR_CLOSED, 3)],
         PatternMatch.MATCHED],
        [[NotState(ObjectStates.OBJECT_DETECTED, 2), DoorStates.DOOR_OPEN, ObjectStates.OBJECT_DETECTED],
         [(ObjectStates.OBJECT_DETECTED, 1), (DoorStates.DOOR_OPEN, 3), (ObjectStates.OBJECT_DETECTED, 1)],
         PatternMatch.MATCHED],
        [[NotState(ObjectStates.OBJECT_DETECTED, 2), DoorStates.DOOR_OPEN, ObjectStates.OBJECT_DETECTED],
         [(ObjectStates.OBJECT_DETECTED, 0), (MotionStates.MOTION_INSIDE_MASK, 1),
          (MotionStates.MOTION_OUTSIDE_MASK, 1),
          (ObjectStates.OBJECT_DETECTED, 1), (MotionStates.MOTION_INSIDE_MASK, 0), (DoorStates.DOOR_OPEN, 1),
          (ObjectStates.OBJECT_DETECTED, 1),
          (DoorStates.DOOR_CLOSED, 1)],
         PatternMatch.NOT_MATCHED],
        [[NotState(ObjectStates.OBJECT_DETECTED, 1), DoorStates.DOOR_OPEN, ObjectStates.OBJECT_DETECTED],
         [(ObjectStates.OBJECT_DETECTED, 0), (DoorStates.DOOR_OPEN, 1), (ObjectStates.OBJECT_DETECTED, 1),
          (DoorStates.DOOR_CLOSED, 1), (DoorStates.DOOR_OPEN, 1), (ObjectStates.OBJECT_DETECTED, 1),
          (DoorStates.DOOR_CLOSED, 1)],
         PatternMatch.MATCHED],
        [[NotState(ObjectStates.OBJECT_DETECTED, 2), DoorStates.DOOR_OPEN, ObjectStates.OBJECT_DETECTED],
         [(ObjectStates.OBJECT_DETECTED, 0), (DoorStates.DOOR_OPEN, 1), (ObjectStates.OBJECT_DETECTED, 1),
          (DoorStates.DOOR_OPEN, 1), (ObjectStates.OBJECT_DETECTED, 1), (DoorStates.DOOR_CLOSED, 1)],
         PatternMatch.NOT_MATCHED],
        [door_movement.pattern_steps[MovementPatterns.PERSON_EXITING_DOOR],
         [(ObjectStates.OBJECT_DETECTED, 1), (DoorStates.DOOR_OPEN, 1), (ObjectStates.OBJECT_DETECTED, 1),
          (DoorStates.DOOR_CLOSED, 1)],
         PatternMatch.PARTIAL_MATCH],
        [door_movement.pattern_steps[MovementPatterns.PERSON_EXITING_DOOR],
         [(ObjectStates.OBJECT_DETECTED, 1), (DoorStates.DOOR_OPEN, 1), (ObjectStates.OBJECT_DETECTED, 1),
          (DoorStates.DOOR_CLOSED, 1), (MotionStates.MOTION_INSIDE_MASK, 5)],
         PatternMatch.MATCHED],
        [door_movement.pattern_steps[MovementPatterns.PERSON_EXITING_DOOR],
         [(ObjectStates.OBJECT_DETECTED, 1), (DoorStates.DOOR_OPEN, 1), (ObjectStates.OBJECT_DETECTED, 1)],
         PatternMatch.PARTIAL_MATCH],
        [door_movement.pattern_steps[MovementPatterns.PERSON_EXITING_DOOR],
         [(ObjectStates.OBJECT_DETECTED, 1), (DoorStates.DOOR_OPEN, 1), (ObjectStates.OBJECT_DETECTED, 1),
          (DoorStates.DOOR_CLOSED, 1), (ObjectStates.OBJECT_DETECTED, 6)],
         PatternMatch.MATCHED],
    ])
    def test_find_mov_ptn_state_history(self, mov_ptn, state_history, exp_result):
        actual_result = PatternDetector(None, door_movement.pattern_steps, door_movement.pattern_evaluation_order,
                                        detection_interval=None).find_mov_ptn_in_state_history(mov_ptn,
                                                                                               self._real_state_history(
                                                                                                   state_history))
        print("mov_ptn: %s" % mov_ptn)
        print("state_history: %s" % state_history)
        print("actual/expected: %s/%s" % (actual_result, exp_result))
        self.assertEqual(
            actual_result,
            exp_result)
