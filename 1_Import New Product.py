import pandas as pd
import requests
import math
from io import StringIO

##############################################################
#### PUT NEW PRODUCT URL DOWN BELOW, REMOVE EXISTING ONES ####
##############################################################

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
    # Add more URLs as needed
]

# Download and combine CSVs
def download_and_process_csv(urls):
    dfs = []

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()

            if not response.text.strip():
                print(f"Warning: No content in CSV file from {url}")
                continue

            data = StringIO(response.text)
            df = pd.read_csv(data)
            dfs.append(df)

        except Exception as e:
            print(f"Error downloading file from {url}: {e}")

    if not dfs:
        print("No valid CSV files were processed.")
        return

    combined_df = pd.concat(dfs, ignore_index=True)

    # Remove unwanted columns
    columns_to_remove = [
        'cleanName', 'categoryId', 'groupId', 'modifiedOn', 'imageCount',
        'lowPrice', 'midPrice', 'highPrice', 'directLowPrice', 'subTypeName',
        'extLife', 'extPower', 'extSubtypes', 'extAttribute', 'extCost',
        'extCounterplus'
    ]
    combined_df = combined_df.drop(columns=columns_to_remove, errors='ignore')

    # Reformat columns
    combined_df = combined_df[['productId','name','extNumber','imageUrl','url',
                               'marketPrice','extRarity','extDescription',
                               'extColor','extCardType']]

    combined_df.to_csv('new_product_database.csv', index=False)
    print("CSV processed → new_product_database.csv")


def generate_formatted_csv(input_file='new_product_database.csv', output_file='formatted_import_shopify.csv'):
    df = pd.read_csv(input_file)

    # Convert rarity abbreviations to full names
    rarity_map = {
        'C': 'Common',
        'UC': 'Uncommon',
        'TR': 'Treasure Rare',
        'SR': 'Super Rare',
        'SEC': 'Secret Rare',
        'L': 'Leader',
        'R': 'Rare',
        'PR': 'Promo',
    }
    df['extRarity'] = df['extRarity'].map(rarity_map).fillna(df['extRarity'])

    df['extColor'] = df['extColor'].astype(str).str.replace(";", ",")

    # Build Title
    df['Title'] = df.apply(
        lambda row: f"{row['name']} ({row['extNumber']})"
        if pd.notna(row['extNumber']) and str(row['extNumber']).strip() != ""
        else row['name'],
        axis=1
    )

    # Price formula
    df['Status'] = 'Draft'
    df['Price'] = df['marketPrice'].apply(
        lambda x: int(math.ceil(x * 1.38 * 1.5)) if pd.notna(x) else ""
    )

    # Fix image URL
    df['Product image URL'] = df['imageUrl'].apply(
        lambda url: url.replace("200w", "in_1000x1000") if pd.notna(url) else ""
    )

    # ---------- EXACT MATCH RARITY OVERWRITE ----------
    def adjust_rarity(row):
        title = str(row['Title'])

        if "(Manga)" in title:
            return "Manga Rare"
        if "(SP)" in title:
            return "Special Rare"

        return row['extRarity']

    df['extRarity'] = df.apply(adjust_rarity, axis=1)

    # ---------- TAG BUILDER ----------
    def build_tags(row):
        tags = ["English", "One Piece"]

        rarity = row['extRarity']
        title = row['Title']

    # Only add Single if rarity exists
        if pd.notna(rarity) and str(rarity).strip() != "":
            tags.append("Single")

    # Add Alternate Art if Title contains "(Alternate Art)" or "(SP)"
        if "(Alternate Art)" in str(title) or "(SP)" in str(title):
            tags.append("Alternate Art")

        return ", ".join(tags)

    df['Tags'] = df.apply(build_tags, axis=1)

    # ---------- FINAL EXPORT ----------
    formatted_df = pd.DataFrame({
        'SKU': df['productId'],
        'Title': df['Title'],
        'Status': df['Status'],
        'Price': df['Price'],
        'Product image URL': df['Product image URL'],
        'Rarity (product.metafields.shopify.rarity)': df['extRarity'],
        'Description': df['extDescription'],
        'Color (product.metafields.shopify.color-pattern)': df['extColor'],
        'Card attributes (product.metafields.shopify.card-attributes)': df['extCardType'],
        'Product Category': 'Arts & Entertainment > Hobbies & Creative Arts > Collectibles > Collectible Trading Cards',
        'Tags': df['Tags'],
    })

    formatted_df.to_csv(output_file, index=False)
    print("CSV generated → formatted_import_shopify.csv")


if __name__ == "__main__":
    download_and_process_csv(urls)
    generate_formatted_csv()
