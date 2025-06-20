import os
import tempfile
from typing_extensions import List
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.config_loader import load_config
from src.utils.model_loader import ModelLoader
from pinecone import ServerlessSpec
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from uuid import uuid4


class DataIngestion:
    def __init__(self):
        print("Initialized Data ingestion...")
        self.model_loader = ModelLoader()
        self._load_env_variable()
        self.config = load_config()

    def _load_env_variable(self):
        """
        Load and validate environment variables.
        """
        load_dotenv()

        required_vars = ["GROQ_API_KEY", "PINECONE_API_KEY"] #, "TAVILY_API_KEY", "POLYGONE_API_KEY"

        missing_vars = [var for var in required_vars if os.getenv(var) is None]
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")
        
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")


    def load_documents(self, uploaded_files)->List[Document]:
        """
        Load documents from uploaded PDF and Docx files.
        """
        documents = []
        for uploaded_file in uploaded_files:
            if uploaded_file.name.endswith("pdf"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    tempfile.write(uploaded_file.read())
                    loader = PyPDFLoader(temp_file.name)
                    documents.extend(loader.load())

            elif uploaded_file.name.endswith("docx"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_file:
                    tempfile.write(uploaded_file.read())
                    loader = Docx2txtLoader(temp_file.name)
                    documents.extend(loader.load())

            else:
                print(f"Unsupported file type: {uploaded_file.name}")
            
            return documents

    def store_in_vectorDB(self, documents: List[Document]):
        """
        Split the documents and create vector store with embedding.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200,
            length_function = len
        )

        documents = text_splitter.split_documents(documents)

        pc = Pinecone(api_key=self.pinecone_api_key)

        if not pc.has_index(self.config["vectordb"]["vdb_name"]):
            pc.create_index(
                name= self.config["vectordb"]["vdb_name"],
                dimension= 2048,
                metric= "cosine",
                spec= ServerlessSpec(cloud="aws", region="us-east-1"),
            )

        index = pc.Index(self.config["vectordb"]["vdb_name"])
        vectore_store = PineconeVectorStore(
            index= index, 
            embedding=self.model_loader.load_embeddings(),
        )

        uuids = [str(uuid4() for _ in range(len(documents)))]

        vectore_store.add_documents(documents=documents, ids= uuids)
        return vectore_store
    
    def run_pipeline(self, upload_files):
        """
        Run full data ingestion: load files, split, embed and store
        """
        documents = self.load_documents(upload_files)
        if not documents:
            print("No valid documents found")
            return
        
        self.store_in_vectorDB(documents)

if __name__ == "__main__":
    pass