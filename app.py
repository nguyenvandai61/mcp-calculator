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

from tools import NewsCrawler, WebBrowser

# Create an MCP server
mcp = FastMCP("NewsCrawler")

# Add a Google search tool
@mcp.tool()
async def google_search(query: str) -> dict:
    """Perform a Google search and return results (titles and URLs).
    
    This tool uses Playwright to automate a Google search and extract the top results.
    Useful for finding information on the web."""
    return await WebBrowser._google_search(query)

# Add a tool to browse a specific URL
@mcp.tool()
async def browse_url(url: str) -> dict:
    """Navigate to a specific URL and extract the page content.
    
    This tool uses Playwright to load a webpage and extract its text content.
    Useful for reading detailed information from any website."""
    return await WebBrowser._browse_url(url)

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
    """Read the full content of a news article from VNExpress or CafeF.
    
    Provide the URL of the article to read its title, description, and full content.
    Useful for getting detailed information after selecting a headline."""
    return NewsCrawler._read_article(url)

# Add a CafeF news crawler tool
@mcp.tool()
def crawl_cafef_news() -> dict:
    """Crawl latest news headlines from CafeF (Vietnamese financial news source).
    
    This tool fetches the latest news headlines from the CafeF homepage.
    Returns a list of top headlines."""
    return NewsCrawler._crawl_cafef_news()

# Add a CafeF news crawler by topic tool
@mcp.tool()
def crawl_cafef_by_topic(topic: str) -> dict:
    """Crawl news headlines by specific topic from CafeF.
    
    Available topics: thoi-su, chung-khoan, bat-dong-san, doanh-nghiep, tai-chinh-ngan-hang, vi-mo, song, thi-truong-hang-hoa
    
    Example: topic="chung-khoan" for stock market news."""
    return NewsCrawler._crawl_cafef_by_topic(topic)

# Start the server
if __name__ == "__main__":
    mcp.run(transport="stdio")
