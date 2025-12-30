import math
import random
import requests
import asyncio
from bs4 import BeautifulSoup
import logging
from playwright.async_api import async_playwright
from urllib.parse import quote_plus

logger = logging.getLogger('Tools')

class Calculator:
    """Class for mathematical calculations."""
    
    @staticmethod
    def _calculate(python_expression: str) -> dict:
        """Calculate the result of a Python expression with math and random available."""
        try:
            result = eval(python_expression, {"math": math, "random": random})
            logger.info(f"Calculating formula: {python_expression}, result: {result}")
            return {"success": True, "result": result}
        except Exception as e:
            logger.error(f"Error in calculation: {e}")
            return {"success": False, "error": str(e)}

class NewsCrawler:
    """Class for news crawling operations."""
    
    @staticmethod
    def _crawl_news() -> dict:
        """Crawl news headlines from VNExpress."""
        try:
            url = "https://vnexpress.net/"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find headlines and links
            headlines = []
            for item in soup.find_all('h3', class_='title-news')[:10]:
                title = item.get_text(strip=True)
                link = item.find('a')
                article_url = link['href'] if link and 'href' in link.attrs else None
                if title and article_url:
                    if not article_url.startswith('http'):
                        article_url = f"https://vnexpress.net{article_url}"
                    headlines.append({"title": title, "url": article_url})

            logger.info(f"Crawled {len(headlines)} news headlines")
            return {"success": True, "headlines": headlines}
        except Exception as e:
            logger.error(f"Error crawling news: {e}")
            return {"success": False, "error": str(e)}

    @staticmethod
    def _crawl_news_by_topic(topic: str) -> dict:
        """Crawl news headlines by topic from VNExpress."""
        topic_urls = {
            "thoi-su": "https://vnexpress.net/thoi-su",
            "the-gioi": "https://vnexpress.net/the-gioi",
            "kinh-doanh": "https://vnexpress.net/kinh-doanh",
            "khoa-hoc-cong-nghe": "https://vnexpress.net/khoa-hoc-cong-nghe",
            "goc-nhin": "https://vnexpress.net/goc-nhin",
            "bat-dong-san": "https://vnexpress.net/bat-dong-san",
            "suc-khoe": "https://vnexpress.net/suc-khoe",
            "the-thao": "https://vnexpress.net/the-thao",
            "giai-tri": "https://vnexpress.net/giai-tri",
            "phap-luat": "https://vnexpress.net/phap-luat",
            "giao-duc": "https://vnexpress.net/giao-duc",
            "doi-song": "https://vnexpress.net/doi-song",
            "oto-xe-may": "https://vnexpress.net/oto-xe-may",
            "du-lich": "https://vnexpress.net/du-lich",
            "y-kien": "https://vnexpress.net/y-kien",
            "tam-su": "https://vnexpress.net/tam-su",
            "thu-gian": "https://vnexpress.net/thu-gian"
        }
        
        if topic not in topic_urls:
            return {"success": False, "error": f"Topic '{topic}' not found. Available topics: {list(topic_urls.keys())}"}
        
        try:
            url = topic_urls[topic]
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            headlines = []
            for item in soup.find_all('h3', class_='title-news')[:10]:
                title = item.get_text(strip=True)
                link = item.find('a')
                article_url = link['href'] if link and 'href' in link.attrs else None
                if title and article_url:
                    if not article_url.startswith('http'):
                        article_url = f"https://vnexpress.net{article_url}"
                    headlines.append({"title": title, "url": article_url})
            
            logger.info(f"Crawled {len(headlines)} headlines for topic '{topic}'")
            return {"success": True, "topic": topic, "headlines": headlines}
        except Exception as e:
            logger.error(f"Error crawling news for topic '{topic}': {e}")
            return {"success": False, "error": str(e)}

    @staticmethod
    def _read_article(url: str) -> dict:
        """Read the full content of a news article from VNExpress or CafeF."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title_text = ""
            desc_text = ""
            content_text = ""

            if "vnexpress.net" in url:
                # Extract title
                title = soup.find('h1', class_='title-detail')
                title_text = title.get_text(strip=True) if title else "No title found"
                
                # Extract description
                description = soup.find('p', class_='description')
                desc_text = description.get_text(strip=True) if description else ""
                
                # Extract main content
                content_div = soup.find('article', class_='fck_detail')
                if content_div:
                    paragraphs = content_div.find_all('p')
                    content_text = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
            
            elif "cafef.vn" in url:
                # Extract title
                title = soup.find('h1', class_='title') or soup.find('h1', class_='title-detail')
                title_text = title.get_text(strip=True) if title else "No title found"
                
                # Extract description
                description = soup.find('h2', class_='sapo')
                desc_text = description.get_text(strip=True) if description else ""
                
                # Extract main content
                content_div = soup.find('div', id='mainContent') or soup.find('div', class_='left_cate_content')
                if content_div:
                    # Remove unwanted elements like related news, ads, etc.
                    for unwanted in content_div.find_all(['div', 'table'], class_=['link-content-footer', 'box-embed-video']):
                        unwanted.decompose()
                    
                    paragraphs = content_div.find_all(['p', 'div'], recursive=False)
                    content_text = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
            
            if not title_text and not content_text:
                return {"success": False, "error": "Could not parse article content. Unsupported site or structure changed."}

            full_content = f"Title: {title_text}\n\nDescription: {desc_text}\n\nContent:\n{content_text}"
            
            logger.info(f"Read article from {url}, length: {len(full_content)}")
            return {"success": True, "url": url, "content": full_content}
        except Exception as e:
            logger.error(f"Error reading article from {url}: {e}")
            return {"success": False, "error": str(e)}

    @staticmethod
    def _crawl_cafef_news() -> dict:
        """Crawl news headlines from CafeF homepage."""
        try:
            url = "https://cafef.vn/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            headlines = []
            # CafeF has several sections, we'll look for common headline patterns
            # Main highlight
            highlight = soup.find('div', class_='top_noibat')
            if highlight:
                link = highlight.find('a')
                title = highlight.find('h2')
                if link and title:
                    article_url = link['href']
                    if not article_url.startswith('http'):
                        article_url = f"https://cafef.vn{article_url}"
                    headlines.append({"title": title.get_text(strip=True), "url": article_url})

            # Other news items
            for item in soup.find_all('h3')[:15]:
                link = item.find('a')
                if link and 'href' in link.attrs:
                    title = item.get_text(strip=True)
                    article_url = link['href']
                    if not article_url.startswith('http'):
                        article_url = f"https://cafef.vn{article_url}"
                    
                    # Avoid duplicates
                    if not any(h['url'] == article_url for h in headlines):
                        headlines.append({"title": title, "url": article_url})

            logger.info(f"Crawled {len(headlines)} CafeF news headlines")
            return {"success": True, "headlines": headlines}
        except Exception as e:
            logger.error(f"Error crawling CafeF news: {e}")
            return {"success": False, "error": str(e)}

    @staticmethod
    def _crawl_cafef_by_topic(topic: str) -> dict:
        """Crawl news headlines by topic from CafeF."""
        topic_urls = {
            "thoi-su": "https://cafef.vn/thoi-su.chn",
            "chung-khoan": "https://cafef.vn/thoi-su-dau-tu/chung-khoan.chn",
            "bat-dong-san": "https://cafef.vn/bat-dong-san.chn",
            "doanh-nghiep": "https://cafef.vn/doanh-nghiep.chn",
            "tai-chinh-ngan-hang": "https://cafef.vn/tai-chinh-ngan-hang.chn",
            "vi-mo": "https://cafef.vn/vi-mo-dau-tu.chn",
            "song": "https://cafef.vn/song.chn",
            "thi-truong-hang-hoa": "https://cafef.vn/thi-truong-hang-hoa.chn"
        }
        
        if topic not in topic_urls:
            return {"success": False, "error": f"Topic '{topic}' not found for CafeF. Available topics: {list(topic_urls.keys())}"}
        
        try:
            url = topic_urls[topic]
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            headlines = []
            # Category pages often use h3 for titles
            for item in soup.find_all('h3')[:15]:
                link = item.find('a')
                if link and 'href' in link.attrs:
                    title = item.get_text(strip=True)
                    article_url = link['href']
                    if not article_url.startswith('http'):
                        article_url = f"https://cafef.vn{article_url}"
                    
                    if not any(h['url'] == article_url for h in headlines):
                        headlines.append({"title": title, "url": article_url})
            
            logger.info(f"Crawled {len(headlines)} CafeF headlines for topic '{topic}'")
            return {"success": True, "topic": topic, "headlines": headlines}
        except Exception as e:
            logger.error(f"Error crawling CafeF news for topic '{topic}': {e}")
            return {"success": False, "error": str(e)}

class WebBrowser:
    """Class for automated web browsing using Playwright."""
    
    @staticmethod
    async def _google_search(query: str) -> dict:
        """Perform a Google search and return results. Falls back to DuckDuckGo if blocked."""
        try:
            async with async_playwright() as p:
                # Launch with anti-automation flags
                browser = await p.chromium.launch(
                    headless=True,
                    args=["--disable-blink-features=AutomationControlled"]
                )
                
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    viewport={'width': 1280, 'height': 800},
                    locale="en-US"
                )
                page = await context.new_page()
                
                # Optimize: Block images
                await page.route("**/*.{png,jpg,jpeg,gif,svg,woff,woff2}", lambda route: route.abort())
                
                # Try Google first
                search_url = f"https://www.google.com/search?q={quote_plus(query)}"
                await page.goto(search_url, timeout=20000)
                
                # Wait random delay to look more human (CÁCH 2)
                await page.wait_for_timeout(random.randint(2000, 4000))
                
                content = await page.content()
                results = []
                source = "Google"

                if "To continue, please type the characters below" in content or "Our systems have detected unusual traffic" in content:
                    logger.warning("Google CAPTCHA detected, falling back to DuckDuckGo")
                    # Fallback to DuckDuckGo (HTML version)
                    await page.goto(f"https://duckduckgo.com/html/?q={quote_plus(query)}", timeout=20000)
                    
                    # Wait for results to load
                    try:
                        await page.wait_for_selector(".result__body", timeout=5000)
                    except:
                        pass

                    content = await page.content()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    for res in soup.select('.result__body')[:5]:
                        title_el = res.select_one('.result__title a')
                        if title_el:
                            title = title_el.get_text(strip=True)
                            url = title_el['href']
                            results.append({"title": title, "url": url})
                    source = "DuckDuckGo (Fallback)"
                else:
                    # Wait for search results to appear (CÁCH 2)
                    try:
                        await page.wait_for_selector("h3", timeout=10000)
                    except:
                        logger.warning("Timeout waiting for h3 selector on Google")

                    # Use locator for more robust extraction as suggested (CÁCH 2)
                    h3_locators = await page.locator("h3").all()
                    for h3 in h3_locators[:5]:
                        title = await h3.inner_text()
                        if not title:
                            continue
                            
                        # Find the parent anchor tag to get the URL
                        parent_a = await h3.evaluate_handle("el => el.closest('a')")
                        if parent_a:
                            url = await parent_a.get_attribute("href")
                            if url and url.startswith('http'):
                                results.append({"title": title, "url": url})
                    
                    # Fallback to BeautifulSoup if locator didn't find enough results
                    if len(results) < 2:
                        content = await page.content()
                        soup = BeautifulSoup(content, 'html.parser')
                        for g in soup.select('div.g')[:5]:
                            anchor = g.select_one('a')
                            title_el = g.select_one('h3')
                            if anchor and title_el:
                                url = anchor['href']
                                if url.startswith('/url?q='):
                                    url = url.split('/url?q=')[1].split('&')[0]
                                
                                title = title_el.get_text(strip=True)
                                if title and url.startswith('http') and not any(r['url'] == url for r in results):
                                    results.append({"title": title, "url": url})

                await browser.close()
                logger.info(f"Search for '{query}' via {source} returned {len(results)} results")
                return {"success": True, "query": query, "results": results[:5], "source": source}
        except Exception as e:
            logger.error(f"Error in search: {e}")
            return {"success": False, "error": str(e)}

    @staticmethod
    async def _browse_url(url: str) -> dict:
        """Navigate to a URL and extract page content."""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
                page = await context.new_page()
                
                # Optimize: Block images
                await page.route("**/*.{png,jpg,jpeg,gif,svg,woff,woff2}", lambda route: route.abort())
                
                await page.goto(url, wait_until="domcontentloaded", timeout=20000)
                
                # Extract title and text content
                title = await page.title()
                # Simple text extraction
                content = await page.evaluate("() => document.body.innerText")
                
                await browser.close()
                logger.info(f"Browsed URL {url}, content length: {len(content)}")
                return {"success": True, "url": url, "title": title, "content": content[:5000]} # Limit content size
        except Exception as e:
            logger.error(f"Error browsing URL {url}: {e}")
            return {"success": False, "error": str(e)}
