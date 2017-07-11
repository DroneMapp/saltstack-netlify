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


def patch(path, data):
    global BASE_URL
    global TOKEN
    url = os.path.join(BASE_URL, path + '?access_token={}'.format(TOKEN))
    return requests.patch(url, data)


def aliases_present(name, access_token, site_id, aliases):
    global TOKEN
    TOKEN = access_token

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
    current_aliases = set(response_data['domain_aliases'])
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
    response = patch(site_path, {"domain_aliases": list(updated_aliases)})
    try:
        response.raise_for_status()
    except HTTPError as ex:
        return {
            "name": name,
            "changes": {"changes": None},
            "comment": "{} ({})".format(ex, ex.response.content),
            "result": False
        }

    return {
        "name": name,
        "comment": "{} new aliases created".format(len(new_aliases)),
        "changes": {"subdomain aliases created": list(new_aliases)},
        "result": True
    }
