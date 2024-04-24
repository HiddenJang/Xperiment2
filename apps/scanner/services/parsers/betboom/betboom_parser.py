import asyncio
import aiohttp
import logging
import requests
import pprint


logger = logging.getLogger('Xperiment2.apps.scanner.betboom.betboom_parser')
CONNECTION_ATTEMPTS = 20

########### HEADERS ##############
HEADERS_GET = {
    'authority': 'sport.betboom.ru',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'cookie': '_ga=GA1.2.71020424.1713800846; _gid=GA1.2.123564127.1713800846; supportOnlineTalkID=BV121L6asmSNRtevELwa3vsn2d0vm1Tq; __zzatgib-w-bb=MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2UrbW0hG0cUI0MTCDJaIhR/JysMOD8UQEorc147ZyZheksbNR0KQ2hSVENdLRtJUBg5Mzk0ZnBXJ2BOWiJMXE95LiETeG8fQU5EJ3VUNDpkdCIPaRMjZHhRP0VuWUZpdRUXQzwcew0qQ20tOmo=ZYxPiQ==; __zzatgib-w-bb=MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2UrbW0hG0cUI0MTCDJaIhR/JysMOD8UQEorc147ZyZheksbNR0KQ2hSVENdLRtJUBg5Mzk0ZnBXJ2BOWiJMXE95LiETeG8fQU5EJ3VUNDpkdCIPaRMjZHhRP0VuWUZpdRUXQzwcew0qQ20tOmo=ZYxPiQ==; cfidsgib-w-bb=Vclgais8eMFpQszHGCfvQ6kVVs43KFbwj6V8+FRmKMtD5zu0fenT5yy9MUe0W7TJcxgcNLPayOWd5WLpPefG6m/JSFZ7r6MONYu7Or031D6KkYnXJre3xdN8EsefyHensu2/mHtgJ5FFbldYViCu/7hCv+p5TRa3k9hAbsE=; cfidsgib-w-bb=Vclgais8eMFpQszHGCfvQ6kVVs43KFbwj6V8+FRmKMtD5zu0fenT5yy9MUe0W7TJcxgcNLPayOWd5WLpPefG6m/JSFZ7r6MONYu7Or031D6KkYnXJre3xdN8EsefyHensu2/mHtgJ5FFbldYViCu/7hCv+p5TRa3k9hAbsE=',
    'if-modified-since': 'Wed, 24 Apr 2024 15:21:44 GMT',
    'referer': 'https://sport.betboom.ru/',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

HEADERS_POST = {
    'authority': 'sport.betboom.ru',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'content-type': 'application/json',
    # 'cookie': '_ga=GA1.2.71020424.1713800846; _gid=GA1.2.123564127.1713800846; supportOnlineTalkID=BV121L6asmSNRtevELwa3vsn2d0vm1Tq; __zzatgib-w-bb=MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2UrbW0hG0cUI0MTCDJaIhR/JysMOD8UQEorc147ZyZheksbNR0KQ2hSVENdLRtJUBg5Mzk0ZnBXJ2BOWiJMXFN5JyEWfW8fQU5EJ3VUNDpkdCIPaRMjZHhRP0VuWUZpdRUXQzwcew0qQ20tOmo=jtfpqw==; __zzatgib-w-bb=MDA0dC0cTApcfEJcdGswPi17CT4VHThHKHIzd2UrbW0hG0cUI0MTCDJaIhR/JysMOD8UQEorc147ZyZheksbNR0KQ2hSVENdLRtJUBg5Mzk0ZnBXJ2BOWiJMXFN5JyEWfW8fQU5EJ3VUNDpkdCIPaRMjZHhRP0VuWUZpdRUXQzwcew0qQ20tOmo=jtfpqw==; cfidsgib-w-bb=NZ3cuDEjBWx5XptyhUWxEkCQWTtmgMJCiqgRN0BePK67VF4VC2wYH6EM4WCbLnE6O1rqEEyedFc6XxkJTchxF5cZV6kiv9JMjeeebd7TEhhelQh9K3imcHceYI9YbWprILhfObkUOatNNxrZ0B9bOJ6dqe/D7qT/42bgGf0=; cfidsgib-w-bb=tvrDh7m5uwqNpMqh8D3xyLmo0QOmPuMJeeAqscL1YAMLUh+8EhGNPuZFoarJyzC/Rl8z8OkW7Rs7y0DMZFKCPuVvvm6tXS/+urN2FNf9OWAv/Wf5VmhO6RVvf664s9jrpQVinaDU2u1Yj0n8J0JKP28aDMoueFz/FU5a9EA=',
    'origin': 'https://sport.betboom.ru',
    'referer': 'https://sport.betboom.ru/',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

############# JSON DATA FOR POST #############
json_data_countries = {
    'sportId': 1,
    'timeFilter': 0,
    'langId': 1,
    'partnerId': 147,
    'countryCode': None,
}

json_data_champs = {
    'countryId': 1343,
    'timeFilter': 0,
    'langId': 1,
    'partnerId': 147,
    'countryCode': None,
}

############ PARAMS ##############
PARAMS_PREMATCH_CHAMP_EVENTS = {
    'champId': '4584',
    'timeFilter': '0',
    'langId': '1',
    'partnerId': '147',
    'countryCode': '',
}

PARAMS_EVENT = {
    'eventId': '18117592',
    'isLive': 'false',
    'langId': '1',
    'partnerId': '147',
    'countryCode': '',
}

PARAMS_LIVE = {
    'sportId': '1',
    'checkIsActiveAndBetStatus': 'false',
    'stakeTypes': [
        '1',
        '702',
        '2',
        '3',
        '37',
    ],
    'partnerId': '147',
    'langId': '1',
    'countryCode': 'CA',
}

#### POST URL #####
COUNTRY_LIST_URL = 'https://sport.betboom.ru/Prematch/GetCountryList'
CHAMPS_LIST_URL = 'https://sport.betboom.ru/Prematch/GetChampsList'

#### GET URL ####
PREMATCH_CHAMP_EVENTS_URL = 'https://sport.betboom.ru/prematch/geteventslist'
LIVE_URL = 'https://sport.betboom.ru/Live/GetLiveEvents'

# res = requests.get(url=COUNTRYS_URL, params=PARAMS_PREMATCH, headers=HEADERS)
# print(res)
# r = res.json()
# pprint.pprint(len(r))

res_post = requests.post(url=COUNTRY_LIST_URL, headers=HEADERS_POST, json=json_data_countries)
print(len(res_post.json()))
# answer = res_post.get("replies")
# print(*answer)
#pprint.pprint(len(r))