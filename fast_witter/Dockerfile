FROM python:3.10-slim-buster
WORKDIR "/app"
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--reload", "--port", "5555",  "--host", "0.0.0.0"]
