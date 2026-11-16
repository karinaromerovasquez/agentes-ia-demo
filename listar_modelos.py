from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

modelos = client.models.list()
for m in modelos.data:
    print(m.id)
