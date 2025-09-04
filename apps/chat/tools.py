from langchain_core.tools import tool
from apps.shared.utils.sequence import get_all_sequences, get_sequence_by_name


@tool
def get_available_sequences() -> str:
    """Get a list of all available robot sequences/animations that can be performed.
    
    Returns:
        A string containing the names of all available sequences, one per line.
    """
    sequences = get_all_sequences()
    if not sequences:
        return "No sequences available."
    
    sequence_names = [seq.animation for seq in sequences]
    return "\n".join(sequence_names)


@tool
def play_sequence(sequence_name: str) -> str:
    """Play a specific robot sequence/animation by name.
    
    Args:
        sequence_name: The name of the sequence to play (e.g., "happy_dance", "comfort_gesture")
    
    Returns:
        A string indicating whether the sequence was successfully started or if there was an error.
    """
    sequence = get_sequence_by_name(sequence_name)
    if sequence is None:
        available_sequences = get_available_sequences()
        return f"Sequence '{sequence_name}' not found. Available sequences:\n{available_sequences}"
    
    try:
        # Start the sequence in a separate thread
        sequence.start()
        return f"Successfully started sequence: {sequence_name}"
    except (ValueError, RuntimeError, AttributeError) as e:
        return f"Error starting sequence '{sequence_name}': {str(e)}"


@tool
def play_emotional_sequence(emotion: str) -> str:
    """Play a robot sequence that matches a specific emotion.
    
    Args:
        emotion: The emotion to express (e.g., "happy", "sad", "excited", "comforting", "celebratory", "sympathetic")
    
    Returns:
        A string indicating the sequence that was played or an error message.
    """
    # Map emotions to likely sequence names
    emotion_to_sequence = {
        "happy": ["happy", "celebration", "joy", "cheerful"],
        "sad": ["sad", "comfort", "sympathy", "gentle"],
        "excited": ["excited", "energetic", "enthusiastic", "bounce"],
        "comforting": ["comfort", "soothing", "gentle", "calm"],
        "celebratory": ["celebration", "happy", "dance", "cheer"],
        "sympathetic": ["sympathy", "gentle", "comfort", "understanding"],
        "playful": ["playful", "fun", "dance", "bounce"],
        "calm": ["calm", "meditation", "peaceful", "gentle"],
        "encouraging": ["encourage", "support", "positive", "uplifting"]
    }
    
    # Get all available sequences
    all_sequences = get_all_sequences()
    sequence_names = [seq.animation.lower() for seq in all_sequences]
    
    # Find matching sequences for the emotion
    emotion_keywords = emotion_to_sequence.get(emotion.lower(), [emotion.lower()])
    
    matching_sequences = []
    for keyword in emotion_keywords:
        for seq_name in sequence_names:
            if keyword in seq_name:
                matching_sequences.append(seq_name)
    
    if not matching_sequences:
        # Fallback: try to find any sequence that might match
        for seq_name in sequence_names:
            if emotion.lower() in seq_name:
                matching_sequences.append(seq_name)
    
    if not matching_sequences:
        available_sequences = get_available_sequences()
        return f"No sequences found for emotion '{emotion}'. Available sequences:\n{available_sequences}"
    
    # Use the first matching sequence
    selected_sequence = matching_sequences[0]
    return play_sequence(selected_sequence)


@tool
def stop_current_sequence() -> str:
    """Stop any currently playing robot sequence.
    
    Returns:
        A string indicating whether the sequence was successfully stopped.
    """
    try:
        # This would need to be implemented based on how sequences are managed
        # For now, return a placeholder message
        return "Sequence stopping functionality needs to be implemented in the robot control system."
    except (ValueError, RuntimeError, AttributeError) as e:
        return f"Error stopping sequence: {str(e)}"


# List of all available tools for the chatbot
CHATBOT_TOOLS = [
    get_available_sequences,
    play_sequence,
    play_emotional_sequence,
    stop_current_sequence
]
