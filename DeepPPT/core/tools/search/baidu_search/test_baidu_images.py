import requests

BASE_URL = "http://127.0.0.1:8288"

def test_search_images():
    """测试图片搜索API"""
    response = requests.get(f"{BASE_URL}/search_images", params={"query": "鸡兔同笼可爱版"})
    assert response.status_code == 200
    data = response.json()
    print(f"搜索关键词: {data['keyword']}")
    print(f"下载图片数量: {data['total_images']}")
    # print(f"图片保存路径: {data['image_paths']}")

if __name__ == "__main__":
    test_search_images() 