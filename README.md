# CCI Metadata Extractor

Package to read CCI datasets and extract high level metadata into a JSON object for each dataset.


## JSON Structure

```json
{
    "var": {
        "default":"bool",
        "type": "primary | auxiliary",
        "parent": "string", #only if type == auxiliary
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
