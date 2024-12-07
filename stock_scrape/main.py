from bs4 import BeautifulSoup
import httpx


# response = httpx.get("https://www.judal.co.kr/?view=stockList&themeIdx=39")
# soup = BeautifulSoup(response.text, "html.parser")

# selector = ".list-group-item.list-group-item-action.list-group-item-sub.px-4.py-0"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
}

response = httpx.get("https://www.judal.co.kr/?view=stockList&themeIdx=39", headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
