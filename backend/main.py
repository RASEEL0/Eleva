from fastapi import FastAPI

app = FastAPI(
    title="CareerPilot AI",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "CareerPilot AI API is running!"
    }