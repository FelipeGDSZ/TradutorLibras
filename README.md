# Identificação de sinais da LIBRAS por meio de Visão Computacional

Este repositório se trata de um projeto que consiste em identificar letras e palavras presentes na **Língua Brasileira de Sinais** por meio de Visão Computacional e Machine Learning, utilizando a webcam ou análise de vídeos. Toda a arquitetura de extração, normalização de dados e treinamento do modelo é feita localmente.

> **Status:** Em desenvolvimento ativo. A arquitetura base e a interface visual (UI) estão prontas. O sistema conta agora com uma ferramenta de extração de dados via vídeo para expansão robusta do vocabulário e criação de base de dados ambidestra.

## Tecnologias Utilizadas
![Python](https://img.shields.io/badge/python-%233670A0.svg?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/opencv-%23fff.svg?style=for-the-badge&logo=opencv&logoColor=black)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

* **Python 3**
* **OpenCV (`cv2`)**: Captura de imagem, criação de interface visual (UI badges) e manipulação em tempo real.
* **MediaPipe**: Extração da malha topológica e landmarks das mãos.
* **Scikit-Learn**: Algoritmo de Machine Learning (KNN) para classificação de padrões.
* **Pandas**: Manipulação do banco de dados (CSV).

## Como funciona a Arquitetura atual

O pipeline do projeto está dividido nas seguintes etapas:

1. **Detecção e Extração Bruta:** O MediaPipe lê o frame, isola a mão e devolve 21 pontos (landmarks) convertidos em pixels (X, Y).
2. **Normalização dos Dados (Imunidade a Posição e Escala):** 
   * **Translação:** O pulso (Landmark 0) é definido matematicamente como a origem `(0,0)`.
   * **Escalonamento:** As distâncias são divididas pelo valor máximo, achatando todas as coordenadas para o intervalo entre `-1.0` e `1.0`.
3. **Coleta de Dados Inteligente:** O projeto possui um *Player Customizado* (`ExtratorDeVideo.py`) que permite pausar vídeos do YouTube e extrair os *landmarks* perfeitamente. O sistema aplica *Data Augmentation* salvando automaticamente a versão espelhada (ambidestra) de cada sinal.
4. **Treinamento e Previsão:** O script treina um modelo **K-Nearest Neighbors (KNN)** (`modelo_libras.pkl`). O tradutor final exibe os resultados na tela com um layout moderno e responsivo.

## Como executar o projeto

### 1. Preparando o Ambiente Virtual
Recomenda-se rodar o projeto em um ambiente isolado:
```bash
python3 -m venv .venv
source .venv/bin/activate  # No Linux/Mac
# .venv\Scripts\activate   # No Windows
```

### 2. Instalando Dependências
```bash
pip install requirements.txt
```

### 3. Rode o tradutor
```bash
python3 DetectorMaos.py
```
##### (Para fechar a aplicação corretamente, pressione a tecla ESC com a janela de vídeo selecionada).

### 4. Como expandir o Banco de Dados (Modo Desenvolvedor)
Como o projeto está em fase de expansão de vocabulário, você pode adicionar novas palavras de duas formas:

Opção A: Via Webcam (`DetectorMaos.py`)
Altere a variável classe_atual no código, rode o script, faça o sinal para a câmera e pressione S para salvar os dados normalizados.

Opção B: Via Vídeos (`ExtratorDeVideo.py`)

1. Adicione um vídeo de Libras (ex: video.mp4) na pasta do projeto.

2. Rode o script e use **ESPAÇO** para pausar no momento exato do sinal.

3. Pressione **C** para digitar qual letra/palavra está na tela.

4. Pressione **S** para extrair os dados originais e espelhados.

4. Atualize a inteligência artificial rodando o treinamento para aprender as novas palavras e sobrescrever o `.pkl` antigo:

```bash
python3 Treinamento.py
```

## Roadmap (Próximos Passos)
☑️ Extração de landmarks da mão.

☑️ Normalização matemática das coordenadas (independência de escala e translação).

☑️ Lógica de gravação do banco de dados em CSV.

☑️ Interface visual (UI) para exibição da tradução.

☑️ Ferramenta de Data Augmentation e extração de dados em vídeos.

☑️ Treinamento do modelo clássico (KNN) e previsão em tempo real.

⏳ [Atual] Expandir o banco de dados para incluir palavras completas e sinais estáticos mais complexos.

⏳ Pesquisar e implementar uma abordagem para sinais dinâmicos (que envolvem movimento contínuo da mão ao longo do tempo).
