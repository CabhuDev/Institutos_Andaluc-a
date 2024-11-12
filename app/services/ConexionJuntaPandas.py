import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Datos de la API
API_URL = 'https://www.juntadeandalucia.es/datosabiertos/portal/api/3/action/datastore_search'
resource_id = os.getenv("resource_id")



"""##-- EXTRACIÓN DE DATOS DE LA API --##"""
# Obtener datos de los centros desde la API de la Junta de Andalucía
def obtener_centros(limit=2000):
    params = {
        'resource_id': '82f92e32-c5ee-4c60-8643-bfb19e130cef',  # ID del recurso
        'limit': limit
    }
    
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['result']['records']
    else:
        print(f"Error al obtener los datos: {response.status_code}")
        return []


"""##-- FILTROS --##"""
# Filtrar centros por provincia especificada
def filtrar_centros_por_provincia(centros, provincia):
    """
    Filtra los centros educativos por provincia y tipo de centro (IES).
    Esta función toma una lista de centros educativos y filtra aquellos que son 
    Institutos de Educación Secundaria (IES) en la provincia especificada.
    Args:
        centros (list): Lista de diccionarios con la información de los centros educativos.
                        Cada diccionario debe contener las claves 'D_DENOMINA' y 'D_PROVINCIA'.
        provincia (str): Nombre de la provincia por la que filtrar los centros.
    Returns:
        list: Lista de diccionarios conteniendo solo los IES de la provincia especificada.
              Cada diccionario mantiene toda la información original del centro.
    Example:
        >>> centros = [{'D_DENOMINA': 'Instituto de Educación Secundaria', 'D_PROVINCIA': 'SEVILLA'}, ...]
        >>> filtrar_centros_por_provincia(centros, 'SEVILLA')
        [{'D_DENOMINA': 'Instituto de Educación Secundaria', 'D_PROVINCIA': 'SEVILLA'}, ...]
    """
    centros_filtrados = []
    for centro in centros:
        denominacion_centro = centro.get("D_DENOMINA")
        provincia_centro = centro.get("D_PROVINCIA")
        
        # Filtrar solo los centros que tienen coordenadas y coinciden con la provincia
        if denominacion_centro == "Instituto de Educación Secundaria" and provincia_centro == provincia:
            centros_filtrados.append(centro)
    
    return centros_filtrados

# Filtrar TODOS  Bilingües
def filtrar_todos_centros_bil(centros):
    """
    Filtra los centros que son institutos de educación secundaria y tienen programas bilingües.
    Esta función examina una lista de centros educativos y selecciona aquellos que son 
    específicamente institutos de educación secundaria (IES) y que además tienen programas 
    bilingües que incluyen inglés en diferentes modalidades (bilingüe o plurilingüe).
    Args:
        centros (list): Lista de diccionarios donde cada diccionario contiene información 
                        de un centro educativo. Cada centro debe tener las claves 'D_DENOMINA' 
                        y 'ESO'.
    Returns:
        list: Lista filtrada de centros que cumplen ambas condiciones:
              - Son institutos de educación secundaria
              - Tienen programas bilingües que incluyen inglés
    Example:
        >>> centros = [{'D_DENOMINA': 'Instituto de Educación Secundaria', 'ESO': 'BIL ING'}, ...]
        >>> filtrar_todos_centros_bil(centros)
        [{'D_DENOMINA': 'Instituto de Educación Secundaria', 'ESO': 'BIL ING'}, ...]
    """
    centros_filtrados = []
    for centro in centros:
        denominacion_centro = centro.get("D_DENOMINA")
        es_bilingue_ing = centro.get("ESO")
        
        # Filtrar solo los centros de educación secundaria y bilingües
        if denominacion_centro == "Instituto de Educación Secundaria" and es_bilingue_ing in["PLURIL FRA/ING","BIL ING","PLURIL ING/FRA","BIL ING + PLURIL ING/FRA","BIL ING + PLURIL ING/ALE","PLURIL ING/FRA + PLURIL FRA/ING","BIL ING + BIL FRA"]:
            centros_filtrados.append(centro)
    
    return centros_filtrados


