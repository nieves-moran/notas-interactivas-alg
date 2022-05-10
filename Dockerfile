FROM ubuntu:20.04
COPY src /src
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip install jupyterlab 
RUN pip install notebook
RUN pip install matplotlib==3.5.1 
RUN pip install ipywidgets 
CMD jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''