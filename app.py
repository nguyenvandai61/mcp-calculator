# server.py
from fastmcp import FastMCP
import sys
import logging
import os

logger = logging.getLogger('NewsCrawler')
logging.basicConfig(level=logging.INFO)


# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

import math
import random
import requests
from bs4 import BeautifulSoup

from tools import NewsCrawler

# Create an MCP server
mcp = FastMCP("NewsCrawler")

# Add a news crawler tool
@mcp.tool()
def crawl_news_today() -> dict:
    """Crawl today's news headlines from VNExpress (Vietnamese news source).
    
    This tool fetches the latest news headlines from the VNExpress homepage.
    Returns a list of top headlines for today."""
    return NewsCrawler._crawl_news()

# Add a news crawler by topic tool
@mcp.tool()
def crawl_news_by_topic(topic: str) -> dict:
    """Crawl news headlines by specific topic from VNExpress.
    
    Available topics: thoi-su, the-gioi, kinh-doanh, khoa-hoc-cong-nghe, goc-nhin, bat-dong-san, suc-khoe, the-thao, giai-tri, phap-luat, giao-duc, doi-song, oto-xe-may, du-lich, y-kien, tam-su, thu-gian
    
    Example: topic="kinh-doanh" for business news."""
    return NewsCrawler._crawl_news_by_topic(topic)

# Add a tool to read full article content
@mcp.tool()
def read_article(url: str) -> dict:
    """Read the full content of a news article from VNExpress.
    
    Provide the URL of the article to read its title, description, and full content.
    Useful for getting detailed information after selecting a headline."""
    return NewsCrawler._read_article(url)

# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
