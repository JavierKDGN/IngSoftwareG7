Readme hecho por el copilot xd

# Proyecto de Sistema de Reservas

Este proyecto es un sistema de reservas desarrollado en Python utilizando el framework Flask.

## Estructura del Proyecto

- `app/`
  - `__init__.py`: Inicializa la aplicación Flask y carga la configuración.
  - `routes.py`: Define las rutas de la aplicación.
  - `templates/`
    - `test.html`: Plantilla HTML para la página de prueba.
- `migrations`: Directorio con las migraciones de la base de datos.
- `config.py`: Archivo de configuración de la aplicación.
- `sistema_reservas.py`: Punto de entrada de la aplicación.

## Requisitos

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-WTF

## Instalación

1. Clona el repositorio:
    ```sh
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_REPOSITORIO>
    ```

2. Crea un entorno virtual:
    ```sh
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

## Configuración

Asegúrate de configurar las variables de entorno necesarias. Puedes usar un archivo `.env` para esto. La clave secreta para CSRF se puede configurar en el archivo `config.py` o mediante una variable de entorno `SECRET_KEY`.

## Ejecución

Para ejecutar la aplicación, usa el siguiente comando:
```sh
flask run
```
Luego para inicializar la Base de Datos
```sh
flask db init
```

Por ultimo para migrar (actualizar) la BD a su ultima version
```sh
flask db upgrade 
```
Si ocurre un error al correr, entonces se debe repetir el ultimo paso hasta que este en la ultima version
```sh