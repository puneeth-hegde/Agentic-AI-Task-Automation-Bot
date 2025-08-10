# llm_adapter.py
import os
from dotenv import load_dotenv
load_dotenv()

try:
    from langchain_groq import ChatGroq
except Exception as e:
    ChatGroq = None

class LLMAdapter:
    def __init__(self, model_name=None, temperature=0.2, max_tokens=1024):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY must be set in .env")
        self.model_name = model_name or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.temperature = temperature
        self.max_tokens = max_tokens
        if ChatGroq is None:
            raise RuntimeError("langchain_groq.ChatGroq is not available. Install langchain-groq.")
        self.client = ChatGroq(groq_api_key=self.api_key, model_name=self.model_name, temperature=self.temperature)

    def chat(self, messages, **kwargs):
        """
        messages: list of {"role":"user"/"system"/"assistant", "content":"..."}
        returns: assistant text (string)
        """
        try:
            resp = self.client.chat(messages=messages, max_tokens=self.max_tokens)
            # many wrappers return dict with 'text' key
            if isinstance(resp, dict) and "text" in resp:
                return resp["text"]
            # or object with .text
            return getattr(resp, "text", str(resp))
        except Exception as e:
            # Fallback: join messages and call generate
            prompt = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages])
            try:
                resp = self.client.generate(prompt=prompt, max_tokens=self.max_tokens, temperature=self.temperature)
                if isinstance(resp, dict) and "text" in resp:
                    return resp["text"]
                return getattr(resp, "text", str(resp))
            except Exception as e2:
                raise RuntimeError(f"LLM call failed: {e} | {e2}")
