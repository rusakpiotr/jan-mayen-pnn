# Dataset description

Data from meteorogical station, located on Jan Mayen. Jan Mayen is Norway's island on north-east direction from Iceland. There are no causal inhibitants, only scientists and military.

Data is really scrupulous and detailed. Best way to get insight is describing features.

## Features

All of features are detailed here:
```
https://frost.met.no/elementtable?utm_source=chatgpt.com
```

Hint, sort records by category.

Categories:

- Athmospheric pressure
- Clouds
- Evaporation
- Humidity
- Icing
- Metadata
- Ocean waves
- Operation
- Precipitation
- Radiation
- Sea ice
- Sea water
- Snow and state of ground
- Sunshine
- Temperature
- Vegetation
- Visibility
- Water level
- Weather
- Wind

For the sake of simplicity (and mental health), we will use only few of them:

- Athmospheric pressure
- Clouds
- Humidity
- Temperature
- Visibility
- Wind

### Exact features

- air_pressure
<!-- - cloud_base_height -->
<!-- - cloud_area_fraction -->
<!-- - dew_point_height_estimated -->
<!-- - dew_point_temperature -->
- relative_humidity
<!-- - latitude -->
<!-- - longtitude -->
<!-- - road_friction -->
<!-- - surface_snow_thickness -->
- air_temperature
<!-- - soil_temperature -->
<!-- - surface_temperature -->
- visibility_in_air_poorest_direction
- wind_speed
<!-- - wind_from_direction -->

### Target variables

Because, we want to make a classifier, our first goal is to predict:

- weather_type

Its scale is described in:

```
dataset/weather_type_code_table.json
```

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

Uncertainities can be found at:
```
https://community.wmo.int/site/knowledge-hub/programmes-and-initiatives/instruments-and-methods-of-observation-programme-imop/guide-instruments-and-methods-of-observation-wmo-no-8?utm_source=chatgpt.com
```

And uncertainities of features used in PNN will be typed into config.yml.

## What is PNN

Its a neural network that has 4 layers:
- input layer
- probabilistic layer
- agregation layer
- decisive layer

Input layer is obvious.

Probabilistic layer computes similarity of input with each record.

Obviously data in input layer and data used in probabilistic layer creation is normalised.

Agregation layer calculates avarage neuron activation for each target variable.

Decisive layer is a classifier, that uses output of agregation layer as input and returns prediction.

How to use uncertainities here?

Using each record and uncertainities, we calculate gauss funciton, and then sample in certain amount of times. And than we create additional neurons in probabilistic layer.

In agregation layer, we calculate probability of occurance targer variable.

## Probabilistic layer structure

## Agregation layer

## Decisive layer

## Results