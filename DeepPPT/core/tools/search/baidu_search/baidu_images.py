# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 10:17:50 2023
@author: MatpyMaster
"""
from fastapi import FastAPI, HTTPException
import requests
import os
import re
from typing import Dict, List
from pathlib import Path
from core.utils import current_dir, get_VLM_resp
import json
import base64

app = FastAPI()

def get_images_from_baidu(keyword: str, page_num: int = 1) -> Dict:
    """
    从百度图片搜索获取图片
    :param keyword: 搜索关键词
    :param page_num: 页数，默认1页
    :return: 包含下载图片信息的字典
    """
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    url = 'https://image.baidu.com/search/acjson?'
    
    save_dir = Path(f"{current_dir}/data") / keyword
    save_dir.mkdir(parents=True, exist_ok=True)
    
    downloaded_images = []
    n = 0
    
    try:
        for pn in range(0, 30 * page_num, 30):
            param = {
                'tn': 'resultjson_com',
                'logid': '7603311155072595725',
                'ipn': 'rj',
                'ct': 201326592,
                'is': '',
                'fp': 'result',
                'queryWord': keyword,
                'cl': 2,
                'lm': -1,
                'ie': 'utf-8',
                'oe': 'utf-8',
                'adpicid': '',
                'st': -1,
                'z': '',
                'ic': '',
                'hd': '',
                'latest': '',
                'copyright': '',
                'word': keyword,
                's': '',
                'se': '',
                'tab': '',
                'width': '',
                'height': '',
                'face': 0,
                'istype': 2,
                'qc': '',
                'nc': '1',
                'fr': '',
                'expermode': '',
                'force': '',
                'cg': '',
                'pn': pn,
                'rn': '30',
                'gsm': '1e',
                '1618827096642': ''
            }
            
            request = requests.get(url=url, headers=header, params=param)
            if request.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to fetch images from Baidu")
                
            request.encoding = 'utf-8'
            html = request.text
            image_url_list = re.findall('"thumbURL":"(.*?)",', html, re.S)
            
            for image_url in image_url_list:
                try:
                    image_data = requests.get(url=image_url, headers=header).content
                    image_path = save_dir / f'{n:06d}.jpg'
                    with open(image_path, 'wb') as fp:
                        fp.write(image_data)
                    downloaded_images.append(str(image_path))
                    n += 1
                except Exception as e:
                    print(f"Failed to download image {image_url}: {str(e)}")
                    continue
                    
        return {
            "status": "success",
            "keyword": keyword,
            "total_images": len(downloaded_images),
            "image_paths": downloaded_images
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def encode_image(image_path):
    """
    将图片编码为Base64字符串。
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def describe_images(image_path: str, query: str):
    """
    描述图片
    :param image_path: 图片路径
    :param query: 搜索关键词
    :param LLM_Config: LLM配置
    """
    if os.getenv("VLMConfig"):
        VLMConfig = os.getenv("VLMConfig")
        VLMConfig = json.loads(VLMConfig)
        base64_image = encode_image(image_path)
        messages = [
            {
                "role": "user","content": [
                    {
                        "type": "text","text": f"这是一份根据关键词`{query}`搜索到的图片，请结合搜索词描述：1. 图片的基本组成(纯文字/文字+图片/纯图片)；2. 图片与搜索词的关系；3. 图片的绘画风格与布局"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
        response = get_VLM_resp(VLMConfig, messages)
        return response
    else:
        raise HTTPException(status_code=500, detail="VLMConfig is not set")


def search_images_with_description(query: str):
    """
    搜索图片
    :param query: 搜索关键词
    :return: 一个list，每个元素是一个dict，包含image_path和description
    每次最多返回10张图片
    """
    images = get_images_from_baidu(query).get("image_paths")[: 10]
    data_home = os.path.dirname(images[0])
    ret = []
    for image_path in images:
        description = describe_images(image_path, query)
        ret.append({
            "image_path": image_path,
            "description": description
        })
    with open(os.path.join(data_home, "search_images.json"), "w", encoding="utf-8") as f:
        json.dump(ret, f, ensure_ascii=False, indent=4)
    return ret


@app.get("/search_images")
async def search_images(query: str, page_num: int = 1):
    """
    搜索图片API端点
    :param query: 搜索关键词
    :param page_num: 页数，默认1页
    :return: 下载结果
    """
    return get_images_from_baidu(query, page_num)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8288)
    # describe_images("tmp/data/胡桃/000000.jpg", "胡桃")