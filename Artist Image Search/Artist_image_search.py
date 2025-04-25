import json
import base64
import pandas as pd  # type: ignore # For reading and writing Excel files
from requests import get, post

# Spotify API credentials
client_id =  # Your Client ID
client_secret =  # Your Client Secret

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    return json_result["access_token"]

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content).get("artists", {}).get("items", [])
    
    if len(json_result) == 0:
        print(f"No artist found for '{artist_name}'")
        return None
    
    # Return the first artist's details
    return json_result[0]

# Main execution
token = get_token()

# Read the artist names from the Excel file
input_file = "artist_names.xlsx"  # Replace with the path to your Excel file
output_file = "artist_images.xlsx"  # Output file to save results

# Assuming the Excel file has a column called 'Artist'
artists_df = pd.read_excel(input_file)
artist_names = artists_df['Artist']

# Create a list to store results
results = []

for artist_name in artist_names:
    print(f"Searching for artist: {artist_name}")
    result = search_for_artist(token, artist_name)
    if result:
        # Extract artist image URL (use the first image URL if available)
        image_url = result["images"][0]["url"] if result["images"] else "No image available"
    else:
        image_url = "No artist found"
    
    # Append the artist name and image URL to results
    results.append({"Artist": artist_name, "Image URL": image_url})

# Create a DataFrame from the results
output_df = pd.DataFrame(results)

# Save the DataFrame to a new Excel file
output_df.to_excel(output_file, index=False)
print(f"Results saved to {output_file}")
