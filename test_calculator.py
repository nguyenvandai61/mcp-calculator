import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the current directory to sys.path to import calculator
sys.path.insert(0, os.path.dirname(__file__))

from tools import Calculator, NewsCrawler

class TestCalculator(unittest.TestCase):
    def test_simple_addition(self):
        result = Calculator._calculate("2 + 3")
        self.assertEqual(result["success"], True)
        self.assertEqual(result["result"], 5)

    def test_math_function(self):
        result = Calculator._calculate("math.sin(0)")
        self.assertEqual(result["success"], True)
        self.assertAlmostEqual(result["result"], 0.0)

    def test_random_function(self):
        result = Calculator._calculate("random.randint(1, 10)")
        self.assertEqual(result["success"], True)
        self.assertIsInstance(result["result"], int)
        self.assertGreaterEqual(result["result"], 1)
        self.assertLessEqual(result["result"], 10)

    def test_invalid_expression(self):
        result = Calculator._calculate("invalid syntax +++")
        self.assertEqual(result["success"], False)
        self.assertIn("invalid syntax", result["error"])

        # Looking at code, no try-except, so eval will raise SyntaxError.
        # To make it testable, perhaps wrap in try-except in function, but since user asked for unittest, I'll test valid cases.

    def test_complex_expression(self):
        result = Calculator._calculate("math.sqrt(16) + random.choice([1,2,3])")
        self.assertEqual(result["success"], True)
        self.assertIsInstance(result["result"], float)

class TestCrawlNewsToday(unittest.TestCase):
    @patch('tools.requests.get')
    def test_successful_crawl(self, mock_get):
        # Mock the response
        mock_response = MagicMock()
        mock_response.content = '''
        <html>
        <body>
        <h3 class="title-news"><a href="/tin-tuc-1">Tin tức 1</a></h3>
        <h3 class="title-news"><a href="/tin-tuc-2">Tin tức 2</a></h3>
        <h3 class="title-news"><a href="/tin-tuc-3">Tin tức 3</a></h3>
        </body>
        </html>
        '''
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = NewsCrawler._crawl_news()
        self.assertEqual(result["success"], True)
        self.assertEqual(len(result["headlines"]), 3)
        self.assertIn("title", result["headlines"][0])
        self.assertIn("url", result["headlines"][0])

    @patch('tools.requests.get')
    def test_request_failure(self, mock_get):
        mock_get.side_effect = Exception("Network error")

        result = NewsCrawler._crawl_news()
        self.assertEqual(result["success"], False)
        self.assertIn("Network error", result["error"])

class TestCrawlNewsByTopic(unittest.TestCase):
    @patch('tools.requests.get')
    def test_successful_topic_crawl(self, mock_get):
        # Mock response for thoi-su
        mock_response = MagicMock()
        mock_response.content = '''
        <html>
        <body>
        <h3 class="title-news"><a href="/tin-thoi-su-1">Tin thời sự 1</a></h3>
        <h3 class="title-news"><a href="/tin-thoi-su-2">Tin thời sự 2</a></h3>
        </body>
        </html>
        '''
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = NewsCrawler._crawl_news_by_topic("thoi-su")
        self.assertEqual(result["success"], True)
        self.assertEqual(result["topic"], "thoi-su")
        self.assertEqual(len(result["headlines"]), 2)

    @patch('tools.requests.get')
    def test_invalid_topic(self, mock_get):
        result = NewsCrawler._crawl_news_by_topic("invalid-topic")
        self.assertEqual(result["success"], False)
        self.assertIn("not found", result["error"])

    @patch('tools.requests.get')
    def test_topic_request_failure(self, mock_get):
        mock_get.side_effect = Exception("Network error")

        result = NewsCrawler._crawl_news_by_topic("kinh-doanh")
        self.assertEqual(result["success"], False)
        self.assertIn("Network error", result["error"])

class TestReadArticle(unittest.TestCase):
    @patch('tools.requests.get')
    def test_successful_article_read(self, mock_get):
        # Mock response with article content
        mock_response = MagicMock()
        mock_response.content = '''
        <html>
        <body>
        <h1 class="title-detail">Test Article Title</h1>
        <p class="description">Test description</p>
        <article class="fck_detail">
        <p>Paragraph 1</p>
        <p>Paragraph 2</p>
        </article>
        </body>
        </html>
        '''
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = NewsCrawler._read_article("https://vnexpress.net/test-article")
        self.assertEqual(result["success"], True)
        self.assertIn("Test Article Title", result["content"])
        self.assertIn("Paragraph 1", result["content"])

    @patch('tools.requests.get')
    def test_article_read_failure(self, mock_get):
        mock_get.side_effect = Exception("Network error")

        result = NewsCrawler._read_article("https://vnexpress.net/test-article")
        self.assertEqual(result["success"], False)
        self.assertIn("Network error", result["error"])

class TestCrawlCafeF(unittest.TestCase):
    @patch('tools.requests.get')
    def test_successful_cafef_crawl(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = '''
        <html>
        <body>
        <div class="top_noibat">
            <h2><a href="/highlight">Highlight News</a></h2>
        </div>
        <h3><a href="/news-1">News 1</a></h3>
        <h3><a href="/news-2">News 2</a></h3>
        </body>
        </html>
        '''
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = NewsCrawler._crawl_cafef_news()
        self.assertEqual(result["success"], True)
        self.assertEqual(len(result["headlines"]), 3)
        self.assertEqual(result["headlines"][0]["title"], "Highlight News")

    @patch('tools.requests.get')
    def test_successful_cafef_topic_crawl(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = '''
        <html>
        <body>
        <h3><a href="/stock-1">Stock News 1</a></h3>
        <h3><a href="/stock-2">Stock News 2</a></h3>
        </body>
        </html>
        '''
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = NewsCrawler._crawl_cafef_by_topic("chung-khoan")
        self.assertEqual(result["success"], True)
        self.assertEqual(result["topic"], "chung-khoan")
        self.assertEqual(len(result["headlines"]), 2)

    @patch('tools.requests.get')
    def test_cafef_article_read(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = '''
        <html>
        <body>
        <h1 class="title">CafeF Article Title</h1>
        <h2 class="sapo">CafeF Sapo</h2>
        <div id="mainContent">
            <p>CafeF Content Paragraph 1</p>
            <p>CafeF Content Paragraph 2</p>
        </div>
        </body>
        </html>
        '''
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = NewsCrawler._read_article("https://cafef.vn/test-article.chn")
        self.assertEqual(result["success"], True)
        self.assertIn("CafeF Article Title", result["content"])
        self.assertIn("CafeF Content Paragraph 1", result["content"])

if __name__ == '__main__':
    unittest.main()