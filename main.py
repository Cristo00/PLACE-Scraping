import asyncio

from place import perfil
from scrap import estado
from tkinter import tix 
from interfaz import interfaz

import tkinterweb
import tkinter as tk

def main():
    root = tix.Tk()
    root.geometry("800x600+300+300")
    root.config(background="#ffffff")
    root.resizable(False, False)
    app = interfaz.MyFrame()
    root.mainloop()
    #perfilTITSA = perfil.Perfil(url='https://contrataciondelestado.es/wps/poc?uri=deeplink%3AperfilContratante&idBp=dTTwiHTCfjEQK2TEfXGy%2BA%3D%3D')
    #pagina = estado.Pagina(estado.EstadoPerfil(), perfilTITSA)
    
if __name__ == "__main__":
    try: 
        main()
    except Exception as error:
        print('Hubo un error en la ejecución: ' + str(error))