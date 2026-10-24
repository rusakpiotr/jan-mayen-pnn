
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

queries = {
    "station_metadata": (
        "/sources/v0.jsonld",
        {
            "ids": STATION
        }
    ),
    "observations": (
        "/observations/v0.jsonld",
        {
            "sources": STATION,
            "referencetime": "2025-01-01/2025-01-02",
            "elements": (
                "air_temperature,"
                "wind_speed,"
                "wind_from_direction,"
                "surface_air_pressure,"
                "relative_humidity,"
                "weather_type",
                "cloud_base"
            )
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

for name, (path, params) in queries.items():
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
            encoding="utf-8"
        )

        print("Records:", len(data.get("data", [])))
    else:
        print(response.text[:500])
