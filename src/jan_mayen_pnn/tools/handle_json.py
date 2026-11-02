import json

def load_data(path: str) -> list[list]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    records = []

    features = [
        "air_temperature",
        "relative_humidity",
        "visibility_in_air_poorest_direction",
        "weather_type"
    ]

    for item in data["data"]:
        observations = {}

        for obs in item["observations"]:
            # Temperatura występuje w różnych rozdzielczościach
            # Wybieramy pomiar godzinowy
            if (
                obs["elementId"] == "air_temperature"
                and obs.get("timeResolution") != "PT1H"
            ):
                continue

            observations[obs["elementId"]] = obs["value"]

        if all(feature in observations for feature in features):
            record = [
                observations[feature]
                for feature in features
            ]
            records.append(record)

    return records

def get_weather_type_dict():
    with open("dataset/weather_type_code_table.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    result = dict()
    for i in range(len(data["data"][0]["values"])):
        result[int(data["data"][0]["values"][i]["value"])] = data["data"][0]["values"][i]["description"]
    
    return result 

if __name__ == "__main__":
    print(get_weather_type_dict())