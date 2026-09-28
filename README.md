***👯‍♂️ Simple AI Digital Twin***

An AI-powered Digital Twin prototype that represents a user through their tasks, goals, and preferences and uses an LLM-based AI Agent to recommend what the user should work on next and perform task-related actions.

The system demonstrates a simple Agentic AI workflow where the agent can reason about the user’s context, interact with tools, maintain conversation memory, and make decisions based on priorities, deadlines, goals, and preferences.

---

 **Project Overview**

The project was developed as part of an AI internship task to demonstrate the core concepts of:

* AI Agents
* Tool Calling
* Short-term Memory
* Decision Making
* LangGraph Workflows
* LLM Integration
* User Context / Digital Twin
* Interactive AI Applications

Instead of using hardcoded user information, the application allows the user to create their own Digital Twin through the interface by providing their:

* Name
* Goals
* Preferences
* Tasks
* Task priorities
* Deadlines

The AI Agent then uses this information to understand the user’s current context and determine the most appropriate next action.
---

✨ Features

👤 Digital Twin

Create a personalized Digital Twin containing:

* User name
* Personal goals
* Preferences
* Tasks
* Task priorities
* Task deadlines
* Task status

🧠 AI Agent

The system uses an LLM-powered agent to:

* Understand natural-language requests
* Analyze the user’s context
* Consider task priorities and deadlines
* Consider the user’s goals and preferences
* Recommend what the user should work on next
* Decide when a tool is required

🛠️ Agent Tools

The agent has access to three task-management tools:

get_tasks()

Retrieves the user’s current tasks.

add_task()

Creates a new task with:

* Title
* Priority
* Deadline

update_task()

Updates the status of an existing task.

---

 **Agentic Workflow**

The system is implemented using LangGraph to explicitly orchestrate the agent workflow.

                    ┌──────────────┐
                    │     START    │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │     AGENT    │
                    └──────┬───────┘
                           ↓
                    Need a tool?
                     /          \
                   YES           NO
                    ↓             ↓
              ┌──────────┐   ┌──────────┐
              │  TOOLS   │   │  MEMORY  │
              └────┬─────┘   └────┬─────┘
                   │              ↓
                   └──→ AGENT    END

Workflow Explanation

1. The user sends a natural-language request.
2. The AI Agent analyzes the request and the Digital Twin context.
3. The agent determines whether a tool is required.
4. If a tool is needed, the appropriate tool is executed.
5. The tool result is returned to the agent.
6. The agent uses the result to continue its reasoning.
7. The final response is generated.
8. The interaction is stored in short-term memory.

---

🧠 Memory

The application includes a simple in-memory conversation history.

Each interaction stores:

User Message
      +
Agent Response

Previous interactions are provided to the agent as context for future requests during the same application session.

The current implementation uses in-memory storage only. The memory is reset when the application restarts.

---

🎯 Decision Making

When recommending the next task, the agent considers:

* Task priority
* Deadlines
* User goals
* User preferences
* Current task status

For example, if a user has a high-priority task and several lower-priority tasks, the agent will prioritize the high-priority task according to the system instructions.

---

🖥️ User Interface

The project includes an interactive Streamlit interface.

The user can:

1. Create their Digital Twin.
2. Enter goals and preferences.
3. Add initial tasks.
4. View their current tasks.
5. Chat with the AI Agent.
6. Add new tasks using natural language.
7. Update existing tasks.
8. Ask the agent what they should work on next.

---

 **Technologies Used**

* Python — Core programming language
* OpenAI API — LLM integration and agent reasoning
* GPT-4o — Language model used by the agent
* LangGraph — Agent workflow orchestration
* Pydantic — Data validation and structured models
* Streamlit — Interactive frontend
* python-dotenv — Environment variable management

---

⚙️ Installation

1. Clone the repository

git clone https://github.com/Nada2oo4/ai-digital-twin.git
cd ai-digital-twin

2. Create a virtual environment

python -m venv .venv

Activate it:

Windows:

.venv\Scripts\activate

macOS / Linux:

source .venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Configure the OpenAI API key

Create a .env file in the project root:

OPENAI_API_KEY=your_api_key_here

Do not commit the .env file to GitHub.

---

▶️ Running the Application

Start the Streamlit application with:

python -m streamlit run frontend/ui.py

The application will open in your browser.

---

💬 Example Interaction

<img width="1280" height="800" alt="Screenshot 2026-09-17 at 8 54 24 PM" src="https://github.com/user-attachments/assets/a66c190d-c779-4183-8483-9b4c453f44fa" />
<img width="1280" height="800" alt="Screenshot 2026-09-17 at 8 54 38 PM" src="https://github.com/user-attachments/assets/c91540dd-239a-4932-95cb-fab512431b2e" />




---

🔐 Security

The OpenAI API key is stored using an environment variable:

OPENAI_API_KEY=...

The .env file is excluded from version control through .gitignore.

No API keys or sensitive credentials are included in the repository.

---

 Future Improvements

Possible extensions for a more advanced version include:

*  Voice-based interaction
*  Arabic and bilingual language understanding
* Persistent memory using a database
*  Multi-user support and authentication
*  Calendar integration
*  Task reminders and notifications
*  Productivity analytics
*  More advanced personalized decision-making
*  Semantic search over long-term user history

---

 Internship Project

Developed as part of an AI Internship project to explore practical implementation of Agentic AI, LLM Tool Calling, LangGraph, Memory, and personalized AI workflows.
