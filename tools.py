import math
import random
import requests
from bs4 import BeautifulSoup
import logging

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
        """Read the full content of a news article from VNExpress."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
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
            else:
                content_text = "No content found"
            
            full_content = f"Title: {title_text}\n\nDescription: {desc_text}\n\nContent:\n{content_text}"
            
            logger.info(f"Read article from {url}, length: {len(full_content)}")
            return {"success": True, "url": url, "content": full_content}
        except Exception as e:
            logger.error(f"Error reading article from {url}: {e}")
            return {"success": False, "error": str(e)}