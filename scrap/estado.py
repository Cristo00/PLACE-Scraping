from __future__ import annotations
from abc import ABC, abstractmethod
from place import *
from pyppeteer import launch
from place.perfil import Perfil
import asyncio

class Pagina:
    
    def __init__(self, estado: Estado, perfil: Perfil) -> None:
        self._loop = asyncio.get_event_loop()
        self._perfil = perfil
        self._estado = estado
        asyncio.get_event_loop().run_until_complete(self.empezar(estado))
        
    async def empezar(self, estado: Estado):
        self._estado = estado
        self._buscador = await launch({"headless": False, "args": ["--start-maximized"]})
        self._pagina_actual = await self._buscador.newPage()
        await self._pagina_actual.setViewport({"width": 1600, "height": 900})
        await self.siguiente_estado(estado)
        
    async def siguiente_estado(self, estado: Estado):
        if estado == None:
            return
        self._estado = estado
        self._estado.pagina = self
        await self.ejecutar_paso()
        
    async def ejecutar_paso(self):
        await self._estado.ejecutar()
        
        
class Estado(ABC):
    @property
    def pagina(self) -> Pagina:
        return self._pagina
    
    @pagina.setter
    def pagina(self, pagina: Pagina) -> None:
        self._pagina = pagina
        
    @abstractmethod
    def ejecutar(self) -> None:
        pass
    
class EstadoPerfil(Estado):
    async def ejecutar(self) -> None:
        print('ESTADO PERFIL')
        await self._pagina._pagina_actual.goto(self._pagina._perfil.url)
        await self._pagina._pagina_actual.waitFor(100)
        await self._pagina.siguiente_estado(EstadoLicitaciones())
        
class EstadoLicitaciones(Estado):
    async def ejecutar(self) -> None:
        print('ESTADO LICITACION')
        licitaciones = await self.pagina._pagina_actual.querySelector("#viewns_Z7_AVEQAI930GRPE02BR764FO30G0_\:perfilComp\:linkPrepLic")
        await licitaciones.click()
        await self._pagina._pagina_actual.waitForNavigation()
        await self._pagina.siguiente_estado(EstadoExpediente())
        
class EstadoExpediente(Estado):
    async def ejecutar(self) -> None:
        print('ESTADO EXPEDIENTE')

    
