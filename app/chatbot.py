import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
# Removed CSVLoader import

load_dotenv()

# CSV_FILE_PATH is no longer needed

def get_conversational_chain():
    # Create embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Create an empty FAISS vector store
    # FAISS.from_documents requires non-empty documents, so we use from_texts with a dummy text
    texts = ["This is a dummy document to initialize the retriever."] # Cannot be empty
    empty_vector_store = FAISS.from_texts(texts, embeddings)
    empty_retriever = empty_vector_store.as_retriever(search_kwargs={"k": 1})


    # Define a more generic prompt template
    prompt_template = """
    You are a helpful AI assistant. Answer the question based on the conversation history and your general knowledge.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Keep the answer concise and to the point.

    Chat History:
    {chat_history}

    Question: {question}

    Answer:
    """
    # Note: ConversationalRetrievalChain internally handles chat_history and context from retriever.
    # The prompt for combine_docs_chain_kwargs should focus on how to use the retrieved documents (if any) and the question.
    # For an empty retriever, the 'context' will likely be minimal or non-existent.
    # Let's refine the prompt for the combine_docs_chain part, assuming 'context' might be empty.
    
    # Revised prompt for combine_docs_chain, which receives 'context' (from retriever) and 'question'
    combine_docs_prompt_template = """
    Based on the following context (if any) and the question, provide an answer.
    If the context is empty or not relevant, answer the question using your general knowledge.
    
    Context:
    {context}

    Question:
    {question}

    Answer:"""
    prompt = PromptTemplate(template=combine_docs_prompt_template, input_variables=["context", "question"])


    # Initialize ChatGoogleGenerativeAI model
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7) # Adjusted temperature for more general conversation

    # Create ConversationalRetrievalChain
    chain = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=empty_retriever, # Use the empty retriever
        combine_docs_chain_kwargs={"prompt": prompt},
        return_source_documents=False # No meaningful source documents anymore
    )
    return chain

if __name__ == '__main__':
    # This is for testing the chain locally
    chain = get_conversational_chain()
    chat_history = []
    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break
        result = chain({"question": query, "chat_history": chat_history})
        print("Bot:", result['answer'])
        chat_history.append((query, result['answer']))
