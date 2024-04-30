import requests
from bs4 import BeautifulSoup
import concurrent.futures
from tqdm import tqdm  # 导入tqdm库
import json
PROXY_FILE = "proxy_list.txt"

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
    # 发送 GET 请求获取文本数据
    url = 'https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http&proxy_format=protocolipport&format=text'
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 按行读取文本数据并写入数组
        lines = response.text.split('\n')
        proxy_list = [line.strip() for line in lines if line.strip()]  # 去除空行并去除每行两端的空白字符
        print(proxy_list)  # 打印结果数组
    else:
        print(f"请求失败，状态码：{response.status_code}")


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