from playwright.sync_api import sync_playwright
from typing import List, Dict
import time
import os
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException

app = FastAPI()

def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    result_block1 = soup.find_all('div', class_='result c-container new-pmd')
    result_block2 = soup.find_all('div', class_='result c-container xpath-log new-pmd')
    result_blocks = result_block1 + result_block2
    results = []
    for block in result_blocks:
        title = block.find('h3').text.strip()
        link = block.find('a')['href']
        contents = block.find_all('span')
        abstract = ''
        for content in contents:
            abstract += content.text
            abstract += ' '
        abstract = ' '.join(abstract.split())
        sources = block.find('div', class_='c-gap-top-xsmall')
        source = ''
        if sources:
            source = sources.find('a').text.strip()
        results.append(
            {
                'title': title,
                'link': link,
                'abstract': abstract,
                'source': source
            }
        )
    return results


def baidu_search(query: str, num: int = 10) -> List[Dict[str, str]]:
    """
    使用百度搜索并返回指定数量的搜索结果
    
    Args:
        query (str): 搜索关键词
        num (int): 需要返回的搜索结果数量，默认为5
        
    Returns:
        List[Dict[str, str]]: 包含标题、链接和摘要的搜索结果列表
    """
    # print("Baidu Search is running, query: ", query)
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto('https://www.baidu.com')
            page.fill('#kw', query)
            page.click('#su')
            page.wait_for_selector('.result.c-container')
            while len(results) < num:
                html_content = page.content()
                new_results = parse_html(html_content)
                results.extend(new_results)
                if len(results) >= num:
                    break
                try:
                    next_button = page.query_selector('a.n:has-text("下一页")')
                    if next_button:
                        next_button.click()
                        page.wait_for_selector('.result.c-container')
                        time.sleep(1)
                    else:
                        break
                except Exception as e:
                    print(f"翻页过程中出现错误: {str(e)}")
                    break
        except Exception as e:
            print(f"搜索过程中出现错误: {str(e)}")
        finally:
            browser.close()
    return results[:num]


@app.get("/search")
async def search(query: str, num: int = 5):
    """
    搜索API端点
    :param query: 搜索关键词
    :param num: 需要返回的搜索结果数量，默认为5
    :return: 搜索结果列表
    """
    try:
        results = baidu_search(query, num)
        return {
            "status": "success",
            "keyword": query,
            "total_results": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8388)
