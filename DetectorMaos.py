import cv2
import mediapipe as mp
import csv
import pickle

class DetectorMaos: #Classe responsável pela detecção das mãos.
    def __init__(self, modo=False, max_maos=2, deteccao_confianca=0.5, rastreio_confianca=0.5, cor_pontos=(0,0,255), cor_conexoes=(255, 255, 255)):
        # Função responsável por iniciar a classe.
        
        # param modo: Modo de captura da imagem. Se for true, a detecção e o rastreio vão ser feitos em todo momento.
            # ps: deixa travado. Se false, não é feito todo momento, mas pode perder um pouco a marcação, mas não trava
        # :param max_maos: Quantidade de mãos para serem detectadas. (2, por enquanto)
        # :param deteccao_confianca: Percentual de taxa de detecção da mão. Se menor que esse limite, não ocorre a detecção!
        # :param rastreio_confianca: Percentual de taxa de rastreio dos pontos a mão. Se for menor que este limite, não ocorre o rastreio.
        # :param cor_pontos: Cor dos pontos.
        # :param cor_conexoes: Cor das conexões.

        # Inicializando os parâmetros
        self.modo = modo;
        self.max_maos = max_maos;
        self.deteccao_confianca = deteccao_confianca;
        self.rastreio_confianca = rastreio_confianca;
        self.cor_pontos = cor_pontos
        self.cor_conexoes = cor_conexoes;

        # Inicializando os módulos de detecção das mãos
        self.maos_mp = mp.solutions.hands;
        self.maos = self.maos_mp.Hands(self.modo, self.max_maos,1, self.deteccao_confianca, self.rastreio_confianca);

        # Função desenho de ponto
        self.desenho_mp = mp.solutions.drawing_utils;

        # Desenhos dos pontos
        self.desenho_config_pontos = self.desenho_mp.DrawingSpec(color=self.cor_pontos);

        # Conexões dos pontos
        self.desenho_config_conexoes = self.desenho_mp.DrawingSpec(color=self.cor_conexoes);

    def encontrarMaos(self,imagem,desenho=True):
        #Função responsáel por detectar as mãos
        #:param imagem: Imagem capturada.
        #:param desenho: Desenhar os pontos e as conexões nas mãos.
        #:return: Retorna a imagem com a detecção.
        

    # Convertendo a imagem para RGB:
        imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB);

    # Passando a imagem convertida pro detector:
        self.resultado = self.maos.process(imagem_rgb);

    #Verificando detecção de mãos
        if self.resultado.multi_hand_landmarks:
            for pontos in self.resultado.multi_hand_landmarks:
                if desenho:
                    #Desenhando os pontos nas mãos que foram detectadas.
                    self.desenho_mp.draw_landmarks(
                        imagem,
                        pontos,
                        self.maos_mp.HAND_CONNECTIONS,
                        self.desenho_config_pontos,
                        self.desenho_config_conexoes
                    )

        return imagem;

    # Guardando os pontos no formato [id, x, y]
    def encontrarPosicao(self, imagem, num_mao=0):
        # Lista que vai guardar os pontos no formato [id, X, Y]
        lista_pontos = []
        
        # Verifica se alguma mão foi detectada
        if self.resultado.multi_hand_landmarks:
            # Seleciona a mão específica (padrão é a primeira detectada, índice 0)
            mao_detectada = self.resultado.multi_hand_landmarks[num_mao]
            
            # Obtendo a altura (h), largura (w) e canais de cor (c) da imagem
            h, w, c = imagem.shape;
            
            # Iterando pelos 21 pontos da mão
            for id, lm in enumerate(mao_detectada.landmark):
                # Convertendo a proporção (lm.x, lm.y) para pixels absolutos da tela
                cx, cy = int(lm.x * w), int(lm.y * h)
                
                # Salvando na nossa lista
                lista_pontos.append([id, cx, cy])
                
        return lista_pontos;

    def normalizarPosicao(self, lista_pontos):
        # Proteção contra lista vazia
        if not lista_pontos:
            return []

        # 1. Translação (Pulso no 0,0)
        base_x = lista_pontos[0][1]
        base_y = lista_pontos[0][2]

        pontos_transladados = []
        for ponto in lista_pontos:
            novo_x = ponto[1] - base_x
            novo_y = ponto[2] - base_y
            pontos_transladados.append([novo_x, novo_y])

        # 2. Escalonamento (Acha a maior distância para achatar o tamanho)
        valores_absolutos = []
        for px, py in pontos_transladados:
            valores_absolutos.extend([abs(px), abs(py)])
            
        valor_maximo = max(valores_absolutos)
        if valor_maximo == 0: 
            valor_maximo = 1.0

        # 3. Achatamento para formato final (1D)
        pontos_normalizados = []
        for px, py in pontos_transladados:
            pontos_normalizados.append(px / valor_maximo)
            pontos_normalizados.append(py / valor_maximo)

        return pontos_normalizados
    
    # Capturar o vídeo da câmera
