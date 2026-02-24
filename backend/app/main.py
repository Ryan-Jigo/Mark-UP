from fastapi import FastAPI
from app.api.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router, prefix="/auth")

@app.get("/")
def root():
    return{"message" : "Backend is running"}