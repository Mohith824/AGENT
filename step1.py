import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client =OpenAI()
response= client.chat.completions.create(
  model="gpt-5.6-luna",
  messages=[
      {"role":"user","content":"Explain what an AI agent is in one sentence."},
  ],
 )
print(response.choices[0].message.content)