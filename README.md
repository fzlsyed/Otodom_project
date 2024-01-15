# Otodom_project
This repository contains the code for a project that uses Bright Data to scrape real estate data from the website Otodom. SnowflakeSQL and Python are then used to clean and analyze the real estate data. 

# Step-by-Step Process 

## Step 1: Scraping the Data
The web scraper website, Bright Data, contains databases from various websites including Otodom. The Otodom database was selected and exported into a SnowflakeSQL account. The database is also included in this repository under the file name 'OtodomPoland.json'.

## Step 2A: Flattening the Data
The file 'SQL_DataFlatten' contains the SQL code that was used to create columns for different sections of the data.

## Step 2B: Converting the Data
The file 'Address.py" contains the Python code that was used to convert latitude and longitude data into Addresses.

## Step 2C: Translating the Data
The file 'TranslateTitle.py' contains the Python code that was used to translate the real estate title data from Polish into English. This was done using the pandas library along with Google Cloud's Google Drive and Google Sheets APIs which allowed for the data to be parsed into Google Sheets and then translated using a formula. The 'SheetstoSnowflake.py' file is the Python code that was then used to parse the translated data back into SnowflakeSQL. 
