
El repositorio tiene el archivo de Docker para crear el contenedor
con todas las dependencias necesarias para ejecutar las notas. 
Los pasos a continuación muestran como crearlo y acceder a las notas: 
Instalar Docker. 
Construir la imagen con el siguiente comando: 
    docker build -t jupyter_image .
Lanzar el contenedor con este comando: 
    docker run -d -p 8888:8888 jupyter_image
Acceder a la siguiente liga: 
    http://localhost:8888/notebooks/usr/notas/