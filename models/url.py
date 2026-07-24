from urllib.parse import urlparse
from config import Config

class URLItem:
    """Represents a target URL with metadata and comparison operators for priority queueing[cite: 1]."""
    
    def __init__(self, url: str, priority: int = 0, depth: int = 0):
        self.url = url
        self.priority = priority
        self.depth = depth
        self.domain = urlparse(url).netloc.lower()

    def is_file(self) -> bool:
        """Determines if the URL points to a binary/media file based on extension[cite: 1]."""
        path = urlparse(self.url).path.lower()
        return any(path.endswith(ext) for ext in Config.FILE_EXTENSIONS)

    def __lt__(self, other):
        """Allows PriorityQueue/heapq to order URLs highest priority first[cite: 1]."""
        if not isinstance(other, URLItem):
            return False
        return self.priority > other.priority

    def __repr__(self):
        return f"<URLItem priority={self.priority} depth={self.depth} url='{self.url}'>"
