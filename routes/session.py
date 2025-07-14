from fastapi import APIRouter, Query
import fastf1
from services.news_data import get_f1_stories
from services.session_data import (
    get_drivers_in_session,
    get_event_names_for_year,
    get_next_race,
    get_session_summary,
    compare_laps_telemetry,
    get_driver_lap_times,
    
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

@session_router.get("/race/pit-stops")
def get_pit_stop_data(year: int, gp: int):
    session = fastf1.get_session(year, gp, "R")
    session.load()
    laps = session.laps

    pit_stops = []
    for drv in session.drivers:
        drv_laps = laps.pick_driver(drv)
        pit_laps = drv_laps[drv_laps['PitInTime'].notna() & drv_laps['PitOutTime'].notna()]
        for lap in pit_laps.itertuples():
            pit_stops.append({
                "driver": session.get_driver(drv).FullName,
                "lap": int(lap.LapNumber),
                "duration": float(getattr(lap, "PitStopTime", 0.0) or 0),
                "team": lap.Team
            })

    return {"pit_stops": pit_stops}

# @session_router.get("/race/tyre-strategy")
# def get_tyre_strategy(year: int, gp: int):
#     session = fastf1.get_session(year, gp, "R")
#     session.load()
#     laps = session.laps

#     strategy = []
#     for drv in session.drivers:
#         drv_laps = laps.pick_driver(drv)
#         stints = get_stint_summary(drv_laps)

#         for stint in stints.itertuples():
#             strategy.append({
#                 "driver": session.get_driver(drv).FullName,
#                 "stint": stint.Index,
#                 "compound": stint.Compound,
#                 "start_lap": stint.Start,
#                 "end_lap": stint.End,
#                 "lap_count": stint.End - stint.Start
#             })

#     return {"strategy": strategy}

@session_router.get("/race/telemetry")
def get_telemetry(year: int, gp: int, driver: str):
    session = fastf1.get_session(year, gp, "R")
    session.load()
    lap = session.laps.pick_driver(driver).pick_fastest()
    telemetry = lap.get_car_data().add_distance()

    return {
        "distance": telemetry["Distance"].tolist(),
        "speed": telemetry["Speed"].tolist(),
        "throttle": telemetry["Throttle"].tolist(),
        "brake": telemetry["Brake"].tolist()
    }