def main():
    cap = cv2.VideoCapture(0);
    detector = DetectorMaos(cor_pontos=(255,0,0), cor_conexoes=(255,0,0)); #Instanciando a classe DetectorMaos

    # # Configurações do Banco de Dados
    # classe_atual = "Z" # Mude isso aqui no código quando for gravar outra letra!!!!!!!!!!
    # arquivo_csv = "banco_de_dados.csv"

   # CARREGANDO A INTELIGÊNCIA ARTIFICIAL
    try:
        with open('modelo_libras.pkl', 'rb') as arquivo:
            modelo = pickle.load(arquivo)
        print("Modelo carregado com sucesso! Abrindo a câmera...")
    except FileNotFoundError:
        print("Erro: Arquivo 'modelo_libras.pkl' não encontrado. Rode o script de Treinamento primeiro!")
        return

    #Fazendo a captura
    while True:
        # Obter a imagem
        _, imagem = cap.read();

        # Invertendo a imagem
        imagem = cv2.flip(imagem, flipCode=1);
        

        # Detecção das mãos
        imagem = detector.encontrarMaos(imagem);

        # Extrai as posições
        lista_posicoes = detector.encontrarPosicao(imagem);

        if len(lista_posicoes) != 0:
            # Normaliza (coloca o pulso no 0,0 e achata o tamanho)
            lista_normalizada = detector.normalizarPosicao(lista_posicoes)
            
            # O predict exige uma matriz 2D (uma lista de listas), por isso os colchetes extras
            previsao = modelo.predict([lista_normalizada])
            letra_traduzida = previsao[0] # Pega o resultado (ex: "A", "B")
            
            # Escreve a letra gigante na tela
            cv2.putText(
                imagem, 
                f"Sinal: {letra_traduzida}", 
                (20, 70), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                2, 
                (0, 255, 0), # Cor Verde
                4 # Espessura
            )
            # -----------------------------



        # # Aplica a normalização matemática
        # lista_normalizada = detector.normalizarPosicao(lista_posicoes)
            
        # # Vamos imprimir a lista final para conferir
        # print(lista_normalizada)
            
        # Note que o primeiro X e Y (índices 0 e 1 da lista) sempre serão 0.0, pois são o pulso!
        
        # Mostrar a imagem de captura:
        cv2.imshow('Tradutor de Libras', imagem);

        # Atualização de loop de captura.
        tecla = cv2.waitKey(1) & 0xFF; # Atraso de 1 milisegundo.

        if tecla==27: #Digite ESC pra fechar a aba e parar a aplicação.
            break;

        # # Se apertar a tecla 's', salva os dados no arquivo CSV
        # elif tecla == ord('s'):
        #     # Verifica se tem uma mão na tela para não salvar lista vazia
        #     if len(lista_posicoes) != 0:
        #         # Junta a string da letra com a lista de 42 números decimais
        #         linha_dados = [classe_atual] + lista_normalizada
                
        #         # Abre o arquivo em modo 'a' (append/adicionar) e escreve a linha
        #         with open(arquivo_csv, mode='a', newline='') as f:
        #             escritor = csv.writer(f)
        #             escritor.writerow(linha_dados)
                    
        #         print(f"Sinal '{classe_atual}' salvo com sucesso! ({len(lista_normalizada)} pontos)")

    cap.release();
    cv2.destroyAllWindows();
if __name__== '__main__':
    main();

