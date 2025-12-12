from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableParallel
from dotenv import load_dotenv

load_dotenv()
model  = ChatOpenAI()

prompt1 = PromptTemplate(
    template = "Generate short and simple notes from the following text \n {text}",
    input_variables = ["text"]
)

prompt2 = PromptTemplate(
    template = "Generate 5 short questions from the following text \n {text}",
    input_variables = ['text']
)

prompt3 = PromptTemplate(
    template = 'Merge the provided notes and quiz into a single document \n {notes} & {quiz}',
    input_variables = ['notes','quiz']
)

parser = StrOutputParser()

parallel_chain = RunnableParallel({
    'notes': prompt1 | model | parser,
    'quiz' : prompt2 | model | parser
})

merge_chain = prompt3 | model | parser

chain = parallel_chain | merge_chain

text = """Wouldn’t it be awesome if you had your own personal encyclopedia that could also hold a conversation? 🤓 Well, with the power of RAG and LangChain, you’re about to become the architect of your very own AI chatbot!

Chatbots are everywhere these days — helping us shop, solving our tech woes, and even keeping us company. But what if you could build a chatbot that’s not just helpful, but actually smart? 😎

Enter RAG (Retrieval-Augmented Generation). It’s like giving your chatbot a brain full of searchable knowledge. Imagine a chatbot that could tap into a vast library of information and generate creative text. That’s the magic of RAG.

And to make things even easier, there’s LangChain — think of it as a set of super helpful building blocks for creating all kinds of AI applications. As the saying goes, “Give a man a fish and you feed him for a day; teach a man to fish and you feed him for a lifetime” Let’s teach you to build an awesomely intelligent chatbot! 🤖

In this comprehensive tutorial, you’ll discover:

The key concepts behind RAG and how to use LangChain to create sophisticated chatbots.
How to build both stateless and stateful (context-aware) chatbots using LangChain with step by step explanation of the code.
The steps to connect your chatbot to a knowledge repository like a PDF, empowering it to answer questions about the document’s content. 📖
Hidden Secrets: A bonus section awaits those who crave a deeper understanding. We’ll crack open some LangChain secrets and see how the magic works under the hood.
Spoiler Alert — In this tutorial, we’ll dive into building a RAG chatbot that can interact with a research paper (PDF format). The beauty is, you can easily adapt the code to work with any content — html files, csv, SQL databases, websites, and more! Get ready to unlock the knowledge within your documents.

To make this journey even smoother, you’ll find the complete code and data on my GitHub repository.

A Note for Experienced AI Adventurers — This article is packed with information! It starts with a thorough exploration of RAG and LangChain concepts and gradually guides you through building your chatbot. If you’re already well-versed in the theory, feel free to jump to the sections titled “Setting up Your Environment” or “Building Your RAG Chatbot (Step-by-Step)”.

However, even for seasoned AI enthusiasts, skimming the earlier sections might provide a helpful refresher. As the saying goes, “Knowledge is power”

Ready to take your AI skills to the next level? Let’s dive in and build the knowledge-powered chatbot of your dreams!

Press enter or click to view image in full size

Prerequisites
Before diving into the world of RAG chatbot creation, let’s make sure you have the right tools and knowledge:

Basic Python Proficiency: While I will provide code examples, a fundamental understanding of Python concepts (variables, functions) will make the process much smoother.
Essential Libraries: You’ll need to install the following libraries using the ‘pip’ package manager in your terminal:
— langchain: The heart of our chatbot building process.
— openai: Lets us tap into powerful language models from OpenAI.
— pinecone-client: For setting up our vector database to store knowledge.
OpenAI and Pinecone Accounts: You’ll need API keys to use these services. Instructions for getting them are included below.
Your Knowledge Source: The beauty of RAG is that you provide the data your chatbot learns from! Have your research paper (PDF) or other content type (text files, website URLs, company documents) ready.
Don’t worry if you’re new to all of this! I’ll help guide you through setting up your environment along the way."""

#result = chain.invoke({'text':text})

chain.get_graph().print_ascii()
