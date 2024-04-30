import requests
from bs4 import BeautifulSoup
PROXY_FILE = "proxy_list.txt"


proxy_list = []

for page in range(1, 11):
    url = f'https://www.freeproxy.world/?type=socks5&anonymity=&country=US&speed=&port=&page={page}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for row in soup.find_all('tr')[1:]:
        cells = row.find_all('td')
        if len(cells) >= 2:
            ip = cells[0].text.strip()
            port = cells[1].text.strip()
            proxy_list.append(f"{ip}:{port}")
        else:
            print(f"警告: 第{len(proxy_list) + 1}行数据格式不正确,已跳过。")

if proxy_list:
    with open(PROXY_FILE, 'w') as f:
        f.write('\n'.join(proxy_list))
    print(f"已保存{len(proxy_list)}个代理IP和端口到proxy_list.txt文件中。")
else:
    print("未找到任何有效的代理 IP 和端口。")