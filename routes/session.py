from fastapi import APIRouter, Query
import fastf1
from services.session_data import (
    get_drivers_in_session,
    get_event_names_for_year,
    get_next_race,
    get_session_summary,
    compare_laps_telemetry,
    get_driver_lap_times
)

session_router = APIRouter()

@session_router.get("/session/drivers")
async def drivers_in_session(
    year: int = Query(...),
    gp: str = Query(...),
    session_type: str = Query("R")
):
    return get_drivers_in_session(year, gp, session_type)

@session_router.get("/session/summary")
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

@session_router.get("/events")
def list_events_for_year(
    year: int = Query(..., description="F1 season year to list events for")
):
    return get_event_names_for_year(year)

@session_router.get("/next-race")
def next_race(year: int = Query(...)):
    return get_next_race(year)