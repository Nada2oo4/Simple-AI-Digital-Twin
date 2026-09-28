from app.graph import build_graph, agent_node, tools_node
from app.data import digital_twin



graph = build_graph()

if __name__ == "__main__":

    print(f"Hello {digital_twin.name}!")

    print("\nGoals:")
    for goal in digital_twin.goals:
        print(f"- {goal}")

    print("\nPreferences:")
    for preference in digital_twin.preferences:
        print(f"- {preference}")

    print("\nType 'exit' to quit.")

    while True:

        user_message = input("\nYou: ")

        if user_message.lower() == "exit":
            break

        result = graph.invoke(
            {
                "user_message": user_message,
                "digital_twin": digital_twin,
                "input_messages": [
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            }
        )

        print("\nAgent:", result["response"].output_text)