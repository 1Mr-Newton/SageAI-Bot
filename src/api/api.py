import requests
from src.constants.headers import default_headers
from src.constants.urls import openai_site_url, openai_token_url


def get_oai_did() -> str | None:
    session = requests.Session()
    response = session.get(openai_site_url, headers=default_headers)
    oai_did = response.cookies.get("oai-did")
    return oai_did


def get_chat_token(oai_did: str) -> str | None:
    print("Oai did", oai_did)
    session = requests.Session()
    default_headers["oai-device-id"] = oai_did
    response = session.post(openai_token_url, headers=default_headers)
    if response.status_code != 200:
        print(response.text)
        return
    token = response.json().get("token")
    return token
