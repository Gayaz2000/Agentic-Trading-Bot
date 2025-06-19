from pydantic  import BaseModel

class RagToolSchema(BaseModel):
    question: str

class QuestionResquest(BaseModel):
    question : str