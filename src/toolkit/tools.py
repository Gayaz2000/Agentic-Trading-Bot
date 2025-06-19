import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from lancedb.rerankers import LinearCombinationReranker
from langchain_community.vectorstores import LanceDB
from langchain_community.tools import TavilySearchResults
from langchain_community.tools.polygon import PolygonFinancials
from langchain_community.utilities.polygon import PolygonAPIWrapper
from langchain_community.tools.bing_search import BingSearchResults
from data_models.models import RagToolSchema


@tool(args_schema=RagToolSchema)
def create_retriever_tool(question):
    """A retriever tool"""
    pass

@tool
def create_tavily_tool(question: str):
    """A tavily search tool"""
    return TavilySearchResults(
        question,#=question,
        max_results = 3,
        include_answer = True,
        include_raw_content = True,
    )

@tool
def create_bing_tool(): #question: str
    """A bing web search tool"""
    return BingSearchResults()

@tool
def create_polygon_tool(): #question: str
    """A polygon tool for finance search"""
    return PolygonFinancials(api_wrapper=PolygonAPIWrapper())

def get_all_tools(question):
    return [
        create_retriever_tool(question),
        create_polygon_tool,
        create_bing_tool,
        create_tavily_tool,
    ]

if __name__ == "__main__":
    try:
        print(get_all_tools("myquestion"))
    except Exception as e:
        print(e)