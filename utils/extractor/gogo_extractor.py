from bs4 import BeautifulSoup as bs
from Cryptodome.Cipher import AES
import base64
import json
import yarl
import requests

s = b"37911490979715163134003223491201"
s_2 = b"54674138327930866480207815084989"
iv = b"3134003223491201"


async def get_crypto(session, url):
    """
    function to get crypto data
    """
    async with session.get(url) as resp:
        soup = bs(await resp.read(), "html.parser")
    for item in soup.find_all(
        "script", attrs={"data-name": "episode", "data-value": True}
    ):
        crypto = str(item["data-value"])
    return crypto


def pad(data):
    """
    helper function
    """
    return data + chr(len(data) % 16) * (16 - len(data) % 16)


def decrypt(key, data):
    """
    function to decrypt data
    """
    return AES.new(key, AES.MODE_CBC, iv=iv).decrypt(base64.b64decode(data))


async def get_m3u8(session, link):
    crypto_data = await get_crypto(session, link)
    decrypted_crypto = decrypt(s, crypto_data)
    new_id = (
        decrypted_crypto[decrypted_crypto.index(b"&") :]
        .strip(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10")
        .decode()
    )
    p_url = yarl.URL(link)
    ajax_url = f"https://{p_url.host}/encrypt-ajax.php"

    encrypted_ajax = base64.b64encode(
        AES.new(s, AES.MODE_CBC, iv=iv).encrypt(pad(p_url.query.get("id")).encode())
    )

    async with session.get(
        f'{ajax_url}?id={encrypted_ajax.decode()}{new_id}&alias={p_url.query.get("id")}',
        headers={"x-requested-with": "XMLHttpRequest"},
    ) as resp:
        x = (await resp.text()).strip('{"data":" ')

    j = json.loads(
        decrypt(s_2, x).strip(
            b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10"
        )
    )
    if j.get("advertising") is not None:
        del j["advertising"]
    if j.get("linkiframe") is not None:
        del j["linkiframe"]
    return j
