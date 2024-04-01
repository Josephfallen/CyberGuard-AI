import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# Initialize MongoDB client and database
client = MongoClient('mongodb://localhost:27017/')
db = client['cyber_threats']
collection = db['documentation']

# List of URLs to search for cyber threat documentation
urls = [
    'https://www.us-cert.gov/ncas/alerts',
    'https://www.cisa.gov/cybersecurity',
    'https://www.ncsc.gov.uk/section/information-for/individuals-families'
]

# Function to scrape and store documentation from a given URL
def scrape_documentation(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract relevant information (e.g., titles, descriptions, links)
        titles = [title.text for title in soup.find_all('h2')]
        descriptions = [desc.text for desc in soup.find_all('p')]
        links = [link['href'] for link in soup.find_all('a', href=True)]
        # Store the extracted information in the MongoDB collection
        for i in range(len(titles)):
            document = {
                'title': titles[i],
                'description': descriptions[i] if i < len(descriptions) else '',
                'link': links[i] if i < len(links) else '',
                'source': url
            }
            collection.insert_one(document)
        print(f"Scraped and stored documentation from {url}")
    else:
        print(f"Failed to retrieve data from {url}")

# Iterate through the list of URLs and scrape documentation
for url in urls:
    scrape_documentation(url)

# Print the total number of documents stored in the database
print(f"Total number of documents stored: {collection.count_documents({})}")


