from fastapi import APIRouter, Query
from services.session_data import get_drivers_in_session , get_session_summary, compare_laps_telemetry

session_router = APIRouter()

@session_router.get("/drivers-in-session")
async def drivers_in_session(
    year: int = Query(...),
    gp: str = Query(...),
    session_type: str = Query("R")
):
    return get_drivers_in_session(year, gp, session_type)

@session_router.get("/session-summary")
async def session_summary(
    year: int = Query(...),
    gp: str = Query(...),
    session_type: str = Query("R")
):
    return get_session_summary(year, gp, session_type)

@session_router.get("/compare-laps")
async def compare_laps(
    driver1: str = Query(...),
    driver2: str = Query(...),
    lap: int = Query(...),
    year: int = Query(...),
    gp: str = Query(...),
    session_type: str = Query("R")
):
    return compare_laps_telemetry(year, gp, session_type, driver1, driver2, lap)