from aiogram import Router
from .start import router as start_router
from .callbacks import router as callbacks_router

main_router = Router()
main_router.include_router(start_router)
main_router.include_router(callbacks_router)
