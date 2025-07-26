from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import os

def get_vector_store():
    # Path where FAISS index will be saved
    index_dir = "vectorstore/"
    os.makedirs(index_dir, exist_ok=True)

    # Initialize embedding
    embeddings = OpenAIEmbeddings()

    # If already saved, load from disk
    if os.path.exists(os.path.join(index_dir, "index.faiss")):
        print("[DEBUG] Loading FAISS index from disk")
        return FAISS.load_local(index_dir, embeddings, allow_dangerous_deserialization=True)

    # Otherwise: embed and save
    print("[DEBUG] Creating new FAISS index from documents")
    loader = PyPDFDirectoryLoader("research_papers")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_docs = splitter.split_documents(docs)

    if not final_docs:
        raise ValueError("No documents found to embed.")

    vector_store = FAISS.from_documents(final_docs, embeddings)

    vector_store.save_local(index_dir)
    print("[DEBUG] FAISS index saved to disk")

    return vector_store

def get_answer(question, vector_store):
    retriever = vector_store.as_retriever()
    llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model="Llama3-8b-8192")

    prompt = ChatPromptTemplate.from_template("""
        Answer the questions based on the provided context only.
        Please provide the most accurate response based on the question.
        <context>
        {context}
        </context>
        Question: {input}
    """)

    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    result = retrieval_chain.invoke({"input": question})
    return result['answer'], result['context']
