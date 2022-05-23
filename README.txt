
El repositorio tiene el archivo de Docker para crear el contenedor
con todas las dependencias necesarias para ejecutar las notas. 
Los pasos a continuación muestran como crearlo y acceder a las notas: 
Instalar Docker. 
Construir la imagen ejecutando el siguiente comando en la 
carpeta donde se encuentra el Dockerfile: 
    docker build -t notas .
Lanzar el contenedor con este comando: 
    docker run -d -p 8888:8888 notas
Acceder a la siguiente liga: 
    http://localhost:8888/notebooks/src/indice/indice.ipynb
Recuerda tener la version más reciente del repositorio. 