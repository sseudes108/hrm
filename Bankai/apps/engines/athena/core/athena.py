from ortools.sat.python import cp_model
import pandas as pd
import numpy as np

# Importe o TurnoTemplate do arquivo onde você o declarou (ex: payload)
# from apps.engines.athena.config.payload import TurnoTemplate

class AthenaEngine:
    """
    Engine Atena para Otimização de Capacidade Operacional Multi-Turnos.
    """
    def __init__(self, df_demand: pd.DataFrame, tma_per_block: int, sla: int, turnos: list):
        self.model = cp_model.CpModel()
        self.demand = df_demand['quantidade'].tolist()
        self.total_blocks = len(self.demand)
        self.sla_blocks = 1
        self.tma = tma_per_block
        
        self.max_analistas = int(sum(self.demand) / self.tma) + 1
        
        # Estruturas de Variáveis
        self.var_inicio = {}     # (analista, index_do_turno, bloco_inicio) -> Booleano
        self.var_trabalha = {}   # (analista, bloco) -> Booleano
        self.analista_ativo = {} # (analista) -> Booleano
        
        # Pré-processa os Turnos para gerar as matrizes binárias [1, 1, 0, 1...]
        self.turnos_processados = self._processar_turnos(turnos, sla)

    def _processar_turnos(self, turnos: list, sla: int) -> list:
        """Converte as regras de negócio de cada turno em matrizes de blocos para o solver."""
        processados = []
        
        # Fallback de segurança caso a UI não mande nenhum turno selecionado
        if not turnos:
            from dataclasses import make_dataclass
            TurnoFallback = make_dataclass("TurnoTemplate", [("nome", str), ("minutos_trabalho", int), ("minutos_almoco", int)])
            turnos = [TurnoFallback(nome="Turno 8:00 (Padrão)", minutos_trabalho=480, minutos_almoco=60)]
            
        for turno in turnos:
            # Converte minutos para blocos
            blocos_trab = int(round(turno.minutos_trabalho / sla))
            blocos_alm = int(round(turno.minutos_almoco / sla))
            
            # Divide a jornada ao meio (CLT)
            trab_1 = blocos_trab // 2
            trab_2 = blocos_trab - trab_1
            
            padrao = [1]*trab_1 + [0]*blocos_alm + [1]*trab_2
            
            processados.append({
                'nome': turno.nome,
                'padrao': padrao,
                'offset_almoco_inicio': trab_1,
                'offset_almoco_fim': trab_1 + blocos_alm,
                'tamanho_total': len(padrao)
            })
            
        return processados

    def build_model(self):
        # 1. Criação das Variáveis (Agora com a dimensão de "Qual Turno?")
        for a in range(self.max_analistas):
            self.analista_ativo[a] = self.model.NewBoolVar(f'analista_ativo_{a}')
            
            blocos_inicio_possiveis = []
            
            # Para cada tipo de turno disponível...
            for t_idx in range(len(self.turnos_processados)):
                for t in range(self.total_blocks):
                    # Cria a variável 3D: "Analista A começa no Turno IDX no Bloco T"
                    var_ini = self.model.NewBoolVar(f'ini_a{a}_turno{t_idx}_t{t}')
                    self.var_inicio[(a, t_idx, t)] = var_ini
                    blocos_inicio_possiveis.append(var_ini)
            
            # A variável de trabalho continua 2D (Ele está produzindo ou não no bloco)
            for t in range(self.total_blocks):
                self.var_trabalha[(a, t)] = self.model.NewBoolVar(f'trabalha_a{a}_t{t}')
            
            # Restrição Vital: Se ativo, escolhe APENAS 1 turno e 1 horário de início.
            self.model.AddExactlyOne(blocos_inicio_possiveis).OnlyEnforceIf(self.analista_ativo[a])
            self.model.Add(sum(blocos_inicio_possiveis) == 0).OnlyEnforceIf(self.analista_ativo[a].Not())

        # 2. A Equação Linear de Deslizamento (Atualizada para varrer múltiplos turnos)
        for a in range(self.max_analistas):
            for t_atual in range(self.total_blocks):
                contribuicoes_para_trabalhar = []
                
                # O analista pode estar trabalhando agora se iniciou o Turno X no passado
                for t_idx, turno_info in enumerate(self.turnos_processados):
                    for offset, estado_producao in enumerate(turno_info['padrao']):
                        if estado_producao == 1:
                            t_start = (t_atual - offset) % self.total_blocks
                            contribuicoes_para_trabalhar.append(self.var_inicio[(a, t_idx, t_start)])
                
                self.model.Add(self.var_trabalha[(a, t_atual)] == sum(contribuicoes_para_trabalhar))

        # 3. Restrição de SLA Acumulado (Segurança de Tipagem Numpy -> Int)
        soma_numpy = np.cumsum(self.demand)
        acumulado_demanda = [int(x) for x in soma_numpy]
        
        producao_bloco = []
        for t in range(self.total_blocks):
            prod_t = self.model.NewIntVar(0, self.max_analistas * self.tma, f'prod_total_t{t}')
            self.model.Add(prod_t == sum(self.var_trabalha[(a, t)] for a in range(self.max_analistas)) * self.tma)
            producao_bloco.append(prod_t)

        for t in range(self.total_blocks):
            limite_sla = min(t + self.sla_blocks, self.total_blocks - 1)
            producao_acumulada_no_limite = sum(producao_bloco[i] for i in range(limite_sla + 1))
            self.model.Add(producao_acumulada_no_limite >= acumulado_demanda[t])

        # 4. Função Objetivo
        self.model.Minimize(sum(self.analista_ativo[a] for a in range(self.max_analistas)))

    def solve(self) -> dict:
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 30.0 
        status = solver.Solve(self.model)
        
        capacidade_final = [0] * self.total_blocks
        escala_detalhada = []
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            for t in range(self.total_blocks):
                ativos_no_bloco = sum(1 for a in range(self.max_analistas) if solver.Value(self.var_trabalha[(a, t)]) == 1)
                capacidade_final[t] = ativos_no_bloco * self.tma
            
            # Mapeia a jornada lendo a dimensão tridimensional
            for a in range(self.max_analistas):
                if solver.Value(self.analista_ativo[a]) == 1:
                    
                    # Procura qual turno e horário ele foi escalado
                    for t_idx, turno_info in enumerate(self.turnos_processados):
                        for t_start in range(self.total_blocks):
                            if solver.Value(self.var_inicio[(a, t_idx, t_start)]) == 1:
                                
                                t_alm_ini = (t_start + turno_info['offset_almoco_inicio']) % self.total_blocks
                                t_alm_fim = (t_start + turno_info['offset_almoco_fim']) % self.total_blocks
                                t_saida = (t_start + turno_info['tamanho_total']) % self.total_blocks
                                
                                escala_detalhada.append({
                                    'analista_id': f"Analista {a+1}",
                                    'turno_aplicado': turno_info['nome'], # Mostra o turno na tabela!
                                    'bloco_entrada': t_start,
                                    'bloco_almoco_inicio': t_alm_ini,
                                    'bloco_almoco_fim': t_alm_fim,
                                    'bloco_saida': t_saida
                                })
                                break
        return {
            "df_capacity": pd.DataFrame({'horario': list(range(self.total_blocks)), 'quantidade': capacidade_final}),
            "df_escala": pd.DataFrame(escala_detalhada)
        }