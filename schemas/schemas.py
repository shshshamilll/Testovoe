from pydantic import BaseModel

class Question(BaseModel):
    text: str

class Answer(BaseModel):
    text: str

class Document(BaseModel):
    url: str
    n: int
