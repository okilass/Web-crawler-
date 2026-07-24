import time
import requests
from urllib.parse import urlparse
from config import Config

class Fetcher:
    """Handles network HTTP requests and respects host politeness intervals[cite: 1]."""
    
    def __init__(self):
        self.domain_last_visited = {}

    def fetch(self, url: str):
        """Fetches a web page while enforcing a delay per domain[cite: 1]."""
        domain = urlparse(url).netloc.lower()
        now = time.time()
        
        # Enforce politeness delay per domain[cite: 1]
        if domain in self.domain_last_visited:
            elapsed = now - self.domain_last_visited[domain]
            if elapsed < Config.POLITENESS_DELAY:
                sleep_time = Config.POLITENESS_DELAY - elapsed
                print(f"  [POLITENESS] Pausing {sleep_time:.2f}s for domain: {domain}")
                time.sleep(sleep_time)

        self.domain_last_visited[domain] = time.time()

        headers = {"User-Agent": Config.USER_AGENT}
        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"  [FETCH ERROR] Failed to download {url}: {e}")
            return None
