from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ Import route modules
from routes import tickers, pipeline, sentiment, headlines

app = FastAPI()

# ✅ Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔐 change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Mount routes
app.include_router(tickers.router)
app.include_router(pipeline.router)
app.include_router(sentiment.router)
app.include_router(headlines.router)

@app.get("/")
def root():
    return {"message": "Financial Sentiment API is running"}
