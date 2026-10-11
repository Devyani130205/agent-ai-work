import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)
client = OpenAI(base_url=os.getenv("BASE_URL"), api_key=os.getenv("API_KEY"))
MODEL = os.getenv("MODEL")

messages = [
    {"role": "system", "content": "You are a concise assistant for a retail bank."},
]

def ask(question):
    messages.append({"role": "user", "content": question})   # add your question
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        #max_tokens=400,
        #temperature=0,     # it's give a stable ans.
        max_tokens=200,     # completion length = 200, is the exactly the cap.
        temperature=0.2,    # it's give a probabilistic ans. coz -> 0.0 = most predictable, 1.0 = most varied or creative.
    )
    answer = response.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})  # remember the answer
    u = response.usage
    print("You:", question)
    print("Bot:", answer)
    print(f"prompt={u.prompt_tokens} completion={u.completion_tokens} total={u.total_tokens}\n")

ask("What is an EMI? One sentence.")
ask("Give me an example with 8 lakh.")