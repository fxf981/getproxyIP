import json

# 示例 JSON 数据
json_data = '''
{
  "data": [
    {
      "_id": "6320d4e92fb0f02dd5521a20",
      "ip": "190.113.12.75",
      "anonymityLevel": "elite",
      "asn": "AS22860",
      "city": "Viña del Mar",
      "country": "CL",
      "created_at": "2022-09-13T19:07:21.705Z",
      "google": false,
      "isp": "Servicios Internet Ltda",
      "lastChecked": 1714472346,
      "latency": 281.037,
      "org": "TECNOERA-WEBHOSTING",
      "port": "3389",
      "protocols": [
        "socks5"
      ],
      "region": null,
      "responseTime": 3401,
      "speed": 4,
      "updated_at": "2024-04-30T10:19:06.292Z",
      "workingPercent": null,
      "upTime": 99.6270262516138,
      "upTimeSuccessCount": 6945,
      "upTimeTryCount": 6971
    },
    {
      "_id": "6306c99cde95dae52104f247",
      "ip": "104.129.199.57",
      "anonymityLevel": "elite",
      "asn": "AS22616",
      "city": "Los Angeles",
      "country": "US",
      "created_at": "2022-08-25T01:00:12.508Z",
      "google": false,
      "isp": "ZSCALER, INC.",
      "lastChecked": 1714472346,
      "latency": 143.891,
      "org": "Zscaler, Inc.",
      "port": "8800",
      "protocols": [
        "socks5"
      ],
      "region": null,
      "responseTime": 1229,
      "speed": 95,
      "updated_at": "2024-04-30T10:19:06.102Z",
      "workingPercent": null,
      "upTime": 96.2313003452244,
      "upTimeSuccessCount": 6690,
      "upTimeTryCount": 6952
    }
  ]
}
'''

# 将 JSON 数据解析为 Python 对象
data = json.loads(json_data)

# 遍历每个对象并输出 protocols 字段
for entry in data['data']:
    protocols_str = ', '.join(entry['protocols'])  # 将列表转换为逗号分隔的字符串
    print(f"Protocols: {protocols_str}")
