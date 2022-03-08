import boto3
from botocore.exceptions import ClientError
from configs.environment import Config
import pytz
from uuid import uuid4
from datetime import datetime

tz = pytz.timezone(Config.TIME_ZONE)

class DyanmoDbService():
    AWS_ACCESS_KEY_ID = None
    AWS_SECRET_ACCESS_KEY = None
    AWS_REGION = None
    DATABASE_DYNAMODB_URL = None

    def __init__(self, serviceEnv):
        self.AWS_ACCESS_KEY_ID = serviceEnv.AWS_ACCESS_KEY_ID
        self.AWS_SECRET_ACCESS_KEY = serviceEnv.AWS_SECRET_ACCESS_KEY
        self.AWS_REGION = serviceEnv.AWS_REGION
        self.DATABASE_DYNAMODB_URL = serviceEnv.DATABASE_DYNAMODB_URL
        
    def get_dynamo_db_resource(self):
        """Coneción de Dynamo DB"""
        
        return boto3.resource(
            'dynamodb',
            region_name = self.AWS_REGION,
            endpoint_url = self.DATABASE_DYNAMODB_URL,
            aws_access_key_id = self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key = self.AWS_SECRET_ACCESS_KEY
        )

    def put_item_dynamo_db(self, tableName, item):
        """Crea una nueva coleccion de elementos

        Args:
            tableName (string): El nombre de la tabla
            item (dict): La coleccion de elementos

        Returns:
            boolean: Verdadero si fue exitoso y falso si hubo error
        """
        try:
            table = self.get_dynamo_db_resource().Table(tableName)
            table.put_item(
                Item=item
                )
            return True

        except ClientError as e:
            print('error al guardar el item',str(e))
            return False
        
    def update_item_dynamo_db(self, tableName, key, expression, newItem):
        """Actualiza una coleccion

        Args:
            tableName (string): El nombre de la tabla
            key (string|integer): Llave primaria con el que se va idenbificar la coleccion
            expression (string): Indica que atributos seran actualizados
            newItem (dict): La nueva coleccion de elementos

            Ejemplo:

                tableName = 'Call'
                key={
                'id': 0dd84228-0ced-4de7-82e1-aadf28a5e63a,
                }
            
                expression='SET intent = :intent, status_call = :status_call'
            
                newItem={
                        ':intent': 4,
                        ':status_call': 'enviado',
                }
            
                response = update_item_dynamo_db(tableName,key,expression,newItem)

        Returns:
            boolean: Verdadero si fue exitoso y falso si hubo error
        """

        try:
            table = self.get_dynamo_db_resource().Table(tableName)
            table.update_item(
            Key=key,
            UpdateExpression=expression,
            ExpressionAttributeValues=newItem,
            ReturnValues="UPDATED_NEW"
            )

            return True
        except ClientError as e:
            print('error al guardar el item',str(e))
            return False


    def communication_log(self, interaction_info):
        interaction_info_keys = list(interaction_info.keys())
        
        item = {
            'id': interaction_info['id'] if 'id' in interaction_info_keys else uuid4(),
            'from_user_type': interaction_info['from_user_type'] if 'from_user_type' in interaction_info_keys else None  ,
            'from_user_id': interaction_info['from_user_id'] if 'from_user_id' in interaction_info_keys else None,
            'from_phone': interaction_info['from_phone'] if 'from_phone' in interaction_info_keys else None,
            'to_user_type': interaction_info['to_user_type'] if 'to_user_type' in interaction_info_keys else None,
            'to_user_id': interaction_info['to_user_id'] if 'to_user_id' in interaction_info_keys else None,
            'to_phone': interaction_info['to_phone'] if 'to_phone' in interaction_info_keys else None,
            'communication_flow_id': interaction_info['communication_flow_id'] if 'communication_flow_id' in interaction_info_keys else None,
            'communication_flow_type_id': interaction_info['communication_flow_type_id'] if 'communication_flow_type_id' in interaction_info_keys else None,
            'media_communication_type_id': interaction_info['media_communication_type_id'] if 'media_communication_type_id' in interaction_info_keys else None,
            'service_id': interaction_info['service_id'] if 'service_id' in interaction_info_keys else None,
            'notificacion_status_id': interaction_info['notificacion_status_id'] if 'notificacion_status_id' in interaction_info_keys else None,
            'message': interaction_info['message'] if 'message' in interaction_info_keys else None,
            'recording_name': interaction_info['recording_name'] if 'recording_name' in interaction_info_keys else None,
            'direction': interaction_info['direction'] if 'direction' in interaction_info_keys else None,
            'error_code': interaction_info['error_code'] if 'error_code' in interaction_info_keys else None,
            'price': interaction_info['price'] if 'price' in interaction_info_keys else None,
            'measurement_unit_id': interaction_info['measurement_unit_id'] if 'measurement_unit_id' in interaction_info_keys else None,
            'created_at': datetime.now(tz=tz),
            'updated_at': datetime.now(tz=tz),
        }

        return self.put_item_dynamo_db(Config.COMMUNICATION_LOG_TABLE_NAME, item)
