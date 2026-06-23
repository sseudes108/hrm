import pandas as pd

def gerar_fluxo_fifo(
    df_demanda: pd.DataFrame, df_capacidade: pd.DataFrame, 
    sla_blocks: int = 1
):
    """
    Simula o atendimento da fila (FIFO) bloco a bloco.
    Retorna um DataFrame com o status da fila no final de cada bloco.
    """
    total_blocks = len(df_demanda)
    demanda_lista = df_demanda['quantidade'].tolist()
    capacidade_lista = df_capacidade['quantidade'].tolist()
    
    acumulo_final = []
    estouros_final = []
    processados_final = []
    
    # A fila é uma lista de lotes: [{'qtd': 15, 'chegada': 0}, {'qtd': 20, 'chegada': 1}]
    fila = []
    
    for t in range(total_blocks):
        # 1. Nova demanda entra no final da fila
        if demanda_lista[t] > 0:
            fila.append({'qtd': demanda_lista[t], 'chegada': t})
            
        cap_disp = capacidade_lista[t]
        processado_no_bloco = 0
        
        # 2. Processamento FIFO (Começa pelos mais antigos no índice 0)
        while cap_disp > 0 and len(fila) > 0:
            lote_mais_antigo = fila[0]
            
            if lote_mais_antigo['qtd'] <= cap_disp:
                # Tem capacidade pra matar esse lote inteiro
                processado_no_bloco += lote_mais_antigo['qtd']
                cap_disp -= lote_mais_antigo['qtd']
                fila.pop(0) # Remove da fila
            else:
                # Tem capacidade só pra matar uma parte do lote
                processado_no_bloco += cap_disp
                lote_mais_antigo['qtd'] -= cap_disp
                cap_disp = 0 # Capacidade zerou
                
        processados_final.append(processado_no_bloco)
        
        # 3. Fim do bloco: O que sobrou na fila vira "Acúmulo" (Backlog)
        estoque_atual = sum(lote['qtd'] for lote in fila)
        acumulo_final.append(estoque_atual)
        
        # 4. Cálculo de Estouro de SLA (CORRIGIDO)
        # Trocamos o '>=' por '==' para contar o evento de estouro APENAS UMA VEZ
        # no momento exato em que a proposta cruza a linha de limite do SLA.
        novos_estouros_neste_bloco = 0
        for lote in fila:
            idade_do_lote = t - lote['chegada']
            if idade_do_lote == sla_blocks: 
                novos_estouros_neste_bloco += lote['qtd']
                
        estouros_final.append(novos_estouros_neste_bloco)
        
    df_fluxo = pd.DataFrame({
        'horario': range(total_blocks),
        'processado': processados_final,
        'acumulo': acumulo_final,
        'estouro_sla': estouros_final
    })
    
    return df_fluxo