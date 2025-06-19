import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_ollama import OllamaEmbeddings
from src.utils.config_loader import load_config
import logging

logger = logging.getLogger(__file__)
class ModelLoader:
    """
        A utility class to load embedding models and llm models
    """
    def __init__(self):
        load_dotenv()
        self._validate_env()
        self.config = load_config()

    def _validate_env(self):
        """validates the env variables"""
        required_variables= ["GROQ_API_KEY"]
        missing_variables = [var for var in required_variables if not os.getenv(var)]
        if missing_variables:
            raise EnvironmentError(f"Missing env variables: {missing_variables}")

    def load_embeddings(self):
        """loads embedding from config file"""
        print("loading embedding model")
        model_name = self.config["embedding_model"]["model_name"]
        return OllamaEmbeddings(model=model_name)

    def load_llm(self):
        """loads an llm"""
        print("loading the llm")
        model_name = self.config["llm"]["model_name"]
        groq_model = ChatGroq(model=model_name)
        return groq_model
