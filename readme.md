# Aviation Weather
A RESTful way to get METARs and TAFs
## Requirements
- Python 2.7
- Requests
- JSON
- Flask
- SQLite3

### Usage
After launching the app:
- Query `/<ICAO_Code>` for METAR
- Query `/<ICAI_Code>/taf` for TAF
- Append `?summary` for a more human readable result

### Data Sources:
Airport Info - [ourairports.com](ourairports.com)
Weather Info - [avwx.rest](avwx.rest)
