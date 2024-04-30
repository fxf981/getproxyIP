import requests
from bs4 import BeautifulSoup
import concurrent.futures
from tqdm import tqdm  # 导入tqdm库
import json


def get_proxy_list(page):
    """获取指定页码的代理IP列表"""
    url = f"https://proxylist.geonode.com/api/proxy-list?limit=50&page={page}&sort_by=lastChecked&sort_type=desc"
    response = requests.get(url)
    data = json.loads(response.text)
    print(data["data"])
    return data["data"]

def check_proxy(proxy):
    """验证代理IP是否可用"""
    try:
        proxies = {
            "http": f"{proxy['protocols']}://{proxy['ip']}:{proxy['port']}",
            "https": f"{proxy['protocols']}://{proxy['ip']}:{proxy['port']}"
        }
        url = "https://ipinfo.io/json"
        response = requests.get(url, proxies=proxies, timeout=5)
        if response.ok:
            ip_info = json.loads(response.text)
            country = ip_info.get("country")
            org = ip_info.get("org")
            if country:
                proxy_info = f"{proxy['protocols']}://{proxy['ip']}:{proxy['port']}#{country}--{org}"
                return proxy_info
    except:
        return None

def main():
    """主函数"""
    validated_proxies = []
    for page in range(1, 11):
        proxy_list = get_proxy_list(page)
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            validated_proxies.extend([proxy for proxy in executor.map(check_proxy, proxy_list) if proxy])
    if validated_proxies:
        with open("proxy_list.txt", 'w') as f:
            for proxy in validated_proxies:
                f.write(f"{proxy['ip']}:{proxy['port']} ({proxy['protocols']})\n")
        print(f"已保存{len(validated_proxies)}个可用代理IP和端口到proxy_list.txt文件中。")
    else:
        print("未找到任何可用的代理 IP 和端口。")
    

if __name__ == "__main__":
    main()