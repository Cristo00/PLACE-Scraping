import asyncio
from dataclasses import Field
from struct import pack
from pyppeteer import launch
from distutils.cmd import Command
from turtle import bgcolor, color
import tkinterweb
import os
import tkinter
from tkinter import BOTTOM, OptionMenu, PhotoImage, Tk, tix, RIGHT, BOTH, RAISED, TOP, LEFT, X, Y
from tkinter.ttk import Frame, Button, Style, Label, Entry

class MyFrame(tkinter.Frame):

    def __init__(self):
        super().__init__()
        questionPath = str(os.getcwd()) + '\\imagenes\\interrogacion.png'
        placePath = str(os.getcwd()) + '\\imagenes\\place.png'
        perfilPath = str(os.getcwd()) + '\\imagenes\\perfil.png'
        enlacePath = str(os.getcwd()) + '\\imagenes\\enlace.png'
        self.questionImage = PhotoImage(file=questionPath).subsample(20, 20)
        self.placeImage = PhotoImage(file=placePath).subsample(1, 1)
        self.perfilImage = PhotoImage(file=perfilPath).subsample(2, 2)
        self.enlaceImage = PhotoImage(file=enlacePath).subsample(2, 2)
        self.helpOne = tix.Balloon(self)
        self.helpTwo = tix.Balloon(self)
        self.helpThree = tix.Balloon(self)
        for sub in self.helpOne.subwidgets_all():
            sub.config(bg='white')
        for sub in self.helpTwo.subwidgets_all():
            sub.config(bg='white')
        for sub in self.helpThree.subwidgets_all():
            sub.config(bg='white')
        self.initUI()


    def initUI(self):
        super().config(bg="#ffffff")
        self.master.title("Perfiles PLACE")
        self.style = Style()
        self.style.theme_use("clam")
        
        frameH = tkinter.Frame(self, relief=RAISED, borderwidth=1, bg="#fff173")
        frame1 = tkinter.Frame(self, relief=RAISED, borderwidth=0, bg="#ffffff")
        frame2 = tkinter.Frame(self, relief=RAISED, borderwidth=0, bg="#ffffff")
        frame3 = tkinter.Frame(self, relief=RAISED, borderwidth=0, bg="#ffffff")
        frame4 = tkinter.Frame(self, relief=RAISED, borderwidth=0, bg="#ffffff")
        frameB = tkinter.Frame(self, relief=RAISED, borderwidth=1, bg="#fff173")
        
        ############### FRAMES ###############
        frameH.pack(side=TOP, fill=X, expand=False)
        frame1.pack(side=TOP, fill=None, expand=False)
        frame2.pack(side=TOP, fill=BOTH, expand=True)
        frame3.pack(side=TOP, fill=None, expand=False)
        frame4.pack(side=TOP, fill=None, expand=False)
        frameB.pack(side=BOTTOM, fill=X, expand=False)
        self.pack(fill=BOTH, expand=True)
        #######################################
        
        ############### FRAME H ###############
        placeLabel= Label(frameH, image=self.placeImage, compound=LEFT, background="#fff173")
        placeLabel.pack(side=TOP)
        #######################################
        
        ############### FRAME 1 ############### 
        searchLabel = Label(frame1, text='Nombre Perfil: ')
        searchLabel.config(background="#ffffff")
        searchLabel.pack(side=LEFT, padx=5, pady=5)
        searchEntry = Entry(frame1)
        searchEntry.config(background="#ffffff")
        searchEntry.pack(side=LEFT, padx=5, pady=5)
        searchButton = Button(frame1, text='Buscar')
        searchButton.pack(side=LEFT, padx=5, pady=5)
        questionImageLabel = Label(frame1, image=self.questionImage, compound=LEFT, width=1, background="#ffffff")
        questionImageLabel.pack(side=LEFT, padx=5, pady=5)
        self.helpOne.label.config(bg='white', image=self.perfilImage)
        self.helpOne.bind_widget(questionImageLabel, balloonmsg="Nota: Si quiere una búsqueda más personalizada, acuda a \"contrataciondelestado.es\"")
        #######################################
        
        ############### FRAME 2 ############### 
        options=tkinter.StringVar()
        options.set("Seleccione una opción")
        option_list = ['']
        optionMenu1 = OptionMenu(frame2, options, *option_list)
        optionMenu1.pack(side=TOP, padx=5, pady=5)
        #######################################
        
        ############### FRAME 3 ############### 
        fileLabel = Label(frame3, text='Introduce el nombre del fichero: ')
        fileLabel.config(background="#ffffff")
        fileLabel.pack(side=LEFT, padx=5, pady=5)
        fileEntry = Entry(frame3)
        fileEntry.pack(side=LEFT, padx=5, pady=5)
        fileButton = Button(frame3, text='Leer fichero')
        fileButton.pack(side=LEFT, padx=5, pady=5)
        fileQuestionLabel = Label(frame3, image=self.questionImage, compound=LEFT, width=1, background="#ffffff")
        fileQuestionLabel.pack(side=LEFT, padx=5, pady=5)
        self.helpTwo.label.config(bg='white')
        self.helpTwo.bind_widget(fileQuestionLabel, balloonmsg="En este campo se ha de introducir el nombre del fichero en el que se añadirán los datos")
        #######################################
        
        ############### FRAME 4 ############### 
        urlLabel = Label(frame4, text='Introduce una URL: ')
        urlLabel.config(background="#ffffff")
        urlLabel.pack(side=LEFT, padx=5, pady=5)
        urlEntry = Entry(frame4)
        urlEntry.pack(side=LEFT, padx=5, pady=5)
        urlButton = Button(frame4, text='Obtener CSV')
        urlButton.pack(side=LEFT, padx=5, pady=5)
        urlQuestionLabel = Label(frame4, image=self.questionImage, compound=LEFT, width=1, background="#ffffff")
        urlQuestionLabel.pack(side=LEFT, padx=5, pady=5)
        self.helpThree.label.config(bg='white', image=self.enlaceImage)
        self.helpThree.bind_widget(urlQuestionLabel, balloonmsg="Nota: Este enlace se debe introducir para generar un CSV con los datos de todos los expedientes")
        #######################################
        
        ############### FRAME B ############### 
        closeButton = Button(frameB, text="Cerrar")
        closeButton.pack(side=RIGHT, padx=5, pady=5)
        okButton = Button(frameB, text="Resetear")
        okButton.pack(side=RIGHT)
        #######################################
        
    def buscarPerfiles():
        None
        #label_3.configure(text='kampo')
        #asyncio.get_event_loop().run_until_complete(buscarPerfilesAsync())
    
    async def buscarPerfilesAsync():
        # Abrir el navegador
        browser = await launch({"frameHless": False, "args": ["--start-maximized"]})
        # Abrir una página nueva
        page = await browser.newPage()
        await page.setViewport({"width": 1600, "height": 900})
        await page.waitFor(1500)


#def main():
#
#    root = tix.Tk()
#    root.geometry("800x600+300+300")
#    root.config(background="#ffffff")
#    root.resizable(False, False)
#    app = MyFrame()
#    root.mainloop()
#
#
#if __name__ == '__main__':
#    main()

