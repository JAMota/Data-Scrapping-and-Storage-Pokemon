# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 00:41:59 2024

@author: AndreMota
"""

import requests
from decimal import Decimal, ROUND_DOWN ## to remove rounding errors
from bs4 import BeautifulSoup

# Replace with the actual URL of the page containing the usage statistics
url = "https://www.smogon.com/stats/2015-01/ou-0.txt"
response = requests.get(url)

# Ensure the response was successful
if response.status_code ==  200:
    # Split the response text into lines
    lines = response.text.split('\n')
    
    # Initialize a list to hold the parsed data
    pokemon_data = []
    
    # Flag to indicate when we start processing the data
    processing_data = False
    
    # Iterate over each line
    for line in lines:
        # Check if the line starts with the pattern for data rows
        if line.strip().startswith("| Rank"):
            processing_data = True
            continue  # Skip the rest of the loop iteration
        
        # If we're not processing data yet, skip this line
        if not processing_data:
            continue
        
        # Split the line into columns by pipe character
        columns = line.split('|')
        # Strip leading and trailing whitespace from each column
        columns = [col.strip() for col in columns if col.strip()]
        
        # Ensure there are enough columns to extract the required data
        if len(columns) >=  4:
            # Extract the Pokémon name, Usage %, and Raw
            pokemon_name = columns[1]
            usage_percentage = float(columns[2].rstrip('%')) /  100  # Convert percentage to decimal
            raw = int(columns[3])
            # Append the data to the list
            pokemon_data.append((pokemon_name, usage_percentage, raw))
        else:
            print(f"Unable to split line into columns: {line}")
else:
    print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")

# Now you have a list of tuples with the Pokémon name, Usage %, and Raw
print(pokemon_data)