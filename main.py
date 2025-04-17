import uvicorn
from fastapi import FastAPI

from app.api import address_api, hotel_api, room_api, booking_api, guest_api, room_type_api, facility_api, invoice_api, \
    review_api, payment_api, statistics_api

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
app.include_router(room_type_api.router)
app.include_router(facility_api.router)
app.include_router(invoice_api.router)
app.include_router(review_api.router)
app.include_router(payment_api.router)
app.include_router(statistics_api.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5049)
