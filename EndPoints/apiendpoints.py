from fastapi import FASTAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from typing_extensions import List
from starlette.response import JSONResponse
from src.data_ingestion_pipe.ingestion_pipeline import DataIngestion
from src.agents.graph import GraphBuilder
from src.data_models.models import *

app = FASTAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],  
)

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        ingestion = DataIngestion()
        ingestion.run_pipeline(files)
        return {"messages": "Files successfully processed and stored."}
    except Exception as e:
        return JSONResponse(status_code= 500, content ={"error": str(e)})
    
@app.post("/query")
async def query_chatbot(request: QuestionResquest):
    try:
        graph_service = GraphBuilder()
        graph_service.build()
        graph = graph_service.get_graph()

        messages = {"messages": [request.question]}

        result = graph.invoke({"messages": messages})

        if isinstance(result, dict) and "messages" in result:
            final_output = result["messages"][-1].content
        else:
            final_output =  str(result)

        return {"answer": final_output}
    except Exception as e:
        return JSONResponse(status_code= 500, content ={"error": str(e)})