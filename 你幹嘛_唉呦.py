import asyncio
import aiohttp
from bs4 import BeautifulSoup
import discord


# 設定 Discord bot 的 token 和聊天頻道 ID
DISCORD_TOKEN = 'aaaaaaaaaaaa'
DISCORD_CHANNEL_ID = 1145141919810
intents = discord.Intents().all()

# 設定網站 URL
URL = 'https://www.tnfsh.tn.edu.tw/latestevent/index.aspx?Parser=9,3,19'


# 設定定時更新的時間間隔（單位為秒）
UPDATE_INTERVAL = 3600  # 每小時更新一次

# 建立 Discord 客戶端
client = discord.Client(intents=intents)

# 定義更新公告的函式
async def update_announcement():
    # 發送 HTTP GET 請求取得網頁內容
    print('Sending HTTP GET request...')
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            html = await response.text(encoding='utf-8')

    # 使用 BeautifulSoup 解析 HTML 文件
    print('Parsing HTML...')
    soup = BeautifulSoup(html, 'html.parser')

    # 找到所有的表格元素
    ul = soup.find("ul", class_="list list_type")
    
    if not ul:
        raise ValueError("找不到目標元素")
    
    # 找到每一個項目
    items = ul.find_all("li")
    
    # 取得指定聊天頻道的物件
    print('Getting Discord channel...')
    channel = client.get_channel(DISCORD_CHANNEL_ID)

    # 發送訊息到指定聊天頻道
    print('Sending message to Discord channel...')

    # 建立 Discord 訊息
    message = ''
    for item in items:
        message = item.get_text().strip()
        if not message:
            print("Announcement message is empty, skipping...")
        else:
            await channel.send(message)


# 當 Discord bot 客戶端啟動時執行
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
 
    # 每隔指定的時間更新一次公告
    while True:
        print('Updating announcement...')
        await update_announcement()
        await asyncio.sleep(UPDATE_INTERVAL)

# 啟動 Discord bot 客戶端
client.run(DISCORD_TOKEN)

