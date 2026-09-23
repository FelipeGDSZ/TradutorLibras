import csv

def main():
    linhas_originais = []
    
    # O padrão do OpenCV é 640. Se a sua webcam for HD, pode ser 1280.
    LARGURA_CAMERA = 640 

    print("1. Lendo o banco de dados atual...")
    with open('banco_de_dados.csv', mode='r') as f:
        leitor = csv.reader(f)
        for linha in leitor:
            linhas_originais.append(linha)
            
    linhas_espelhadas = []
    
    print("2. Gerando as mãos espelhadas...")
    for linha in linhas_originais:
        letra = linha[0]
        coordenadas = [float(x) for x in linha[1:]] 
        
        coordenadas_invertidas = []
        for i in range(len(coordenadas)):
            if i % 2 == 0:
                # É um eixo X -> Subtrai da largura da tela para espelhar!
                coordenadas_invertidas.append(LARGURA_CAMERA - coordenadas[i])
            else:
                # É um eixo Y -> Mantém igual
                coordenadas_invertidas.append(coordenadas[i])
                
        nova_linha = [letra] + coordenadas_invertidas
        linhas_espelhadas.append(nova_linha)

    print("3. Adicionando as mãos esquerdas ao banco...")
    with open('banco_de_dados.csv', mode='a', newline='') as f:
        escritor = csv.writer(f)
        for linha in linhas_espelhadas:
            escritor.writerow(linha)
            
    print(f"Sucesso! {len(linhas_espelhadas)} novas linhas esquerdas salvas.")

if __name__ == '__main__':
    main()