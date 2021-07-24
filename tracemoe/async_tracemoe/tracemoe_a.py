from __future__ import annotations

import asyncio
import aiohttp
from typing import Optional, Union

from async_tracemoe_response import AsyncTraceMoeResponse
from async_tracemoe_errors import (
    InvalidURL, 
    Ratelimited, 
    ConcurrencyOrRatelimit, 
    InvalidAPIKey,
)

class AsyncTraceMoe:

    def __init__(self, *, token:Optional[str]=None, session:Optional[aiohttp.ClientSession]=None) -> None:
        self.token = token
        self._error_dict = {
            429:Ratelimited("To many HTTP requests, you are blocked from accessing the trace.moe api for 60 minutes."),
            402:ConcurrencyOrRatelimit("Max concurrency of use reached or you have been ratelimited."),
            403:InvalidAPIKey("The API key provided was invalid."),
            400:InvalidURL(f'Invalid image url'),
        }
        self.session = session or aiohttp.ClientSession()
    
    async def __aenter__(self) -> AsyncTraceMoe:
        return self

    async def __aexit__(self) -> None:
        await self.close()
    
    async def close(self) -> None:
        await self.session.close()
    
    async def url_search(
        self, 
        url:str, *, 
        anilist_id:Optional[int]=None, 
        cut_borders:Optional[bool]=False,
    ) -> AsyncTraceMoeResponse:
        base_url = "https://api.trace.moe/search?"

        if anilist_id is not None:
            base_url+=f"anilistID={anilist_id}"

        if cut_borders:
            check = f"&cutBorders&" if anilist_id is not None else f"cutBorders&"
            base_url+=check
        
        base_url+=f"url={url}"
        
        headers:Union[dict[str, str], dict[str, None]] = {"x-trace-key":self.token} if self.token is not None else {"x-trace-key":None}
        async with self.session.get(base_url, headers=headers) as r:
            if r.status in range(200,300):
                data = await r.json()
                return AsyncTraceMoeResponse(data)
            else:
                raise self._error_dict.get(r.status, r.raise_for_status()) # May change raise_for_status()

    async def me(self) -> dict:
        base_url = "https://api.trace.moe/me"
        
        headers:Union[dict[str, str], dict[str, None]] = {"x-trace-key":self.token} if self.token is not None else {"x-trace-key":None}

        async with self.session.get(base_url, headers=headers) as r:
            if r.status in range(200,300):
                data = await r.json()
                return data
            else:
                raise self._error_dict.get(r.status, r.raise_for_status())

    async def image_upload(self, *, e_file:str) -> AsyncTraceMoeResponse:
        base_url = "https://api.trace.moe/search"

        headers:Union[dict[str, str], dict[str, None]] = {"x-trace-key":self.token} if self.token is not None else {"x-trace-key":None}
        async with self.session.post(
            base_url, files={
            "image":open(e_file, 'rb')
            }, 
            headers=headers
        ) as r:
            if r.status in range(200,300):
                data = await r.json()
                return AsyncTraceMoeResponse(data)
            else:
                raise self._error_dict.get(r.status, r.raise_for_status())
