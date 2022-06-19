import asyncio

from place import perfil
from scrap import estado
from tkinter import tix 
from interfaz import interfaz
import threading
import tkinter as tk

def main():
    root = tix.Tk()
    root.geometry("800x600+300+300")
    root.config(background="#f9fafd")
    root.iconbitmap('.\\imagenes\\placeLogo.ico')
    root.resizable(False, False)
    app = threading.Thread(target=interfaz.MyFrame())
    root.mainloop()
    
if __name__ == "__main__":
    try: 
        main()
    except Exception as error:
        print('Hubo un error en la ejecución: ' + str(error))