from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage
import gradio as gr  


MODEL = "llama3.2:latest"
DB_NAME = "vector_db"
load_dotenv(override=True)


embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory=DB_NAME, embedding_function=embeddings)

# Retriever for RAG pipeline
retriever = vectorstore.as_retriever()

# For Ollama, you can pass temperature when creating the instance:
llm = OllamaLLM(model=MODEL, temperature=0)

# Test the retriever
query = "Who is Avery?"
retrieved_docs = retriever.invoke(query)
print(f"\n=== Retrieved Documents for: '{query}' ===")
print(f"Number of documents: {len(retrieved_docs)}\n")

# for i, doc in enumerate(retrieved_docs):
#     print(f"Document {i+1}:")
#     print(f"Content: {doc.page_content[:500]}...")  # Print first 500 chars
#     print(f"Metadata: {doc.metadata}\n")

# Generate response from LLM
print(f"\n=== LLM Response ===")
response = llm.invoke("Who is Avery?")
print(f"Response:\n{response}")


SYSTEM_PROMPT_TEMPLATE = """
You are a knowledgeable, friendly assistant representing the company Insurellm.
You are chatting with a user about Insurellm.
If relevant, use the given context to answer any question.
If you don't know the answer, say so.
Context:
{context}
"""


def answer_question(question: str, history):
    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=context)
    response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=question)])
    # OllamaLLM returns string directly, not a message object
    return response if isinstance(response, str) else response.content

output = answer_question("Who is Averi Lancaster?", [])

print(f"\n=== Final Answer ===")
print(output)

gr.ChatInterface(answer_question).launch()