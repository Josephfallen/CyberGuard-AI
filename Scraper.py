import feedparser
import pymongo
from datetime import datetime

# RSS Feed URL
RSS_FEED_URL = "https://feeds.feedburner.com/TheHackersNews?format=xml"

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
    "cyber attack": ("Cyber Attack", "high")

}

# Function to fetch, search for keywords, assign severities, and format RSS feed data
def fetch_and_format_feed():
    # Parse RSS feed
    feed = feedparser.parse(RSS_FEED_URL)
    
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
    
    # Insert data into collection
    result = collection.insert_many(data)
    
    # Print inserted IDs
    print(f"Inserted IDs: {result.inserted_ids}")

# Main function
def main():
    for _ in range(500):  # Loop 500 times
        formatted_threats = fetch_and_format_feed()
        
        if formatted_threats:
            insert_into_mongodb(formatted_threats)
        else:
            print("No cyber threats to insert.")
        
        print(f"Iteration {_ + 1} completed.")
        print("-" * 50)

if __name__ == "__main__":
    main()