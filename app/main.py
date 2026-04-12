from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "message": "Hello from Azure DevOps CI/CD Pipeline"}

@app.get("/health")
def health():
    return {"status": "healthy"}
