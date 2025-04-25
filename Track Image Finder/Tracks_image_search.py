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

def get_track_details(token, track_id):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = get_auth_header(token)
    
    result = get(url, headers=headers)
    
    # Print the raw response for debugging
    print(f"Response status code: {result.status_code}")
    print(f"Response content: {result.content.decode('utf-8')}")
    
    try:
        json_result = json.loads(result.content)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return None
    
    if 'error' in json_result:
        print(f"Error fetching track with ID '{track_id}': {json_result['error']['message']}")
        return None
    
    return json_result

# Main execution
token = get_token()

# Read the track IDs from the Excel file
input_file = "track_ids.xlsx"  # Replace with the path to your Excel file
output_file = "track_images.xlsx"  # Output file to save results

# Assuming the Excel file has a column called 'Track ID'
tracks_df = pd.read_excel(input_file)
track_ids = tracks_df['Track ID']

# Create a list to store results
results = []

for track_id in track_ids:
    print(f"Fetching details for track ID: {track_id}")
    result = get_track_details(token, track_id)
    if result:
        # Extract track image URL (use the first image URL if available)
        image_url = result["album"]["images"][0]["url"] if result["album"]["images"] else "No image available"
    else:
        image_url = "No track found"
    
    # Append the track ID and image URL to results
    results.append({"Track ID": track_id, "Image URL": image_url})

# Create a DataFrame from the results
output_df = pd.DataFrame(results)

# Save the DataFrame to a new Excel file
output_df.to_excel(output_file, index=False)
print(f"Results saved to {output_file}")