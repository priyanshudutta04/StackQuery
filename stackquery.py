import os
import requests
from dotenv import load_dotenv
from langchain import hub
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.agents import create_tool_calling_agent
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import AgentExecutor


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY") 
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7, google_api_key=api_key) 

def is_coding(query):
    
    prompt = PromptTemplate.from_template(
        "Is the following question related to programming or software development? Reply with 'Yes' or 'No'.\n\nQuestion: {query}"
    )

    response = llm.invoke(prompt.format(query=query))
    response_text = response.content.strip().lower()  

    return response_text == "yes"

def fetch_stackoverflow(query):
    url = f"https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q={query}&site=stackoverflow"
    response = requests.get(url)
    data = response.json()

    results = []
    for item in data.get("items", []):
        title = item.get("title", "No title available")
        link = item.get("link", "")
        answer_id = item.get("accepted_answer_id", "No answer ID")
        
        results.append(f"Title: {title}\nLink: {link}\nAnswer ID: {answer_id}")
    
    return results

def stackquery(query):
    if is_coding(query):
        results = fetch_stackoverflow(query)
        links = [res.split("\n")[1].replace("Link: ", "") for res in results[:5]] if results else []

        if links:
            loaders = [WebBaseLoader(link) for link in links]
            loaded_docs = [loader.load() for loader in loaders]

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            split_docs = [text_splitter.split_documents(docs) for docs in loaded_docs]

            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

            retriever_tools = []
            for i, (link, docs) in enumerate(zip(links, split_docs)):
                vectordb = Chroma.from_documents(docs, embeddings, persist_directory="./chroma_db")
                retriever = vectordb.as_retriever()

                tool = create_retriever_tool(
                    retriever,
                    f"stackoverflow_search_{i+1}",
                    f"Search for solutions from Stack Overflow article: {link}",
                )
                retriever_tools.append(tool)

            prompt = PromptTemplate.from_template(
                "You are an AI assistant helping developers find answers from Stack Overflow.\n"
                "Based on the retrieved information, provide a concise and helpful answer to the following query:\n\n"
                "{input}\n\n"
                "Use the following retrieved documents if needed:\n"
                "{agent_scratchpad}"
            )

            agent=create_tool_calling_agent(llm,retriever_tools,prompt)
            agent_executor=AgentExecutor(agent=agent,tools=retriever_tools,verbose=True)
            response = agent_executor.invoke({"input": query})
            response_text = response["output"]
            return response_text

        else:
            return "No Stack Overflow links found."

    else:
        return "This does not seem to be a coding-related question."


# print(stackquery("flutter doctor is not working"))