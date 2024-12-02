import csv
import requests
from bs4 import BeautifulSoup

def get_country_for_city(city):
    """Searches for the country of a given city via a web search."""
    search_url = f"https://www.google.com/search?q={city}+country"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        print(f"Error: Failed to fetch data for {city}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract a likely snippet containing the country name
    country = None
    for result in soup.find_all("span"):
        if "country" in result.text.lower():
            country = result.text
            break
    
    return country or "Country not found"

def main():
    # Replace 'city-country.csv' with the path to your file
    file_path = "city_of_residence,country_of_residence.csv"
    
    # Open and process the CSV file
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Extract the first city for processing
        first_row = next(reader, None)
        if not first_row:
            print("The file is empty.")
            return
        
        city = first_row["city_of_residence"]
        print(f"City: {city}")
        
        # Get the country for the first city
        country = get_country_for_city(city)
        print(f"Country: {country}")

if __name__ == "__main__":
    main()
