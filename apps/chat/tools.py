from langchain_core.tools import tool
from apps.shared.utils.sequence import get_all_sequences, get_all_sequences_str, get_sequence_by_name


@tool(parse_docstring=True)
def get_available_sequences() -> str:
    """Get a list of all available robot sequences/animations that can be performed.
    
    Returns:
        A string containing the names of all available sequences, one per line.
    """
    # print("Getting available sequences")
    sequences = get_all_sequences()
    if not sequences:
        return "No sequences available."
    
    sequence_names = [seq.animation for seq in sequences]
    return "\n".join(sequence_names)


@tool(parse_docstring=True)
def play_sequence(sequence_name: str) -> str:
    """Play a specific robot sequence/animation by name.
    
    Args:
        sequence_name: The name of the sequence to play (e.g., "happy_dance", "comfort_gesture")
    
    Returns:
        A string indicating whether the sequence was successfully started or if there was an error.
    """
    # print(f"Playing sequence: {sequence_name}")
    sequence = get_sequence_by_name(sequence_name)
    if sequence is None:
        return f"Sequence '{sequence_name}' not found. Available sequences:\n{get_all_sequences_str()}"
    
    try:
        # Start the sequence in a separate thread
        sequence.start()
        return f"Successfully started sequence: {sequence_name}"
    except (ValueError, RuntimeError, AttributeError) as e:
        return f"Error starting sequence '{sequence_name}': {str(e)}"


CHATBOT_TOOLS = [
    get_available_sequences,
    play_sequence,
]
