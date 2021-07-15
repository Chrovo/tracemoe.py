from __future__ import annotations

import json
import re
import urllib
from typing import Optional, Union

import requests

from ..sync_tracemoe_errors import (
    ConcurrencyOrRatelimit,
    TraceMoeError,
)
from ..tracemoe_response import TraceMoeResponse

class TraceMoe:

    def __init__(self, *, token:Optional[str]) -> None:
        self.token = token

    def pic_to_url(self, url:str) -> TraceMoeResponse:
        pass #Do later