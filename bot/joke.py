from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableParallel,RunnableSequence
from dotenv import load_dotenv
load_dotenv()

prompt1 = PromptTemplate(
    template = 'Write a joke on {topic}',
    input_variable = ['topic']
)

model = ChatOpenAI()
parser = StrOutputParser()

prompt2 = PromptTemplate(
    template = 'Explain the following {joke}',
    input_variable = ['joke']
)

chain1 = RunnableSequence(prompt1,model,parser)

joke = chain1.invoke({'topic':'Sachin Tendulkar'})


print("Joke is :",joke)

chain2 = RunnableSequence(prompt2,model,parser)

explain = chain2.invoke({'joke':joke})

print("Explaination of the joke is: ",explain)

