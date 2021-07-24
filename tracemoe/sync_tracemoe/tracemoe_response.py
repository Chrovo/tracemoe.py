from __future__ import annotations

from typing import Optional, Union


class TraceMoeResponse:

    def __init__(self, data:dict) -> None:
        self.data = data

    @property
    def error(self) -> str:
        return self.data['error'] # This will return '' if there is no error

    @property
    def frame_count(self) -> int:
        return self.data['frameCount']
    
    @property
    def results(self) -> dict:
        return self.data['result']
    
    def anilist(self, index:int) -> int:
        return self.data['result'][index]['anilist']

    def filename(self, index:int) -> str:
        return self.data['result'][index]['filename']

    def episode(self, index:int) -> Optional[Union[int, str, float]]:
        return self.data['result'][index]['episode']
    
    def from_sec(self, index:int) -> int:
        return self.data['result'][index]['from']

    def to(self, index:int) -> int:
        return self.data['result'][index]['to']
    
    def similarity(self, index:int) -> float:
        return self.data['result'][index]['similarity']
    
    def video(self, index:int) -> str:
        return self.data['result'][index]['video']
    
    def image(self, index:int) -> str:
        return self.data['result'][index]['image']