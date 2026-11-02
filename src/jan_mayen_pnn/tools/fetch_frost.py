
import yaml
import requests
import json
from pathlib import Path

ROOT = next(
    p for p in Path(__file__).resolve().parents
    if p.name == "jan-mayen-pnn"
)

with open(ROOT / "config.yml", "r") as f:
    config = yaml.safe_load(f)

CLIENT_ID = config["client_id"]
STATION = config["station"]

session = requests.Session()
session.auth = (CLIENT_ID, "")

base = "https://frost.met.no"
out = ROOT / "dataset"
out.mkdir(parents=True, exist_ok=True)

HOURS = [
    "6:00",
    "9:00",
    "12:00",
    "15:00"
]

def observation_template(referancetime: str, *args):
    temp = ",".join(args)
    return (
        "/observations/v0.jsonld",
        {
            "sources": STATION,
            "referencetime": referancetime,
            "elements": temp
        }
    )

metadata_queries = {
    "station_metadata": (
        "/sources/v0.jsonld",
        {
            "ids": STATION
        }
    ),
    "air_pressure_element": (
        "/elements/v0.jsonld",
        {
            "ids": "air_pressure",
            "lang": "en-US"
        }
    ),
    "relative_humidity_element": (
        "/elements/v0.jsonld",
        {
            "ids": "relative_humidity",
            "lang": "en-US"
        }
    ),
    "air_temperature_element": (
        "/elements/v0.jsonld",
        {
            "ids": "air_temperature",
            "lang": "en-US"
        }
    ),
    "visibility_in_air_poorest_direction_element": (
        "/elements/v0.jsonld",
        {
            "ids": "visibility_in_air_poorest_direction",
            "lang": "en-US"
        }
    ),
    "wind_speed_element": (
        "/elements/v0.jsonld",
        {
            "ids": "wind_speed",
            "lang": "en-US"
        }
    ),
    "weather_element": (
        "/elements/v0.jsonld",
        {
            "ids": "weather_type",
            "lang": "en-US"
        }
    ),
    "weather_type_code_table": (
        "/elements/codeTables/v0.jsonld",
        {
            "ids": "Været ved observasjonstida",
            "lang": "en-US"
        }
    ),
}

for name, (path, params) in metadata_queries.items():
    response = session.get(
        base + path,
        params=params,
        timeout=30
    )

    print(name, response.status_code)

    if response.ok:
        data = response.json()

        (out / f"{name}.json").write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        print("Records:", len(data.get("data", [])))
    else:
        print(response.text[:500])

observations_queries = dict()
for i, hour in enumerate(HOURS):
    observations_queries[str(i)] = observation_template(
        f"R2/2025-01-01T{hour}/2025-06-30T{hour}/P1D",
        "air_temperature",
        "relative_humidity",
        "visibility_in_air_poorest_direction",
        "weather_type"
    )

temp = None
for name, (path, params) in observations_queries.items():
    response = session.get(
        base + path,
        params=params,
        timeout=30
    )

    print(name, response.status_code)

    if response.ok:
        data = response.json()
        if temp == None:
            temp = data
        else:
            if type(data["data"]) != list:
                temp["data"].append(data["data"])
            else:
                temp["data"].extend(data["data"])

        print("Records:", len(data.get("data", [])))
    else:
        print(response.text[:500])

with open((out / "observations.json"), "w") as f:
    f.write(json.dumps(temp, indent=2, ensure_ascii=False))