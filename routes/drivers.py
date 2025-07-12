from fastapi import APIRouter
from fastf1 import get_session
import fastf1
import datetime

from data.driver_image_map import driver_image_map  # Ensure this is correct

fastf1.Cache.enable_cache("cache")

driver_router = APIRouter()


@driver_router.get("/drivers")
def get_top_drivers(year: int = datetime.datetime.now().year, round_number: int = 1):
    try:
        session = get_session(year, round_number, "R")
        session.load()

        drivers_data = []
        for drv_num in session.drivers:
            drv_info = session.get_driver(drv_num)
            abbrev = drv_info.Abbreviation

            print(f"Processing driver: {abbrev} - {drv_info.FullName}")
            photo_url = driver_image_map.get(abbrev, "/default-driver.png")

            drivers_data.append({
                "name": drv_info.FullName,
                "team": drv_info.TeamName,
                "number": abbrev,
                "photo": photo_url,
                "link": f"/drivers/{drv_num.lower()}",
                "nationality": "N/A"
            })

        return {"drivers": drivers_data}

    except Exception as e:
        print(f"[ERROR] Failed to fetch drivers: {e}")
        return {"error": f"Failed to fetch drivers using FastF1: {str(e)}"}
