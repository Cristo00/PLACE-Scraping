import asyncio

from place import perfil
from scrap import estado

def main():
    perfilTITSA = perfil.Perfil(url='https://contrataciondelestado.es/wps/poc?uri=deeplink%3AperfilContratante&idBp=dTTwiHTCfjEQK2TEfXGy%2BA%3D%3D')
    print(perfilTITSA.url)
    pagina = estado.Pagina(estado.EstadoPerfil(), perfilTITSA)
    
if __name__ == "__main__":
    main()