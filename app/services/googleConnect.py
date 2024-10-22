# Geocodificación del Origen (si el usuario introduce una dirección): 
# Utiliza la API de geocodificación de Google Maps para convertir la dirección del usuario en coordenadas. 
# Esta conversión es necesaria si el usuario introduce una dirección en lugar de coordenadas.

import googlemaps
import googlemaps.distance_matrix
import googlemaps.geocoding


GOOGLE_MAPS_API_KEY = 'AIzaSyCHz6LeaKlnFSES-7x5wolAcmT2VxuHtU8'

# Función para obtener las coordenadas de una dirección proporcionada por el usuario
def obtener_coordenadas(direccion_usuario: str) -> tuple:
    try:
        # Inicializar el cliente de Google Maps con la API Key
        gmaps = googlemaps.Client(GOOGLE_MAPS_API_KEY)
        
        # Realizar la geocodificación de la dirección proporcionada para obtener resultados de ubicación
        geocode_result = googlemaps.geocoding.geocode(gmaps,direccion_usuario)
        
        # Verificar si la respuesta contiene resultados
        if geocode_result:
            # Extraer la latitud y longitud del primer resultado
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
            print(lat)
            print(lng)
            return lat, lng
        else:
            # Imprimir un mensaje si no se encontraron coordenadas para la dirección
            print("No se pudieron obtener coordenadas para la dirección proporcionada.")
    except Exception as e:
        # Capturar cualquier excepción y mostrar el mensaje de error
        print(f"Error al obtener coordenadas: {e}")


    # Devolver None, None si no se pudo obtener la geocodificación
    return None, None


# Función para calcular la distancia entre dos direcciones proporcionadas 
def calcular_distancias(direccion_origen: str, direccion_destino: str) -> dict:
    try:
        # Inicializar el cliente de Google Maps con la API Key
        gmaps = googlemaps.Client(GOOGLE_MAPS_API_KEY)

        # Realizar la consulta de distancia entre el origen y el destino
        result = googlemaps.distance_matrix.distance_matrix(gmaps,origins=direccion_origen, destinations=direccion_destino,language="ES", mode="driving")
        
        # Verificar si la respuesta contiene resultados
        if result['rows'] and result['rows'][0]['elements'] and result['rows'][0]['elements'][0]['status'] == 'OK':
            # Extraer la distancia y la duración de los resultados
            distancia_km = result['rows'][0]['elements'][0]['distance']['text']  # Extraer la distancia en formato legible (ej. '10 km')
            distancia_value = result['rows'][0]['elements'][0]['distance']['value']  # Extraer la distancia en formato valor en metros
            duracion = result['rows'][0]['elements'][0]['duration']['text']  # Extraer la duración estimada del viaje en formato legible (ej. '15 mins')
            return {
                "distancia en Km": distancia_km,  # Devolver la distancia como parte del resultado
                "distancia en m": distancia_value,  # Devolver la distancia como parte del resultado
                "duracion": duracion  # Devolver la duración como parte del resultado
            }
        else:
            # Imprimir un mensaje si no se pudo calcular la distancia
            print("No se pudo calcular la distancia para las direcciones proporcionadas.")
    except Exception as e:
        # Capturar cualquier excepción y mostrar el mensaje de error
        print(f"Error al calcular la distancia: {e}")
        
    # Devolver un diccionario vacío si no se pudo calcular la distancia
    return {}


"""#-- PRUEBA DE LAS FUNCIONES --#
direccion_origen = "Calle Costa Rica 49, 18194, Churriana de la Vega, Granada"
direccion_destino = " C/ La Salud, 6     14100               La Carlota     Córdoba"
coordenadas_origen = obtener_coordenadas(direccion_origen)
coordenadas_destino = obtener_coordenadas(direccion_destino)
print("------------------")
print(coordenadas_origen)
print(coordenadas_destino)

#IES JOSE MARÍN
lat_test = 37.65969
lng_test = -2.07848
destino = f"{lat_test},{lng_test}"
print (destino)

print("------------------")
print(calcular_distancias(direccion_origen,direccion_destino))"""
