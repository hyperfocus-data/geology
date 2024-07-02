"""
Title: Duration of geological eras with their respective periods
By: Caio Madeira

"""
import numpy as np
import pandas as pd
import re
from model.models import Eon, DataFrame

pd.options.mode.chained_assignment = None # hide warnings

path = "collections/Geological_Event_Chart.xlsx"
df = pd.read_excel(path)

PRECAMBRIAN_START_INDEX = 121
PRECAMBRIAN_END_INDEX = len(df)

PHANEROZOIC_START_INDEX = 1
PHANEROZOIC_END_INDEX = PRECAMBRIAN_START_INDEX - 1

DF_END_INDEX = len(df)


UNNAMED: dict = {
    'Geological Time':'Eon',
    'Unnamed: 1':'Eras',
    'Unnamed: 2':'System',
    'Unnamed: 3': 'NaN',
    'Unnamed: 4':'Series/Epoch',
    'Unnamed: 5':'Sub-series', # Has values
    'Unnamed: 6':'Stage',
    'Unnamed: 7':'Sub-stage',
    'Unnamed: 8':'Sub-substage', # Has values
    'Unnamed: 9':'Age (Ma)',
}

def select_valid_columns(df: pd.DataFrame) -> list:
    valid: list = []
    check_null = df.loc[0].isnull()
    for k, v in check_null.to_dict().items():
        if not v:
            valid.append(k)
    return valid            

def column_isempty(column_name: str, df: pd.DataFrame) -> bool:
    nan_sum = df[column_name].isnull().sum()
    if nan_sum >= 140:
        return True
    else:
        return False

def rm_nan_columns(df: pd.DataFrame) -> tuple:
    invalids = [11, 15, 21]
    columns = select_valid_columns(df)
    for name in columns:
        if column_isempty(name, df):
            columns.remove(str(name))
            
    # second
    for name in columns:
        for index in invalids:
            if str(index) in name:
                columns.remove(name)
    # third
    for name in columns:
        if not 'Unnamed' in name and name != 'Geological Time':
            columns.remove(name)
    
    #fourth
    last_element = columns[len(columns) - 1]
    if str(17) in last_element:
       columns.remove(last_element)
    
    columns_indexes = []
    #fifth
    for name in columns:
        try:
            if name == 'Geological Time':
                index = 0
            else:
                index = int(re.search(r'\d+', name).group())
        except AttributeError:
            index = 0
        columns_indexes.append(index)    
    return (columns_indexes, columns)

def get_categories(target_indexes: tuple, df: pd.DataFrame) -> list:
    categories: list = []
    info = dict(zip(target_indexes[1], target_indexes[0]))
    categories_cols = df.loc[info['Geological Time']]
    for i in range(0, 10):
        if not pd.isna(categories_cols.iloc[i]):
            categories.append([i, categories_cols.iloc[i]]) # get pos
    return categories

def get_data_from(category: list, df: pd.DataFrame):
    count = 0
    result = []
    index = category[0]
    info_by_index = df.iloc[index].dropna()
    for k, v in info_by_index.items():
        count = count + 1
        result.append([count, k, v])
        if count == 7:
            break
    return result

def get_subdata_from(subcategory: list, df: pd.DataFrame):
    row: list = []
    item_index = df[subcategory[0][1]]
    for i, v in item_index.items():
        try:
            if v == 'More Info' or 'J.M. Pellé' in v or 'Chronostratigraphic' in v:
                pass
            else:
                row.append([i, v])
        except TypeError:
            v = str(v)
    return row

def create_scope(start_index: int, end_index: int, df: pd.DataFrame, start_col=10, end_col=23, showinfo=True):
    invalid_columns: list = []
    scope = df.loc[start_index: end_index]
    for i in range(start_col, end_col):
        invalid_columns.append(scope.columns[i])
    
    # remove invalid columns
    for columns in invalid_columns:
        scope.drop(columns, axis=1, inplace=True)
    
    if showinfo:
        print("NEW SCOPE INFO")
        print("numbers of columns: ", len(scope.columns))
        print("numbers of rows: ", len(scope))
        print("number of elements: ", scope.size)
        print("valid START index: ", scope.first_valid_index())
        print("valid LAST index: ", scope.last_valid_index())
        print("===========================================")
    return scope

def get_categories_list(df: pd.DataFrame) -> list:
    target_indexes = rm_nan_columns(df)
    categories = get_categories(target_indexes, df)
    return categories

