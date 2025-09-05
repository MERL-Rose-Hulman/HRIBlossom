import uuid
from langchain_core.messages import AIMessage, HumanMessage
from .chatbot.agent import create_chat_agent


def main():
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    chatbot = create_chat_agent()

    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        
        print("Blossom: ", end="", flush=True)
        for chunk, metadata in chatbot.stream(
            {"messages": [HumanMessage(content=user_input)]}, 
            config=config,
            stream_mode="messages"
        ):
            if isinstance(chunk, AIMessage):
                print(chunk.content, end="", flush=True)

        print()


if __name__ == "__main__":
    main()