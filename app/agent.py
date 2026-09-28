import os

from dotenv import load_dotenv
from openai import OpenAI

from app.memory import get_memory
from app.models import DigitalTwin


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


tools = [
    {
        "type": "function",
        "name": "get_tasks",
        "description": "Get all current tasks for the user.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "type": "function",
        "name": "add_task",
        "description": "Add a new task for the user.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the task."
                },
                "priority": {
                    "type": "string",
                    "description": "Task priority: high, medium, or low."
                },
                "deadline": {
                    "type": ["string", "null"],
                    "description": "The deadline exactly as stated by the user, such as 'tomorrow', 'next week', or 'Friday'. Do not convert it to a calendar date."
                }
            },
            "required": ["title", "priority", "deadline"]
        }
    },
    {
        "type": "function",
        "name": "update_task",
        "description": "Update the status of an existing task.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "The ID of the task to update."
                },
                "status": {
                    "type": "string",
                    "description": "The new status of the task, such as pending or completed."
                }
            },
            "required": ["task_id", "status"]
        }
    }
]


def call_llm(
    user_message: str,
    digital_twin: DigitalTwin,
    input_messages: list
):

    memory = get_memory()

    instructions = f"""
You are an AI digital twin assistant.

You are helping {digital_twin.name}.

User goals:
{digital_twin.goals}

User preferences:
{digital_twin.preferences}

previous interactions:
{memory}

The user has access to tools for getting, adding, and updating tasks.

When you need information about the user's tasks, use get_tasks.

When the user asks to add a task, use add_task.

When the user asks to update a task, use update_task.

When recommending what the user should work on next:
- Consider task priority.
- Consider deadlines.
- Consider the user's goals.
- Consider the user's preferences.

- only consider pending tasks when making recommendations.
- choose the highest priority pending task.
- if there are multiple tasks with the same highest priority, choose the one with the earliest deadline.
- never choose a lower priority task over a higher priority task, even if the lower priority task has an earlier deadline.
- Be concise and explain the reason for your recommendation.
- Don't assume or invent the current date.
- If a date is not provided for a task, do not mention a specific date.
- When adding a task, preserve the deadline exactly as the user stated it.
- Do not convert relative deadlines such as "tomorrow" or "next week" into calendar dates.
- Never invent or assume the current date.
"""

    response = client.responses.create(
        model="gpt-4o",
        instructions=instructions,
        input=input_messages,
        tools=tools
    )

    return response