def get_eon_df(eon: str, df: pd.DataFrame, showinfo=False) -> pd.DataFrame:
    
    target_indexes = rm_nan_columns(df)
    categories = get_categories(target_indexes, df)
    eon_category = get_data_from(category=categories[1], df=df)
    row = get_subdata_from(eon_category, df)

    # Getting data from row
    PHANEROZOIC_START_INDEX = row[1][0]
    PRECAMBRIAN_START_INDEX = row[2][0]
    DF_END_INDEX = len(df)
    
    if (eon == 'PHANEROZOIC'):
        # Phanerozoic configurations
        phanerozoic_scope = create_scope(PHANEROZOIC_START_INDEX, PRECAMBRIAN_START_INDEX - 1, df, showinfo=showinfo)
        return phanerozoic_scope
    elif (eon == 'PRE-CAMBRIAN' or eon == 'PRECAMBRIAN'):
        # Pre-Cambrian configurations
        precambrian_scope = create_scope(PRECAMBRIAN_START_INDEX, DF_END_INDEX, df, showinfo=showinfo)
        return precambrian_scope
    else:
        raise ValueError("Invalid name of Eon. Try PHANEROZOIC or PRE-CAMBRIAN.")

def get_eon_info(eon_df: pd.DataFrame, EON_START_INDEX, EON_END_INDEX):
    all_data: list = []
    data: dict = {}
    count = 0
    #PHANEROZOIC_END_INDEX = 26
    #for i in range(1, PHANEROZOIC_END_INDEX): # for columns
    for i in range(EON_START_INDEX, EON_END_INDEX): # for columns
        new_df =  eon_df.loc[i].dropna()
        count += 1
        for key, value in new_df.to_dict().items():
            if count == 1:
                data[UNNAMED[str(key)] + '_key'] = [{UNNAMED[str(key)] : [count, value]}]
            else:
                try:
                    data[UNNAMED[str(key)] + '_key'] += [{UNNAMED[str(key)] : [count, value]}]
                except KeyError:
                    data[UNNAMED[str(key)]+ '_key'] = [{UNNAMED[str(key)] : [count, value]}]
    all_data.append(data)
    return all_data

def get_era_indexes(eon_info: str):
    eon_type = eon_info[0]['Eon_key'][0]['Eon'][1]

    data: dict = {}

    if eon_type == 'Phanerozoic':
        data['Cenozoic'] = [1, 24]
        data['Mesozoic'] = [25, 54]
        data['Paleozoic'] = [55, 120]
    elif eon_type == 'Pre-Cambrian':
        data['Proterozoic'] = [1, 130]
        data['Archean'] = [131, 134]
        data['Hadean'] = [135, 137]    
                    
    return data

def get_era_df(eon_info: list, eon_df: pd.DataFrame, era_name: str, drop_null_columns=True, rename_columns=True, drop_custom_columns=None) -> pd.DataFrame:
    era_index: dict = get_era_indexes(eon_info)
    era_df = create_scope(era_index[era_name][0], era_index[era_name][1], eon_df, start_col=0, end_col=0, showinfo=False)
    if drop_null_columns:
        null_columns_dict = era_df.isnull().all().to_dict()
        for c, is_null in null_columns_dict.items():
            if is_null == True:
                era_df.drop(c, axis=1, inplace=True)
    if rename_columns:
        for old_name, new_name in UNNAMED.items():
            era_df.rename(columns={str(old_name) : str(new_name)}, inplace=True)

        if drop_custom_columns != None : # Reduntant columns = Eon and Eras column
            for col in drop_custom_columns:
                try:
                    era_df.drop(col, axis=1, inplace=True)
                except KeyError:
                    pass

    return era_df

@DeprecationWarning
def age_sum(df: pd.DataFrame, root_type=None) -> float:
    all_ages: list = []
    for age in df['Age (Ma)'].dropna():
        if '±' in str(age):
            age_splited = age.split()
            if root_type == '+':
                all_ages.append(float(age_splited[0]) + float(age_splited[2]))
            elif root_type == '-':
                all_ages.append(float(age_splited[0]) - float(age_splited[2]))
            else:
                all_ages.append(float(age_splited[0]))
        elif '~' in str(age):
            #print(age.split('~'))
            all_ages.append(float(age.split('~')[1]))
        else:
            all_ages.append(age)
    
    #print("ages:", all_ages)
    new_list = [float(i) for i in all_ages]
    
    return '~' + str(sum(new_list))

