import requests
import json
from scrape_restaurants import search_restaurants

def get_menu_categories(store_uuid, store_url):
    """
    Get the menu categories for a given store.

    :param store_uuid: The UUID of the store
    :param store_url: The URL of the store
    :return: A list of tuples, each containing a menu category and its UUID
    """

    menu_categories = []
    subsection_uuids = []

    url = "https://www.ubereats.com/_p/api/getStoreV1"

    payload = json.dumps({
    "storeUuid": f"{store_uuid}",
    "diningMode": "DELIVERY",
    "time": {
        "asap": True
    },
    "cbType": "EATER_ENDORSED"
    })
    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'cookie': 'uev2.id.xp=a92b466a-251e-40a3-aedf-2c65e3e7d5c8; dId=2566066d-cbb8-4efb-88e9-aed227d4c54d; uev2.id.session=353ea08f-3998-4d3c-90fe-515211a93739; uev2.ts.session=1742875417590; _ua={"session_id":"3bf1c9d3-fddd-4ac8-b713-d58360e19d19","session_time_ms":1742875417624}; marketing_vistor_id=40b88d68-8fb4-4f72-80bd-0f91d4ac20bb; uev2.embed_theme_preference=dark; utag_main__sn=1; utag_main_ses_id=1742875422222%3Bexp-session; utm_medium=undefined; utm_source=undefined; utag_main__ss=0%3Bexp-session; uev2.gg=true; _scid=4__45_VgeoCRlbtURTz3NBkEtGTNFkAQ; _gcl_au=1.1.42276734.1742875428; _tt_enable_cookie=1; _ttp=01JQ5QH16FPZQESQN158CGDAMP_.tt.1; _ga=GA1.1.1992587885.1742875428; _yjsu_yjad=1742875428.7b965ac2-116a-4f5c-b11f-c3221d5db51b; _clck=1oi2gkh%7C2%7Cfui%7C0%7C1910; uev2.loc=%7B%22address%22%3A%7B%22address1%22%3A%2240%20Fountain%20Ave%22%2C%22address2%22%3A%22Middletown%2C%20CT%22%2C%22aptOrSuite%22%3A%22%22%2C%22eaterFormattedAddress%22%3A%2240%20Fountain%20Ave%2C%20Middletown%2C%20CT%2006457-3111%2C%20US%22%2C%22subtitle%22%3A%22Middletown%2C%20CT%22%2C%22title%22%3A%2240%20Fountain%20Ave%22%2C%22uuid%22%3A%22%22%7D%2C%22latitude%22%3A41.55184%2C%22longitude%22%3A-72.65923%2C%22reference%22%3A%22here%3Aaf%3Astreetsection%3AipvJbd8MwPfQs1PrxJRprB%3ACggIBCCvhpfJAxABGgI0MA%22%2C%22referenceType%22%3A%22here_places%22%2C%22type%22%3A%22here_places%22%2C%22addressComponents%22%3A%7B%22city%22%3A%22Middletown%22%2C%22countryCode%22%3A%22US%22%2C%22firstLevelSubdivisionCode%22%3A%22CT%22%2C%22postalCode%22%3A%2206457-3111%22%7D%2C%22categories%22%3A%5B%22address_point%22%5D%2C%22originType%22%3A%22user_autocomplete%22%2C%22source%22%3A%22manual_auto_complete%22%2C%22userState%22%3A%22Unknown%22%7D; _ScCbts=%5B%5D; _sctr=1%7C1742875200000; uev2.diningMode=DELIVERY; jwt-session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InNsYXRlLWV4cGlyZXMtYXQiOjE3NDI4ODAyNjUyNzB9LCJpYXQiOjE3NDI4NzU0MTcsImV4cCI6MTc0Mjk2MTgxN30.v7wp_kz0VDfHDUmgkoQtEVKLpFzZiA4eU4YuJsiLXnc; utag_main__pn=5%3Bexp-session; _scid_r=_3_45_VgeoCRlbtURTz3NBkEtGTNFkAQACQEdg; _userUuid=; u-cookie-prefs=eyJ2ZXJzaW9uIjoxMDAsImRhdGUiOjE3NDI4Nzg0NzEyNzQsImNvb2tpZUNhdGVnb3JpZXMiOlsiYWxsIl0sImltcGxpY2l0Ijp0cnVlfQ%3D%3D; _ga_P1RM71MPFP=GS1.1.1742875428.1.1.1742878476.60.0.0; utag_main__se=28%3Bexp-session; utag_main__st=1742880294086%3Bexp-session; _uetsid=271dc560092e11f0868ee3a1f7ce527a; _uetvid=271e13e0092e11f091b2751f2d5a0bbd; marketing_vistor_id=40b88d68-8fb4-4f72-80bd-0f91d4ac20bb; uev2.embed_theme_preference=dark; uev2.id.session=353ea08f-3998-4d3c-90fe-515211a93739; uev2.ts.session=1742875417590; jwt-session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InNsYXRlLWV4cGlyZXMtYXQiOjE3NDI5MTYzODAwNjR9LCJpYXQiOjE3NDI4NzU0MTcsImV4cCI6MTc0Mjk2MTgxN30.Er2rFMtwIMbXbJVgT0BM0wIMg_mFYyoLKpWZOqWbrRs',
    'origin': 'https://www.ubereats.com',
    'priority': 'u=1, i',
    'referer': f'https://www.ubereats.com{store_url}',
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
    data = response.json()['data']
    uuid = data['sections'][0]['uuid']
    for _ in data['sections'][0]['subsectionUuids']:
        subsection_uuids.append(_)
    
    i = 0
    for section in data['catalogSectionsMap'][uuid]:
        menu_categories.append((section['payload']['standardItemsPayload']['title']['text'], subsection_uuids[i]))
        i += 1
    return menu_categories, uuid


