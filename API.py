import feedparser
import pymongo
from datetime import datetime
import time

# RSS Feed URL
RSS_FEED_URLS = [
"https://feeds.feedburner.com/TheHackersNews?format=xml",
"https://www.welivesecurity.com/en/rss/feed/"
]

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "cyber_threats"
COLLECTION_NAME = "resources"

# Expanded keywords and their corresponding types and severities
KEYWORDS = {
    "ransomware": ("Ransomware", "high"),
    "phishing": ("Phishing", "medium"),
    "malware": ("Malware", "high"),
    "exploit": ("Exploit", "high"),
    "vulnerability": ("Vulnerability", "medium"),
    "data breach": ("Data Breach", "high"),
    "cryptojacking": ("Cryptojacking", "medium"),
    "botnet": ("Botnet", "high"),
    "ddos": ("DDoS Attack", "high"),
    "social engineering": ("Social Engineering", "medium"),
    "zero-day": ("Zero-Day", "high"),
    "trojan": ("Trojan", "high"),
    "backdoor": ("Backdoor", "high"),
    "keylogger": ("Keylogger", "medium"),
    "rootkit": ("Rootkit", "high"),
    "spyware": ("Spyware", "medium"),
    "adware": ("Adware", "low"),
    "pharming": ("Pharming", "medium"),
    "man-in-the-middle": ("Man-in-the-Middle", "high"),
    "whaling": ("Whaling", "medium"),
    "watering hole": ("Watering Hole", "medium"),
    "fileless malware": ("Fileless Malware", "high"),
    "drive-by download": ("Drive-By Download", "medium"),
    "credential stuffing": ("Credential Stuffing", "medium"),
    "typosquatting": ("Typosquatting", "medium"),
    "formjacking": ("Formjacking", "medium"),
    "clickjacking": ("Clickjacking", "medium"),
    "identity theft": ("Identity Theft", "high"),
    "cyber espionage": ("Cyber Espionage", "high"),
    "advanced persistent threat": ("Advanced Persistent Threat", "high"),
    "iot": ("IoT Threat", "medium"),
    "mobile malware": ("Mobile Malware", "medium"),
    "supply chain attack": ("Supply Chain Attack", "high"),
    "file encryption": ("File Encryption", "high"),
    "sandbox evasion": ("Sandbox Evasion", "medium"),
    "polymorphic malware": ("Polymorphic Malware", "high"),
    "malvertising": ("Malvertising", "medium"),
    "ransomware-as-a-service": ("Ransomware-as-a-Service", "high"),
    "credential phishing": ("Credential Phishing", "medium"),
    "smishing": ("Smishing", "medium"),
    "vishing": ("Vishing", "medium"),
    "malspam": ("Malspam", "medium"),
    "zero-day vulnerability": ("Zero-Day Vulnerability", "high"),
    "ransomware attack": ("Ransomware Attack", "high"),
    "phishing attack": ("Phishing Attack", "medium"),
    "data breach incident": ("Data Breach Incident", "high"),
    "cyber attack": ("Cyber Attack", "high"),
    "hijacking": ("Hyjacking", "low")

}


# Function to fetch, search for keywords, assign severities, and format RSS feed data
def fetch_and_format_feed(feed_url):
    # Parse RSS feed
    feed = feedparser.parse(feed_url)
    
    # List to store formatted cyber threats
    formatted_threats = []
    
    # Loop through feed entries
    for entry in feed.entries:
        # Extract relevant data
        title = entry.title.lower()  # Convert title to lowercase for keyword search
        link = entry.link
        description = entry.description
        published = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z")
        
        # Search for keywords in title
        threat_type = "News"  # Default type if no keyword is found
        severity = "info"  # Default severity if no keyword is found
        for keyword, (threat, sev) in KEYWORDS.items():
            if keyword in title:
                threat_type = threat
                severity = sev
                break
        
        # Format data for MongoDB
        threat = {
            "_id": link,  # Use link as the unique identifier to prevent duplicates
            "type": threat_type,
            "severity": severity,
            "description": f"{title}\n{link}\n{description}",
            "published": published
        }
        
        formatted_threats.append(threat)
    
    return formatted_threats

# Function to insert data into MongoDB
def insert_into_mongodb(data):
    # Connect to MongoDB
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    # Insert data into collection with upsert=True to prevent duplicates
    for threat in data:
        collection.update_one({"_id": threat["_id"]}, {"$set": threat}, upsert=True)
    
    print("Insertion completed.")

# Main function
def main():
    for feed_url in RSS_FEED_URLS:
        formatted_threats = fetch_and_format_feed(feed_url)
        
        if formatted_threats:
            insert_into_mongodb(formatted_threats)
        else:
            print(f"No cyber threats from {feed_url} to insert.")
        
        print(f"Processed {feed_url}.")
        print("-" * 50)

if __name__ == "__main__":
    main()
