from selenium import webdriver
from bs4 import BeautifulSoup
from flask import Blueprint,request, jsonify
import time
from urllib.parse import unquote

scrape_bp = Blueprint('scrape', __name__)

@scrape_bp.route('/scrape', methods=['GET'])
def scrape():
    keyword = request.args.get('keyword')
    if keyword:
        keyword = unquote(keyword)  
    else:
        return jsonify({"error": "Keyword parameter is required"}), 400

    print(f"Received keyword: {keyword}") 
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless') 
    driver = webdriver.Chrome(options=options)

    url = 'https://product.kyobobook.co.kr/category/KOR/01?type=all&per=20&sort=new&page=1'

    driver.get(url)

    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    print(keyword)

    prod_items = soup.select('li.prod_item')
    results = []

    for item in prod_items:
        title_tag = item.select_one('.prod_name')
        if title_tag:
            title = title_tag.get_text(strip=True)
            if keyword in title:
                img_tag = item.select_one('.prod_thumb_box img')
                img_url = img_tag.get('src') if img_tag else None
                author_tag = item.select_one('.prod_author')
                result = author_tag.get_text(strip=True)
                if "·" in result:
                    author = result.split("·")[0].strip() 
                else:
                    author = result.strip()

                if img_url:
                    results.append({'title': title, 'author':author, 'img_url': img_url})

    driver.quit()

    return jsonify(results)

