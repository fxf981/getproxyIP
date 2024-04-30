import requests
import socket
import time
import os

PROXY_URL = "https://www.freeproxy.world/?type=socks5&anonymity=&country=US&speed=&port=&page={}"
PROXY_FILE = "proxy_list.txt"

def get_proxy_list():
    proxy_list = []
    for page in range(1, 11):
        url = PROXY_URL.format(page)
        response = requests.get(url)
        # 使用正则表达式或 BeautifulSoup 解析代理 IP 和端口
        proxies = /* 解析代理列表 */
        proxy_list.extend(proxies)
    return proxy_list

def check_proxy_availability(proxy):
    ip, port = proxy.split(":")
    try:
        sock = socket.create_connection((ip, int(port)), timeout=5)
        sock.close()
        return True
    except:
        return False

def save_proxy_list(proxy_list):
    available_proxies = [proxy for proxy in proxy_list if check_proxy_availability(proxy)]
    with open(PROXY_FILE, "w") as f:
        f.write("\n".join(available_proxies))

def main():
    proxy_list = get_proxy_list()
    save_proxy_list(proxy_list)

if __name__ == "__main__":
    main()