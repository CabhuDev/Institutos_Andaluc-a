# Backend de Aplicación de Centros Educativos

## Descripción
Este proyecto es un backend desarrollado en Python para una aplicación que consulta un listado de centros educativos disponibles en la Junta de Andalucía y permite ordenarlos por distancia a una ubicación dada. La aplicación utiliza FastAPI para exponer la API, y está integrada con la API de Google Maps para calcular las distancias entre los centros y la ubicación proporcionada.

## Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py               # Punto de entrada principal para iniciar el servidor (FastAPI)
│   ├── models/
│   │   ├── CentroEducativo.py # Modelos de datos
│   ├── services/
│   │   ├── ConexionJuntaPandas.py  # Conexión con la API de la Junta de Andalucía usando Pandas
│   │   ├── googleConnect.py       # Conexión con Google Maps API
│   ├── routers/
│   │   ├── centros.py            # Endpoints relacionados con los centros educativos
├── requirements.txt        # Dependencias del proyecto
└── README.md
```

### Archivos y Carpetas Principales
- **`main.py`**: Archivo principal para ejecutar el servidor de FastAPI.
- **`models/`**: Contiene los modelos de datos que representan los centros educativos.
- **`services/`**: Contiene los servicios que interactúan con la API de la Junta y Google Maps.
- **`routers/`**: Contiene los endpoints que expone el backend para gestionar la información de los centros educativos.

## Instalación

Sigue estos pasos para instalar y ejecutar el proyecto en tu entorno local.

### Requisitos Previos
- Python 3.9 o superior
- `pip` para gestionar paquetes de Python

### Instrucciones
1. Clona el repositorio:
   ```sh
   git clone <URL_DEL_REPOSITORIO>
   cd backend
   ```

2. Crea y activa un entorno virtual:
   ```sh
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```

4. Configura las claves necesarias para la API de Google Maps:
   - Crea un archivo `.env` en la carpeta raíz del proyecto y añade la clave de API de Google Maps:
     ```
     GOOGLE_MAPS_API_KEY=<tu_clave_api>
     ```

5. Ejecuta la aplicación:
   ```sh
   uvicorn app.main:app --reload
   ```

6. Accede a la documentación interactiva de la API (Swagger) en:
   [http://localhost:8000/docs](http://localhost:8000/docs)

## Endpoints Principales

- **`GET /api/centros`**: Devuelve una lista de centros educativos, permitiendo filtrado por provincia o distancia.
- **`POST /api/centros/ordenar`**: Ordena los centros por distancia a una ubicación dada.

## Ejemplo de Uso
Puedes usar herramientas como `curl` o Postman para interactuar con la API.

Ejemplo con `curl` para obtener centros educativos en una provincia específica:
```sh
curl -X GET "http://localhost:8000/api/centros?provincia=Almería"
```

## Tecnologías Utilizadas
- **Python**
- **FastAPI**: Framework para construir APIs de manera rápida y eficiente.
- **Pandas**: Para gestionar y manipular los datos de los centros educativos.
- **Google Maps API**: Para calcular las distancias entre ubicaciones.

## Contribuciones
Las contribuciones son bienvenidas. Si deseas colaborar, por favor, abre un issue o crea un pull request en el repositorio.

## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
