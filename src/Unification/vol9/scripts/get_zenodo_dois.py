import requests
import pandas as pd
import time

# 1. Define the API endpoint
url = "https://zenodo.org/api/records"

records = []
page = 1

print("Querying Zenodo API (Paginated)...")

while True:
    # 2. Use the new anonymous limit (25) and paginate
    params = {
        "q": 'creators.name:"Kish, Timothy John"', 
        "all_versions": True,
        "size": 25,  
        "sort": "mostrecent",
        "page": page
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        hits = data.get('hits', {}).get('hits', [])
        
        # If the page returns empty, we've pulled everything
        if not hits:
            break 
            
        # Parse the JSON payload
        for item in hits:
            metadata = item.get('metadata', {})
            records.append({
                "Title": metadata.get('title'),
                "DOI": item.get('doi'),
                "Published Date": metadata.get('publication_date'),
                "Version": metadata.get('version', '1.0.0')
            })
        
        print(f"Fetched page {page} ({len(hits)} records)...")
        page += 1
        
        # Be polite to the API (Zenodo's new limit is 30 requests/minute)
        time.sleep(2) 
        
    else:
        print(f"Failed to connect on page {page}. Status Code: {response.status_code}")
        print(response.text)
        break

if records:
    # 3. Format as a clean DataFrame
    df = pd.DataFrame(records)
    
    # Save to CSV for your records
    df.to_csv("my_zenodo_publications.csv", index=False)
    
    print(f"\nSuccessfully pulled all {len(df)} records. Here is the top of your manifest:\n")
    print(df.head(10).to_string(index=False))
    print(f"\n...Saved full list of {len(df)} DOIs to 'my_zenodo_publications.csv'.")