from tools import WebBrowser
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

async def test_real_google_search():
    print("Starting real Google search test (Async)...")
    result = await WebBrowser._google_search("MCP protocol")
    if result["success"]:
        print(f"Successfully found {len(result['results'])} results:")
        for i, res in enumerate(result["results"], 1):
            print(f"{i}. {res['title']} - {res['url']}")
    else:
        print(f"Search failed: {result.get('error')}")

if __name__ == "__main__":
    asyncio.run(test_real_google_search())
