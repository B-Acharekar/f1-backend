from fastapi import APIRouter, Query
from services.session_data import get_driver_lap_times
from concurrent.futures import ThreadPoolExecutor
import asyncio

telemetry_router = APIRouter()
executor = ThreadPoolExecutor()

@telemetry_router.get("/lap-times")
async def lap_times(
    driver: str = Query(...),
    year: int = Query(...),
    gp: str = Query(...),
    session_type: str = Query(...),
    best_lap_only: bool = Query(False)
):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        executor,
        lambda: get_driver_lap_times(driver, year, gp, session_type, best_only=best_lap_only)
    )
