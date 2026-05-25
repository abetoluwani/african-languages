import csv

def extract_african_languages(input_file: str, output_file: str):
    """
    Reads the Glottolog languages and dialects geography dataset
    and extracts only the entries located in the 'Africa' macroarea.
    """
    with open(input_file, mode='r', encoding='utf-8') as infile, \
         open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        
        reader = csv.DictReader(infile)
        
        # Check that we have the necessary columns
        if not reader.fieldnames or 'macroarea' not in reader.fieldnames:
            print("Error: The input file does not have a 'macroarea' column.")
            return

        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        
        count = 0
        for row in reader:
            if row['macroarea'] == 'Africa':
                writer.writerow(row)
                count += 1
                
        print(f"Extraction complete! Filtered {count} African languages/dialects.")

if __name__ == '__main__':
    extract_african_languages('languages_and_dialects_geo.csv', 'african_languages.csv')
