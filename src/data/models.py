import pandas
import numpy as np

class DataUtils(object):
    def __init__(self, dataframe: pandas.DataFrame):
        if dataframe is None or dataframe.empty:
            raise ValueError("You need to pass a non-empty pandas DataFrame.")
        self._dataframe = dataframe
        self._columns = self._dataframe.columns.to_list()
        self._columns_total = len(self._columns)
    
    """
        Get subdataframe in range the rows and the columns (eliminating some)
    """
    def get_subdataframe(self, df: pandas.DataFrame, m_range: tuple, n_range: tuple, rm_na_cols=True) -> pandas.DataFrame:
        new = df.loc[m_range[0] : m_range[1]] 
        new.drop([x for x in self._columns[n_range[0]:n_range[1]]], axis=1, inplace=True)
        if rm_na_cols:
            return new.dropna(axis=1, how='all')
        return new
    
    def rename_columns(self, names: dict) -> None:
        self._dataframe.rename(columns=names, inplace=True)
        self._columns = self._dataframe.columns
    
    # DataFrame
    @property # Getter
    def dataframe(self) -> pandas.DataFrame:
        return self._dataframe
    
    @dataframe.setter
    def dataframe(self, dataframe: pandas.DataFrame):
        if not dataframe:
            raise ValueError("Dataframe can`t be empty")
        self._dataframe = dataframe
        
    @property
    def columns(self) -> list:
        return self._columns.to_list()
    
    def check_null_columns(self) -> list:
        null: list = []
        for column in self._dataframe.columns:
            if self._dataframe[column].isnull().all():
                null.append(column)
        return null
    
    def fill_null_values(self, fill_with: any):
        for column in self._dataframe.columns:
            if self._dataframe[column].isnull().any():
                if str(column) == 'Age (Ma)':
                    self._dataframe[column].fillna(0, inplace=True)
                self._dataframe[column].fillna(fill_with, inplace=True)
    
    def remove_columns_except(self, keep: str):
        for column in self._dataframe.columns:
            if column != keep:
                self._dataframe = self._dataframe.drop(column, axis=1)
    
    def rename_one_column(self, old_name: str, new_name: str):
        if old_name or new_name:
            self._dataframe = self._dataframe.rename(columns={old_name : new_name})
        else:
            raise ValueError("You need to set a new name for column and expecify the old name.")
    
    def remove_row(self, index: int):
        self._dataframe = self._dataframe.drop(index, axis=0)
        
    # Data validation
    # In case of NaN values irregular distribution
    def validate_data(self, **kwargs):
        for _, v in kwargs.items():
            if 'median' in v:
                    self._dataframe = self._dataframe.fillna(self._dataframe.mean())
            elif 'linear' in v:
                self._dataframe = self._dataframe.interpolate(method='linear')
            else:
                raise ValueError("You need to choose a valid method.")

# Data model for Eon
class Eon(DataUtils):
    def __init__(self, m_range: tuple, n_range: tuple, dataframe: pandas.DataFrame):
        super().__init__(dataframe)
        self._m_range = m_range
        self._n_range = n_range
        self._dataframe = self.get_subdataframe(dataframe, m_range, n_range)
        self._name = str()
        self._columns = self._dataframe.columns
        self._age = float()
        self._type = str()
        
    @property 
    def type(self) -> str:
        if self._type == "" or not self._type:
            raise ValueError("type is empty.")
        return self._type
    
    @type.setter
    def type(self, type: str) -> None:
        if not type:
            raise ValueError("type is empty.")
        self._type = type
    
    # Name
    @property # Getter
    def name(self) -> str:
        if self._name == "" or not self._name:
                raise ValueError("name is empty.")
        return self._name
    
    @name.setter
    def name(self, name: str) -> None:
        if not name:
            raise ValueError("name is empty.")
        self._name = name
    
    # Age
    @property
    def age(self) -> float:
        if not self._age:
            raise ValueError("Age not set.")
        return self._age
    
    # Setter for the age
    def set_age(self, root_type: str):
        for column in self._dataframe.columns:
            if 'Age' in column:
                num = self._dataframe.at[self._dataframe.index[-1], column] # -1 pega a ultima linha
                if type(num) == str:
                    num = num.split()

                if '±' in str(num):
                    if root_type == '+':
                        num = float(num[0]) + float(num[2])
                    elif root_type == '-':
                        num = float(num[0]) - float(num[2])
                    else:
                        num = float(num[0])
                elif '~' in str(num):
                    num = self._dataframe[column][self._m_range[1]].split('~')[1]
                else:
                    pass     
        self._age = float(num)
    
    @staticmethod
    def clean_age(age):
        if isinstance(age, str):
            age = age.replace('~', '').replace('±', '').split()[0]
        try:
            return float(age)
        except ValueError:
            return np.nan