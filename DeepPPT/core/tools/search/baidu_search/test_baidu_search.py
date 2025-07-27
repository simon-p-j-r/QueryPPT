import requests

BASE_URL = "http://127.0.0.1:8388"

def test_search():
    """测试图片搜索API"""
    response = requests.get(f"{BASE_URL}/search", params={"query": "鸡兔同笼可爱版"})
    assert response.status_code == 200
    data = response.json()
    print(data)

if __name__ == "__main__":
    test_search() 