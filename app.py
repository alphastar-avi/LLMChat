from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Function to load diary entries from a single file
def load_diary_entries(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Function to append to diary entries
def append_diary_entry(file_path, entry):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, 'a') as file:
        file.write(f"\n[{timestamp}]\n{entry}\n")
    return True

# Initialize the knowledge base
def initialize_knowledge_base(model_name="deepseek-r1:1.5b"):
    diary_file_path = "diary.txt"
    diary_content = load_diary_entries(diary_file_path)
    
    # Split the text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_texts = text_splitter.split_text(diary_content)
    
    # Create embeddings and vector store
    embeddings = OllamaEmbeddings(model=model_name)
    vectorstore = Chroma.from_texts(split_texts, embeddings)
    
    # Set up the LLM
    llm = OllamaLLM(model=model_name, streaming=True)
    
    # Create a retrieval QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )
    
    return qa_chain, model_name

# Global variables to store the current QA chain and model
current_qa_chain, current_model = initialize_knowledge_base()
use_memory = True  # Default to using memory

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/toggle_memory', methods=['POST'])
def toggle_memory():
    global use_memory
    data = request.json
    use_memory = data.get('use_memory', True)
    return jsonify({"success": True, "use_memory": use_memory})

@app.route('/api/memory', methods=['GET'])
def get_memory():
    try:
        content = load_diary_entries("diary.txt")
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/memory', methods=['POST'])
def add_memory():
    try:
        data = request.json
        entry = data.get('entry', '').strip()
        if entry:
            append_diary_entry("diary.txt", entry)
            # Reinitialize knowledge base with new content
            global current_qa_chain
            current_qa_chain, _ = initialize_knowledge_base(current_model)
            return jsonify({"success": True})
        return jsonify({"error": "Empty entry"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query')
    model = data.get('model', 'deepseek-r1:1.5b')
    
    global current_qa_chain, current_model, use_memory
    
    # If model changed, reinitialize the knowledge base
    if model != current_model:
        current_qa_chain, current_model = initialize_knowledge_base(model)
    
    try:
        if use_memory:
            result = current_qa_chain.invoke({"query": query})
            return jsonify({
                "response": result["result"],
                "sources": [doc.page_content for doc in result.get("source_documents", [])]
            })
        else:
            # Raw model inference without memory
            llm = OllamaLLM(model=model, streaming=True)
            response = llm.invoke(query)
            return jsonify({
                "response": response,
                "sources": []
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

