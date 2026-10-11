"""Session 2 — your first LLM call. Run with:  uv run python hello.py"""
import os
from pyexpat.errors import messages
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)   # .env wins over anything an editor put in the environment
client = OpenAI(base_url=os.getenv("BASE_URL"), api_key=os.getenv("API_KEY"))
MODEL = os.getenv("MODEL")

k = os.getenv("API_KEY")
print("key length:", len(k) if k else None, "| starts:", repr(k[:4]) if k else None, "| ends:", repr(k[-2:]) if k else None)
print("base url:", os.getenv("BASE_URL"))

load_dotenv(override=True)

messages = [
    {"role": "system", "content": "You are a helpful assistant for a retail bank."},
    {"role": "user", "content": "Name one thing AI agents can do. One sentence."},
]

print(type(messages), messages)

stream = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    stream=True,
    stream_options={"include_usage": True},
    #max_tokens=100,   #HARD CAP ON THE ANSWER LENGTH
    #temperature=0.0,  # 0 = MOST PREDICTABLE, 1 = MOST VARIED.
    
    #max_tokens=30,     #(truncated text)   #set a hard cap on the answer length, so we don't get a long essay.
    #max_tokens=60,
    max_tokens=150,     #(truncated text)   #set a hard cap on the answer length, so we don't get a long essay.
    #temperature=0.1, 
    temperature=0.3
    
    # comparing temperature 0.0 vs 0.1, 0.2, 0.3, 0.5, 1.0. Lower = more predictable, higher = more varied.
)
for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
        
    if chunk.usage:
        u = chunk.usage
        print(f"\n\nprompt={u.prompt_tokens} completion={u.completion_tokens} total={u.total_tokens}")


# 0.0 (Most Predictable / Deterministic):
    # The model always picks the absolute most mathematically probable next word.
    # If you run the exact same prompt ten times, you will get the exact same response every single time.
    # Best used for: Tasks that require strict accuracy, code generation, data extraction, or factual Q&A where you don't want the AI to "hallucinate" or guess.

# 1.0 (Most Varied / Creative):
    # The model introduces more randomness by choosing words that are less obvious or less frequent, based on their probability scores.
    # If you run the same prompt multiple times, you will get different, more creative, or unexpected answers each time.
    # Best used for: Creative writing, brainstorming story plots, poetry, or coming up with diverse ideas.
    
    
#RESULTS OF TESTING MAX_TOKENS AND TEMPERATURE:

# max_tokens : sets the maximum ceiling for output length—capping it too low truncates the answer mid-sentence, 
# while setting it higher allows the model to naturally complete its thought.   

# temperature : controls creativity, where 0.0 produces strict, repeatable outputs and 
# higher values (like 0.1 or 0.3) allow for slightly more varied phrasing.  