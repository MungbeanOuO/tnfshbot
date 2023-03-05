import requests
from bs4 import BeautifulSoup

url = "https://www.tnfsh.tn.edu.tw/latestevent/Index.aspx?Parser=9,3,19"

# 設定請求標頭
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63"
}

try:
    # 發送 GET 請求
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # 解析 HTML 原始碼
    soup = BeautifulSoup(response.text, "html.parser")

    # 找到所有的表格元素
    ul = soup.find("ul", class_="list list_type")

    if not ul:
        raise ValueError("找不到目標元素")


    # 找到每一個項目
    items = ul.find_all("li")

    # 逐一取得每個項目中的文字內容
    for item in items:
        text = item.get_text().strip()

        # 輸出資料到終端機上
        print(text)
        
except requests.exceptions.RequestException as e:
    print("發生錯誤：", e)
except (AttributeError, TypeError) as e:
    print("找不到目標元素：", e)
except Exception as e:
    print("其他錯誤：", e)
