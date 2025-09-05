from fastapi import FastAPI

from apps.web.sequence import SequenceResponse

# TODO: Complete blockly app to create custom gestures.

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Server is running"}

@app.post("/reset")
async def reset():
    pass

@app.get("/sequences")
async def get_sequences():
    pass

@app.get("/sequences/{sequence_id}")
async def get_sequence(sequence_id: str):
    pass

@app.get("/sequences/names")
async def get_sequence_by_name():
    pass

@app.post("/sequences")
async def create_sequence(sequence: SequenceResponse):
    pass

@app.get("/sequences/{sequence_id}/play")
async def play_sequence(sequence_id: str):
    pass

@app.get("/sequences/{sequence_id}/stop")
async def stop_sequence(sequence_id: str):
    pass

@app.get("/sequences/{sequence_id}/pause")
async def pause_sequence(sequence_id: str):
    pass

@app.post("/sequences/play")
async def play_custom_sequence(sequence: SequenceResponse):
    pass