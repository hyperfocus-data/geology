import pandas as pd
import re
import os 
from dotenv import load_dotenv
from load_data import LoadData
from models import Eon, DataUtils

pd.options.mode.chained_assignment = None # hide warnings

load_dotenv()

UNNAMED: dict = {
    'Geological Time':'Eon',
    'Unnamed: 1':'Eras',
    'Unnamed: 2':'System',
    'Unnamed: 3':'NaN',
    'Unnamed: 4':'Series/Epoch',
    'Unnamed: 5':'Sub-series', # Has values
    'Unnamed: 6':'Stage',
    'Unnamed: 7':'Sub-stage',
    'Unnamed: 8':'Sub-substage', # Has values
    'Unnamed: 9':'Age (Ma)',
}

# Geological_Event_Chart.xlsx
data = LoadData(path=r'D:\GitHub\Hyperfocus\geology\data\raw\Geological_Event_Chart.xlsx')
df = data.load()

"""
Supereon: Pre-Cambrian
Eons: Phanerozoic, Proterozoic, Hadean and Archean

"""
# Super Eon
precambrian = Eon(dataframe=df, m_range=(121, 135), n_range=(10, 23))
precambrian.rename_columns(UNNAMED)
precambrian.name = 'Pre-cambrian'
precambrian.set_age('+')
precambrian.type = 'Supereon'

# Eons 
phanerozoic = Eon(dataframe=df, m_range=(df.first_valid_index(), 120), n_range=(10, 23))
phanerozoic.rename_columns(UNNAMED)
phanerozoic.name = 'Phanerozoic'
phanerozoic.set_age('+')
phanerozoic.type = 'Eon'

proterozoic = Eon(dataframe=df, m_range=(121, 130), n_range=(10, 23))
proterozoic.rename_columns(UNNAMED)
proterozoic.name = 'Proterozoic'
proterozoic.set_age('+')
proterozoic.type = "Eon"
#print("Dataframe: ", proterozoic.dataframe)
print("Name: ", proterozoic.name)
print("Type: ", proterozoic.type)
print("Age: ", proterozoic.age)

archean = Eon(dataframe=df, m_range=(131, 134), n_range=(10, 23))
archean.rename_columns(UNNAMED)
archean.name = "Archean"
archean.set_age('+')
archean.type = 'Eon'
#print("Dataframe: ", archean.dataframe)
print("Name: ", archean.name)
print("Type: ", archean.type)
print("Age: ", archean.age)

hadean = Eon(dataframe=df, m_range=(135, 135), n_range=(10, 23))
hadean.rename_columns(UNNAMED)
hadean.name = "Hadean"
hadean.set_age('+')
hadean.type = 'Eon'
#print("Dataframe: ", hadean.dataframe)
print("Name: ", hadean.name)
print("Type: ", hadean.type)
print("Age: ", hadean.age)