#   Web Crawler

# Topic-focused web crawler system. Built with Python, using priority queueing, politeness rate-limiting, static file classification, and URL deduplication.


## 📖 Table of Contents
- [Overview](#-overview)
- [System Requirements Met](#-system-requirements-met)
- [Project Architecture](#-project-architecture)
- [Directory Structure](#-directory-structure)
- [Getting Started](#-getting-started)
- [Running the Crawler](#-running-the-crawler)
- [System Design Document (SSD)](#-system-design-document-ssd)


## Overview

A web crawler  traverses the internet automatically to collect web pages and data for search engines, price aggregators, and research applications. 


##  System Requirements 

This system implements all core requirements specified:

| Requirement | Implementation Detail |
| Seed URLs | Ingests custom starting URLs to boot the frontier queue (`main.py`). |
| Politeness Policy | Enforces per-domain request rate limits to prevent target server overloads (`crawler/fetcher.py`). |
| File vs. Page Separation | Automatically distinguishes HTML pages from binary files (`.pdf`, `.zip`, `.png`) (`models/url.py`, `crawler/parser.py`). |
| Priority Queueing | Ranks discovered URLs based on relevance scores using standard heap structures (`crawler/frontier.py`) |
| Duplicate Prevention | Tracks processed URLs via an internal registry to avoid infinite loops (`crawler/frontier.py`)


##  Project Architecture

```text
[ Seed URLs ] ---> [ URL Frontier (Priority Queue) ]
                           |
                           v
                 [ Politeness Engine ] 
                           |
                           v
                   [ HTTP Fetcher ]
                           |
                           v
                [ Content / HTML Parser ]
                 /                     \
       (Binary Files)              (Web Links)
             |                          |
    [ Skip Processing ]     [ Duplicate Filter ]
                                        | (New URLs)
                                        v
                            [ Enqueue to Frontier ]
