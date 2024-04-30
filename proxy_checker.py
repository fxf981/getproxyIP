import requests
from bs4 import BeautifulSoup
import concurrent.futures
from tqdm import tqdm  # 导入tqdm库

PROXY_FILE = "proxy_list.txt"


def check_proxy(proxy):
    try:
        url = "https://httpbin.org/ip"
        response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.ok:
            return proxy
    except Exception as e:
        pass
    return None


proxy_list = []

for page in tqdm(range(1, 11)):  # 使用tqdm显示进度条
    url = f'https://www.freeproxy.world/?type=http&anonymity=&country=US&speed=&port=&page={page}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for row in soup.find_all('tr')[1:]:
        cells = row.find_all('td')
        if len(cells) >= 2:
            ip = cells[0].text.strip()
            port = cells[1].text.strip()
            proxy = f"{ip}:{port}"
            proxy_list.append(proxy)
        else:
            print(f"警告: 第{len(proxy_list) + 1}行数据格式不正确,已跳过。")

if proxy_list:
    validated_proxies = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(check_proxy, proxy_list)
        for result in tqdm(results, total=len(proxy_list), desc="验证代理中"):  # 使用tqdm显示验证进度
            if result:
                validated_proxies.append(result)

    if validated_proxies:
        with open(PROXY_FILE, 'w') as f:
            f.write('\n'.join(validated_proxies))
        print(f"已保存{len(validated_proxies)}个可用代理IP和端口到proxy_list.txt文件中。")
    else:
        print("未找到任何可用的代理 IP 和端口。")
else:
    print("未找到任何有效的代理 IP 和端口。")
