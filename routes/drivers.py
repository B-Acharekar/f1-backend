from fastapi import APIRouter, HTTPException
from db.mongo import db
from bson.objectid import ObjectId

driver_router = APIRouter()

@driver_router.get("/drivers")
async def get_all_drivers():
    try:
        cursor = db.drivers.find()
        drivers = await cursor.to_list(length=None)

        for driver in drivers:
            driver["_id"] = str(driver["_id"])

        return {"drivers": drivers}

    except Exception as e:
        print(f"[ERROR] Failed to fetch drivers from DB: {e}")
        return {"error": f"Failed to fetch drivers from database: {str(e)}"}


@driver_router.get("/drivers/{abbrv}")
async def get_driver_by_abbrv(abbrv: str):
    try:
        driver = await db.drivers.find_one({"abbrv": abbrv.upper()})
        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found")

        driver["_id"] = str(driver["_id"])
        return {"driver": driver}

    except Exception as e:
        print(f"[ERROR] Failed to fetch driver '{abbrv}': {e}")
        return {"error": f"Failed to fetch driver '{abbrv}': {str(e)}"}
