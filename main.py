from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.telementry import telemetry_router
from routes.session import session_router  # ✅ renamed from endpoints

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In prod, replace with actual frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(session_router, prefix="/api")
app.include_router(telemetry_router, prefix="/api")
