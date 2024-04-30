import requests
from bs4 import BeautifulSoup
import socket

PROXY_URL = "https://www.freeproxy.world/?type=socks5&anonymity=&country=US&speed=&port=&page={}"
PROXY_FILE = "proxy_list.txt"

def get_proxy_list():
    proxy_list = []
    for page in range(1, 11):
        url = PROXY_URL.format(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        table = soup.find("table", {"class": "table table-striped table-bordered"})
        if table:
            for row in table.find_all("tr")[1:]:
                cols = row.find_all("td")
                ip = cols[0].text.strip()
                port = cols[1].text.strip()
                proxy_list.append(f"{ip}:{port}")

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