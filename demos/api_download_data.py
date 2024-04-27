"""
Example on how to automate downloading participation data using the meadows API

Look at oauth_oidc.sh for details on setting up authentication.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Dict
from pathlib import Path
from os.path import join
from time import sleep
import requests, pandas
from urllib.parse import quote
MEAD_URL = 'https://meadows-research.com/experiments/'


token = 'xyz'


name, version = 'myExp', '0'
url_safe_name = quote(name)
partions_url = join(MEAD_URL, url_safe_name, 'v', version, 'participations')
metadata_url = join(partions_url, 'exports', 'metadata')

sleep(1)
response = requests.get(
    metadata_url,
    headers=dict(
        Accept='application/json',
        Authorization=f'Bearer {token}'
    ),
    allow_redirects=False,
)
assert response.status_code == 200
content = response.json()
df = pandas.DataFrame(content)
selected = df[df.status=='finished'] # & df.include == True
n = len(selected)
data = dict()
for p, partion in selected.iterrows():
    sleep(2)
    partion_url = join(partions_url, partion['name'], 'exports', 'tree')
    response = requests.get(
        partion_url,
        headers=dict(
            Accept='application/json',
            Authorization=f'Bearer {token}'
        ),
        allow_redirects=False,
    )
    assert response.status_code == 200
    data[partion['name']] = response.json()

