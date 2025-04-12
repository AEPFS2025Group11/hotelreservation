import uvicorn
from fastapi import FastAPI

from app.api import address_api, hotel_api

app = FastAPI()


app.include_router(address_api.router)
app.include_router(hotel_api.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)
