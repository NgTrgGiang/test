import requests
from bs4 import BeautifulSoup

def crawl_vnexpress_education():
    url = 'https://vnexpress.net/giao-duc'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Tìm tất cả các thẻ h3 có class 'title-news'
    articles = soup.find_all('h3', class_='title-news')

    print("📰 Bài viết mới nhất trong chuyên mục Giáo dục:\n")

    for i, article in enumerate(articles[:10], start=1):  # Lấy 10 bài đầu tiên
        title = article.get_text(strip=True)
        link = article.a['href'] if article.a else 'Không có link'
        print(f"{i}. {title}\n   🔗 {link}\n")

if __name__ == '__main__':
    crawl_vnexpress_education()
