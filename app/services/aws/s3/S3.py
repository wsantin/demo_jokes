import boto3
import time
import io
from botocore.config import Config as ConfigBotoCore
from botocore.exceptions import ClientError
from datetime import datetime, timezone

class S3Service():
    
    AWS_ACCESS_KEY_ID = None
    AWS_SECRET_ACCESS_KEY = None
    AWS_S3_REGION = None
    AWS_S3_BUCKET = None
    TYPE_ROUTE_TELE_ASSISTANCE_NAME_FARMER = None
    TYPE_ROUTE_TELE_ASSISTANCE_NAME_TELE_ASSISTANCE = None
    TYPE_ROUTE_TELE_ASSISTANCE_NAME_INFORMATION = None

    def __init__(self, serviceEnv):
        self.AWS_ACCESS_KEY_ID = serviceEnv.AWS_ACCESS_KEY_ID
        self.AWS_SECRET_ACCESS_KEY = serviceEnv.AWS_SECRET_ACCESS_KEY
        self.AWS_S3_REGION = serviceEnv.AWS_S3_REGION
        self.AWS_S3_BUCKET = serviceEnv.AWS_S3_BUCKET
        self.TYPE_ROUTE_TELE_ASSISTANCE_NAME_FARMER = serviceEnv.TYPE_ROUTE_TELE_ASSISTANCE_NAME_FARMER
        self.TYPE_ROUTE_TELE_ASSISTANCE_NAME_TELE_ASSISTANCE = serviceEnv.TYPE_ROUTE_TELE_ASSISTANCE_NAME_TELE_ASSISTANCE
        self.TYPE_ROUTE_TELE_ASSISTANCE_NAME_INFORMATION = serviceEnv.TYPE_ROUTE_TELE_ASSISTANCE_NAME_INFORMATION

    def config_s3(self):
        """Configuracion de S3"""
        return ConfigBotoCore(
            retries = dict(
                max_attempts = 10
        )
    )   
        
    def get_s3_resource(self):
        """Coneción de S3 por metodo Resource"""
        
        return boto3.resource('s3',
            region_name = self.AWS_S3_REGION,
            aws_access_key_id =  self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = self.AWS_SECRET_ACCESS_KEY,
            config = self.config_s3()
        )

    def get_s3_client(self):
        """Coneción de S3 por metodo Cliente"""
        
        return boto3.client('s3',
            region_name =  self.AWS_S3_REGION,
            aws_access_key_id = self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key =  self.AWS_SECRET_ACCESS_KEY,
            config = self.config_s3()
        )

    def upload_file(self, keyUrl='', body='', ContentType='', bucket=None):
        """Subir archivos a S3
        :param keyUrl: ruta y nombre de la URL. Example: /username/1/photo.png || *.txt || ..etc
        :param body: DataObjt Parser
        :param ContentType: Headers Content-Type
        :param bucket: Nombre del bucket en S3
        """
        
        if bucket is None:
            bucket = self.AWS_S3_BUCKET
            
        #Verificamos si existe body
        if body is None:
            body=''
        
        try:
            self.get_s3_client().put_object(Bucket=bucket, Key=keyUrl,  Body=body, ACL='public-read', ContentType=ContentType)
            return True
        
        except ClientError as e:
            return False

    def get_s3_url(self, bucket=None, region=None):
        """Obtener la Ruta del S3
        :param bucket: Nombre del bucket en S3
        :param region: region del Bucket
        """
        
        if bucket is None:
            bucket = self.AWS_S3_BUCKET
            
        if region is None:
            region = self.AWS_S3_REGION
        
        return "https://{}.s3.{}.amazonaws.com/".format(bucket, region)
    
    def read_key_s3(self, keyUrl='', bucket=None):
        """Leer un archivo en S3 mediante una ruta
        :param keyUrl: ruta y nombre de la URL. Example: /username/1/archivo.txt || .png || ..etc
        :param bucket: Nombre del bucket en S3
        """
        
        if bucket is None:
            bucket = self.AWS_S3_BUCKET

        try:

            fileobj = self.get_s3_client().get_object(
                Bucket= bucket,
                Key=  keyUrl
            )
            readKey = fileobj['Body'].read()
            # contentObj = readKey.decode('utf-8')

            return readKey

        except:
            time.sleep(1)
            pass
        
    def qualify_key_s3(self, key='', bucket=None):
        """Obtener cantidad de objetos que hay dentor de una ruta
        :param keyUrl: ruta y nombre de la URL. Example: /username/1/
        :param bucket: Nombre del bucket en S3
        """
        
        count = 0
        prefix = key
        
        if bucket is None:
            bucket = self.AWS_S3_BUCKET

        paginator = self.get_s3_client().get_paginator('list_objects_v2')
        response_iterator = paginator.paginate( Bucket=bucket, Prefix=prefix, Delimiter='')

        for page in response_iterator:
            for obj in page['Contents']:
                count=count+1

        return count
    
    def qualify_key_s3_notxt(self, keyUrl='', bucket=None):
        
        """Obtener cantidad de objetos que hay dentor de una ruta a excepcion de los formatos *.txt
        :param keyUrl: ruta y nombre de la URL. Example: /username/1/
        :param bucket: Nombre del bucket en S3
        """
        
        count = 0
        prefix = keyUrl
        
        if bucket is None:
            bucket = self.AWS_S3_BUCKET

        paginator = self.get_s3_client().get_paginator('list_objects_v2')
        response_iterator = paginator.paginate( Bucket=bucket, Prefix=prefix, Delimiter='')

        for page in response_iterator:
            for obj in page['Contents']:
                
                objKey = obj.get('Key')

                #No mostrar los txt
                if objKey.find('.txt') == -1:
                    count=count+1

        return count
    
    def qualify_key_s3_scout(self, user_id,tele_assistance_id,rutaTipo, bucket=None, flow_name=None):
        
        countImages = 0
        countAudio = 0
        countVideos = 0
        
        if bucket is None:
            bucket = self.AWS_S3_BUCKET
        if flow_name is None:
            flow_name = ''

        prefix = '{}/{}/{}/{}/{}/{}'.format(self.TYPE_ROUTE_TELE_ASSISTANCE_NAME_FARMER,
                                                user_id,
                                                self.TYPE_ROUTE_TELE_ASSISTANCE_NAME_TELE_ASSISTANCE,
                                                tele_assistance_id,
                                                flow_name,
                                                rutaTipo)
        
        paginator = self.get_s3_client().get_paginator('list_objects_v2')
        response_iterator = paginator.paginate( Bucket=bucket, Prefix=prefix, Delimiter='')
         
        try:
            for page in response_iterator:
            
                for obj in page['Contents']:
                    
                    objKey = obj.get('Key')

                    #No mostrar los txt
                    if objKey.find('.txt') == -1:
                
                        if objKey.find('.jpeg') >= 0:
                            countImages = countImages + 1
                        elif (objKey.find('.ogg') >= 0) or (objKey.find('.mp3') >= 0) or (objKey.find('.wav') >= 0):
                            countAudio = countAudio +1
                        elif objKey.find('.mp4') >= 0:
                            countVideos = countVideos +1

            return {
                "countImages" : countImages, 
                "countAudio" : countAudio,
                "countVideos" : countVideos 
            }
        except:
            return{
                "countImages" : 0, 
                "countAudio" : 0,
                "countVideos" : 0 
            }