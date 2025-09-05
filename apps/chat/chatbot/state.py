from typing import Annotated, List
from pydantic import BaseModel
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


class ChatBotState(BaseModel):
    messages: Annotated[List[BaseMessage], add_messages]