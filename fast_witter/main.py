from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def hellp():
    return {'message': 'Hello'}

