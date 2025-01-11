import requests
import logging
import time
from datetime import datetime
#from database import SessionLocal, CVE
from ..database import SessionLocal, CVE


API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

'''def fetch_cves(offset=0, limit=100):
    response = requests.get(API_URL, params={"startIndex": offset, "resultsPerPage": limit})
    data = response.json().get("vulnerabilities", [])
    return data'''

'''def sync_cves():
    db = SessionLocal()
    offset = 0
    limit = 100
    while True:
        cve_data = fetch_cves(offset, limit)
        if not cve_data:
            break

        for item in cve_data:
            cve_id = item["cve"]["id"]
            description = item["cve"]["descriptions"][0]["value"]
            published_date = datetime.fromisoformat(item["published"])
            last_modified_date = datetime.fromisoformat(item["lastModified"])
            base_score = item.get("metrics", {}).get("cvssMetricV3", {}).get("cvssData", {}).get("baseScore")

            # Upsert logic
            existing_cve = db.query(CVE).filter(CVE.cve_id == cve_id).first()
            if existing_cve:
                existing_cve.last_modified_date = last_modified_date
                existing_cve.base_score = base_score
            else:
                db.add(CVE(
                    cve_id=cve_id,
                    description=description,
                    published_date=published_date,
                    last_modified_date=last_modified_date,
                    base_score=base_score
                ))
        db.commit()
        offset += limit
    db.close()'''
import requests
import logging

API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

'''2 def fetch_cves(offset=0, limit=100):
    try:
        # Send the request to the API
        response = requests.get(API_URL, params={"startIndex": offset, "resultsPerPage": limit})

        # Log the response status code and content for debugging
        logging.debug(f"Response status code: {response.status_code}")
        logging.debug(f"Response content: {response.text}")

        # Check if the response is valid and contains JSON
        if response.status_code == 200:
            try:
                data = response.json()
                return data.get("vulnerabilities", [])
            except ValueError as e:
                logging.error(f"Error parsing JSON: {e}")
                return []
        else:
            logging.error(f"Request failed with status code {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return []'''
import time

def fetch_cves(offset=0, limit=100):
    try:
        response = requests.get(API_URL, params={"startIndex": offset, "resultsPerPage": limit})
        
        if response.status_code == 403:
            logging.error(f"Request failed with status code 403: Access Forbidden")
            time.sleep(5)  # Wait for 5 seconds before retrying
            return []

        if response.status_code == 200:
            return response.json().get("vulnerabilities", [])
        else:
            logging.error(f"Request failed with status code {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return []



def sync_cves():
    db = SessionLocal()
    offset = 0
    limit = 100
    while True:
        cve_data = fetch_cves(offset, limit)
        if not cve_data:
            break

        for item in cve_data:
            cve_id = item["cve"]["id"]
            description = item["cve"]["descriptions"][0]["value"]
            
            # Safely access keys with fallback values
            published_date = item.get("published")
            if published_date:
                published_date = datetime.fromisoformat(published_date)
            
            last_modified_date = item.get("lastModified")
            if last_modified_date:
                last_modified_date = datetime.fromisoformat(last_modified_date)

            base_score = item.get("metrics", {}).get("cvssMetricV3", {}).get("cvssData", {}).get("baseScore")

            # Upsert logic
            existing_cve = db.query(CVE).filter(CVE.cve_id == cve_id).first()
            if existing_cve:
                existing_cve.last_modified_date = last_modified_date
                existing_cve.base_score = base_score
            else:
                db.add(CVE(
                    cve_id=cve_id,
                    description=description,
                    published_date=published_date,
                    last_modified_date=last_modified_date,
                    base_score=base_score
                ))
        db.commit()
        offset += limit
    db.close()

