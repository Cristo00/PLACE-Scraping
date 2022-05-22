
from dataclasses import dataclass

@dataclass
class Expediente: 
    id: str
    fecha: str
    organo: str
    estado: str
    objeto: str
    presupuesto: str
    valor: str
    tipo: str
    cpv: str
    lugar: str
    procedimiento: str
    
# asdict
# merge