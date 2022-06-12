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
from place.perfil import *
from scrap.estado import *


class MyFrame(tkinter.Frame):

    def __init__(self):
        super().__init__()
        self.urls = []
        dict_expedientes = {'id': [], 'fecha': [], 'organo': [], 'estado': [], 'objeto': [], 'presupuesto': [], 'valor': [], 'tipo': [], 'cpv': [], 'lugar': [], 'procedimiento': []}
        self.data = pd.DataFrame.from_dict(dict_expedientes)
        self.dataframes = []
        questionPath = str(os.getcwd()) + '\\imagenes\\interrogacion.png'
        placePath = str(os.getcwd()) + '\\imagenes\\place.png'
        perfilPath = str(os.getcwd()) + '\\imagenes\\perfil.png'
        enlacePath = str(os.getcwd()) + '\\imagenes\\enlace.png'
        tickPath = str(os.getcwd()) + '\\imagenes\\tick.png'
        crossPath = str(os.getcwd()) + '\\imagenes\\cross.png'
        self.questionImage = PhotoImage(file=questionPath).subsample(20, 20)
        self.placeImage = PhotoImage(file=placePath).subsample(1, 1)
        self.perfilImage = PhotoImage(file=perfilPath).subsample(2, 2)
        self.enlaceImage = PhotoImage(file=enlacePath).subsample(2, 2)
        self.tickImage = PhotoImage(file=tickPath).subsample(15, 15)
        self.crossImage = PhotoImage(file=crossPath).subsample(40, 40)
        self.helpOne = tix.Balloon(self)
        self.helpTwo = tix.Balloon(self)
        self.helpThree = tix.Balloon(self)
        for sub in self.helpOne.subwidgets_all():
            sub.config(bg='white')
        for sub in self.helpTwo.subwidgets_all():
            sub.config(bg='white')
        for sub in self.helpThree.subwidgets_all():
            sub.config(bg='white')
        self.ficheroFinal = ''
        self.initUI()


    def initUI(self):
        super().config(bg="#ffffff")
        self.master.title("Perfiles PLACE")
        self.style = Style()
        self.style.theme_use("clam")
        
        self.frameH = tkinter.Frame(self, relief=RAISED, borderwidth=1, bg="#fff173")
        self.frame1 = tkinter.Frame(self, relief=RAISED, borderwidth=0, bg="#ffffff")
        self.frame2 = tkinter.Frame(self, relief=RAISED, borderwidth=0, bg="#ffffff")
        self.frame3 = tkinter.Frame(self, relief=RAISED, borderwidth=0, bg="#ffffff")
        self.frame4 = tkinter.Frame(self, relief=RAISED, borderwidth=0, bg="#ffffff")
        self.frame5 = tkinter.Frame(self, relief=RAISED, borderwidth=0, bg="#ffffff")
        self.frameB = tkinter.Frame(self, relief=RAISED, borderwidth=1, bg="#fff173")
        
        ############### FRAMES ###############
        self.frameH.pack(side=TOP, fill=X, expand=False)
        self.frame1.pack(side=TOP, fill=None, expand=False)
        self.frame2.pack(side=TOP, fill=BOTH, expand=True)
        self.frame3.pack(side=TOP, fill=None, expand=False)
        self.frame4.pack(side=TOP, fill=None, expand=False)
        self.frame5.pack(side=TOP, fill=None, expand=False)
        self.frameB.pack(side=BOTTOM, fill=X, expand=False)
        self.pack(fill=BOTH, expand=True)
        #######################################
        
        ############### FRAME H ###############
        self.placeLabel= Label(self.frameH, image=self.placeImage, compound=LEFT, background="#fff173")
        self.placeLabel.pack(side=TOP)
        #######################################
        
        ############### FRAME 1 ############### 
        self.searchLabel = Label(self.frame1, text='Nombre Perfil: ')
        self.searchLabel.config(background="#ffffff")
        self.searchLabel.pack(side=LEFT, padx=5, pady=5)
        self.searchEntry = Entry(self.frame1)
        self.searchEntry.config(background="#ffffff")
        self.searchEntry.pack(side=LEFT, padx=5, pady=5)
        self.searchButton = Button(self.frame1, text='Buscar')
        self.searchButton.pack(side=LEFT, padx=5, pady=5)
        self.questionImageLabel = Label(self.frame1, image=self.questionImage, compound=LEFT, width=1, background="#ffffff")
        self.questionImageLabel.pack(side=LEFT, padx=5, pady=5)
        self.helpOne.label.config(bg='white', image=self.perfilImage)
        self.helpOne.bind_widget(self.questionImageLabel, balloonmsg="Nota: Si quiere una búsqueda más personalizada, acuda a \"contrataciondelestado.es\"")
        #######################################
        
        ############### FRAME 2 ############### 
        self.options=tkinter.StringVar()
        self.options.set("Seleccione una opción")
        option_list = ['']
        self.optionMenu1 = OptionMenu(self.frame2, self.options, *option_list)
        self.optionMenu1.pack(side=TOP, padx=5, pady=5)
        #######################################
        
        ############### FRAME 3 ############### 
        self.fileLabel = Label(self.frame3, text='Introduce el nombre del fichero: ')
        self.fileLabel.config(background="#ffffff")
        self.fileLabel.pack(side=LEFT, padx=5, pady=5)
        self.fileEntry = Entry(self.frame3)
        self.fileEntry.pack(side=LEFT, padx=5, pady=5)
        self.fileButton = Button(self.frame3, text='Leer fichero', command=self.cargarFichero)
        self.fileButton.pack(side=LEFT, padx=5, pady=5)
        self.fileQuestionLabel = Label(self.frame3, image=self.questionImage, compound=LEFT, width=1, background="#ffffff")
        self.fileQuestionLabel.pack(side=LEFT, padx=5, pady=5)
        self.helpTwo.label.config(bg='white')
        self.helpTwo.bind_widget(self.fileQuestionLabel, balloonmsg="En este campo se ha de introducir el nombre del fichero en el que se añadirán los datos")
        self.tickTwoImageLabel = Label(self.frame3, compound=LEFT, width=1, background="#ffffff")
        #######################################
        
        ############### FRAME 4 ############### 
        self.urlLabel = Label(self.frame4, text='Introduce una URL: ')
        self.urlLabel.config(background="#ffffff")
        self.urlLabel.pack(side=LEFT, padx=5, pady=5)
        self.urlEntry = Entry(self.frame4, width=70)
        self.urlEntry.pack(side=LEFT, padx=5, pady=5)
        self.urlButton = Button(self.frame4, text='Cargar Perfil', command=self.crearPerfil)
        self.urlButton.pack(side=LEFT, padx=5, pady=5)
        self.urlQuestionLabel = Label(self.frame4, image=self.questionImage, compound=LEFT, width=1, background="#ffffff")
        self.urlQuestionLabel.pack(side=LEFT, padx=5, pady=5)
        self.helpThree.label.config(bg='white', image=self.enlaceImage)
        self.helpThree.bind_widget(self.urlQuestionLabel, balloonmsg="Nota: Este enlace se debe introducir para generar un CSV con los datos de todos los expedientes")
        self.tickThreeImageLabel = Label(self.frame4, compound=LEFT, width=1, background="#ffffff")
        #######################################
        
        ############### FRAME B ############### 
        self.closeButton = Button(self.frameB, text="Cerrar", command=self.cerrar)
        self.closeButton.pack(side=RIGHT, padx=5, pady=5)
        self.okButton = Button(self.frameB, text="Obtener o Actualizar CSV", command=self.poblarCSV)
        self.okButton.pack(side=RIGHT)
        #######################################
    
    def cargarFichero(self):
        self.ficheroFinal = self.fileEntry.get()
        if self.ficheroFinal[-4:] != '.csv':
            self.tickTwoImageLabel.configure(image=self.crossImage, compound=LEFT, width=1, background="#ffffff")
            self.tickTwoImageLabel.pack(side=LEFT, padx=5, pady=5)
            return   
        fichero = os.getcwd() + '\\' + str(self.ficheroFinal)
        if os.path.exists(fichero):
            try:
                self.data = pd.read_csv(self.ficheroFinal)
                self.data = self.data.drop(['Unnamed: 0'], axis=1)
                self.dataframes.append(self.data)
            except:
                print(self.ficheroFinal, " está vacío.")
                pass
        elif not os.path.exists(fichero):
            f = open(self.ficheroFinal, 'w')
            f.close()
        
        self.tickTwoImageLabel.configure(image=self.tickImage, compound=LEFT, width=1, background="#ffffff")
        self.tickTwoImageLabel.pack(side=LEFT, padx=5, pady=5)
            
    def crearPerfil(self):
        if str(self.urlEntry.get()) not in self.urls:
            self.urls.append(self.urlEntry.get())
            #TODO check perfiles
            perf = Label(self.frame5, text=str(self.urlEntry.get()))
            perf.config(background="#ffffff")
            perf.pack(side=TOP, padx=5, pady=5)
        
    def poblarCSV(self):
        for url in self.urls:
            pagina = Pagina(EstadoPerfil(), Perfil(url), self.data)
            self.dataframes.append(pagina._perfil.data)
        self.data = pd.concat(self.dataframes)
        self.data.to_csv(self.ficheroFinal)
        
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
        
    def cerrar(self):
        self.master.destroy()

