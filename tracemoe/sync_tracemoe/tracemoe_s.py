from __future__ import annotations

import json
import re
import urllib
from typing import Optional, Union

import requests

from ..sync_tracemoe_errors import (
    InvalidURL,
    TraceMoeError,
    Ratelimited,
    ConcurrencyOrRatelimit,
    HTTPConnectionError,
    InvalidAPIKey
)
from ..tracemoe_response import TraceMoeResponse


class TraceMoe:

    def __init__(self, *, token:Optional[str]) -> None:
        self.token = token
        self._error_dict = {
            429:Ratelimited("To many HTTP requests, you are blocked from accessing the trace.moe api for 60 minutes."),
            402:ConcurrencyOrRatelimit("Max concurrency of use reached or you have been ratelimited."),
            403:InvalidAPIKey("The API key provided was invalid."),
            400:InvalidURL(f'Invalid image url'),
        }

    def url_search(
        self, url:str, *, 
        anilist_id:Optional[int]=None, 
        cut_borders:Optional[bool]=False,
    ) -> TraceMoeResponse: # Add api token stuff later
        base_url = "https://api.trace.moe/search?"

        if anilist_id is not None:
            base_url+=f"anilistID={anilist_id}"

        if cut_borders:
            check = f"&cutBorders&" if anilist_id is not None else f"cutBorders&"
            base_url+=check
        
        base_url+=f"url={url}"
        if self.token:
            base_url+=f"&key={self.token}"
        
        response = requests.get(base_url)

        if response.ok:
            return TraceMoeResponse(response.json())
        else:
            try:
                raise self._error_dict[response.status_code]()
            except KeyError:
                raise HTTPConnectionError(f"{response.status_code}: {response.reason}")

    @property
    def me(self) -> dict: # Add API key stuff later
        base_url = "https://api.trace.moe/me"
        
        if self.token:
            base_url+=f"?key={self.token}"
        resp = requests.get(base_url)

        if resp.ok:
            return resp.json()
        else:
            try:
                raise self._error_dict[resp.status_code]()
            except KeyError:
                raise HTTPConnectionError(f"{resp.status_code}: {resp.reason}")

    def image_upload(self, *, e_file:str) -> TraceMoeResponse: # Add API key stuff later
        base_url = "https://api.trace.moe/search"

        r = requests.post(
            base_url, files={
            "image":open(e_file, "rb")
        }
    )
        if r.ok:
            return TraceMoeResponse(r.json())
        else:
            try:
                raise self._error_dict[r.status_code]()
            except KeyError:
                raise HTTPConnectionError(f"{r.status_code}: {r.reason}")