import json
import mysql.connector
from datetime import datetime

# Connect to the MySQL database
myDb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="parola123"
)

myCursor = myDb.cursor()

# Create a database if it doesn't already exist
myCursor.execute("CREATE DATABASE IF NOT EXISTS food_ingredients")

# Select the database
myCursor.execute("USE food_ingredients")

# # Drop existing tables
# myCursor.execute("DROP TABLE IF EXISTS Compound")
# myCursor.execute("DROP TABLE IF EXISTS CompoundsHealthEffect")
# myCursor.execute("DROP TABLE IF EXISTS HealthEffect")

### todo check if the name has to be unique
# Create new tables with corrected column names
createCompoundTable = """
CREATE TABLE IF NOT EXISTS Compound (
    id INT PRIMARY KEY,
    public_id VARCHAR(255),
    name VARCHAR(255),
    state VARCHAR(255),
    annotation_quality VARCHAR(255),
    description TEXT,
    cas_number VARCHAR(255),
    moldb_smiles TEXT,
    moldb_inchi TEXT,
    moldb_mono_mass VARCHAR(255),
    moldb_inchikey VARCHAR(255),
    moldb_iupac TEXT,
    kingdom VARCHAR(255),
    superklass VARCHAR(255),
    klass VARCHAR(255),
    subklass VARCHAR(255)
)
"""

createCompoundsHealthEffectTable = """
CREATE TABLE IF NOT EXISTS CompoundsHealthEffect (
    id INT PRIMARY KEY,
    compound_id INT,
    health_effect_id INT,
    orig_health_effect_name VARCHAR(255),
    orig_compound_name VARCHAR(255),
    orig_citation TEXT,
    citation VARCHAR(255),
    citation_type VARCHAR(255),
    created_at DATETIME,
    updated_at DATETIME,
    creator_id INT,
    updater_id INT,
    source_id INT,
    source_type VARCHAR(255)
)
"""

createHealthEffectTable = """
CREATE TABLE IF NOT EXISTS HealthEffect (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    chebi_name VARCHAR(255),
    chebi_id VARCHAR(255),
    created_at DATETIME,
    updated_at DATETIME,
    creator_id INT,
    updater_id INT,
    chebi_definition TEXT
)
"""


# Function to create tables
def createTable(query):
    myCursor.execute(query)


createTable(createCompoundTable)
createTable(createCompoundsHealthEffectTable)
createTable(createHealthEffectTable)


# Convert datetime from string to DATETIME format
def convertDatetime(dateStr):
    if dateStr:
        try:
            return datetime.strptime(dateStr, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return datetime.strptime(dateStr, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
    return None


# Insert data into a specified table
def insertData(table, data):
    if not data:
        return

    columns = ', '.join(data[0].keys())
    placeholders = ', '.join(['%s'] * len(data[0]))
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

    # Convert dictionaries to list of tuples
    values = [tuple(d.values()) for d in data]

    myCursor.executemany(sql, values)
    myDb.commit()


# Load data from JSON files
with open("InitialTables/Compound.json", encoding='utf-8') as compoundTable:
    compoundData = [json.loads(line) for line in compoundTable]

with open("InitialTables/CompoundsHealthEffect.json", encoding='utf-8') as compoundHealthEffectTable:
    compoundHealthEffectData = [json.loads(line) for line in compoundHealthEffectTable]
    for item in compoundHealthEffectData:
        item['created_at'] = convertDatetime(item.get('created_at'))
        item['updated_at'] = convertDatetime(item.get('updated_at'))

with open("InitialTables/HealthEffect.json", encoding='utf-8') as healthEffectTable:
    healthEffectData = [json.loads(line) for line in healthEffectTable]
    for item in healthEffectData:
        item['created_at'] = convertDatetime(item.get('created_at'))
        item['updated_at'] = convertDatetime(item.get('updated_at'))

# Insert data into tables
insertData('Compound', compoundData)
insertData('CompoundsHealthEffect', compoundHealthEffectData)
insertData('HealthEffect', healthEffectData)

print("Data inserted successfully!")

# Close the connection
myCursor.close()
myDb.close()
