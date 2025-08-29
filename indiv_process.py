import pandas as pd
import requests
from io import StringIO

# URLs of the CSV files to be downloaded
urls = [
    'https://tcgcsv.com/tcgplayer/68/24241/ProductsAndPrices.csv',
    # Add more URLs as needed
]

# Function to download and process CSV
def download_and_process_csv(urls):
    dfs = []  # List to hold DataFrames

    for url in urls:
        try:
            # Download CSV from the URL
            response = requests.get(url)
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

    # Save the final DataFrame as 'database.csv'
    combined_df.to_csv('database.csv', index=False)
    print("CSV file processed and saved as 'database.csv'")

if __name__ == "__main__":
    download_and_process_csv(urls)
