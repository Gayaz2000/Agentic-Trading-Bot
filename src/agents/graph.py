from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, Annotated, List
from langgraph.graph.message import add_messages
from src.utils.model_loader import ModelLoader
from toolkit.tools import *

class State(TypedDict):
    messages : Annotated[List, add_messages]

class GraphBuilder:
    def __init__(self):
        pass

    def chatbot_node(self, state:State):
        """A node for chatbot"""
        pass

    def build(self):
        """buildes a workflow"""
        pass

    def get_graph(self):
        """compiles the workflow as graph"""
        pass