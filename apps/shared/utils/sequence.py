from typing import List
from ..constants import get_blossom_robot, SEQUENCE_DIR
from ..models.sequence import Sequence


def get_all_sequences() -> List[Sequence]:
    return Sequence.get_all_sequences(SEQUENCE_DIR, get_blossom_robot())

def get_sequence_by_name(name: str) -> Sequence | None:
    return next((sequence for sequence in get_all_sequences() if sequence.animation == name), None)