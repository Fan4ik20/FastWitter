from fastapi import FastAPI
import uvicorn

import config

from routers import users
from routers import posts
from routers import users_posts


app = FastAPI(docs_url='/api/v1/docs/')

app.include_router(users.router, prefix='/api/v1')
app.include_router(posts.router, prefix='/api/v1')
app.include_router(users_posts.router, prefix='/api/v1')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=65432)
