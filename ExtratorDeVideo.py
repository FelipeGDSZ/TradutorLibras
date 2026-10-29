import cv2
import csv
from DetectorMaos import DetectorMaos 

def main():
    # 1. Configurações
    caminho_video = 'video2libras.mp4'  
    classe_atual = "A"           # Valor inicial ao abrir o programa
    arquivo_csv = "banco_normalizado.csv"
    
    # 2. Carrega o vídeo e o detector
    cap = cv2.VideoCapture(caminho_video)
    detector = DetectorMaos(cor_pontos=(0, 255, 0), cor_conexoes=(0, 255, 0))
    
    pausado = False
    
    print("\n--- CONTROLES DO PLAYER ---")
    print("[ESPAÇO] Pausar / Despausar o vídeo")
    print("[ S ] Salvar o frame atual (Original + Espelhado)")
    print("[ C ] Trocar a letra/palavra atual")
    print("[ Q ] Sair do programa")
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
        
        if tecla == 27:
            break
            
        elif tecla == ord(' '):
            pausado = not pausado
            estado = "PAUSADO" if pausado else "RODANDO"
            print(f"Vídeo {estado}")

        # --- SISTEMA DE TROCA DE CLASSE ---
        elif tecla == ord('c'):
            print("\n--- TROCA DE SINAL ---")
            nova_classe = input(f"Sinal atual: '{classe_atual}'. Digite a nova letra/palavra: ")
            
            if nova_classe.strip() != "": 
                classe_atual = nova_classe.strip().upper() 
                print(f"Classe alterada com sucesso! Agora o 'S' vai guardar como: {classe_atual}\n")
        # ----------------------------------
            
        elif tecla == ord('s'):
            if len(lista_posicoes) != 0:
                lista_normalizada = detector.normalizarPosicao(lista_posicoes)
                
                lista_espelhada = []
                for i in range(len(lista_normalizada)):
                    if i % 2 == 0:  
                        lista_espelhada.append(lista_normalizada[i] * -1)
                    else:           
                        lista_espelhada.append(lista_normalizada[i])
                
                with open(arquivo_csv, mode='a', newline='') as f:
                    escritor = csv.writer(f)
                    escritor.writerow([classe_atual] + lista_normalizada) 
                    escritor.writerow([classe_atual] + lista_espelhada)   
                    
                print(f"Sinais '{classe_atual}' (Original e Espelhado) guardados com sucesso!")
            else:
                print("Nenhuma mão detetada neste frame. Tente noutro momento.")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()