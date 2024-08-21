import pandas as pd
from fastapi import FastAPI
from schemas.schemas import Question, Answer, Document
from langchain.chains import GraphCypherQAChain
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain.graphs import Neo4jGraph
from database.database import create_database
import urllib.request

app = FastAPI()

@app.post('/database_creating')
def database_creating(document: Document):
    load_dotenv()

    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPEN_AI_HOST = os.getenv('OPENAI_HOST')

    NEO4J_URI = os.getenv('NEO4J_URI')
    NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

    filename = os.path.join('documents/', os.path.basename(document.url))

    req = urllib.request.Request(document.url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        with open(filename, 'wb') as file:
            file.write(response.read())

    df = pd.read_parquet(f'{filename}')

    create_database(OPENAI_API_KEY, OPEN_AI_HOST, NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, df, document.n)

@app.post('/question_answering')
def question_answering(question: Question):
    load_dotenv()

    NEO4J_URI = os.getenv('NEO4J_URI')
    NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

    graph = Neo4jGraph(
        url=NEO4J_URI,
        username=NEO4J_USERNAME,
        password=NEO4J_PASSWORD
    )

    chain = GraphCypherQAChain.from_llm(
        ChatOpenAI(temperature=0), graph=graph, verbose=True,
    )

    text = chain.run(question.text)

    return Answer(text = text)

