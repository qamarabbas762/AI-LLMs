import os
from scrapy.selector import Selector
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
uc.Chrome.__del__ = lambda self: None
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
import time,random,tempfile
import numpy as np
from langchain_community.document_loaders import BSHTMLLoader
from dotenv import load_dotenv

load_dotenv()

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
MAX_TOKENS = 15000
MODEL_NAME = 'gpt-4o-mini'
TEMPERATURE = 0.4

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

def scrape(url):
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    ]

    options = uc.ChromeOptions()
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    #url = 'https://medium.com/@suraj_bansal/build-your-own-ai-chatbot-a-beginners-guide-to-rag-and-langchain-0189a18ec401'

    # THIS FIXES THE ERROR
    with uc.Chrome(options=options, headless=False) as driver:

        driver.get(url)
        time.sleep(4)

        sel = Selector(text=driver.page_source)

        XPATH_TARGETS = """
            //h1//text() |
            //h2//text() |
            //h3//text() |
            //h4//text() |
            //h5//text() |
            //h6//text() |
            //p//text()  |
            //li//text() |
            //span//text() |
            //strong//text() |
            //em//text() | 
            //blockquote//text()
        """

        raw_text = sel.xpath(XPATH_TARGETS).getall()
        cleaned = [t.strip() for t in raw_text if t.strip()]

        print("\n=== FULL TEXT EXTRACTED ===\n")
        return cleaned


def creating_text_chuncks(cleaned):
    if cleaned:
        docs = [Document(page_content=text) for text in cleaned]

        text_splitter = CharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )

        texts = text_splitter.split_documents(docs)
        return texts


llm = ChatOpenAI(
    model_name = MODEL_NAME,
    temperature = TEMPERATURE,
    max_tokens = MAX_TOKENS
)

template = """Context: {context}
Question : {question}
Answer the question concisely based only on the given context.If the context doesn't contain the relevant information, say "I don't have enough information to answer the question".
But if the question is generic , then go ahead and answer the question, for example what is an electric vehicle


"""

PROMPT = PromptTemplate(
    template=template,input_variables=['context','question']
)

def rag_pipeline(query,qa_chain,vectorstore):
    relevant_docs = vectorstore.similarity_search_with_score(query,k=3)
    print("\n Top three most relevant chunks")
    context = ""
    for i, (doc,score) in enumerate(relevant_docs,1):
        print(f"{i}. Relevance Score: {score:.4f}")
        print(f" Content: {doc.page_content[:200]}")
        print()
        context += doc.page_content + "\n\n"

    full_prompt = PROMPT.format(context=context,question=query)
    print("\n Full prompt send to the model")
    print(full_prompt)
    print("\n"+ "="*50 + "\n")
    response = qa_chain.invoke({"query":query})
    return response['result']

if __name__ == "__main__":
    cleaned = scrape(url = 'https://medium.com/@abhipillai/3i-atlas-the-third-interstellar-comet-discovery-journey-and-why-it-matters-e713f6712f40')
    texts = creating_text_chuncks(cleaned)
    print("Now creating embeddings and vector store")
    embeddings = OpenAIEmbeddings()
    #vectorstore = FAISS.from_documents(texts,embeddings)
    vectorstore = Chroma.from_documents(texts, embeddings)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt":PROMPT}
    )
    print("RAG pipeline is now initializad")
    print("Enter your new query or type 'quit' to quit website")
    while True:
        user_query = input("Enter your query")
        if user_query.lower() == 'quit':
            print("Exiting the program")
            break
        result = rag_pipeline(user_query,qa,vectorstore)
        print(f"RAG response is : {result}")