from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict, Annotated, List
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from src.utils.model_loader import ModelLoader
from toolkit.tools import *

class State(TypedDict):
    messages : Annotated[List, add_messages]

class GraphBuilder:
    def __init__(self):
        self.model_loader = ModelLoader()
        self.llm = self.model_loader.load_llm()
        self.tools = [create_bing_tool, create_polygon_tool, create_tavily_tool]
        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        self.graph = None

    def chatbot_node(self, state:State):
        """A node for chatbot"""
        return {"messages": [self.llm_with_tools.invoke(state["messages"])]}

    def build(self):
        """buildes a workflow"""
        graph_builder = StateGraph(State)

        graph_builder.add_node("chatbot", self.chatbot_node)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))

        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_conditional_edges("chatbot", tools_condition)
        graph_builder.add_edge("tools", "chatbot")

        self.graph = graph_builder.compile()

    def get_graph(self):
        """compiles the workflow as graph"""
        
        if self.graph is None:
            raise ValueError("Graph is not build, call build() method first")
        
        return self.graph