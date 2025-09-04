from typing import Annotated, List, Optional
from pydantic import BaseModel
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


class ChatBotState(BaseModel):
    messages: Annotated[List[BaseMessage], add_messages]
    input_emotion: Optional[str] = None