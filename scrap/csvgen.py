# -*- coding: utf-8 -*-

import pandas as pd
import json
import asyncio
from pyppeteer import launch
import os.path
import os
import csv
import warnings
import numpy as np

warnings.simplefilter(action='ignore', category=FutureWarning)

# Funcion para acceder a las licitaciones de un perfil especificando su URL
async def acceder_licitaciones(page, url):
    # Acceso al perfil
    await page.goto(url)
    await page.waitFor(250)
    # Acceso a licitaciones
    licitaciones = await page.querySelector("#viewns_Z7_AVEQAI930GRPE02BR764FO30G0_\:perfilComp\:linkPrepLic")
    await licitaciones.click()
    await page.waitForNavigation()

# Funcion para acceder de uno en uno a todos los expedientes de un perfil
# Crea un diccionario con toda la informacion
async def acceder_expedientes(page, url, df):
    # Numero de paginas de la tabla de expedientes
    total_h = await page.querySelector("#viewns_Z7_AVEQAI930GRPE02BR764FO30G0_\:form1\:textTotalPaginaasdasd")
    total_paginas = int(await (await total_h.getProperty('textContent')).jsonValue())
    # Bucle para cada pagina de la tabla de expedientes
    for pagina_actual in range(total_paginas):
        # Bucle para cada expediente de la tabla
        for n_expediente  in range(len((await page.querySelectorAll('#tableLicitacionesPerfilContratante > tbody > tr')))):
            # Click en el expediente si se puede acceder
            selector = '#tableLicitacionesPerfilContratante > tbody > tr:nth-child(' + str(n_expediente + 1) + ')'
            tr = await page.querySelector(selector)
            await page.waitFor(250) 
            a = await tr.querySelector('a')
            if str(type(a)) == '<class \'NoneType\'>':
                continue
            # Id expediente
            id_exp = await (await a.getProperty('textContent')).jsonValue()
            await page.waitFor(250)
            est_exp = await (await (await tr.querySelector('td.tdEstado.textAlignLeft')).getProperty('textContent')).jsonValue()
            await page.waitFor(250)
            print('tabla:' + str(est_exp))
            # Comprobar si ya se tiene ese expediente por id y estado
            if id_exp in df['id'].values:
                query = 'id==\'' + str(id_exp) +'\''
                dummy = df.query(query)
                print(dummy['estado'].tolist())
                if est_exp in dummy['estado'].tolist():
                    print('ehe')
                    continue
            await a.click()  
            await page.waitForNavigation()
            # Guardar los datos del expediente
            await guardar_expediente(page, df)
            await acceder_licitaciones(page, url)
        if pagina_actual+1 != total_paginas:
            siguiente = await page.querySelector('#viewns_Z7_AVEQAI930GRPE02BR764FO30G0_\:form1\:siguienteLink')
            await siguiente.click()
            await page.waitForNavigation()

# Funcion para guardar en un diccionario la informacion de un expediente
# La pagina tiene que ser la de un expediente
async def guardar_expediente(page, df):
    datos = await page.querySelector('#DetalleLicitacionVIS_UOE > div.capaAtributos.fondoAtributosDetalle')
    fila = []
    for entrada in range(len(df.columns)):
        if entrada == 0:
            id_expediente = await (await (await page.querySelector('#viewns_Z7_AVEQAI930OBRD02JPMTPG21006_\:form1\:text_Expediente')).getProperty('textContent')).jsonValue()
            fila.append(id_expediente)
        elif entrada == 1:
            fecha_elem = await page.querySelector('#myTablaDetalleVISUOE > tbody > tr:nth-child(1) > td.fechaPubLeft.padding0punto2')
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
    df.loc[len(df)] = fila
    
async def main():
    # Abrir el navegador
    browser = await launch({"headless": False, "args": ["--start-maximized"]})
    # Abrir una página nueva
    page = await browser.newPage()
    await page.setViewport({"width": 1600, "height": 900})
    # Cargar los parametros
    with open('param.json', 'r') as paramfile:
        params = json.load(paramfile)
       
    df = None
    if os.path.isfile('datosPLACE.csv'):
        try:
            df = pd.read_csv('datosPLACE.csv')
            df = df.drop(['Unnamed: 0'], axis=1)
            #os.remove('datosPLACE.csv')
        except:
            print('Error al abrir el fichero de lectura')
    else:
        # Diccionario con todos los datos
        dict_expedientes = {'id': [], 'fecha': [], 'organo': [], 'estado': [], 'objeto': [], 'presupuesto': [], 'valor': [], 'tipo': [], 'cpv': [], 'lugar': [], 'procedimiento': []}
        df = pd.DataFrame.from_dict(dict_expedientes)
    #print(df.columns)
    #print(df.to_string())
    # Extraer informacion de todos los perfiles especificados
    for n_perfil in range(len(params['Parametros'])):
        # Acceder a las licitaciones del perfil especificado
        await acceder_licitaciones(page, url=params['Parametros'][n_perfil]['URL'])
        # Crear un diccionario con los datos del perfil
        await acceder_expedientes(page, params['Parametros'][n_perfil]['URL'], df)
    # Crear un fichero CSV a partir del diccionario
    df.to_csv('datosPLACE.csv')

    # Cerrar el navegador
    await browser.close()   

asyncio.get_event_loop().run_until_complete(main())