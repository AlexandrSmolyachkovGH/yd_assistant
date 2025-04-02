from fastapi import FastAPI
import uvicorn

from yandex_auth.routers import index, token

app = FastAPI()
app.include_router(index.router)
app.include_router(token.router)

if __name__ == "__main__":
    uvicorn.run(
        app="yandex_auth.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True, )
