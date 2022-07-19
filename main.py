from fastapi import FastAPI

from routers import comment, laundry, oauth2, user
app = FastAPI()

app.include_router(
    oauth2.router,
    prefix=''
)

app.include_router(
    laundry.router,
    prefix='/api/laundry'
)

app.include_router(
    comment.router,
    prefix='/api/comment'
)

app.include_router(
    user.router,
    prefix='/api/user'
)
