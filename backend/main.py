from fastapi import FastAPI

app = FastAPI(
    title="ِEleva",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "ِEleva  API is running!"
    }