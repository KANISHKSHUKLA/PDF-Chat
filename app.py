import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from htmlTemp import css, bot_template, user_template

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator= "\n",
        chunk_size = 1000,
        chunk_overlap= 200,
        length_function= len 
    )
    chunks = text_splitter.split_text(text)
    return chunks

# def get_vectorstore(text_chunks): ############ openai embeddings 
#     embeddings = OpenAIEmbeddings()
#     vectorstore = FAISS.from_text(text=text_chunks, embedding = embeddings)
#     return vectorstore


def get_vectorstore(text_chunks): # instructor embeddings 
    embeddings = HuggingFaceInstructEmbeddings(model_name= "hkunlp/instructor-xl")
    vectorstore = FAISS.from_text(text=text_chunks, embedding = embeddings)
    return vectorstore 


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key= 'chat_history' return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever= vectorstore.as_retriever(),
        memory= memory
    )
    return conversation_chain

def main():
    load_dotenv() 
    st.set_page_config(page_title="Chat with your PDFs")

if "conversation" not in st.session_state:
    st.session_state.conversation = none         ## when the app is going to re reun it will check whether it is in the convers  and is going to reinitialsise it to none and if it is already initialised it is not gouoing to to do anything
    st.header("Chat with your PDF")
    st.text_input("Ask anything to your pdf")

    with st.sidebar:
        st.subheader("Uploaded files")
        pdf_docs = st.file_uploader(
                "Upload/Drop your pdf here", accept_multiple_files=True)
        if st.button("Start"):
            with st.spinner("Processing"):
                # text of the pdf
                raw_text = get_pdf_text(pdf_docs)
                

                # chunkifiying the text
                text_chunks = get_text_chunk(raw_text)

                # vector store 
                vectorstore = get_vectorstore(text_chunks)

                #convo shain
                st.session_state.conversation = get_conversation_chain(vectorstore)










if __name__ == '__main__':
    main()