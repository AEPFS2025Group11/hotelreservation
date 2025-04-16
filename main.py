import uvicorn
from fastapi import FastAPI

from app.api import address_api, hotel_api, room_api, booking_api, guest_api

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

app = FastAPI()

app.include_router(address_api.router)
app.include_router(hotel_api.router)
app.include_router(room_api.router)
app.include_router(booking_api.router)
app.include_router(guest_api.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)
