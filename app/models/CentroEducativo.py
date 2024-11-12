from services.googleConnect import calcular_distancias
import re

class CentroEducativo:
    def __init__(self, direccion,codigo_postal, municipio, provincia,codigo_centro,tipo_centro,nombre_centro,publico_privado,bil,compensatoria):
        """
        Constructor de la clase CentroEducativo.

        Esta clase representa un centro educativo con sus atributos básicos y de geolocalización.

        Args:
            direccion (str): Dirección física del centro educativo
            codigo_postal (str): Código postal del centro
            municipio (str): Municipio donde se encuentra el centro
            provincia (str): Provincia donde se ubica el centro
            codigo_centro (str): Código identificativo único del centro
            tipo_centro (str): Tipo de centro educativo (ej: CEIP, IES, etc)
            nombre_centro (str): Nombre completo del centro
            publico_privado (str): Indica si es un centro público o privado

        Attributes:
            distancia_km (float): Distancia en kilómetros hasta el centro (inicialmente None)
            distancia_m (float): Distancia en metros hasta el centro (inicialmente None) 
            duracion (float): Tiempo estimado de llegada en minutos (inicialmente None)
        """
        self.direccion = direccion
        self.codigo_postal = codigo_postal
        self.municipio = municipio
        self.provincia = provincia
        self.codigo_centro = codigo_centro
        self.nombre_centro = nombre_centro
        self.tipo_centro = tipo_centro
        self.publico_privado = publico_privado
        self.bil = bil
        self.compensatoria = compensatoria
        self.distancia_km = None
        self.distancia_m = None
        self.duracion = None

    def __repr__(self):
        """
        Método especial que devuelve una representación en string del objeto CentroEducativo.
        Se usa principalmente para debugging y desarrollo.
        
        Returns:
            str: Representación del centro educativo con su nombre y código
        """
        return f"CentroEducativo({self.nombre_centro}, {self.codigo_centro})"
    
    
    def calcula_distancia_clase(self, direccion_origen):
        """
        Calcula la distancia entre una dirección de origen y el centro educativo.
        Esta función utiliza el servicio de Google Maps para calcular la distancia y tiempo
        de viaje entre dos puntos. Actualiza los atributos del centro con los resultados.
        Args:
            direccion_origen (str): La dirección de origen para calcular la distancia
        Returns:
            bool: True si el cálculo se realizó con éxito, False si hubo error
        Attributes modified:
            distancia_km (float): Distancia en kilómetros hasta el centro
            distancia_m (int): Distancia en metros hasta el centro  
            duracion (str): Tiempo estimado del trayecto
        Example:
            >>> centro.calcula_distancia_clase("Calle Example 123, Ciudad")
            True
        """
        # Construir la dirección completa de destino
        direccion_destino = f"{self.direccion},{self.codigo_postal}, {self.municipio}, {self.provincia}"
        
        # Calcular las distancias usando el servicio de Google
        resultado = calcular_distancias(direccion_origen, direccion_destino)
        
        # Si se obtiene un resultado válido, actualizar los atributos del centro
        if resultado:
            self.distancia_km = resultado['distancia en Km']
            self.distancia_m = resultado['distancia en m']
            self.duracion = resultado['duracion']
            return True
        else:
            # Si no se pudo calcular, mostrar mensaje de error y retornar False
            print(f"No se pudo calcular la distancia para el destino: {direccion_destino}")
            return False
        


    @staticmethod
    def convertir_duracion_a_minutos(duracion_str):
        """
        Convierte una cadena de texto que representa una duración en formato 'Xh Ymin' a minutos totales.

        Args:
            duracion_str (str): Cadena de texto que representa la duración en formato 'Xh Ymin'.
                               Ejemplos válidos: '2h 15min', '1h', '30min'

        Returns:
            int: Total de minutos calculados. Por ejemplo:
                 '2h 15min' -> 135 minutos
                 '1h' -> 60 minutos
                 '30min' -> 30 minutos

        Examples:
            >>> convertir_duracion_a_minutos('2h 15min')
            135
            >>> convertir_duracion_a_minutos('1h')
            60
            >>> convertir_duracion_a_minutos('30min')
            30

        Note:
            - La función utiliza expresiones regulares para extraer las horas y minutos
            - Acepta formatos flexibles siempre que contengan 'h' para horas y/o 'min' para minutos
            - Si la cadena no contiene un formato válido, devolverá 0
        """
        # Función para convertir una duración en formato '2h 15min' a minutos
        partes = re.findall(r'(\d+)\s*(h|min)', duracion_str)
        total_minutos = 0
        for valor, unidad in partes:
            valor = int(valor)
            if unidad == 'h':
                total_minutos += valor * 60  # Convertir horas a minutos
            elif unidad == 'min':
                total_minutos += valor  # Sumar los minutos
        return total_minutos
    
    
