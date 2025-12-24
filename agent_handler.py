# Developed by Waatmani
# Facebook: Facebook.com/waatmani
# Instagram: Instagram.com/waatmanii

import asyncio
import json
import time
import os
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from google.api_core.exceptions import ResourceExhausted

class AgentHandler:
    def __init__(self, provider="gemini"):
        self.provider = provider
        # Initialize API keys
        self.groq_api_key = os.environ.get("GROQ_API_KEY")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.google_api_key = os.environ.get("GOOGLE_API_KEY")
        
        # Fallback models for Gemini
        self.gemini_models = ["gemini-2.0-flash-exp", "gemini-exp-1206"]
        
        print(f"DEBUG: AgentHandler initialized with provider: {self.provider}")

        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        if self.provider == "groq":
            if not self.groq_api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables.")
            print("Initializing Groq Agent...")
            return ChatGroq(model_name="llama-3.3-70b-versatile", api_key=self.groq_api_key)
        
        elif self.provider == "openai":
            if not self.openai_api_key:
                 raise ValueError("OPENAI_API_KEY not found in environment variables.")
            print("Initializing OpenAI Agent...")
            return ChatOpenAI(model="gpt-4o-mini", api_key=self.openai_api_key) # efficient model
            
        elif self.provider == "gemini":
             print("Initializing Gemini Agent...")
             return ChatGoogleGenerativeAI(model=self.gemini_models[0], google_api_key=self.google_api_key)
        
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    async def _decide_action_async(self, task, page_info):
        # Prevent strict Token Limit Exceeded (413) errors
        limited_elements = page_info['actionable_elements'][:50]
        if len(page_info['actionable_elements']) > 50:
             print(f"Warning: Truncating actionable elements from {len(page_info['actionable_elements'])} to 50 to save tokens.")

        prompt = f"""
        You are an autonomous browser agent. Your goal is to complete the following task: "{task}"
        
        CRITICAL: 
        1. You MUST select an action from the provided list of actionable elements.
        2. Do NOT hallucinate actions or IDs. Use ONLY the "geminiId" provided in the JSON below.
        3. Even if the page looks simple, find the most relevant step to move forward.
        4. If you need to click something, return a "click" action.
        5. If you need to type, return a "type" action.
        6. Only return "done" if the task is FULLY completed.

        Here is the current state of the web page:
        URL: {page_info['url']}
        Title: {page_info['title']}
        Summary of visible content: {page_info['content_summary']}

        Here are the actionable elements (buttons, links, inputs):
        {json.dumps(limited_elements, indent=2)}

        Decide the next best action.
        Response JSON Format:
        {{
            "action": {{ "type": "click", "target_gemini_id": "g-ID" }} OR
                      {{ "type": "type", "target_gemini_id": "g-ID", "text": "..." }} OR
                      {{ "type": "navigate", "url": "..." }} OR
                      {{ "type": "done" }},
            "result": "A helpful message to the user explaining what you are doing (e.g., 'I am clicking the Login button...')."
        }}
        """

        messages = [
            HumanMessage(content=prompt) 
        ]

        try:
            print(f"Attempting to use {self.provider}...")
            response = await self.llm.ainvoke(messages)
            response_text = response.content
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            ai_decision = json.loads(response_text)
            return ai_decision
        except Exception as e:
            print(f"{self.provider} failed: {e}.")
            # Basic fallback logic could be re-implemented here if desired, 
            # but per requirements strict separation is implied.
            return {"action": {"type": "error"}, "result": f"{self.provider} failed: {str(e)}"}

    def decide_action(self, task, page_info):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self._decide_action_async(task, page_info))
        finally:
            loop.close()
