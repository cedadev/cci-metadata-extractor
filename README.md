# CCI Metadata Extractor

Package to read CCI datasets and extract high level metadata into a JSON object for each dataset.

## JSON Structure

```json
{
    "var": {
        "default":"bool",
        "type": "primary | auxiliary | coordinate",
        "min":"float",
        "max": "float",
        "units": "string",
        "display": {
            "min": "float",
            "max": "float",
            "colour": "string",
            "class_encoding": ["array"]
      }
    },
    ...
    "var_n": {}
}
```
## Configuration

There are various configurable parameters.

### defaults.py

In `cci_scanner/conf/defaults.py` you will find the default options.
These are global defaults and any matches will apply to all datasets.
Defaults comprise of:

- DEFAULT_VARIABLES

    A list of variables to mark as default when they are encountered.

- COORDINATE_VARIABLES
    
    A list of variables to mark as coordinates by default. All variables with the
    same name as the first dimension name are marked as coordinates without explicitly
    setting here.

- AUXILIARY_COORDINATES

    A list of variables to mark as auxiliary.

- VARIABLE_DISPLAY_SETTINGS

    A dictionary containing mappings for the display settings for each variable.
    The key is the variable name with a dict as the value. These settings will override
    the values extracted from the file
    
### custom_mapping.json

In `cci_scanner/conf/custom_mapping.json` you will find a json file which
allows you to override the output for specific ids.

IDs are matched using regular expressions so:

    esacci.SOILMOISTURE.day.L3S.*

will match:

    esacci.SOILMOISTURE.day.L3S.SSMS.multi-sensor.multi-platform.ACTIVE.03-2.r1.v20170611
    esacci.SOILMOISTURE.day.L3S.SSMS.multi-sensor.multi-platform.ACTIVE.04-2.r1.v20180618
    esacci.SOILMOISTURE.day.L3S.SSMV.multi-sensor.multi-platform.COMBINED.03-2.r1.v20170611
    esacci.SOILMOISTURE.day.L3S.SSMV.multi-sensor.multi-platform.COMBINED.04-2.r1.v20180618
    esacci.SOILMOISTURE.day.L3S.SSMV.multi-sensor.multi-platform.PASSIVE.03-2.r1.v20170611
    esacci.SOILMOISTURE.day.L3S.SSMV.multi-sensor.multi-platform.PASSIVE.04-2.r1.v20180618

You could override valuses in the output using this matching.
E.g.

MODIS Longitude Values:

    "lon": {
        "default": false, 
        "units": "degrees_east", 
        "statistics": {
            "max": 179.75, 
            "min": -179.75
        }, 
        "type": "primary", 
        "display": {
            "display_max": 180.0, 
            "color_map": "inferno", 
            "display_min": 179.0, 
            "scale": "linear"
        }
    }
    
Example setup of custom_mapping.json

```json
{
  "esacci.CLOUD.mon.L3C.CLD_PRODUCTS.MODIS.Aqua.*" :{
    "lon": {
       "statistics": {
          "max": 180,
          "min": -180
       }
    }
  }
} 
```

This would overwrite the max and min values for lon to +-180 for all IDs which 
match the pattern.
