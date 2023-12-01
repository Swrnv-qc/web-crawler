import requests
from bs4 import BeautifulSoup
import csv
import json
from urllib.parse import urlencode

base_url = "https://google.com/search"

def generate_url(params):
        
    url = base_url + '?q=' + params["primary_category"].replace(' ', '+')+"+"+params["secondary_category"].replace(' ', '+')+"+"+params["geography"].replace(' ', '+')+"+"+params["date_range"]
    print (url)
    return url

def crawl_websites(params):
    primary_category = params.get("Primary Category", "")
    secondary_category = params.get("Secondary Category", "")
    geography = params.get("Geography", "")
    date_range = params.get("Date Range", "")

    url = generate_url({
        "primary_category": primary_category,
        "secondary_category": secondary_category,
        "geography": geography,
        "date_range": date_range,
    })

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        links = soup.find_all("a")

        filtered_links = [link.get("href") for link in links if "https" in link.get("href", "") and "google" not in link.get("href", "")]

        with open('output.csv', 'w', newline='') as csvfile:
            fieldnames = ['Link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for link in filtered_links:
                writer.writerow({'Link': link})

        print("Links stored in output.csv")

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

import csv

def create_substring_csv(input_filename, output_filename):
    with open(input_filename, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        links = [row['Link'] for row in reader]

    with open(output_filename, 'w', newline='') as csvfile:
        fieldnames = ['SubStringed_Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for link in links:
            start_index = link.find("https")
            end_index = link.find("&") if "&" in link else None
            substringed_link = link[start_index:end_index]

            writer.writerow({'SubStringed_Link': substringed_link})

    print(f"Substringed links stored in {output_filename}")

if __name__ == "__main__":
    with open('parameters.json', 'r') as json_file:
        parameters = json.load(json_file)

    crawl_websites(parameters)
    create_substring_csv('output.csv', 'output_filtered.csv')
