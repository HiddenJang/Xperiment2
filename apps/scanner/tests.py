import requests

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'baggage': 'sentry-environment=production,sentry-release=1737355356409,sentry-public_key=103e26ab0315f2335e929876414ae8d8,sentry-trace_id=a260f4c3dbc244839e3a8a9b499ab7fb,sentry-sample_rate=1,sentry-sampled=true',
    'content-type': 'application/json',
    # 'cookie': 'Path=/; _sa=SA1.cfc06580-dedd-4a85-a2b1-a3b9d7b87369.1719406286; visitor_id=82cc43ab0d3e1fcb24fff0ef8242dd70; visitor_id_version=2; _ga=GA1.2.1887908695.1719406287; __exponea_etc__=aae1d5de-c0c2-4a9b-aa42-a1823a04f11f; user_ukey=b2e7f9c5-2823-40b9-90da-83bfca6c4898; acceptedCookiesPolicy=1; __exponea_time2__=-0.21917200088500977',
    'origin': 'https://www.olimp.bet',
    'priority': 'u=1, i',
    'referer': 'https://www.olimp.bet/results?sportId=1&startDate=2025-01-23&endDate=2025-01-23&shouldSearchByChamps=false',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': 'a260f4c3dbc244839e3a8a9b499ab7fb-ac300e0c0c3b4f03-1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'x-cupis': '1',
    'x-guid': '82cc43ab0d3e1fcb24fff0ef8242dd70',
    'x-token': '02ced4de2fab79eb6a2d08c040664335',
}

json_data = {
    'time_shift': -240,
    'id': 1,
    'date': '2025-01-23',
    'date_end': '2025-01-23',
    'lang_id': '0',
    'platforma': 'SITE_CUPIS',
}

response = requests.post('https://www.olimp.bet/api/results', headers=headers, json=json_data)
print(response.text)