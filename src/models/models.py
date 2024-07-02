import pandas
import warnings
from dataclasses import dataclass

#@dataclass
#class DataFrame:
    #dataframe: pandas.DataFrame
    #columns: list
    #size: int

# Data model for Eon
class Eon:
    
    def __init__(self, dataframe: pandas.DataFrame):
        if dataframe is None or dataframe.empty:
            raise ValueError("You need to pass a non-empty pandas DataFrame.")
        self._dataframe = dataframe
        self._name = str()
        self._number_of_eras = int()
        self._duration = float()
        self._eras = list()
        self._start_index = int()
        self._end_index = int()
        
    # Set DataFrame
    @property
    def dataframe(self) -> pandas.DataFrame:
        return self._dataframe
    
    @dataframe.setter
    def dataframe(self, datafrane: pandas.DataFrame):
        if not datafrane:
            raise ValueError("Dataframe can`t be empty")
        self._dataframe = datafrane
    
    # Name of Eon
    @property # Getter
    def name(self) -> str:
        if not self._name:
            raise ValueError("name is empty.")
        return self._name
    
    @name.setter
    def set_name(self, name: str) -> None:
        if not name:
            raise ValueError("name is empty.")
        self._name = name

    # Number of Eras in Eon
    def set_number_of_eras(self, num_eras: int) -> None:
        self._number_of_eras = num_eras
        
    def get_number_of_eras(self) -> int:
        return self._number_of_eras
    
    # Eon duration
    def set_duration(self, duration: float) -> None:
         self._duration = duration
         
    def get_duration(self) -> float:
        return self._duration
    
    # Eras
    def set_eras(self, eras: list) -> None:
        self._eras = eras
    
    def get_eras(self) -> list:
        return self._eras
    
    # Start index of Eon in DF
    def set_indexes(self, start: int, end: int) -> None:
        self._start_index = start
        self._end_index = end
        
    def get_indexes(self) -> tuple:
        return tuple(self._start_index, self._end_index)
    