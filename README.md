# Docker + Docker-compose + Selenium + Python

Se puede usar de tres maneras diferentes:

1. Nativo
2. Dockerfile
3. Docker-compose con simulador

## Nativo

Para correrlo nativo debes:

1. Instalar Chrome o Firefox en tu equipo

2. Iniciar el ambiente de trabajo
    ```shell
    virtualenv venv
    source venv/bin/activate
    ```
3. Copiar el .env de la raiz a la carpeta source
    ```shell
   cp .env source/
    ```
   En este caso la configuracion puede ser `source/.env`

    ```dotenv
    ENVIRONMENT=local
    PATH_ASSETS=assets/
    BROWSER=chrome
    EXTENSIONS_CHROME=[""]
    #BROWSER=firefox
    #EXTENSIONS_FIREFOX=[""]
    ```

5. Ingresar a la carpeta `source`
    ```shell
   cd source 
    ```

6. Instalar las dependencias
    ```shell
    python -m pip install --upgrade pip
    pip install -r requirements.txt
   ```
7. Ejecutar el programa
    ```shell
    python app.py
    ```
   