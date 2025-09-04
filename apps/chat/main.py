from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from apps.chat.prompts import BlossomPrompts
from apps.chat.state import ChatBotState
from apps.chat.tools import CHATBOT_TOOLS

llm = ChatOpenAI(model="gpt-4o-mini")

def create_chat_agent():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", BlossomPrompts.CHATBOT_SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ]
    )

    llm_with_tools = llm.bind_tools(CHATBOT_TOOLS)

    chain = prompt | llm_with_tools

    llm_with_message_history = RunnableWithMessageHistory(chain, InMemoryChatMessageHistory(), input_messages_key="input", history_messages_key="history")

    def chatbot(state: ChatBotState):
        query = state.messages[-1].content
        return {"messages": [llm_with_message_history.invoke({"input": query})]}

    def response(state: ChatBotState):
        pass

    def get_input_emotion(input: str) -> str:
        messages = [
            SystemMessage(content=BlossomPrompts.GET_INPUT_EMOTION_SYSTEM_PROMPT),
            HumanMessage(content=input),
        ]
        llm_with_structured_output = llm.with_structured_output({"emotion": str})
        emotion = llm_with_structured_output.invoke(messages).emotion
        return {"input_emotion": emotion}

    tools_node = ToolNode(CHATBOT_TOOLS)

    graph = StateGraph(ChatBotState)

    graph.add_node("chatbot", chatbot)
    graph.add_node("get_input_emotion", get_input_emotion)
    graph.add_node("tools", tools_node)
    graph.add_node("response", response)

    graph.add_edge(START, "chatbot")
    graph.add_edge("chatbot", "get_input_emotion")
    graph.add_edge("get_input_emotion", "tools")

    graph.add_conditional_edges(
        "tools",
        tools_condition,
        {
            "tools": "tools",
            END: "response"
        }
    )

    graph.add_edge("response", END)
    
    return graph.compile()