import pandas as pd

class Perfil:
    
    def __init__(self, url) -> None:
        self.url = url
        self.expedientes = []
        self.claves = []
        dict_expedientes = {'id': [], 'fecha': [], 'organo': [], 'estado': [], 'objeto': [], 'presupuesto': [], 'valor': [], 'tipo': [], 'cpv': [], 'lugar': [], 'procedimiento': []}
        self.data = pd.DataFrame.from_dict(dict_expedientes)
        
        
    def anadir_expediente(self, expediente) -> None:
        self.expedientes.append(expediente)
        
    def crearDataframe(self) -> pd.DataFrame:
        None
        
    
    
        
    