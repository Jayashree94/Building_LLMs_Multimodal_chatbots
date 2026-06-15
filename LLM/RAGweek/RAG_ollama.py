import os
import glob
import tiktoken
import numpy as np
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sklearn.manifold import TSNE
import plotly.graph_objects as go


# Using Llama 3.2 open source model via Ollama (free, no API key needed)

MODEL = "llama3.2:latest"
db_name = "vector_db"
load_dotenv(override=True)


llm = OllamaLLM(model=MODEL)
print(f"Using open-source model: {MODEL} via Ollama")


# How many characters in all the documents?

knowledge_base_path = "LLM/knowledge-base/**/*.md"
files = glob.glob(knowledge_base_path, recursive=True)
print(f"Found {len(files)} files in the knowledge base")

entire_knowledge_base = ""

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        entire_knowledge_base += f.read()
        entire_knowledge_base += "\n\n"

print(f"Total characters in knowledge base: {len(entire_knowledge_base):,}")


# How many tokens in all the documents?

# Use standard encoding for Llama (tiktoken is primarily for OpenAI models)
try:
    encoding = tiktoken.get_encoding("cl100k_base")  # Standard encoding
    tokens = encoding.encode(entire_knowledge_base)
    token_count = len(tokens)
    print(f"Total tokens (approximate): {token_count:,}")
except Exception as e:
    print(f"Token counting skipped: {e}")


    # Load in everything in the knowledgebase using LangChain's loaders

folders = glob.glob("LLM/knowledge-base/*")

documents = []
for folder in folders:
    doc_type = os.path.basename(folder)
    loader = DirectoryLoader(folder, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
    folder_docs = loader.load()
    for doc in folder_docs:
        doc.metadata["doc_type"] = doc_type
        documents.append(doc)

print(f"Loaded {len(documents)} documents")
print(f"Sample document metadata: {documents[1]}")


# Divide into chunks using the RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

print(f"Divided into {len(chunks)} chunks")
print(f"First chunk:\n\n{chunks[0]}")