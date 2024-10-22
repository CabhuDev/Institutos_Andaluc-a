from app.services.googleConnect import calcular_distancias
import re

class CentroEducativo:
    def __init__(self, direccion,codigo_postal, municipio, provincia,codigo_centro,tipo_centro,nombre_centro,publico_privado):
        self.direccion = direccion
        self.codigo_postal = codigo_postal
        self.municipio = municipio
        self.provincia = provincia
        self.codigo_centro = codigo_centro
        self.nombre_centro = nombre_centro
        self.tipo_centro = tipo_centro
        self.publico_privado = publico_privado
        self.distancia_km = None
        self.distancia_m = None
        self.duracion = None
    
    def calcula_distancia_clase(self, direccion_origen):
        direccion_destino = f"{self.direccion},{self.codigo_postal}, {self.municipio}, {self.provincia}"
        resultado = calcular_distancias(direccion_origen, direccion_destino)
        if resultado:
            self.distancia_km = resultado['distancia en Km']
            self.distancia_m = resultado['distancia en m']
            self.duracion = resultado['duracion']
            return True
        else:
            print(f"No se pudo calcular la distancia para el destino: {direccion_destino}")
            return False
        

    @staticmethod
    def convertir_duracion_a_minutos(duracion_str):
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
    
    
