# African Languages Dataset & API

This repository provides a comprehensive dataset and a **Static API** of African languages
## Contents
- `api/v1/`: The automatically generated Static JSON API ready for use.
- `african_languages.csv`: The filtered CSV dataset containing languages from the "Africa" macroarea.
- `build_api.py`: Python script that reverse-geocodes the coordinates and builds the Static API.
- `extract.py`: Python script used to extract African languages from the original Glottolog dataset.

## Using the Static API

This repository acts as a highly available, zero-latency static API hosted via GitHub Pages. You can fetch the JSON endpoints directly in your application!

Base URL: `https://abetoluwani.github.io/african-languages/api/v1`

### Endpoints

- **GET `/languages.json`**: Returns an array of **all** African languages and dialects.
- **GET `/countries.json`**: Returns an array of all available country codes (e.g. `["ng", "za", ...]`).
- **GET `/summary.json`**: Returns metrics on the dataset (total languages, dialects, countries).
- **GET `/country/{country_code}.json`**: Returns an array of all languages spoken in a specific country. (Example: `/country/ng.json` for Nigeria).
- **GET `/language/{glottocode}.json`**: Returns the details for a single specific language. (Example: `/language/aari1239.json`).

### Examples (JavaScript)

**1. Fetch all African languages (The entire dataset at once)**
```javascript
fetch("https://abetoluwani.github.io/african-languages/api/v1/languages.json")
  .then(res => res.json())
  .then(data => console.log(`Loaded ${data.length} languages!`));
```

**2. Fetch all languages spoken in a specific country (e.g., Nigeria)**
```javascript
fetch("https://abetoluwani.github.io/african-languages/api/v1/country/ng.json")
  .then(res => res.json())
  .then(data => console.log(data));
```

**3. Fetch details for a single specific language (e.g., Aari)**
```javascript
fetch("https://abetoluwani.github.io/african-languages/api/v1/language/aari1239.json")
  .then(res => res.json())
  .then(data => console.log(data.name));
```

## Original Data Source
The original dataset `languages_and_dialects_geo.csv` was downloaded from Glottolog (Version 5.3). 
The data is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
The code (scripts) are licensed under the MIT License.
