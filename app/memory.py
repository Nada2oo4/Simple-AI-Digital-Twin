conversation_history = []


def add_memory(user_message: str, agent_response: str):
    conversation_history.append({
        "user": user_message,
        "agent": agent_response
    })


def get_memory():
    return conversation_history