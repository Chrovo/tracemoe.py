from __future__ import annotations

import json
import re
import urllib
from typing import Optional, Union

import requests

from ..sync_tracemoe_errors import (
    InvalidURL,
    TraceMoeError,
)
from ..tracemoe_response import TraceMoeResponse

class TraceMoe:

    def __init__(self, *, token:Optional[str]) -> None:
        self.token = token

    def pic_to_url(
        self, url:str, *, 
        anilist_id:Optional[int]=None, 
        cut_borders:Optional[bool]=False,
    ) -> TraceMoeResponse: # Add api token stuff later
        base_url = "https://api.trace.moe/search?"

        if anilist_id is not None:
            base_url+=f"anilistID={anilist_id}"

        if cut_borders is not None:
            check = f"&cutBorders&" if anilist_id is not None else f"cutBorders&"
            base_url+=check
        
        base_url+=f"url={url}"
        response = requests.get(base_url)
        if response.ok:
            return TraceMoeResponse(response.json())
        elif response.status_code == 400:
            raise InvalidURL(f'Invalid URL "{url}" provided.')
        else:
            pass # Add more exceptions later.