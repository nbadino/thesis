import requests
import csv
from datetime import datetime, timedelta
import os
import sys
import shutil

def download_and_rename_file(url, original_filename, new_filename_prefix, destination_path):
    # Send HTTP request to the specified URL and save the response from server in a response object called r
    r = requests.get(url)

    # Open a csv file in write mode
    with open(original_filename, 'w') as f:
        f.write(r.text)

    # Open the csv file in read mode
    with open(original_filename, 'r') as f:
        reader = csv.reader(f)
        # Get the first row
        first_row = next(reader)
        # Extract the date string
        date_string = first_row[0].split(' ')[2]
        date_object = datetime.strptime(date_string, '%Y-%m-%d')

    # Get yesterday's date
    yesterday = datetime.now() - timedelta(days=1)

    if date_object.date() != yesterday.date():
        # Remove the file
        os.remove(original_filename)
        # Exit the script
        sys.exit("The date in the file is not yesterday's date.")
    else:
        # Define the new filename
        new_filename = new_filename_prefix + yesterday.strftime('%m%d')
        
        # Add the extension
        new_filename += ".csv"
        
        # Check if the new filename already exists
        if os.path.exists(os.path.join(destination_path, new_filename)):
            # If it exists, remove the original file and exit the script
            os.remove(original_filename)
            sys.exit(f"The file {new_filename} already exists.")
        
        # Move and rename the file
        shutil.move(original_filename, os.path.join(destination_path, new_filename))

# Download and rename the first file
download_and_rename_file(
    'https://www.mimit.gov.it/images/exportCSV/prezzo_alle_8.csv', 
    'prezzo_alle_8.csv', 
    'price_', 
    'data/nuovi/prices/'
)

# Download and rename the second file
download_and_rename_file(
    'https://www.mimit.gov.it/images/exportCSV/anagrafica_impianti_attivi.csv', 
    'anagrafica_impianti_attivi.csv', 
    'name_', 
    'data/nuovi/gas_station_info/'
)
