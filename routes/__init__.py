from fastapi import FastAPI
from . import internal, auth, user, feedback

def include(app: FastAPI):
    app.include_router(auth.router)
    app.include_router(user.router)
    app.include_router(internal.router)
    app.include_router(feedback.router)