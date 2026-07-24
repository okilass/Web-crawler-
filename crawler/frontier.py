import heapq
from typing import Set, Optional
from models.url import URLItem

class URLFrontier:
    """Manages prioritizing URLs and tracking duplicate addresses to prevent re-indexing[cite: 1]."""
    
    def __init__(self):
        self._queue = []
        self._visited_urls: Set[str] = set()

    def add_url(self, item: URLItem) -> bool:
        """Enqueues a URL if it has not been visited before[cite: 1]."""
        # Normalize trailing slash for deduplication check[cite: 1]
        normalized_url = item.url.rstrip('/')
        
        if normalized_url in self._visited_urls:
            return False
            
        self._visited_urls.add(normalized_url)
        heapq.heappush(self._queue, item)
        return True

    def get_next(self) -> Optional[URLItem]:
        """Pulls the next highest-priority URL from the queue[cite: 1]."""
        if self._queue:
            return heapq.heappop(self._queue)
        return None

    def has_urls(self) -> bool:
        """Checks if the queue contains pending URLs."""
        return len(self._queue) > 0

    def size(self) -> int:
        """Returns current queue depth."""
        return len(self._queue)
