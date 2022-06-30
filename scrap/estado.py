from __future__ import annotations
from abc import ABC, abstractmethod
from pyppeteer import launch
from place.perfil import Perfil

import asyncio

class Pagina:
    
    def __init__(self, estado: Estado, perfil: Perfil, data) -> None:
        self._perfil = perfil
        self._estado = estado
        self._data = data
        asyncio.new_event_loop().run_until_complete(self.empezar(estado))
        
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
        return self.pagina
    
    @pagina.setter
    def pagina(self, pagina: Pagina) -> None:
        self._pagina = pagina
        
    @abstractmethod
    def ejecutar(self) -> None:
        pass
    
'''
Acceso a la página principal del perfil
''' 
class EstadoPerfil(Estado):
    async def ejecutar(self) -> None:
        await self._pagina._pagina_actual.goto(self._pagina._perfil.url)
        await self._pagina._pagina_actual.waitFor(100)
        await self._pagina.siguiente_estado(EstadoLicitaciones())
  
''' 
Acceso al apartado de licitaciones por primera vez y número de páginas de la tabla
'''      
class EstadoLicitaciones(Estado):
    async def ejecutar(self) -> None:
        licitaciones = await self._pagina._pagina_actual.querySelector("#viewns_Z7_AVEQAI930GRPE02BR764FO30G0_\:perfilComp\:linkPrepLic")
        await licitaciones.click()
        await self._pagina._pagina_actual.waitForNavigation()
        self._pagina._n_tablas = int(await (
                                        await (
                                            await self._pagina._pagina_actual.querySelector(
                                                "#viewns_Z7_AVEQAI930GRPE02BR764FO30G0_\:form1\:textTotalPaginaasdasd"
                                            )
                                        ).getProperty('textContent')
                                    ).jsonValue()
        )
        
        await self._pagina.siguiente_estado(EstadoLicitacion())
        
'''

'''
class EstadoLicitacion(Estado):
    async def ejecutar(self) -> None:
        # Numero de paginas de la tabla de expedientes
        total_h = await self._pagina._pagina_actual.querySelector("#viewns_Z7_AVEQAI930GRPE02BR764FO30G0_\:form1\:textTotalPaginaasdasd")
        total_paginas = int(await (await total_h.getProperty('textContent')).jsonValue())
        # Bucle para cada pagina de la tabla de expedientes
        for pagina_actual in range(total_paginas):
            # Bucle para cada expediente de la tabla
            for n_expediente  in range(len((await self._pagina._pagina_actual.querySelectorAll('#tableLicitacionesPerfilContratante > tbody > tr')))):
                # Click en el expediente si se puede acceder
                selector = '#tableLicitacionesPerfilContratante > tbody > tr:nth-child(' + str(n_expediente + 1) + ')'
                tr = await self._pagina._pagina_actual.querySelector(selector)
                await self._pagina._pagina_actual.waitFor(250) 
                a = await tr.querySelector('a')
                if str(type(a)) == '<class \'NoneType\'>':
                    continue
                # Id expediente
                id_exp = await (await a.getProperty('textContent')).jsonValue()
                await self._pagina._pagina_actual.waitFor(250)
                est_exp = await (await (await tr.querySelector('td.tdEstado.textAlignLeft')).getProperty('textContent')).jsonValue()
                await self._pagina._pagina_actual.waitFor(250)
                # print('tabla:' + str(est_exp))
                # Comprobar si ya se tiene ese expediente por id y estado
                if id_exp in self._pagina._data['id'].values:
                    query = 'id==\'' + str(id_exp) +'\''
                    dummy = self._pagina._data.query(query)
                    # print(dummy['estado'].tolist())
                    if est_exp in dummy['estado'].tolist():
                        # print('ehe')
                        continue
                await a.click()  
                await self._pagina._pagina_actual.waitForNavigation()
                # Guardar los datos del expediente
                await self.guardar_expediente()
                await self._pagina._pagina_actual.goto(self._pagina._perfil.url)
                await self._pagina._pagina_actual.waitFor(250)
                # Acceso a licitaciones
                licitaciones = await self._pagina._pagina_actual.querySelector("#viewns_Z7_AVEQAI930GRPE02BR764FO30G0_\:perfilComp\:linkPrepLic")
                await licitaciones.click()
                await self._pagina._pagina_actual.waitForNavigation()
            if pagina_actual+1 != total_paginas:
                siguiente = await self._pagina._pagina_actual.querySelector('#viewns_Z7_AVEQAI930GRPE02BR764FO30G0_\:form1\:siguienteLink')
                await siguiente.click()
                await self._pagina._pagina_actual.waitForNavigation()
        await self._pagina._buscador.close()
        
    async def guardar_expediente(self):
        datos = await self._pagina._pagina_actual.querySelector('#DetalleLicitacionVIS_UOE > div.capaAtributos.fondoAtributosDetalle')
        fila = []
        for entrada in range(len(self._pagina._perfil.data.columns)):
            if entrada == 0:
                id_expediente = await (await (await self._pagina._pagina_actual.querySelector('#viewns_Z7_AVEQAI930OBRD02JPMTPG21006_\:form1\:text_Expediente')).getProperty('textContent')).jsonValue()
                fila.append(id_expediente)
            elif entrada == 1:
                fecha_elem = await self._pagina._pagina_actual.querySelector('#myTablaDetalleVISUOE > tbody > tr:nth-child(1) > td.fechaPubLeft.padding0punto2')
                if str(type(fecha_elem)) == '<class \'NoneType\'>':
                    fila.append('')
                else:
                    fecha_expediente = await (await fecha_elem.getProperty('textContent')).jsonValue()
                    fila.append(fecha_expediente)
            else:
                indice = await datos.querySelector('ul:nth-child(' + str(entrada-1) + ') > li:nth-child(2)')
                content = await indice.getProperty('textContent')
                text = (((await content.jsonValue()).strip()).replace("\n", "")).replace("\t","")
                fila.append(text)
        self._pagina._perfil.data.loc[len(self._pagina._perfil.data)] = fila
        

