import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st

from app.data import create_digital_twin
from app.graph import build_graph
from app.models import Task


st.set_page_config(
    page_title="Digital Twin",
    page_icon="👯‍♂️",
    layout="wide"
)


# --------------------------------
# Session State
# --------------------------------

if "digital_twin" not in st.session_state:
    st.session_state.digital_twin = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "setup_goals" not in st.session_state:
    st.session_state.setup_goals = [""]

if "setup_preferences" not in st.session_state:
    st.session_state.setup_preferences = [""]

if "setup_tasks" not in st.session_state:
    st.session_state.setup_tasks = []


# --------------------------------
# Initial Setup
# --------------------------------

if st.session_state.digital_twin is None:

    st.title("👯‍♂️ Digital Twin")

    st.caption(
        "Let's build your personal AI-powered Digital Twin."
    )

    st.divider()

    st.subheader("👤 About You")

    name = st.text_input(
        "What's your name?"
    )

    st.divider()

    st.subheader("🎯 Your Goals")

    goals = []

    for i in range(len(st.session_state.setup_goals)):

        goal = st.text_input(
            f"Goal {i + 1}",
            value=st.session_state.setup_goals[i],
            key=f"goal_{i}"
        )

        goals.append(goal)

    if st.button("➕ Add Goal"):

        st.session_state.setup_goals.append("")

        st.rerun()

    st.divider()

    st.subheader("⚙️ Your Preferences")

    preferences = []

    for i in range(
        len(st.session_state.setup_preferences)
    ):

        preference = st.text_input(
            f"Preference {i + 1}",
            value=st.session_state.setup_preferences[i],
            key=f"preference_{i}"
        )

        preferences.append(preference)

    if st.button("➕ Add Preference"):

        st.session_state.setup_preferences.append("")

        st.rerun()

    st.divider()

    st.subheader("📋 Your Tasks")

    if st.session_state.setup_tasks:

        for i, task in enumerate(
            st.session_state.setup_tasks
        ):

            st.write(
                f"**{i + 1}. {task['title']}** "
                f"— `{task['priority']}`"
            )

            if task["deadline"]:
                st.caption(
                    f"Deadline: {task['deadline']}"
                )

    task_title = st.text_input(
        "Task title",
        key="new_task_title"
    )

    task_priority = st.selectbox(
        "Priority",
        ["high", "medium", "low"],
        key="new_task_priority"
    )

    task_deadline = st.text_input(
        "Deadline (optional)",
        key="new_task_deadline"
    )

    if st.button("➕ Add Task"):

        if task_title.strip():

            st.session_state.setup_tasks.append(
                {
                    "title": task_title.strip(),
                    "priority": task_priority,
                    "deadline": task_deadline.strip() or None
                }
            )

            

            st.rerun()

    st.divider()

    if st.button(
        "✦ Create My Digital Twin",
        type="primary",
        use_container_width=True
    ):

        clean_goals = [
            goal.strip()
            for goal in goals
            if goal.strip()
        ]

        clean_preferences = [
            preference.strip()
            for preference in preferences
            if preference.strip()
        ]

        tasks = [
            Task(
                id=i + 1,
                title=task["title"],
                priority=task["priority"],
                deadline=task["deadline"]
            )
            for i, task in enumerate(
                st.session_state.setup_tasks
            )
        ]

        if not name.strip():

            st.error("Please enter your name.")

        elif not clean_goals:

            st.error("Please enter at least one goal.")

        elif not clean_preferences:

            st.error(
                "Please enter at least one preference."
            )

        elif not tasks:

            st.error(
                "Please add at least one task."
            )

        else:

            st.session_state.digital_twin = (
                create_digital_twin(
                    name=name.strip(),
                    goals=clean_goals,
                    preferences=clean_preferences,
                    tasks=tasks
                )
            )

            st.session_state.messages = []

            st.rerun()


# --------------------------------
# Digital Twin Dashboard
# --------------------------------

else:

    digital_twin = st.session_state.digital_twin

    graph = build_graph()

    st.title("👯‍♂️ Digital Twin")
    st.caption(
        "Your AI-powered personal work assistant"
    )

    st.divider()

    left, right = st.columns([1, 2])

    # ----------------------------
    # Profile
    # ----------------------------

    with left:

        st.subheader("👤 Profile")

        st.markdown(
            f"### {digital_twin.name}"
        )

        st.caption("AI-powered Digital Twin")

        st.divider()

        st.markdown("### 🎯 Goals")

        for goal in digital_twin.goals:
            st.write(f"• {goal}")

        st.divider()

        st.markdown("### ⚙️ Preferences")

        for preference in digital_twin.preferences:
            st.write(f"• {preference}")

        st.divider()

        st.markdown("### 📋 Tasks")

        pending_tasks = [
            task
            for task in digital_twin.tasks
            if task.status == "pending"
        ]

        for task in pending_tasks:

            if task.priority == "high":
                icon = "🔴"
            elif task.priority == "medium":
                icon = "🟡"
            else:
                icon = "🟢"

            st.write(
                f"{icon} **{task.title}**"
            )

            st.caption(
                f"Priority: {task.priority}"
            )

            if task.deadline:
                st.caption(
                    f"Deadline: {task.deadline}"
                )

    # ----------------------------
    # AI Assistant
    # ----------------------------

    with right:

        st.subheader(
            f"Good evening, {digital_twin.name} 👋"
        )

        st.write(
            "Ask your Digital Twin what you should "
            "work on, add a task, or update a task."
        )

        for message in st.session_state.messages:

            with st.chat_message(message["role"]):
                st.write(message["content"])

        user_message = st.chat_input(
            "Ask your Digital Twin..."
        )

        if user_message:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": user_message
                }
            )

            with st.chat_message("user"):
                st.write(user_message)

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

            response = result["final_response"]

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )

            with st.chat_message("assistant"):
                st.write(response)

            st.rerun()