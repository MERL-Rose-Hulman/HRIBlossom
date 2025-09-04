from typing import List
from apps.shared.constants import BLOSSOM_ROBOT, SEQUENCE_DIR
from apps.shared.models.sequence import Sequence


def get_all_sequences() -> List[Sequence]:
    return Sequence.get_all_sequences(SEQUENCE_DIR, BLOSSOM_ROBOT)

def get_sequence_by_name(name: str) -> Sequence | None:
    return next((sequence for sequence in get_all_sequences() if sequence.animation == name), None)