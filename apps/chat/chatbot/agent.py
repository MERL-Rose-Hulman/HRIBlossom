import dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from .prompts import BlossomPrompts
from .state import ChatBotState
from .tools import CHATBOT_TOOLS


dotenv.load_dotenv()
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

    def chatbot_node(state: ChatBotState):
        query = state.messages[-1].content
        response = chain.invoke({"input": query, "history": state.messages})
        return {"messages": [response]}

        
    tools_node = ToolNode(CHATBOT_TOOLS)

    graph = StateGraph(ChatBotState)

    graph.add_node("chatbot", chatbot_node)
    graph.add_node("tools", tools_node)

    graph.add_edge(START, "chatbot")
    
    graph.add_conditional_edges(
        "chatbot",
        tools_condition,
        {
            "tools": "tools",
            END: END
        }
    )

    graph.add_conditional_edges(
        "tools",
        tools_condition,
        {
            "tools": "tools",
            END: END
        }
    )
    
    memory = MemorySaver()
    return graph.compile(checkpointer=memory)