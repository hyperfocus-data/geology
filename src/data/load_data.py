import pandas as pd
import re

class LoadData(object):
    def __init__(self, path: str) -> None:
        if not path:
            raise ValueError("Path must be filled.")
        self._path = path
        self._START_INDEX = int
        self._END_INDEX = int
        
    # Getter
    @property
    def path(self) -> str:
        return self._path
        
    def load(self) -> pd.DataFrame:
        return pd.read_excel(self._path)
    