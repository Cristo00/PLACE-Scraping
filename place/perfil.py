
class Perfil:
    
    def __init__(self, url) -> None:
        self.url = url
        self.expedientes = []
        self.claves = []
        
    def anadir_expediente(self, expediente) -> None:
        self.expedientes.append(expediente)
        
    
        
    