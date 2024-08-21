FROM python:3.9
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./schemas /code/schemas
COPY ./database /code/database
COPY ./documents /code/documents
COPY ./main.py /code/main.py
EXPOSE 8000
