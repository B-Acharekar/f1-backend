import fastf1
import os
import pandas as pd
from fastf1.events import get_event_schedule

os.makedirs('./cache', exist_ok=True)
fastf1.Cache.enable_cache('./cache')

def get_driver_lap_times(driver: str, year: int, gp: str, session_type: str, best_only: bool = False):
    try:
        session = fastf1.get_session(year, gp, session_type)
        session.load()

        laps = session.laps.pick_driver(driver)
        if laps.empty:
            return {"error": f"No laps found for driver '{driver}'."}

        if best_only:
            best = laps.pick_fastest()
            return [{
                "lap": int(best["LapNumber"]),
                "time": best["LapTime"].total_seconds(),
                "sectors": {
                    "S1": best["Sector1Time"].total_seconds() if pd.notnull(best["Sector1Time"]) else None,
                    "S2": best["Sector2Time"].total_seconds() if pd.notnull(best["Sector2Time"]) else None,
                    "S3": best["Sector3Time"].total_seconds() if pd.notnull(best["Sector3Time"]) else None,
                }
            }]

        return [
            {
                "lap": int(row["LapNumber"]),
                "time": row["LapTime"].total_seconds(),
                "is_pit": pd.notnull(row["PitOutTime"]) or pd.notnull(row["PitInTime"])
            }
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

        event = session.event
        weather = session.weather_data

        summary = {
            "circuit": event['EventName'],
            "location": event['Location'],
            "country": event['Country'],
            "session_type": session.name,
            "session_date": session.date.isoformat(),
            "weather": {
                "air_temp": f"{weather['AirTemp'].mean():.1f}°C" if not weather.empty else "N/A",
                "humidity": f"{weather['Humidity'].mean():.1f}%" if not weather.empty else "N/A",
                "rainfall": f"{weather['Rainfall'].mean():.1f}mm" if not weather.empty else "N/A",
            },
        }

        return summary
    except Exception as e:
        print(f"ERROR: {e}")
        return {"error": str(e)}

def compare_laps_telemetry(year: int, gp: str, session_type: str, driver1: str, driver2: str, lap: int):
    try:
        session = fastf1.get_session(year, gp, session_type)
        session.load()

        laps = session.laps
        lap1 = laps[(laps["Driver"] == driver1) & (laps["LapNumber"] == lap)]
        lap2 = laps[(laps["Driver"] == driver2) & (laps["LapNumber"] == lap)]

        if lap1.empty or lap2.empty:
            return {"error": "Lap not found for one or both drivers."}

        tel1 = lap1.iloc[0].get_car_data().add_distance()
        tel2 = lap2.iloc[0].get_car_data().add_distance()

        def simplify_telemetry(data):
            return [
                {
                    "distance": float(d),
                    "speed": float(s),
                    "throttle": float(t),
                    "brake": bool(b),
                    "gear": int(g)
                }
                for d, s, t, b, g in zip(
                    data["Distance"],
                    data["Speed"],
                    data["Throttle"],
                    data["Brake"],
                    data["nGear"]
                )
            ]

        return {
            driver1: simplify_telemetry(tel1),
            driver2: simplify_telemetry(tel2)
        }

    except Exception as e:
        print(f"ERROR: {e}")
        return {"error": str(e)}

def get_event_names_for_year(year: int):
    try:
        schedule = get_event_schedule(year)
        return {"events": schedule['EventName'].dropna().unique().tolist()}
    except Exception as e:
        return {"error": str(e)}
    
def get_next_race(year: int):
    try:
        schedule = get_event_schedule(year)
        now = pd.Timestamp.now(tz='UTC')

        future_events = schedule[schedule['Session1Date'] > now]
        if future_events.empty:
            return {"message": "No upcoming races this season."}

        next_event = future_events.iloc[0]
        return {
            "event": next_event['EventName'],
            "location": next_event['Location'],
            "country": next_event['Country'],
            "session_type": "R",  # You can adjust this dynamically if needed
            "session_date": next_event['Session1Date'].isoformat()
        }

    except Exception as e:
        print(f"[NEXT RACE ERROR] {e}")
        return {"error": str(e)}
        