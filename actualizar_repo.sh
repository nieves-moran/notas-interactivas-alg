#!/bin/bash
docker build -t notas-imagen:latest .
docker tag notas-imagen 793656262514.dkr.ecr.us-east-1.amazonaws.com/notas
aws ecr get-login-password | docker login --username AWS --password-stdin 793656262514.dkr.ecr.us-east-1.amazonaws.com/notas
docker push 793656262514.dkr.ecr.us-east-1.amazonaws.com/notas
