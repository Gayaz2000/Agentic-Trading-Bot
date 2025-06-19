import os
import tempfile
from typing_extensions import List
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import LanceDB
from utils.config_loader import load_config
from pinecone import ServerlessSpec
from pinecone import Pinecone
from uuid import uuid4


class DataIngestion:
    def __init__(self):
        pass

    def _load_env_variable(self):
        pass

    def load_documents(self):
        pass

    def store_in_vectorDB(self):
        pass