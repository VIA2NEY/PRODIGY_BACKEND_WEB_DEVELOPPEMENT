from fastapi import APIRouter
from app.api.v1.routes import auth, hotels, rooms, bookings

router = APIRouter()

router.include_router(auth.router, prefix="/v1")
router.include_router(hotels.router, prefix="/v1")
router.include_router(rooms.router, prefix="/v1")
router.include_router(bookings.router, prefix="/v1")
