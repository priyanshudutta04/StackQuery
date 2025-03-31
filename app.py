import os
import requests
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.tools.retriever import create_retriever_tool
from flask import Flask, request, jsonify

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7, google_api_key=api_key)

app = Flask(__name__)

def is_coding_question(query):
    prompt = PromptTemplate.from_template(
        "Is the following question related to programming or software development? Reply with 'Yes' or 'No Strictly'.\n\nQuestion: {query}"
    )
    response = llm.invoke(prompt.format(query=query))
    return response.content.strip().lower() == "yes"

def fetch_stackoverflow_answers(query):
    url = f"https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=relevance&q={query}&site=stackoverflow"
    response = requests.get(url)
    data = response.json()
    
    results = []
    for item in data.get("items", []):
        results.append({
            "title": item.get("title", "No title available"),
            "link": item.get("link", ""),
            "answer_id": item.get("accepted_answer_id", "No answer ID")
        })
    return results

@app.route("/query", methods=["POST"])
def process_query():
    data = request.json
    query = data.get("query", "")
    
    if is_coding_question(query):
        results = fetch_stackoverflow_answers(query)
        return jsonify({"coding_related": True, "results": results})
    else:
        return jsonify({"coding_related": False, "message": "Not a coding-related question."})

if __name__ == "__main__":
    app.run(debug=True)