# Filtrar TODOS IES
def filtrar_todos_centros(centros):
    """
    Filters education centers to return only secondary education institutes.
    Args:
        centros (list): A list of dictionaries containing information about education centers.
                        Each dictionary should have 'D_DENOMINA' and 'ESO' keys.
    Returns:
        list: A filtered list of dictionaries containing only secondary education institutes.
              Returns an empty list if no centers match the criteria.
    Example:
        >>> centers = [
                {"D_DENOMINA": "Instituto de Educación Secundaria", "ESO": True},
                {"D_DENOMINA": "Colegio de Educación Infantil y Primaria", "ESO": False}
            ]
        >>> filtrar_todos_centros_bil(centers)
        [{"D_DENOMINA": "Instituto de Educación Secundaria", "ESO": True}]
    """

    centros_filtrados = []
    for centro in centros:
        denominacion_centro = centro.get("D_DENOMINA")        
        # Filtrar solo los centros de educación secundaria
        if denominacion_centro == "Instituto de Educación Secundaria":
            centros_filtrados.append(centro)
    
    return centros_filtrados



# Filtrar centros por provincia especificada de educación secundaria y bilingües
def filtrar_centros_por_provincia_bil(centros, provincia):
    centros_filtrados = []
    for centro in centros:
        denominacion_centro = centro.get("D_DENOMINA")
        provincia_centro = centro.get("D_PROVINCIA")
        es_bilingue_ing = centro.get("ESO")
        
        # Filtrar solo los centros que tienen coordenadas y coinciden con la provincia
        if denominacion_centro == "Instituto de Educación Secundaria" and es_bilingue_ing in["PLURIL FRA/ING","BIL ING","PLURIL ING/FRA","BIL ING + PLURIL ING/FRA","BIL ING + PLURIL ING/ALE","PLURIL ING/FRA + PLURIL FRA/ING","BIL ING + BIL FRA"]  and provincia_centro == provincia:
            centros_filtrados.append(centro)
    
    return centros_filtrados


"""##-- CONSULTAS --##"""
def consulta_todos_centros_bil(limit = 3000 ):
    centros = obtener_centros(limit)  # Puedes ajustar el límite
    centros_filtrados = filtrar_todos_centros_bil(centros)
    df = pd.DataFrame(centros_filtrados)
    return (df[["D_DOMICILIO","C_POSTAL","D_MUNICIPIO","D_PROVINCIA","D_DENOMINA","D_ESPECIFICA","codigo","D_TIPO","ESO"]])



def consulta_todos_centros(limit = 3000 ):
    centros = obtener_centros(limit)  # Puedes ajustar el límite
    centros_filtrados = filtrar_todos_centros(centros)
    df = pd.DataFrame(centros_filtrados)
    return (df[["D_DOMICILIO","C_POSTAL","D_MUNICIPIO","D_PROVINCIA","D_DENOMINA","D_ESPECIFICA","codigo","D_TIPO","ESO"]])



def consulta_direccion(provincia_destino,limit = 1800 ):
    centros = obtener_centros(limit)  # Puedes ajustar el límite
    centros_filtrados = filtrar_centros_por_provincia(centros, provincia_destino)
    df = pd.DataFrame(centros_filtrados)
    return (df[["D_DOMICILIO"]])


def consulta_direccion_municipio_provincia(provincia_destino,limit = 1800 ):
    centros = obtener_centros(limit)  # Puedes ajustar el límite
    centros_filtrados = filtrar_centros_por_provincia_bil(centros, provincia_destino)
    df = pd.DataFrame(centros_filtrados)
    return (df[["D_DOMICILIO","C_POSTAL","D_MUNICIPIO","D_PROVINCIA","D_DENOMINA","D_ESPECIFICA","codigo","D_TIPO","ESO"]])



"""# Ejemplo de uso
def main():
    provincia = "Córdoba"  # Especificar la provincia por la que se desea filtrar
    return consulta_direccion_municipio_provincia(provincia)


print(main())

print(consulta_todos_centros())
"""


