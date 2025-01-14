"""
Script principal para obtener y procesar información sobre centros educativos.
Este script permite obtener datos de centros educativos desde una base de datos, calcular
las distancias desde una dirección de origen hasta cada centro, y mostrar/exportar los
resultados ordenados por tiempo de viaje.
Variables globales:
    direccion_origen (str): Dirección desde la cual se calcularán las distancias
    provincia_destino (str): Provincia para filtrar los centros educativos (opcional)
Flujo principal:
1. Obtiene listado de centros educativos (filtrado por provincia o completo)
2. Para cada centro:
    - Crea objeto CentroEducativo
    - Calcula distancia desde dirección origen
3. Ordena centros por duración del trayecto
4. Muestra resultados por consola
5. Opcionalmente exporta resultados a CSV
Dependencias:
    - services.ConexionJuntaPandas: Para consultas a la base de datos
    - models.CentroEducativo: Modelo de datos para centros educativos
    - pandas: Para manejo de datos tabulares
    - dotenv: Para gestión de variables de entorno
Notas:
    - Los tiempos son calculados usando la API de Google Maps
    - Las distancias se muestran en kilómetros
    - Los códigos de centro se muestran resaltados en amarillo
    - Las distancias y duraciones se muestran resaltadas en verde
"""

from services.ConexionJuntaPandas import consulta_direccion_municipio_provincia, consulta_todos_centros
from models.CentroEducativo import CentroEducativo
import pandas as pd

# Importar dotenv_values desde dotenv para leer variables de entorno
from dotenv import dotenv_values
# Imprimir todas las variables de entorno cargadas del archivo .env
print(dotenv_values())

# Dirección de origen proporcionada por el usuario
direccion_origen = "Calle Costa Rica 49, 18194, Churriana de la Vega, Granada"

# Provincia de destino para filtrar los centros educativos
provincia_destino = "Granada"



def creacion_csv_bil(direccion_origen):

    """###-------------------------------------------------------------------------------------###"""
    """###--- DATOS POR PROVINCIA ---###"""
    # Obtener la lista de direcciones de centros en la provincia especificada
    # direcciones_centros = consulta_direccion_municipio_provincia(provincia_destino)

    """###--- LISTADO COMPLETO ---###"""
    # Obtener la lista de direcciones de TODOS los centros sin filtro de provincia
    direcciones_centros = consulta_todos_centros()
    """###-------------------------------------------------------------------------------------###"""

    # Asegurarnos de que tenemos al menos una dirección
    if not direcciones_centros.empty:
        # Lista para almacenar los objetos de centros educativos
        centros_educativos = []
        
        # Iterar sobre todas las direcciones de la lista y crear objetos CentroEducativo
        for i, row in direcciones_centros.iterrows():
            centro = CentroEducativo(
                direccion=row["D_DOMICILIO"],
                codigo_postal = row["C_POSTAL"],
                municipio=row["D_MUNICIPIO"],
                provincia=row["D_PROVINCIA"],
                tipo_centro=row["D_DENOMINA"],
                nombre_centro=row["D_ESPECIFICA"],
                codigo_centro = row["codigo"],
                publico_privado = row["D_TIPO"],
                bil = row["ESO"],
                compensatoria="No"
            )
            
            # Calcular la distancia desde la dirección de origen
            if centro.calcula_distancia_clase(direccion_origen):
                centros_educativos.append(centro)
        

        # Ordenar los centros por duración estimada (convertida a minutos)
        centros_educativos_ordenados = sorted(centros_educativos, key=lambda x: CentroEducativo.convertir_duracion_a_minutos(x.duracion) if x.duracion is not None else float('inf'))


        """###--- MOSTRAR DATOS ---###"""
        # Mostrar los resultados ordenados
        for centro in centros_educativos_ordenados:
            #Resalta el codigo por consola
            codigo_centro_resaltado = f"\033[93m{centro.codigo_centro}\033[0m" 
            distancia_resaltada = f"\033[92m{centro.distancia_km}\033[0m"
            duracion_resaltada = f"\033[92m{centro.duracion}\033[0m"

            print(f"\n##-- Código:{codigo_centro_resaltado}-Centro {centro.publico_privado} {centro.tipo_centro } {centro.bil}-{ centro.nombre_centro}||{centro.municipio},{centro.provincia} --##")
            #print(f"Distancia desde '{direccion_origen}' hasta '{centro.direccion}, {centro.municipio}, {centro.provincia}':")
            print(f"- Distancia: {distancia_resaltada}")
            print(f"- Duración estimada: {duracion_resaltada}")

        """###--- EXPORTAR DATOS ---###"""
        # Crear un DataFrame para exportar los resultados
        datos_exportar = []
        for centro in centros_educativos_ordenados:
            datos_exportar.append({
                "Código Centro": centro.codigo_centro,
                "Tipo Centro": centro.tipo_centro,
                "Nombre Centro": centro.nombre_centro,
                "Público/Privado": centro.publico_privado,
                "Dirección": centro.direccion,
                "Código Postal": centro.codigo_postal,
                "Municipio": centro.municipio,
                "Provincia": centro.provincia,
                "Distancia (Km)": centro.distancia_km,
                "Duración": centro.duracion,
                "Idiomas": centro.bil
            })

        df_exportar = pd.DataFrame(datos_exportar)
        
        # Exportar el DataFrame a un archivo CSV
        df_exportar.to_csv("centros_educativos_ordenados.csv", index=False, encoding='utf-8-sig')
        print("Los datos se han exportado correctamente a 'centros_educativos_ordenados.csv'")


    else:
        print("No se encontraron direcciones de centros en la provincia especificada.")





