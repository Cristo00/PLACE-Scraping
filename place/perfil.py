
class Perfil:
    
    url = ''
    expedientes = []
    
    def __init__(self, url) -> None:
        self.url = url
        
    def anadir_expediente(self, expediente) -> None:
        self.expedientes.append(expediente)
        
    
        
    