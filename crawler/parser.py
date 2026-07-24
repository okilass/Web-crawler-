from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from models.page import Page
from models.url import URLItem
from config import Config

class Parser:
    """Parses document response body, extracts text, and separates web page links from media files[cite: 1]."""
    
    @staticmethod
    def parse(response, base_url_item: URLItem):
        content_type = response.headers.get('Content-Type', '')
        
        # If response isn't HTML, return basic document info without parsing outgoing links[cite: 1]
        if 'text/html' not in content_type:
            return Page(url=base_url_item.url, content_type=content_type), []

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title
        title = soup.title.string.strip() if soup.title and soup.title.string else "Untitled Page"
        
        # Extract raw text snippet
        text_content = soup.get_text(separator=' ', strip=True)
        
        extracted_urls = []
        new_depth = base_url_item.depth + 1
        
        # Enforce maximum depth threshold
        if new_depth <= Config.MAX_DEPTH:
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href'].strip()
                full_url = urljoin(base_url_item.url, href)
                
                parsed = urlparse(full_url)
                if parsed.scheme in ['http', 'https']:
                    # Simple heuristic: higher priority if link text contains keyword
                    priority = base_url_item.priority
                    link_text = a_tag.get_text().lower()
                    if any(kw in link_text for kw in ['python', 'design', 'system', 'docs']):
                        priority += 2

                    extracted_urls.append(
                        URLItem(url=full_url, priority=priority, depth=new_depth)
                    )

        page_data = Page(
            url=base_url_item.url,
            content_type=content_type,
            title=title,
            text_content=text_content[:300],
            raw_html=response.text
        )

        return page_data, extracted_urls
