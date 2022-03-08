# Demo - Microservicio - Lambda

Microservicio para las api CRUD de User
Utilizamos el servicio gratuito de Mysql

## INSTALACIÓN

### Crear ENV VirtualEnv
```
python3 -m pip install --upgrade pip
pip3 install virtualenv
virtualenv -p python3.6 env --clear

LINUX: source env/bin/activate  && deactivate
WINDOWS: .\env\Scripts\activate && deactivate
```
### Instalar dependencicas
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Iniciar Aplicación con UVICORN LOCAL
```
uvicorn app.api:app --reload --port 7000 || python -m uvicorn app.api:app --reload --port 7000
```

## Iniciar Aplicación con Docker Local
```
docker build -t fastapi-demo .
docker run -dp 9000:8000 fastapi-demo
browser: http://localhost:9000/docs
```

## Testing
```
pip install pytest
pytest
```

## INSTALACIÓN
## Crear modelo en base de datos
```
python .\seeds\create_db.py
```

## DEPLOY CON DOCKER
### Crear repositorio en ECR
```
Nombre: app-demo-fastapi
```

### Ingresar al docker login
```
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 854529565818.dkr.ecr.us-east-2.amazonaws.com
```

### Generar Imagen y subir
```
docker build -t app-demo-fastapi:0.1.0-stage . -f Dockerfile.aws.lambda
docker tag app-demo-fastapi:0.1.0-stage 854529565818.dkr.ecr.us-east-2.amazonaws.com/app-demo-fastapi:0.1.0-stage
docker push 854529565818.dkr.ecr.us-east-2.amazonaws.com/app-demo-fastapi:0.1.0-stage
```
### Crear lambda 
```
Crear por imagen de contenedor
Nombre: fastapi-mysql-demo
Examinar imagenes
Seleccionar app-demo-fastapi
Selccionar la version que hemos subido: 0.1.0-stage
Crear función
```

### Crear un endpoint ApiGateway
```
Crear por API REST - API Nueva
Nombre: fastapi-mysql-demo
Crear Recurso: Selecciona recurso de Proxy
  Nombre recurso: proxy
  Ruta recurso: {proxy+}
Seleccionar en Any y escoger la lambda: fastapi-mysql-demo
Seleccionar en Proxy e implementar API
Nueva etapa: stage
```


## Script
Crear usuario cognito
```
python .\scripts\cognito\create_user.py -u +51900000000 -p passwordtemporal -n "Mis nombres" -d 03600000 -e huas@gmail.com
python .\scripts\cognito\create_user.py -u +51918558986 -p factura12 -n "walter santin zapata" -d 73318291 -e hugo.93wal@gmail.com
```