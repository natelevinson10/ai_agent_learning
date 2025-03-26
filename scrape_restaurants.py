import requests
import json

def search_restaurants(query):
    """
    Search for restaurants on Uber Eats based on a query.

    :param query: A string representing the user's search query
    :return: A dictionary of restaurants with their title, action URL, and rating
    """
    restaurants = {}

    url = "https://www.ubereats.com/_p/api/getSearchFeedV1"

    payload = json.dumps({
    "userQuery": f"{query}",
    "date": "",
    "startTime": 0,
    "endTime": 0,
    "sortAndFilters": [],
    "vertical": "ALL",
    "searchSource": "SEARCH_SUGGESTION",
    "displayType": "SEARCH_RESULTS",
    "searchType": "GLOBAL_SEARCH",
    "keyName": "",
    "cacheKey": "",
    "recaptchaToken": ""
    })
    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'cookie': 'uev2.id.xp=a92b466a-251e-40a3-aedf-2c65e3e7d5c8; dId=2566066d-cbb8-4efb-88e9-aed227d4c54d; uev2.id.session=353ea08f-3998-4d3c-90fe-515211a93739; uev2.ts.session=1742875417590; _ua={"session_id":"3bf1c9d3-fddd-4ac8-b713-d58360e19d19","session_time_ms":1742875417624}; marketing_vistor_id=40b88d68-8fb4-4f72-80bd-0f91d4ac20bb; jwt-session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InNsYXRlLWV4cGlyZXMtYXQiOjE3NDI4NzcyMTc2MjN9LCJpYXQiOjE3NDI4NzU0MTcsImV4cCI6MTc0Mjk2MTgxN30.0PZmikGg_Trsg3dWDE5-rtINW9qwIw68YZMFFz2qaf8; uev2.embed_theme_preference=dark; utag_main__sn=1; utag_main_ses_id=1742875422222%3Bexp-session; utm_medium=undefined; utm_source=undefined; utag_main__ss=0%3Bexp-session; uev2.gg=true; _scid=4__45_VgeoCRlbtURTz3NBkEtGTNFkAQ; _gcl_au=1.1.42276734.1742875428; _tt_enable_cookie=1; _ttp=01JQ5QH16FPZQESQN158CGDAMP_.tt.1; _ga=GA1.1.1992587885.1742875428; _yjsu_yjad=1742875428.7b965ac2-116a-4f5c-b11f-c3221d5db51b; _clck=1oi2gkh%7C2%7Cfui%7C0%7C1910; uev2.loc=%7B%22address%22%3A%7B%22address1%22%3A%2240%20Fountain%20Ave%22%2C%22address2%22%3A%22Middletown%2C%20CT%22%2C%22aptOrSuite%22%3A%22%22%2C%22eaterFormattedAddress%22%3A%2240%20Fountain%20Ave%2C%20Middletown%2C%20CT%2006457-3111%2C%20US%22%2C%22subtitle%22%3A%22Middletown%2C%20CT%22%2C%22title%22%3A%2240%20Fountain%20Ave%22%2C%22uuid%22%3A%22%22%7D%2C%22latitude%22%3A41.55184%2C%22longitude%22%3A-72.65923%2C%22reference%22%3A%22here%3Aaf%3Astreetsection%3AipvJbd8MwPfQs1PrxJRprB%3ACggIBCCvhpfJAxABGgI0MA%22%2C%22referenceType%22%3A%22here_places%22%2C%22type%22%3A%22here_places%22%2C%22addressComponents%22%3A%7B%22city%22%3A%22Middletown%22%2C%22countryCode%22%3A%22US%22%2C%22firstLevelSubdivisionCode%22%3A%22CT%22%2C%22postalCode%22%3A%2206457-3111%22%7D%2C%22categories%22%3A%5B%22address_point%22%5D%2C%22originType%22%3A%22user_autocomplete%22%2C%22source%22%3A%22manual_auto_complete%22%2C%22userState%22%3A%22Unknown%22%7D; _ScCbts=%5B%5D; _sctr=1%7C1742875200000; utag_main__pn=3%3Bexp-session; _scid_r=_X_45_VgeoCRlbtURTz3NBkEtGTNFkAQACQEdA; _userUuid=; u-cookie-prefs=eyJ2ZXJzaW9uIjoxMDAsImRhdGUiOjE3NDI4NzY2OTgxMjEsImNvb2tpZUNhdGVnb3JpZXMiOlsiYWxsIl0sImltcGxpY2l0Ijp0cnVlfQ%3D%3D; _ga_P1RM71MPFP=GS1.1.1742875428.1.1.1742876698.47.0.0; uev2.diningMode=DELIVERY; utag_main__se=20%3Bexp-session; utag_main__st=1742878541397%3Bexp-session; _uetsid=271dc560092e11f0868ee3a1f7ce527a; _uetvid=271e13e0092e11f091b2751f2d5a0bbd; marketing_vistor_id=40b88d68-8fb4-4f72-80bd-0f91d4ac20bb; uev2.embed_theme_preference=dark; uev2.id.session=353ea08f-3998-4d3c-90fe-515211a93739; uev2.ts.session=1742875417590; jwt-session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InNsYXRlLWV4cGlyZXMtYXQiOjE3NDI5MTU0OTAwMjd9LCJpYXQiOjE3NDI4NzU0MTcsImV4cCI6MTc0Mjk2MTgxN30.FyOklQKuV-JH570a58YbXGH0IlzGGFfyYcPFoq0u1jY',
    'origin': 'https://www.ubereats.com',
    'priority': 'u=1, i',
    'referer': 'https://www.ubereats.com/search?eventSource=text&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMjQwJTIwRm91bnRhaW4lMjBBdmUlMjIlMkMlMjJyZWZlcmVuY2UlMjIlM0ElMjJoZXJlJTNBYWYlM0FzdHJlZXRzZWN0aW9uJTNBaXB2SmJkOE13UGZRczFQcnhKUnByQiUzQUNnZ0lCQ0N2aHBmSkF4QUJHZ0kwTUElMjIlMkMlMjJyZWZlcmVuY2VUeXBlJTIyJTNBJTIyaGVyZV9wbGFjZXMlMjIlMkMlMjJsYXRpdHVkZSUyMiUzQTQxLjU1MTg0JTJDJTIybG9uZ2l0dWRlJTIyJTNBLTcyLjY1OTIzJTdE&q=Indian%20Food&sc=SEARCH_SUGGESTION&searchEntered=indian%20food&searchType=GLOBAL_SEARCH&vertical=ALL',
    'sec-ch-prefers-color-scheme': 'dark',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-csrf-token': 'x',
    'x-uber-client-gitref': '49e2ec1cefad4068d97029dc59c2003076262bc2'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()['data']['feedItems']
    for store in data:
       restaurants[store['store']['title']['text']] = [store['store']['actionUrl'], store['store']['tracking']['storePayload']['storeUUID']]
       try:
           restaurants[store['store']['title']['text']].append(store['store']['rating']['text'])
       except KeyError:
           restaurants[store['store']['title']['text']].append(None)

    return restaurants
