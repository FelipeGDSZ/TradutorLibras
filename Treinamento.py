import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import pickle

def main():
    print("1. Lendo o banco de dados...")
    # Carrega o CSV (header=None porque não colocamos título nas colunas)
    df = pd.read_csv('banco_normalizado.csv', header=None)

    # Separa o que é a Letra (coluna 0) do que são as Coordenadas (todas as outras colunas)
    y = df.iloc[:, 0].values  
    X = df.iloc[:, 1:].values 

    print("2. Separando dados de treino e teste...")
    # Esconde 20% dos dados para fazer uma prova final com o modelo depois do treino
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("3. Treinando a Inteligência Artificial (KNN)...")
    # n_neighbors=3 significa que ele vai basear a decisão olhando os 3 sinais mais parecidos
    modelo = KNeighborsClassifier(n_neighbors=3)
    modelo.fit(X_train, y_train)

    print("4. Avaliando o modelo...")
    previsoes = modelo.predict(X_test)
    acuracia = accuracy_score(y_test, previsoes)
    print(f"-> Acurácia do modelo: {acuracia * 100:.2f}%")

    print("5. Salvando o cérebro treinado...")
    with open('modelo_libras.pkl', 'wb') as arquivo:
        pickle.dump(modelo, arquivo)
    print("-> Arquivo 'modelo_libras.pkl' gerado com sucesso!")

if __name__ == '__main__':
    main()