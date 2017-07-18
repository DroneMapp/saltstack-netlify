import os.path

import requests
from requests.exceptions import HTTPError

BASE_URL = 'https://api.netlify.com/api/v1'
TOKEN = 'NO_TOKEN_SET'


def get(path):
    global BASE_URL
    global TOKEN

    url = os.path.join(BASE_URL, path + '?access_token={}'.format(TOKEN))
    return requests.get(url)


def put(path, data):
    global BASE_URL
    global TOKEN
    url = os.path.join(BASE_URL, path + '?access_token={}'.format(TOKEN))
    return requests.put(url, json=data)

def get_current_aliases(site_id, access_token):
    site_path = 'sites/{}'.format(site_id)
    response = get(site_path)
    try:
        response.raise_for_status()
    except HTTPError as ex:
        return {
            "name": name,
            "changes": {"changes": None},
            "comment": "{} ({})".format(ex, ex.response.content),
            "result": False
        }

    response_data = response.json()
    return set(response_data['domain_aliases'])


def aliases_present(name, access_token, site_id, aliases):
    global TOKEN
    TOKEN = access_token

    site_path = 'sites/{}'.format(site_id)

    current_aliases = get_current_aliases(site_id, access_token)
    updated_aliases = set(current_aliases)

    for alias_name in aliases:
        updated_aliases.add(alias_name)

    if updated_aliases == current_aliases:
        return {
            "name": name,
            "comment": "No new aliases created",
            "changes": {"changes": None},
            "result": True
        }

    new_aliases = updated_aliases - current_aliases

    success_return = {
        "name": name,
        "comment": "{} new aliases created".format(len(new_aliases)),
        "changes": {"subdomain aliases created": list(new_aliases)},
        "result": True
    }

    payload = {"domain_aliases": list(updated_aliases)}
    response = put(site_path, payload)
    try:
        response.raise_for_status()
    except HTTPError as ex:
        try:
            new_current_aliases = get_current_aliases(site_id, access_token)
        except:
            pass
        else:
            if new_current_aliases == updated_aliases:
                success_return['changes']['status_code'] = response.status_code
                return success_return

        return {
            "name": name,
            "changes": {"changes": None},
            "comment": "{} ({}) : {}".format(ex, ex.response.content, payload),
            "result": False
        }

    return success_return
