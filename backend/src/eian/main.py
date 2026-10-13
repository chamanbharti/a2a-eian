from fastapi import FastAPI

app = FastAPI(
    title="Enterprise Insurance Agent Network",
    version="0.1.0",
)

@app.get("/health")
def health() -> dict[str,str]:
    return {"status": "ok", "service":"a2a-eian"}