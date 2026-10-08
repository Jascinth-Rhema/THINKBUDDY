import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv(".env", override=True)
for m in Groq(api_key=os.getenv("GROQ_API_KEY")).models.list().data:
    print(m.id)