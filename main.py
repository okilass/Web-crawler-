import sys
from models.url import URLItem
from crawler.frontier import URLFrontier
from crawler.fetcher import Fetcher
from crawler.parser import Parser

def run_crawler():
    print("==================================================")
    print("       Web Crawler Starting           ")
    print("==================================================\n")
    
    frontier = URLFrontier()
    fetcher = Fetcher()

    # 1. System Requirement: Provide seed URLs[cite: 1]
    seed_urls = [
        "https://quotes.toscrape.com/",
        "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    ]
    
    print("[1] Initializing Seed URLs...")
    for seed in seed_urls:
        item = URLItem(url=seed, priority=5, depth=0)
        frontier.add_url(item)
        print(f"  -> Added Seed: {seed}")

    print("\n[2] Beginning Crawl Loop...\n")
    processed_count = 0
    max_pages_to_crawl = 5

    while frontier.has_urls() and processed_count < max_pages_to_crawl:
        current_item = frontier.get_next()
        if not current_item:
            break

        print(f"--- Processing ({processed_count + 1}/{max_pages_to_crawl}) ---")
        print(f"URL: {current_item.url}")
        print(f"Priority: {current_item.priority} | Depth: {current_item.depth}")

        # 2. System Requirement: Separate links to files and web pages[cite: 1]
        if current_item.is_file():
            print(f"  [RESULT] Identified as static file link. Skipping HTML parser.\n")
            processed_count += 1
            continue

        # 3. System Requirement: Heed politeness policies[cite: 1]
        response = fetcher.fetch(current_item.url)
        if not response:
            print("  [RESULT] Fetch failed.\n")
            continue

        # Parse content and retrieve new links
        page, new_url_items = Parser.parse(response, current_item)
        print(f"  [PAGE PARSED] Title: '{page.title}'")
        print(f"  [DISCOVERED] Extracted {len(new_url_items)} links.")

        # 4. System Requirement: Prevent indexing the same page twice[cite: 1]
        added_count = 0
        for new_item in new_url_items:
            if frontier.add_url(new_item):
                added_count += 1

        print(f"  [FRONTIER] {added_count} new unique links added to queue.")
        print(f"  [QUEUE SIZE] Current active queue length: {frontier.size()}\n")
        
        processed_count += 1

    print("==================================================")
    print("             Crawl Job Completed                  ")
    print("==================================================")

if __name__ == "__main__":
    run_crawler()