def era_age(df: pd.DataFrame, root_type=None):
    ages: list = []
    index = 0
    for age in df['Age (Ma)'].dropna():
        index += 1
        ages.append(age)
    
    last_age = ages[-1]
    if '±' in str(last_age):
        last_age = last_age.split()
        if root_type == '+':
            last_age = float(last_age[0]) + float(last_age[2])
        elif root_type == '-':
            last_age = float(last_age[0]) - float(last_age[2])
        else:
            last_age = float(last_age[0])
            
    elif '~' in str(last_age):
        last_age = last_age.split("~")[1]
    else: 
        pass
    return float(last_age)    
def get_era_age(df: pd.DataFrame, eon: str, root_type=None, show_info=False) -> tuple:
    
    if (eon == "PHANEROZOIC"):
        phanarezoic_info = get_eon_info(df, PHANEROZOIC_START_INDEX, PHANEROZOIC_END_INDEX)
        cenozoic_df = get_era_df(eon_info=phanarezoic_info, eon_df=df, era_name='Cenozoic', drop_custom_columns=['Eon', 'Eras'])
        mesozoic_df = get_era_df(eon_info=phanarezoic_info, eon_df=df, era_name='Mesozoic', drop_custom_columns=['Eon', 'Eras'])
        paleozoic_df = get_era_df(eon_info=phanarezoic_info, eon_df=df, era_name='Paleozoic', drop_custom_columns=['Eon', 'Eras'])
        # Geochronometry is the field of geochronology that numerically quantifies geologic time.[12]
        
        # Ma - 1 milhao de anos // Ka (Kilo annum) - mil anos
        #print(">> cenozoic ages:\n", cenozoic_df['Age (Ma)'].sum()) # Ma - 1 milhao de anos // Ka (Kilo annum) - mil anos // Ga - Bilhoes de anos
        #print(">> mesozoicages:\n", mesozoic_df['Age (Ma)'].sum())
        # root_type can be '+', '-' or None
        cenozoic_age = era_age(df=cenozoic_df, root_type=root_type)
        mesozoic_age = era_age(df=mesozoic_df, root_type=root_type)
        paleozoic_age = era_age(df=paleozoic_df, root_type=root_type)
        
        if show_info:
            print(f"Cenozoic age (root type= '{root_type}'): ", str(cenozoic_age) + ' Million(s) years ago')
            print(f"Mesozoic age (root type= '{root_type}'): ", str(mesozoic_age) + ' Million(s) years ago')
            print(f"Paleozoic age (root type= '{root_type}'): ", str(paleozoic_age) + ' Million(s) years ago')
        return { 'Cenozoic': cenozoic_age, 'Mesozoic': mesozoic_age, 'Paleozoic': paleozoic_age }

    elif (eon == "PRECAMBRIAN"):
        precambrian_info = get_eon_info(df, PRECAMBRIAN_START_INDEX, PRECAMBRIAN_END_INDEX)
        proterozoic_df = get_era_df(eon_info=precambrian_info, eon_df=df, era_name='Proterozoic', drop_custom_columns=['Eon', 'Eras'])
        archean_df = get_era_df(eon_info=precambrian_info, eon_df=df, era_name='Archean', drop_custom_columns=['Eon', 'Eras'])
        hadean_df = get_era_df(eon_info=precambrian_info, eon_df=df, era_name='Hadean', drop_custom_columns=['Eon', 'Eras'])
        
        proterozoic_age = era_age(df=proterozoic_df, root_type=root_type)
        archean_age = era_age(df=archean_df, root_type=root_type)
        hadean_age = era_age(df=hadean_df, root_type=root_type)
        
        if show_info:
            print(f"Proterozoic age (root type= '{root_type}'): ", str(proterozoic_age) + ' Million(s) years ago')
            print(f"Archean age (root type= '{root_type}'): ", str(archean_age) + ' Million(s) years ago')
            print(f"Hadean age (root type= '{root_type}'): ", str(hadean_age) + ' Million(s) years ago')
        
        return { 'Proterozoic': proterozoic_age, 'Archean': archean_age, 'Hadean': hadean_age }
    
    else:
        raise TypeError("Invalid by_eron name.")


#phanerozoic_df = get_eon_df(eon='PHANEROZOIC', df=df)
#precambrian_df = get_eon_df(eon='PRECAMBRIAN', df=df)
#print(get_era_age(by_eron='PHANEROZOIC', root_type='+'))
#print(get_era_age(by_eron='PRECAMBRIAN', root_type='+'))
#name = eon.set_name("Phanerozoic")
#duration = eon.set_duration(233.0)
#print(eon.get_name())


df1 = get_eon_df(eon='PHANEROZOIC', df=df)


eon = Eon(df1)
eon.set_name = df1['Geological Time'][1]
print(eon.name)
