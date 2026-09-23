import csv

def main():
    print("1. Lendo o banco de dados bruto...")
    try:
        with open('banco_de_dados.csv', mode='r') as f:
            leitor = csv.reader(f)
            # Lê todas as linhas ignorando possíveis linhas em branco
            linhas_brutas = [linha for linha in leitor if linha] 
    except FileNotFoundError:
        print("Erro: O arquivo 'banco_de_dados.csv' não foi encontrado.")
        return

    linhas_normalizadas = []

    print("2. Aplicando Normalização e gerando as mãos esquerdas...")
    for linha in linhas_brutas:
        letra = linha[0]
        # Converte as strings das coordenadas para números decimais (floats)
        coords = [float(x) for x in linha[1:]]

        # --- PASSO A: TRANSLAÇÃO (Pulso no 0,0) ---
        base_x = coords[0]
        base_y = coords[1]

        pontos_transladados = []
        # O loop pula de 2 em 2 para pegar os pares (X, Y)
        for i in range(0, len(coords), 2):
            x_transladado = coords[i] - base_x
            y_transladado = coords[i+1] - base_y
            pontos_transladados.append((x_transladado, y_transladado))

        # --- PASSO B: ESCALONAMENTO (Achatar tamanho para -1 a 1) ---
        valores_absolutos = []
        for px, py in pontos_transladados:
            valores_absolutos.extend([abs(px), abs(py)])
        
        valor_maximo = max(valores_absolutos)
        if valor_maximo == 0: 
            valor_maximo = 1.0

        # --- PASSO C: GERANDO AS DUAS MÃOS ---
        mao_direita = []
        mao_esquerda = []

        for px, py in pontos_transladados:
            # Divide tudo pela maior distância (Normalização final)
            nx = px / valor_maximo
            ny = py / valor_maximo

            # Mão Original (Direita)
            mao_direita.append(nx)
            mao_direita.append(ny)

            # Mão Espelhada (Esquerda - Inverte apenas o eixo X)
            mao_esquerda.append(nx * -1)
            mao_esquerda.append(ny)

        # Adiciona as duas versões na nossa nova lista
        linhas_normalizadas.append([letra] + mao_direita)
        linhas_normalizadas.append([letra] + mao_esquerda)

    print("3. Salvando o banco de dados definitivo...")
    # Salva em um arquivo NOVO para não estragar o original caso dê erro
    with open('banco_normalizado.csv', mode='w', newline='') as f:
        escritor = csv.writer(f)
        for linha in linhas_normalizadas:
            escritor.writerow(linha)
            
    print(f"Sucesso! {len(linhas_normalizadas)} amostras perfeitas foram criadas.")

if __name__ == '__main__':
    main()