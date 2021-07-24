from __future__ import annotations

from typing import Optional, Union

import requests

from sync_tracemoe_errors import (
    InvalidURL, 
    Ratelimited, 
    ConcurrencyOrRatelimit, 
    InvalidAPIKey,
)

from tracemoe_response import TraceMoeResponse


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
    ) -> TraceMoeResponse:
        base_url = "https://api.trace.moe/search?"

        if anilist_id is not None:
            base_url+=f"anilistID={anilist_id}"

        if cut_borders:
            check = f"&cutBorders&" if anilist_id is not None else f"cutBorders&"
            base_url+=check
        
        base_url+=f"url={url}"
        
        headers:Union[dict[str, str], dict[str, None]] = {"x-trace-key":self.token} if self.token is not None else {"x-trace-key":None}
        response = requests.get(base_url, headers=headers)

        if response.status_code in range(200,300):
            return TraceMoeResponse(response.json())
        else:
            raise self._error_dict.get(response.status_code, response.raise_for_status())

    @property
    def me(self) -> dict:
        base_url = "https://api.trace.moe/me"
        
        headers:Union[dict[str, str], dict[str, None]] = {"x-trace-key":self.token} if self.token is not None else {"x-trace-key":None}

        resp = requests.get(base_url, headers=headers)

        if resp.status_code in range(200,300):
            return resp.json()
        else:
            raise self._error_dict.get(resp.status_code, resp.raise_for_status())

    def image_upload(self, *, e_file:str) -> TraceMoeResponse:
        base_url = "https://api.trace.moe/search"

        headers:Union[dict[str, str], dict[str, None]] = {"x-trace-key":self.token} if self.token is not None else {"x-trace-key":None}

        r = requests.post(base_url, files={"image":open(e_file, "rb")}, headers=headers)
        if r.status_code in range(200,300):
            return TraceMoeResponse(r.json())
        else:
            raise self._error_dict.get(r.status_code, r.raise_for_status())
