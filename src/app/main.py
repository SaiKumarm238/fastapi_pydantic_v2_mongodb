from fastapi import FastAPI
from src.routers.student import student_router
from src.routers.health import health_router

app = FastAPI(
    title="Student Course API",
    summary="A sample application showing how to use FastAPI to add a ReST API to a MongoDB collection.",
)

app.include_router(student_router)
app.include_router(health_router)