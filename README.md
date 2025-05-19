# Overview
This repository contains two Python scripts that interact with the Spotify API to fetch artist and track images. The scripts are designed to:
* Search for artist images by artist name
* Retrieve track images by Spotify track ID

## Prerequisites
Before using these scripts, you'll need:
* Python 3 installed. Required Python packages: requests, pandas
* [A Spotify Developer account](https://developer.spotify.com/)
* Spotify API credentials (Client ID and Client Secret)

## Setup
* Clone this repository
* Obtain your Spotify API credentials:
    * Go to the Spotify Developer Dashboard
    * Create an app to get your Client ID and Client Secret
* Add your credentials to both Python files

## Scripts
1. Artist Image Search (Artist_image_search.py)

**Purpose**: Fetches artist images from Spotify by artist name.

**Input Requirements:**
* Excel file named artist_names.xlsx
* Excel file must contain a column named "Artist" with artist names

**Output:**

Creates artist_images.xlsx with two columns:
* Artist: The artist name searched
* Image URL: The URL of the artist's image (or "No image available"/"No artist found")


2. Track Image Search (Tracks_image_search.py)

**Purpose:** Fetches track/album images from Spotify by track ID.

**Input Requirements:**

* Excel file named track_ids.xlsx
* Excel file must contain a column named "Track ID" with Spotify track IDs

**Output:**

Creates track_images.xlsx with two columns:

* Track ID: The Spotify track ID searched
* Image URL: The URL of the track's album image (or "No image available"/"No track found")
