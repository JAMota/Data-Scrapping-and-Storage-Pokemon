# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 00:41:59 2024

@author: AndreMota
"""

import requests
import configparser
import psycopg2
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
            usage_percentage = float(columns[2].rstrip('%')) #/  100  # Convert percentage to decimal
            raw = int(columns[3])
            # Append the data to the list
            pokemon_data.append((pokemon_name, usage_percentage, raw))
        else:
            print(f"Unable to split line into columns: {line}")
else:
    print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")

# Now you have a list of tuples with the Pokémon name, Usage %, and Raw
print(pokemon_data)




# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the .ini file
config.read('database.ini')

# Access the database section
db_config = config['postgres']


# Now you can access individual items like this:
host = db_config['host']
dbname = db_config['dbname']
user = db_config['user']
password = db_config['password']
port = db_config['port']
endpoint = db_config['endpoint']

# Combine the password with the endpoint for the initial connection
initial_password = f"{endpoint}${password}"

# Establish the connection with SSL enforced
conn = psycopg2.connect(
    host=host,
    database=dbname,
    user=user,
    password=initial_password,
    port=port,
    sslmode='require'
)

cur = conn.cursor()

# Create the table if it doesn't exist
create_table_query = '''
CREATE TABLE IF NOT EXISTS PokemonData (
    id SERIAL PRIMARY KEY,
    name VARCHAR(75) NOT NULL,
    usage_percentage DECIMAL(10,   9) NOT NULL,
    raw_count INTEGER NOT NULL
);
'''
cur.execute(create_table_query)
conn.commit()



# Insert the scraped data into the table
for row in pokemon_data:
    insert_query = '''
    INSERT INTO PokemonData (name, usage_percentage, raw_count) VALUES (%s, %s, %s);
    '''
    cur.execute(insert_query, (row[0], row[1], row[2]))
conn.commit()

# Close the cursor and the connection
cur.close()
conn.close()