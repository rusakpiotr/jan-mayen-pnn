# Dataset description

Data from NOAA meteorogical station, located on Jan Mayen. Jan Mayen is Norway's island between iceland and greenland. There are no causal inhibitants, only scientists and military.

Data is really scrupulous and detailed, registered and shared daily since 2015. Best way to get insight is describing features.

## Features

All of features are detailed here:
```
https://frost.met.no/elementtable?utm_source=chatgpt.com
```

### Features we will use

TODO

## Measurement errors

One does not simply to get Jan Mayen measurements uncertainity. Its available through Frost API. Official MET's Norway API.

The station id is:
```
SN99950
```

I used fetch_frost.py to get informations about that station and then. In observations.json each observation has "performanceCategory". Its scale is:

- A: The sensor type fulfills the requirements from WMO/CIMOs on measurement accuracy, calibration and maintenance.
- B: Rutines for calibration and maintanance are known. Control of the montage exists. The precision of the measurment is lower than the WMO/CIMO requirements.
- C: The sensor type is assumed to fulfill the WMO/CIMO requirements. Missing measurement for control, rutines for calibration, or maintanence.
- D: The sensor type is assumed to fulfill the WMO/CIMO requirements. Some controls show deviations from the WMO/CIMO requirements.
- E: Less valuable. Possibly useful for extraordinary purposes. Unknown performance

That scale is available at:
```
https://frost.met.no/dataclarifications.html?utm_source=chatgpt.com
```

Fortunatelly, sensors on Jan Mayen station have C category, so I assume its enough to use WMO/CIMO uncertainities.

## Probabilistic layer structure

## Agregation layer

## Decisive layer

## Results