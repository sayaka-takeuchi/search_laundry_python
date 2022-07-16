from fastapi import FastAPI

from routers import laundry
app = FastAPI()

app.include_router(
    laundry.router,
    prefix='/api/laundry'
)