# print(get_menu_categories("f9f535fa-4afe-4a64-bdf0-54b53ce4e447"))

import requests
import json
def get_menu_category_items(store_uuid, uuid, store_url, menu_categories: list):
    """
    Get the menu items for a given store and menu category.

    :param store_uuid: The UUID of the store
    :param uuid: The UUID of the menu category
    :param store_url: The URL of the store
    :param menu_categories: A list of tuples, each containing a menu category and its UUID
    :return: A dictionary of menu items with their title and description
    """
    
    menu_items = {}

    url = "https://www.ubereats.com/_p/api/getStoreV1"

    payload = json.dumps({
    "storeUuid": f"{store_uuid}",
    "diningMode": "DELIVERY",
    "time": {
        "asap": True
    },
    "cbType": "EATER_ENDORSED"
    })
    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'cookie': 'uev2.id.xp=a92b466a-251e-40a3-aedf-2c65e3e7d5c8; dId=2566066d-cbb8-4efb-88e9-aed227d4c54d; uev2.id.session=353ea08f-3998-4d3c-90fe-515211a93739; uev2.ts.session=1742875417590; _ua={"session_id":"3bf1c9d3-fddd-4ac8-b713-d58360e19d19","session_time_ms":1742875417624}; marketing_vistor_id=40b88d68-8fb4-4f72-80bd-0f91d4ac20bb; uev2.embed_theme_preference=dark; utag_main__sn=1; utag_main_ses_id=1742875422222%3Bexp-session; utm_medium=undefined; utm_source=undefined; utag_main__ss=0%3Bexp-session; uev2.gg=true; _scid=4__45_VgeoCRlbtURTz3NBkEtGTNFkAQ; _gcl_au=1.1.42276734.1742875428; _tt_enable_cookie=1; _ttp=01JQ5QH16FPZQESQN158CGDAMP_.tt.1; _ga=GA1.1.1992587885.1742875428; _yjsu_yjad=1742875428.7b965ac2-116a-4f5c-b11f-c3221d5db51b; _clck=1oi2gkh%7C2%7Cfui%7C0%7C1910; uev2.loc=%7B%22address%22%3A%7B%22address1%22%3A%2240%20Fountain%20Ave%22%2C%22address2%22%3A%22Middletown%2C%20CT%22%2C%22aptOrSuite%22%3A%22%22%2C%22eaterFormattedAddress%22%3A%2240%20Fountain%20Ave%2C%20Middletown%2C%20CT%2006457-3111%2C%20US%22%2C%22subtitle%22%3A%22Middletown%2C%20CT%22%2C%22title%22%3A%2240%20Fountain%20Ave%22%2C%22uuid%22%3A%22%22%7D%2C%22latitude%22%3A41.55184%2C%22longitude%22%3A-72.65923%2C%22reference%22%3A%22here%3Aaf%3Astreetsection%3AipvJbd8MwPfQs1PrxJRprB%3ACggIBCCvhpfJAxABGgI0MA%22%2C%22referenceType%22%3A%22here_places%22%2C%22type%22%3A%22here_places%22%2C%22addressComponents%22%3A%7B%22city%22%3A%22Middletown%22%2C%22countryCode%22%3A%22US%22%2C%22firstLevelSubdivisionCode%22%3A%22CT%22%2C%22postalCode%22%3A%2206457-3111%22%7D%2C%22categories%22%3A%5B%22address_point%22%5D%2C%22originType%22%3A%22user_autocomplete%22%2C%22source%22%3A%22manual_auto_complete%22%2C%22userState%22%3A%22Unknown%22%7D; _ScCbts=%5B%5D; _sctr=1%7C1742875200000; uev2.diningMode=DELIVERY; jwt-session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InNsYXRlLWV4cGlyZXMtYXQiOjE3NDI4ODAyNjUyNzB9LCJpYXQiOjE3NDI4NzU0MTcsImV4cCI6MTc0Mjk2MTgxN30.v7wp_kz0VDfHDUmgkoQtEVKLpFzZiA4eU4YuJsiLXnc; utag_main__pn=5%3Bexp-session; _scid_r=_3_45_VgeoCRlbtURTz3NBkEtGTNFkAQACQEdg; _userUuid=; u-cookie-prefs=eyJ2ZXJzaW9uIjoxMDAsImRhdGUiOjE3NDI4Nzg0NzEyNzQsImNvb2tpZUNhdGVnb3JpZXMiOlsiYWxsIl0sImltcGxpY2l0Ijp0cnVlfQ%3D%3D; _ga_P1RM71MPFP=GS1.1.1742875428.1.1.1742878476.60.0.0; utag_main__se=28%3Bexp-session; utag_main__st=1742880294086%3Bexp-session; _uetsid=271dc560092e11f0868ee3a1f7ce527a; _uetvid=271e13e0092e11f091b2751f2d5a0bbd; marketing_vistor_id=40b88d68-8fb4-4f72-80bd-0f91d4ac20bb; uev2.embed_theme_preference=dark; uev2.id.session=353ea08f-3998-4d3c-90fe-515211a93739; uev2.ts.session=1742875417590; jwt-session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InNsYXRlLWV4cGlyZXMtYXQiOjE3NDI5MTYzODAwNjR9LCJpYXQiOjE3NDI4NzU0MTcsImV4cCI6MTc0Mjk2MTgxN30.Er2rFMtwIMbXbJVgT0BM0wIMg_mFYyoLKpWZOqWbrRs',
    'origin': 'https://www.ubereats.com',
    'priority': 'u=1, i',
    'referer': f'https://www.ubereats.com{store_url}',
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
    data = response.json()['data']
    for category in menu_categories:
        for item in data['catalogSectionsMap'][uuid][menu_categories.index(category)]['payload']['standardItemsPayload']['catalogItems']:
            try:
                menu_items[item['titleBadge']['text']] = item['itemDescriptionBadge']['text']
            except KeyError:
                menu_items[item['titleBadge']['text']] = "No description"

    return menu_items
        


# stores = search_restaurants("Thai")
# #now to take a random store, get the keys of the stores dictionary
# random_store = list(stores.keys())[0]
# step1 = get_menu_categories(stores[random_store][1], stores[random_store][0])
# step2 = get_menu_category_items(stores[random_store][1], step1[1], stores[random_store][0], step1[0])
