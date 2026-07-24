from datetime import datetime

class Page:
    """Represents a downloaded and parsed web document[cite: 1]."""
    
    def __init__(self, url: str, content_type: str, title: str = "", text_content: str = "", raw_html: str = ""):
        self.url = url
        self.content_type = content_type
        self.title = title
        self.text_content = text_content
        self.raw_html = raw_html
        self.crawled_at = datetime.utcnow()

    def __repr__(self):
        return f"<Page title='{self.title[:25]}...' url='{self.url}'>"
