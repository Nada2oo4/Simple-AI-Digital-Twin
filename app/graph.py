import json
from typing import Any, TypedDict

from langgraph.graph import StateGraph, START, END

from app.models import DigitalTwin
from app.agent import call_llm
from app.tools import add_task, get_tasks, update_task
from app.memory import add_memory, get_memory

class AgentState(TypedDict):
    user_message: str
    digital_twin: DigitalTwin
    input_messages: list
    response: Any
    final_response: str


def agent_node(state: AgentState):

    response = call_llm(
        state["user_message"],
        state["digital_twin"],
        state["input_messages"]
    )

    return {
        "response": response
    }


def tools_node(state: AgentState):

    response = state["response"]

    messages = state["input_messages"] + response.output

    for tool_call in response.output:

        if tool_call.type != "function_call":
            continue

        arguments = json.loads(tool_call.arguments)

        if tool_call.name == "get_tasks":
            result = get_tasks(state["digital_twin"])

        elif tool_call.name == "add_task":
            result = add_task(
                state["digital_twin"],
                **arguments
            )

        elif tool_call.name == "update_task":
            result = update_task(
                state["digital_twin"],
                **arguments
            )

        else:
            result = None

        messages.append(
            {
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": str(result)
            }
        )

    return {
        "input_messages": messages
    }


def should_continue(state: AgentState):

    response = state["response"]

    for item in response.output:
        if item.type == "function_call":
            return "tools"

    return "end"

def memory_node(state: AgentState):

    final_response = state["response"].output_text

    add_memory(
        state["user_message"],
        final_response
    )

    return {
        "final_response": final_response
    }

def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node("agent", agent_node)
    graph.add_node("tools", tools_node)
    graph.add_node("memory", memory_node)
    graph.add_edge(START, "agent")

    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": 'memory'
        }
    )

    graph.add_edge("tools", "agent")
    graph.add_edge('memory', END)

    return graph.compile()