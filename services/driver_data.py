# services/driver_data.py
import requests

def get_top_drivers(limit: int = 10):
    url = "http://ergast.com/api/f1/current/driverStandings.json"
    resp = requests.get(url)
    resp.raise_for_status()
    standings = resp.json()["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]

    drivers = []
    for d in standings[:limit]:
        drv = d["Driver"]
        constructors = d["Constructors"][0]["name"]
        drivers.append({
            "name": f"{drv['givenName']} {drv['familyName']}",
            "team": constructors,
            "number": drv["permanentNumber"],
            "photo": f"https://via.placeholder.com/400x400?text={drv['givenName']}_{drv['familyName']}",
            "link": f"/drivers/{drv['driverId']}",
            "nationality": drv.get("nationality", "")
        })

    return {"drivers": drivers}
