import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.environ.get("GROQ_API_KEY")

user_instruction = "change Screen 3.2's audio narration to a bit formal"

intent_sys_prompt = """You are an Intent Classifier for a highly-precise Instructional Design Document Editor.

Evaluate the USER'S FINAL MESSAGE to determine if they want to EDIT the document or just CHAT.

**CRITICAL RULE: RECENTENCY BIAS**
The user's FINAL message is the ONLY one that matters for intent! Even if the entire chat history was purely conversational greetings, if their final message asks to change, edit, update, or modify ANYTHING about the document, the intent MUST be "EDIT".

**CRITICAL RULE: FOLLOW-UP EDITS**
If the final message uses pronouns or short phrases like "change its ost too", "make that one longer", "fix the spelling there", or "do the next screen", this is an "EDIT" request. Do NOT classify requests to change/fix things as CHAT.

- If intent is "EDIT", do not generate a chat reply.
- If intent is "CHAT" (like greetings, asking how you are, etc.), generate a friendly, natural conversational reply in `chat_reply`.

Respond in JSON format:
{
    "intent": "EDIT" or "CHAT",
    "chat_reply": "Your conversational response if CHAT, otherwise empty string"
}"""

groq_client = Groq(api_key=groq_api_key)
groq_messages = [{"role": "system", "content": intent_sys_prompt}]

# Simulating what the frontend sends in chat_history when chaining commands
chat_history = [
    {"role": "user", "content": "I meant change the osts of all screens of module 2 to be descriptive"},
    {"role": "assistant", "content": "I have updated the On-Screen Text (OST) for all screens in Module 2 to be more descriptive while keeping it concise. Please review the changes."}
]

for msg in chat_history:
    groq_messages.append({"role": msg['role'], "content": msg['content']})
    
groq_messages.append({"role": "user", "content": f"FINAL USER MESSAGE TO CLASSIFY: {user_instruction}"})

intent_response = groq_client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=groq_messages,
    response_format={"type": "json_object"},
    max_tokens=250
)

print(intent_response.choices[0].message.content)
