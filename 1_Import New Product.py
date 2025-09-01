import pandas as pd
import requests
import math
from io import StringIO

##############################################################
##############################################################
#### PUT NEW PRODCUT URL DOWN BELOW, REMOVE EXISITING ONES####
##############################################################
##############################################################

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
    combined_df.to_csv('new_product_database.csv', index=False)
    print("CSV file processed and saved as 'new_product_database.csv'")

def generate_formatted_csv(input_file='new_product_database.csv', output_file='formatted_import_shopify.csv'):
    # Read the existing database.csv
    df = pd.read_csv(input_file)

    # Build Title = name + (extNumber) if exists
    df['Title'] = df.apply(
        lambda row: f"{row['name']} ({row['extNumber']})"
        if pd.notna(row['extNumber']) and str(row['extNumber']).strip() != ""
        else row['name'],
        axis=1
    )

    # Status = Draft
    df['Status'] = 'Draft'

    # Price = ceil(marketPrice * 1.38 * 1.5)
    df['Price'] = df['marketPrice'].apply(
        lambda x: int(math.ceil(x * 1.38 * 1.5)) if pd.notna(x) else ""
    )

    # Fix image URL: replace '200w' with '1000w'
    df['Product image URL'] = df['imageUrl'].apply(
        lambda url: url.replace("200w", "1000w") if pd.notna(url) else ""
    )

    # Map the final DataFrame
    formatted_df = pd.DataFrame({
        'Title': df['Title'],
        'Status': df['Status'],
        'Price': df['Price'],
        'Product image URL': df['imageUrl'],
        'Rarity': df['extRarity'],
        'Description': df['extDescription'],
        'Color': df['extColor'],
        'CardType': df['extCardType']
    })

    # Save as a new CSV
    formatted_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    download_and_process_csv(urls)
    generate_formatted_csv()

