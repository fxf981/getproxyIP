import requests
from bs4 import BeautifulSoup
import concurrent.futures
from tqdm import tqdm  # 导入tqdm库
import json
PROXY_FILE = "proxy_list.txt"

def get_proxy_list(page):
    """获取指定页码的代理IP列表"""
    url = f"https://proxylist.geonode.com/api/proxy-list?limit=500&page={page}&sort_by=lastChecked&sort_type=desc"
    response = requests.get(url)
    data = json.loads(response.text)
    return data["data"]

def check_proxy(proxy):
    try:
        url = "https://ipinfo.io/json"
        response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.ok:
            ip_info = json.loads(response.text)
            country = ip_info.get("country")
            org = ip_info.get("org")
            if country:
                proxy_info = f"{proxy}#{country}--{org}"
                return proxy_info
    except Exception as e:
        pass
    return None

def main():
    """主函数"""
    proxy_list = []
    for page in tqdm(range(1, 10)):  # 使用tqdm显示进度条
        data = get_proxy_list(page)
        if data:
            for entry in data:
                ip = entry['ip']
                port = entry['port']
                protocols_str = ', '.join(entry['protocols'])  # 将列表转换为逗号分隔的字符串
                proxy = f"{protocols_str}://{ip}:{port}"
                proxy_list.append(proxy)

    if proxy_list:
        validated_proxies = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
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

if __name__ == "__main__":
    main()