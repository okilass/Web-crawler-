"""Crawler modules for fetching, parsing, and queue frontier management."""
from .frontier import URLFrontier
from .fetcher import Fetcher
from .parser import Parser

__all__ = ["URLFrontier", "Fetcher", "Parser"]
