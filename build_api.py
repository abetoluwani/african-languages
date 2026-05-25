import csv
import json
import os
import shutil
import reverse_geocoder as rg

INPUT_FILE = "african_languages.csv"
API_DIR = "api/v1"

def build_api():
    if os.path.exists(API_DIR):
        shutil.rmtree(API_DIR)
    
    os.makedirs(os.path.join(API_DIR, "language"), exist_ok=True)
    os.makedirs(os.path.join(API_DIR, "country"), exist_ok=True)
    
    languages = []
    total_languages = 0
    total_dialects = 0
    
    coords_to_geocode = []
    indices_to_geocode = []
    
    # First pass: read and clean data
    with open(INPUT_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            # Clean up types
            lat = row.get("latitude")
            lon = row.get("longitude")
            
            try:
                row["latitude"] = float(lat) if lat else None
            except ValueError:
                row["latitude"] = None
                
            try:
                row["longitude"] = float(lon) if lon else None
            except ValueError:
                row["longitude"] = None
                    
            if row.get("level") == "language":
                total_languages += 1
            elif row.get("level") == "dialect":
                total_dialects += 1
                
            row["country_code"] = "unknown"
            
            languages.append(row)
            
            if row["latitude"] is not None and row["longitude"] is not None:
                coords_to_geocode.append((row["latitude"], row["longitude"]))
                indices_to_geocode.append(i)
                
    # Reverse Geocode in bulk
    print(f"Reverse geocoding {len(coords_to_geocode)} coordinates...")
    if coords_to_geocode:
        results = rg.search(coords_to_geocode)
        for i, result in zip(indices_to_geocode, results):
            languages[i]["country_code"] = result["cc"].lower()
            
    # Write individual files and collect country data
    country_groups = {}
    
    for row in languages:
        cc = row["country_code"]
        if cc not in country_groups:
            country_groups[cc] = []
        country_groups[cc].append(row)
        
        glottocode = row.get("glottocode")
        if glottocode:
            lang_file = os.path.join(API_DIR, "language", f"{glottocode}.json")
            with open(lang_file, "w", encoding="utf-8") as lf:
                json.dump(row, lf, indent=2, ensure_ascii=False)
                
    # Write country files
    for cc, langs in country_groups.items():
        country_file = os.path.join(API_DIR, "country", f"{cc}.json")
        with open(country_file, "w", encoding="utf-8") as cf:
            json.dump(langs, cf, indent=2, ensure_ascii=False)
            
    # Write full list
    with open(os.path.join(API_DIR, "languages.json"), "w", encoding="utf-8") as lf:
        json.dump(languages, lf, indent=2, ensure_ascii=False)
        
    # Write countries list
    with open(os.path.join(API_DIR, "countries.json"), "w", encoding="utf-8") as cf:
        json.dump(list(country_groups.keys()), cf, indent=2, ensure_ascii=False)
        
    # Write summary
    summary = {
        "total_records": len(languages),
        "total_languages": total_languages,
        "total_dialects": total_dialects,
        "total_countries": len(country_groups)
    }
    with open(os.path.join(API_DIR, "summary.json"), "w", encoding="utf-8") as sf:
        json.dump(summary, sf, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    print(f"Building API from {INPUT_FILE}...")
    build_api()
    print("API build complete.")
