import pandas as pd
from dataclasses import dataclass, field

@dataclass
class TurnoTemplate:
    """Representa a estrutura matemática de um turno de trabalho."""
    id: int
    nome: str
    minutos_trabalho: int  # Ex: 480 (8 horas)
    minutos_almoco: int    # Ex: 60 (1 hora)

@dataclass
class AthenaPayload:
    """Estrutura estrita para armazenar as regras de negócio vindas da UI."""
    df_demand: pd.DataFrame 
    sla: int        
    tma: int       
    # default_factory cria uma lista nova e vazia para cada instância com segurança
    turnos: list[TurnoTemplate] = field(default_factory=list) 
    
    # Podemos remover o almoco_tempo daqui, pois cada TurnoTemplate já terá o seu!
    
    @property
    def total_blocks_per_day(self) -> int:
        return int((24 * 60) / self.sla)