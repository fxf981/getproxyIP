const fs = require('fs');

async function getProxyList() {
  let proxyList = [];
  for (let page = 1; page <= 10; page++) {
    const response = await fetch(`https://www.freeproxy.world/?type=socks5&anonymity=&country=US&speed=&port=&page=${page}`);
    const data = await response.text();
    // 使用正则表达式或 DOM 解析提取代理 IP 和端口
    const pageProxies = /* 解析代理列表 */
    proxyList = proxyList.concat(pageProxies);
  }
  return proxyList;
}

async function checkProxyAvailability(proxyHost, proxyPort) {
  return new Promise((resolve, reject) => {
    const net = require('net');
    const client = net.createConnection({ host: proxyHost, port: proxyPort }, () => {
      client.end();
      resolve(true);
    });
    client.on('error', () => {
      resolve(false);
    });
    client.setTimeout(5000, () => {
      client.destroy();
      resolve(false);
    });
  });
}

async function saveProxyList(proxyList) {
  const availableProxies = await Promise.all(proxyList.map(async (proxy) => {
    const isAvailable = await checkProxyAvailability(proxy.ip, proxy.port);
    return isAvailable ? proxy : null;
  }));
  const proxyData = availableProxies.filter(Boolean).map(proxy => `${proxy.ip}:${proxy.port}`).join('\n');
  fs.writeFileSync('proxy-list.txt', proxyData);
}

async function main() {
  const proxyList = await getProxyList();
  await saveProxyList(proxyList);
}

main();