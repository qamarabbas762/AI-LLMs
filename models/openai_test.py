from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

model = ChatOpenAI(model='gpt-4')
result = model.invoke('WHat is the gdp of India')
print(result)