import numpy as np
from dotenv import load_dotenv
from src.data.load_data import LoadData
from src.data.models import Eon, DataUtils
import pandas as pd

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

arbitrary_values = [0, -1, np.nan, 'Unknown']

# Super Eon
#precambrian = Eon(dataframe=df, m_range=(121, 135), n_range=(10, 23))
#precambrian.rename_columns(UNNAMED)
#precambrian.name = 'Pre-cambrian'
#precambrian.set_age('+')
#precambrian.type = 'Supereon'


# Eons 
def prepare_object(root_type: str, name: str, fillna=False, **kwargs):
    for key, value in kwargs.items():
        if 'eon' in key:
            value.rename_columns(UNNAMED)
            if name:
                value.name = name
            value.type = 'Eon'
            if fillna:
                value.fill_null_values(arbitrary_values[2])
            value.remove_columns_except('Age (Ma)')
            if name == 'Phanerozoic':
                value.remove_row(0) # Specific for phanerozoic
            value.set_age(root_type)
            value.rename_one_column(old_name='Age (Ma)', new_name=f'{value.name} Age (Ma)')
            
    
# Phanerozoic Eon
phanerozoic = Eon(dataframe=df, m_range=(df.first_valid_index(), 120), n_range=(10, 23))
prepare_object(root_type="+", eon=phanerozoic, name='Phanerozoic')

# Proterozoic Eon
proterozoic = Eon(dataframe=df, m_range=(121, 130), n_range=(10, 23))
prepare_object(root_type="+", eon=proterozoic, name='Proterozoic')

# Archean Eon
archean = Eon(dataframe=df, m_range=(131, 134), n_range=(10, 23))
prepare_object(root_type="+", eon=archean, name='Archean')

# Hadean Eon
hadean = Eon(dataframe=df, m_range=(135, 135), n_range=(10, 23))
prepare_object(root_type="+", eon=hadean, name='Hadean')

#data: dict = {phanerozoic.name: [phanerozoic.age],
              #proterozoic.name: [proterozoic.age],
              #archean.name: [archean.age],
              #hadean.name: [hadean.age]}

#df1 = pd.DataFrame(data)

#print(df1)

def clean_age(age):
    if isinstance(age, str):
        age = age.replace('~', '').replace('±', '').split()[0]
    try:
        return float(age)
    except ValueError:
        return np.nan

def clean_data(df: any):
    for column in df.columns:
        if 'Age' in column:
            df[column] = df[column].apply(clean_age)
            df.dropna(subset=[column], inplace=True)

clean_data(phanerozoic.dataframe)
clean_data(proterozoic.dataframe)
clean_data(archean.dataframe)
clean_data(hadean.dataframe)


phanerozoic.dataframe.reset_index(drop=True, inplace=True)
proterozoic.dataframe.reset_index(drop=True, inplace=True)
archean.dataframe.reset_index(drop=True, inplace=True)
hadean.dataframe.reset_index(drop=True, inplace=True)

"""
Substituir os dados ausentes (NaN) pela media eh uma tarefa vantajosa pois:
- Eh simples;
- Preserva o tamanho do conjunto de dados. Ao preencher os valores NaN, voce evita a exclusao de linhas inteiras,
preservando assim o tamanho do conjunto de dados original.
- A media da coluna permanece inalterada apos a imputacao, o que pode ser util em algumas analises estatisticas.
- Eh uma alternativa melhor que a exclusao completa, em muitos casos, preencher valores NaN com a media pode ser preferivel
a exclusao completa das linhas com NaN, especialmente quando os dados sao escassos.

DESVANTAGENS:

- Reduz a variabilidade dos dados, tornando-os menos representativos da realidade
- Pode introduzir um vies se os valores ausentes nao forem distribuidos aleatoriamente.
Por exemplo, se os NaN ocorrem mais frequentemente em certos intervalos de tempo ou 
grupos especificos.

- Preencher a media ignora a distruibuicao dos dados e a correlacao entre variaveis. Isso pode
afetar a performance de modelos que dependem dessas caracteristicas.

Preencher valores NaN com a média é uma técnica simples e frequentemente usada, mas não é isenta 
de desvantagens. Dependendo da natureza dos seus dados e do problema que você está tentando resolver,
outras técnicas de imputação podem ser mais apropriadas. Avalie cuidadosamente o impacto da imputação 
no desempenho do seu modelo e considere alternativas quando necessário.


A interpolação é uma técnica poderosa para preencher valores ausentes em dados contínuos, 
especialmente quando a mudança entre os pontos é suave e previsível. A interpolação linear é 
simples e eficaz na maioria dos casos, mas outras técnicas, como spline ou polinomial, podem 
ser mais adequadas dependendo da natureza dos dados.

"""

#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)

#df_eon_age = DataUtils(dataframe=df_combined)
# Usando interpolacao linear
# Estima os valores desconhecidos entre dois pontos conhecidos, assumindo que a mudança entre os pontos é linear.
    
# Usando interpolacao polinomial
# Usa polinômios para estimar valores. Pode ser mais precisa que a linear,
# mas também mais suscetível a oscilações se os dados forem complexos.


df_combined = pd.concat([phanerozoic.dataframe, proterozoic.dataframe, archean.dataframe, hadean.dataframe], axis=1)

eon_ages_origin = DataUtils(dataframe=df_combined)
eon_ages_linear = DataUtils(dataframe=df_combined)
eon_ages_median = DataUtils(dataframe=df_combined)

eon_ages_linear.validate_data(method='linear')
eon_ages_median.validate_data(method='median')
print("W/ LINEAR INTERPOLATION: \n", eon_ages_linear.dataframe)
#print("W/ MEDIAN: \n", eon_ages_median.dataframe)