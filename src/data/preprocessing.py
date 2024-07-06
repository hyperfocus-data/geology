import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from analyze import *
import os

"""
 x_train, y_train = conjunto de dados de treinamento
 x_test, y_test = conjunto de dados de teste
 
 A funcao train_test_split divide arrays ou matrizes em conjuntos de treinamentos e teste de forma aleatoria.
 x = variaveis independentes (features). As entradas que o modelo usa pra fazer previsoes. 
 Retorna subconjuntos de dados de acordo c a proporcao definida
 
 y = variaveis dependentes (target). Essa eh a saida que o modelo esta tentando prever
 
 test_size=0.2 eh a proporcao do conjunto de dados que deve ser alocada para o conjunto de teste
 
 20% para teste e os 80% restantes para treinamento
 
 random_state: Este parametro eh usado para garantir que a divisao dos dados seja reproduzivel. 
 Ao definir um random_state fixo, a funcao produzira a mesma divisao dos dados toda vez que for executada.
 O numero 42 eh um valor arbitrario. Qualquer inteiro pode ser usado aqui.
 
 Essa abordagem eh necessaria para que o modelo seja treinado de maneira justa. Permitindo medir seu desempenho
 em dados que ele nao viu durante o treinamento.

"""
 # 20% dos dados serao para teste // 80% serao para treinamento
""" 
A normalizacao de dados transforma os dados para que eles tenham uma escala comum.
Isso pode melhorar o desempenho e a eficiencia dos algoritmos de aprendizado.

A normalizacao utilizando o StandardScaler padroniza as caracteristicas removendo a 
media e escalando para a variancia unitaria. Ou seja, transforma os dados para que tenham
media 0 e desvio padrao 1. 

Formula: X_standard = X - u / n | Sendo u a media dos dados e n o desvio padrao dos dados.

As vantagens do standard eh que se os dados seguem uma destribuicao normal (gaussiana)
ele pode ser uma boa escolha e os dados escalados manterao a relacao original entre eles.
Entretanto eles sao sensiveis a outliers. Caso os dados tenham outliers, o desvio e a media
podem ser afetados, distorcendo a transformacao.

Outliers sao valores observados nos dados que se desviam dos outros valores do
conjunto de dados. Eles podem surgir devido a variacoes naturais nos dados, erros
de mediacao, erros de entrada de dados ou podem ser eventos raros que realmente sao significativos.
Ex: em um conjunto de idade, uma pessoa com um valor de 200 anos seria um outlier, ja que eh
muito maior que o esperado.

Um outlier pode ser, nesse contexto, os primeiros dados. Por ex o dado da era cenozoica.
0.0042 milhoes de anos que convertendo (0.0042 x 1.000.000 = 4.200 anos) ou seja esta na casa
dos mil

No contexto do projeto, devemos identificar as caracteristicas a serem normalizadas.
No caso, vamos normalizar as idades geologicas as quais envolvem uma ampla gamas de valores
pois sao medidas de tempo de milhoes de anos.
Com isso, dividimos o conjunto de dados em teste e treino para evitar o vazamento de dados e
garantir que a avaliacao do modelo seja justa.


"""

def preprocess_and_split_data(df: pd.DataFrame, target: str, verification=True):
    test_size=0.2
    x = df.drop(target, axis=1)
    y = df[target]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=42)
    
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)
    
    if verification:
        df1_col_size = len(df.columns)
        df1_row_size = len(df)

        train_size = int((1 - test_size) * 100)
        train_x_expected = int((train_size / 100) * df1_row_size)
        train_y_expected = df1_col_size - 1

        test_x_expected = int(test_size * df1_row_size)
        test_y_expected = train_y_expected
        
        print(f"df size: ", df.shape)
        print("train_size: ", train_size)
        print("train_x_expected: ", train_x_expected)
        print("train_y_expected: ", train_y_expected)
        print("test_x_expected: ", test_x_expected)
        print("test_y_expected: ", test_y_expected)

        print(f"x_train shape: {x_train.shape}")
        print(f"x_test shape: {x_test.shape}")
        print(f"y_train shape: {y_train.shape}")
        print(f"y_test shape: {y_test.shape}")
    
    return x_train_scaled, x_test_scaled, y_train, y_test


def save_data(data: any, dir: str, filename: str, extension='csv', index=False) -> None:
    os.makedirs(dir, exist_ok=True)
    pd.DataFrame(data).to_csv(os.path.join(dir, f'{filename}.{extension}'), index=index)
    print(f"({filename}) salvo corretamente em '{dir}'.")

if __name__ == "__main__":
    df1 = phanerozoic.dataframe
    
    x_train_scaled, x_test_scaled, y_train, y_test = preprocess_and_split_data(df1, 'Age (Ma)')
    
    processed_dir: str = 'D:/GitHub/Hyperfocus/geology/data/processed'
    os.makedirs(processed_dir, exist_ok=True)
    save_data(data=x_train_scaled, dir=processed_dir, filename='x_train_scaled')
    save_data(data=x_test_scaled, dir=processed_dir, filename='x_test_scaled')
    save_data(data=y_train, dir=processed_dir, filename='y_train')
    save_data(data=y_test, dir=processed_dir, filename='y_test')

    