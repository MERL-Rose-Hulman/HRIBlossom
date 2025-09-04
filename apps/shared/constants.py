from apps.shared.models.robot import BlossomRobot
from apps.shared.models.robot_config import RobotConfig


CONFIG = RobotConfig().config
BLOSSOM_ROBOT = BlossomRobot.from_config(CONFIG)
SEQUENCE_DIR = "gestures/sequences"