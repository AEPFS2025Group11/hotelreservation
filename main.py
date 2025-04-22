import logging

import uvicorn
from fastapi import FastAPI
from sqlalchemy import event, Engine
from starlette.middleware.cors import CORSMiddleware

from app.api import address_api, hotel_api, room_api, booking_api, room_type_api, facility_api, invoice_api, \
    review_api, payment_api, statistics_api, user_api
from app.auth import auth_api

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)


@event.listens_for(Engine, "connect")
def enforce_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


app = FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(address_api.router)
app.include_router(hotel_api.router)
app.include_router(room_api.router)
app.include_router(booking_api.router)
app.include_router(room_type_api.router)
app.include_router(user_api.router)
app.include_router(facility_api.router)
app.include_router(invoice_api.router)
app.include_router(review_api.router)
app.include_router(payment_api.router)
app.include_router(statistics_api.router)
app.include_router(auth_api.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)
