import fastf1
import os
import pandas as pd

# Create cache folder if it doesn’t exist
os.makedirs('./cache', exist_ok=True)
fastf1.Cache.enable_cache('./cache')

def get_driver_lap_times(driver: str, year: int, gp: str, session_type: str):
    try:
        session = fastf1.get_session(year, gp, session_type)
        session.load()

        laps = session.laps.pick_driver(driver)
        if laps.empty:
            return {"error": f"No laps found for driver '{driver}'."}

        return [
            {"lap": int(row["LapNumber"]), "time": row["LapTime"].total_seconds()}
            for _, row in laps.iterrows()
            if pd.notnull(row["LapTime"])
        ]
    except Exception as e:
        print(f"ERROR: {e}")
        return {"error": str(e)}

def get_drivers_in_session(year: int, gp: str, session_type: str = "R"):
    try:
        session = fastf1.get_session(year, gp, session_type)
        session.load()
        driver_codes = session.laps['Driver'].unique().tolist()
        return {"drivers": driver_codes}
    except Exception as e:
        print(f"ERROR: {e}")
        return {"error": str(e)}

def get_session_summary(year: int, gp: str, session_type: str = "R"):
    try:
        session = fastf1.get_session(year, gp, session_type)
        session.load()

        summary = {
            "circuit": session.event['EventName'],
            "location": session.event['Location'],
            "country": session.event['Country'],
            "session_type": session.name,
            "session_date": session.date.isoformat(),
            "weather": {
                "air_temp": str(session.weather_data['AirTemp'].mean()) + "°C" if not session.weather_data.empty else "N/A",
                "humidity": str(session.weather_data['Humidity'].mean()) + "%" if not session.weather_data.empty else "N/A",
                "rainfall": str(session.weather_data['Rainfall'].mean()) + "mm" if not session.weather_data.empty else "N/A",
            },
        }

        return summary
    except Exception as e:
        print(f"ERROR: {e}")
        return {"error": str(e)}

def compare_laps_telemetry(
    year: int,
    gp: str,
    session_type: str,
    driver1: str,
    driver2: str,
    lap: int
):
    try:
        session = fastf1.get_session(year, gp, session_type)
        session.load()

        laps = session.laps

        lap1 = laps[(laps["Driver"] == driver1) & (laps["LapNumber"] == lap)].iloc[0]
        lap2 = laps[(laps["Driver"] == driver2) & (laps["LapNumber"] == lap)].iloc[0]

        tel1 = lap1.get_car_data().add_distance()
        tel2 = lap2.get_car_data().add_distance()

        def simplify_telemetry(data):
            return [
                {
                    "distance": float(d),
                    "speed": float(s),
                    "throttle": float(t),
                    "brake": bool(b),
                    "gear": int(g),
                }
                for d, s, t, b, g in zip(
                    data["Distance"],
                    data["Speed"],
                    data["Throttle"],
                    data["Brake"],
                    data["nGear"],
                )
            ]

        return {
            driver1: simplify_telemetry(tel1),
            driver2: simplify_telemetry(tel2)
        }

    except Exception as e:
        print(f"ERROR: {e}")
        return {"error": str(e)}
