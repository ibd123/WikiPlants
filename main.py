from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import os
from langchain.chains.conversation.base import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
import warnings
from langchain.schema import Document
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain


warnings.filterwarnings("ignore")




def load_plants_data():
    import json
    with open("plant_database.json", encoding="utf-8") as data:
        plants = json.load(data)
    return plants

def prepare_documents(plants_data):
    documents = []
    for plant in plants_data:
        text = "\n".join([f"{k.replace('_', ' ').capitalize()}: {v}" for k, v in plant.items()])
        documents.append(Document(page_content=text, metadata={"name": plant.get("name", "Unknown")}))
    return documents


def chatbot1(): #simple chatbot using langchain and openai, support only one query
    model = init_chat_model("gpt-4o-mini", model_provider="openai")
    response= model.invoke("what is the sintax for an if  condition in java?")
    print(response.content)


def chatbot2(): #simple chatbot using langchain and openai, support multiple queries, keeps hold of the conversation
    print("Welcome to chatbot2! Type 'exit' to quit.")
    while True:
        query = input("Write a query: ")
        if query.lower() == "exit":
            print("Goodbye!")
            break
        else:
            print(query)
            response= conversation_chain(query)
            print(response.get("response"))



def chatbot3(query): #chatbot using vectorstore and langchain, support multiple queries, keeps hold of the conversation
    response = qa_chain({"question": query})
    return response["answer"]


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
embedding = OpenAIEmbeddings()
documents = prepare_documents(load_plants_data())
vectorstore = FAISS.from_documents(documents, embedding)
llm = init_chat_model("gpt-4o-mini", model_provider="openai")
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history", 
    return_messages=True,
    input_key="question",       # Clé que tu envoies à la chaîne
    output_key="answer"         # Clé que la chaîne retourne
)



conversation_chain = ConversationChain(
    llm=llm,
    memory=ConversationBufferMemory()
)

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    memory=memory,
    return_source_documents=True
)