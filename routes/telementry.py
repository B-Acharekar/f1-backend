from fastapi import APIRouter, Query
from services.session_data import get_driver_lap_times

telemetry_router = APIRouter()

@telemetry_router.get("/lap-times")
async def lap_times(driver: str = Query(...), year: int = Query(2024), gp: str = Query("Monaco"), session_type: str = Query("R")):
    return get_driver_lap_times(driver, year, gp, session_type)
