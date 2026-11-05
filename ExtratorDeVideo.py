import cv2
import csv
from DetectorMaos import DetectorMaos 

def main():
    # 1. Configurações
    caminho_video = 'video2libras.mp4'  
    classe_atual = "A"           # Valor inicial ao abrir o programa
    
    # Aponta para o arquivo de dados brutos
    arquivo_csv = "banco_de_dados.csv" 
    
    # 2. Carrega o vídeo e o detector
    cap = cv2.VideoCapture(caminho_video)
    detector = DetectorMaos(cor_pontos=(0, 255, 0), cor_conexoes=(0, 255, 0))
    
    pausado = False
    
    print("\n--- CONTROLES DO PLAYER ---")
    print("[ESPAÇO] Pausar / Despausar o vídeo")
    print("[ S ] Salvar o frame atual (Apenas Coordenadas Brutas)")
    print("[ C ] Trocar a letra/palavra atual")
    print("[ ESC ] Sair do programa")
    print("---------------------------\n")

    while True:
        if not pausado:
            sucesso, imagem = cap.read()
            if not sucesso:
                print("Fim do vídeo alcançado!")
                break
                
            # O MediaPipe só desenha se o vídeo não estiver pausado
            imagem = detector.encontrarMaos(imagem)
            lista_posicoes = detector.encontrarPosicao(imagem)
            
        cv2.imshow('Coletor de Dados via YouTube', imagem)
        
        tecla = cv2.waitKey(30) & 0xFF
        
        if tecla == 27: # ESC
            break
            
        elif tecla == ord(' '):
            pausado = not pausado
            estado = "PAUSADO" if pausado else "RODANDO"
            print(f"Vídeo {estado}")

        # ------------------------------------
        # Troca de Classe
        elif tecla == ord('c'):
            print("\n--- TROCA DE SINAL ---")
            nova_classe = input(f"Sinal atual: '{classe_atual}'. Digite a nova letra/palavra: ")
            
            if nova_classe.strip() != "": 
                classe_atual = nova_classe.strip().upper() 
                print(f"Classe alterada com sucesso! Agora o 'S' vai guardar como: {classe_atual}\n")
        # ----------------------------------
            
        elif tecla == ord('s'):
            if len(lista_posicoes) != 0:
                
                # Extrair apenas as coordenadas X e Y brutas
                # O detector geralmente retorna [[id, x, y], [id, x, y]...]. 
                # Vamos achatar isso para uma lista simples [x1, y1, x2, y2...]
                lista_bruta = []
                if isinstance(lista_posicoes[0], list): 
                    for ponto in lista_posicoes:
                        lista_bruta.extend([ponto[1], ponto[2]]) # Ignora o ID, pega X e Y
                else:
                    lista_bruta = lista_posicoes # Caso a sua função já retorne achatado
                
                # Guardar sem normalizar
                with open(arquivo_csv, mode='a', newline='') as f:
                    escritor = csv.writer(f)
                    escritor.writerow([classe_atual] + lista_bruta) 
                    
                print(f"Sinal '{classe_atual}' (Dados Brutos) guardado com sucesso em {arquivo_csv}!")
            else:
                print("Nenhuma mão detetada neste frame. Tente noutro momento.")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()