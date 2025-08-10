# agent.py
import os
from dotenv import load_dotenv
load_dotenv()

from langchain.agents import Tool, initialize_agent
from langchain.chains.conversation.memory import ConversationBufferMemory
from llm_adapter import LLMAdapter
from tools import draft_email_tool, extract_data_tool, generate_report_tool, create_calendar_event_tool

# If langchain_groq provides ChatGroq integration, prefer it
try:
    from langchain_groq import ChatGroq
    GROQ_AVAILABLE = True
except Exception:
    GROQ_AVAILABLE = False

class AssistantAgent:
    def __init__(self, temperature=0.2):
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.tools = [
            Tool(name="draft_email", func=draft_email_tool, description="Draft a professional email. Input: dict or text."),
            Tool(name="extract_data", func=extract_data_tool, description="Extract structured numbers/money from text."),
            Tool(name="generate_report", func=generate_report_tool, description="Generate a report summary. Input: dict or text."),
            Tool(name="create_calendar_event", func=create_calendar_event_tool, description="Create a calendar event (stub).")
        ]
        self.agent_executor = None
        if GROQ_AVAILABLE:
            model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
            groq_llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name=model_name, temperature=temperature)
            try:
                self.agent_executor = initialize_agent(self.tools, groq_llm, agent="zero-shot-react-description", verbose=False, memory=self.memory,max_iterations=15,max_execution_time=60)
            except Exception as e:
                print("LangChain initialize_agent failed:", e)
                self.agent_executor = None
        self.llm_adapter = LLMAdapter(temperature=temperature)

    def run(self, user_input: str):
        """
        Run the assistant: if LangChain agent is initialized, use it.
        Otherwise, ask LLMAdapter for a JSON plan and execute tools in order.
        """
        if self.agent_executor:
            return self.agent_executor.run(user_input)

        # fallback: ask LLMAdapter to create plan
        messages = [
            {"role":"system", "content":"You are an assistant that returns a JSON list of operations for tools: extract_data, draft_email, generate_report, create_calendar_event."},
            {"role":"user", "content": f"User request: {user_input}\nReturn operations as JSON list: [{'{'}\"tool\":\"tool_name\",\"input\":...{'}'}] in order."}
        ]
        plan_text = self.llm_adapter.chat(messages)
        import json
        ops = []
        try:
            ops_parsed = json.loads(plan_text.strip())
            if isinstance(ops_parsed, list):
                ops = ops_parsed
        except Exception:
            # simple heuristics
            if any(token in user_input.lower() for token in ["$", "revenue", "numbers", "extract"]):
                ops.append({"tool":"extract_data","input":user_input})
            if any(token in user_input.lower() for token in ["email", "draft", "compose"]):
                ops.append({"tool":"draft_email","input":{"recipient":"Acme Corp","subject":"Follow-up","points":["Following up about Q2 report."],"signature":"Puneeth Hegde"}})
            if "report" in user_input.lower():
                ops.append({"tool":"generate_report","input":user_input})
            if any(token in user_input.lower() for token in ["schedule", "meeting", "calendar"]):
                ops.append({"tool":"create_calendar_event","input":{"title":"Meeting","start":"TBD","duration":"30min"}})

        results = {}
        for op in ops:
            t = op.get("tool")
            inp = op.get("input")
            if t == "extract_data":
                results["extract_data"] = extract_data_tool(inp)
            elif t == "draft_email":
                results["draft_email"] = draft_email_tool(inp)
            elif t == "generate_report":
                results["generate_report"] = generate_report_tool(inp)
            elif t == "create_calendar_event":
                results["create_calendar_event"] = create_calendar_event_tool(inp)
        return results
