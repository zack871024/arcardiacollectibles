import os
import pandas as pd
import requests
import time
from io import StringIO

# Delay between each CSV fetch, in seconds
FETCH_DELAY_SECONDS = 1

# Optional authentication / header configuration
API_TOKEN = os.getenv('TCGCSV_API_TOKEN')
AUTH_USERNAME = os.getenv('TCGCSV_USER')
AUTH_PASSWORD = os.getenv('TCGCSV_PASS')

DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/csv,application/csv,application/octet-stream;q=0.9,*/*;q=0.8',
}

# URLs of the CSV files to be downloaded
urls = [
    'https://tcgcsv.com/tcgplayer/68/3188/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/3189/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/3190/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/3191/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/3192/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/17658/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/17659/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/17660/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/17661/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/17675/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/17687/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/17698/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/17699/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/22890/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/22930/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/22934/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/22956/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/22957/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23024/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23213/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23232/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23243/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23250/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23272/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23297/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23304/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23333/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23348/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23349/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23368/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23387/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23424/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23462/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23489/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23490/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23491/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23492/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23493/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23494/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23495/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23496/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23512/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23589/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23590/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23737/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23766/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23834/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23890/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23907/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/23991/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24068/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24241/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24242/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24282/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24283/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24284/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24285/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24286/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24287/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24302/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24303/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24304/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24305/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24306/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24537/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24575/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24545/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24575/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24579/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24637/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24677/ProductsAndPrices.csv',
    'https://tcgcsv.com/tcgplayer/68/24664/ProductsAndPrices.csv',
    # Add more URLs as needed
]

# Function to download and process CSV
def download_and_process_csv(urls):
    dfs = []  # List to hold DataFrames

    auth = None
    if AUTH_USERNAME and AUTH_PASSWORD:
        auth = (AUTH_USERNAME, AUTH_PASSWORD)

    headers = DEFAULT_HEADERS.copy()
    if API_TOKEN:
        headers['Authorization'] = f'Bearer {API_TOKEN}'

    session = requests.Session()
    session.headers.update(headers)

    for url in urls:
        # Wait before fetching the next file to avoid hammering the server
        time.sleep(FETCH_DELAY_SECONDS)
        try:
            # Download CSV from the URL
            print(f"Fetching {url}")
            response = session.get(url, auth=auth, timeout=30)
            response.raise_for_status()  # Check for successful download

            # Check if the content is empty
            if not response.text.strip():
                print(f"Warning: No content in CSV file from {url}")
                continue  # Skip this file and move on to the next

            # Read the CSV into a DataFrame using StringIO
            data = StringIO(response.text)
            df = pd.read_csv(data)

            # Append the DataFrame to the list
            dfs.append(df)

        except requests.exceptions.HTTPError as e:
            status = getattr(e.response, 'status_code', 'unknown')
            print(f"HTTP error {status} downloading {url}: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading the file from {url}: {e}")
        except pd.errors.EmptyDataError:
            print(f"Warning: Empty CSV file from {url}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    # If there are no DataFrames, exit the function
    if not dfs:
        print("No valid CSV files were processed.")
        return

    # Combine all DataFrames
    combined_df = pd.concat(dfs, ignore_index=True)

    # Drop certain columns (example: 'column_to_remove')
    columns_to_remove = ['cleanName', 'categoryId', 'groupId', 'modifiedOn', 'imageCount', 'lowPrice', 'midPrice', 'highPrice', 'directLowPrice', 'subTypeName', 'extLife', 'extPower', 'extSubtypes', 'extAttribute', 'extCost', 'extCounterplus']
    combined_df = combined_df.drop(columns=columns_to_remove, errors='ignore')

    # Reformat combined DataFrame to match your database.csv structure
    combined_df = combined_df[['productId','name', 'extNumber', 'imageUrl', 'url', 'marketPrice','extRarity', 'extDescription', 'extColor', 'extCardType',]]  # Adjust as needed

    # Save the final DataFrame as 'search_database.csv'
    combined_df.to_csv('search_database.csv', index=False)
    print("CSV file processed and saved as 'search_database.csv'")

if __name__ == "__main__":
    download_and_process_csv(urls)
