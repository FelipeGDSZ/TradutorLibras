# Identificação de sinais da LIBRAS por meio de Visão Computacional

Este repositório se trata de um projeto que consiste em identificar letras e palavras presentes na **Língua Brasileira de Sinais** por meio de Visão Computacional e Machine Learning, utilizando a webcam. Toda a arquitetura de extração, normalização de dados e treinamento do modelo é feita localmente.


> **Status:** Em desenvolvimento. A base de reconhecimento de letras estáticas foi concluída. A meta atual do projeto é a expansão do banco de dados para a identificação de palavras e o aprimoramento do vocabulário.


## Tecnologias Utilizadas
![Python](https://img.shields.io/badge/python-%233670A0.svg?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/opencv-%23fff.svg?style=for-the-badge&logo=opencv&logoColor=black)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

* **Python 3**
* **OpenCV (`cv2`)**: Captura e manipulação de imagem em tempo real.
* **MediaPipe**: Extração da malha topológica e landmarks das mãos.
* **Scikit-Learn**: Algoritmo de Machine Learning (KNN) para classificação de padrões.
* **Pandas**: Manipulação do banco de dados (CSV).

## Como funciona a Arquitetura atual

O pipeline do projeto está dividido nas seguintes etapas:

1. **Detecção e Extração Bruta:** O MediaPipe lê o frame da câmera, isola a mão e devolve 21 pontos (landmarks) em proporções de tela, que são convertidos em pixels (X, Y).
2. **Normalização dos Dados (Imunidade a Posição e Escala):** 
   * **Translação:** O pulso (Landmark 0) é definido matematicamente como a origem `(0,0)`. Isso torna a detecção independente de onde a mão está posicionada na tela.
   * **Escalonamento:** As distâncias são divididas pelo valor máximo, achatando todas as coordenadas para o intervalo entre `-1.0` e `1.0`. Isso torna a detecção independente da distância da mão para a câmera.
3. **Coleta do Dataset:** Ao pressionar a tecla `S`, as coordenadas normalizadas são salvas em um arquivo `banco_de_dados.csv` junto com a classe (letra ou palavra) correspondente.
4. **Treinamento e Previsão:** O script de machine learning lê o CSV e treina um modelo **K-Nearest Neighbors (KNN)**, exportando o cérebro treinado como `modelo_libras.pkl`. O script principal utiliza esse arquivo para traduzir os sinais em tempo real.

## Como executar o projeto

### 1. Preparando o Ambiente Virtual (Linux)
Recomenda-se rodar o projeto em um ambiente virtual isolado:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalando Dependências
```bash
pip install opencv-python mediapipe pandas scikit-learn
```
##### (Nota: Caso utilize uma versão recente do MediaPipe que tenha removido a API Solutions, você pode precisar fazer o downgrade temporal para a versão 0.10.14 ou atualizar a sintaxe para a Tasks API).

### 3. Rode o tradutor
```bash
python3 DetectorMaos.py
```
##### (Para fechar a aplicação corretamente, pressione a tecla ESC com a janela de vídeo selecionada).

### 4. Como expandir o Banco de Dados (Modo Desenvolvedor)
1. Como o projeto está em fase de expansão de vocabulário, você pode adicionar novas palavras seguindo este fluxo:

2. No arquivo `DetectorMaos.py`, altere a variável classe_atual para a nova palavra que deseja gravar (ex: "Obrigado").

3. Rode o script e pressione S repetidas vezes enquanto faz o sinal, variando levemente a inclinação e distância da mão.

4. Atualize a inteligência artificial rodando o treinamento para aprender as novas palavras e sobrescrever o `.pkl` antigo:

```bash
python3 Treinamento.py
```

## Roadmap (Próximos Passos)
☑️ Extração de landmarks da mão.

☑️ Normalização matemática das coordenadas (independência de escala e translação).

☑️ Lógica de gravação do banco de dados em CSV com captura manual.

☑️ Treinamento do modelo clássico (KNN) e previsão em tempo real.

⏳ [Atual] Expandir o banco de dados para incluir palavras completas e sinais estáticos mais complexos.

⏳ Pesquisar e implementar uma abordagem para sinais dinâmicos (que envolvem movimento contínuo da mão ao longo do tempo).