FROM python:3.7

WORKDIR /app/fastapi

# Copiar fuente de Lambda
COPY ./app ./app
COPY ./requirements.txt ./requirements.txt
COPY ./env ./env

RUN python -m pip install --upgrade pip
RUN python -m pip install uvicorn

# Instalación de paquetes en packages/
RUN pip install -r ./requirements.txt
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--reload", "--port", "8000"]

#docker build -t points-sales .
#docker run -dp 9000:8000 --name points-sales points-sales