class SqlSchemaError(Exception):
    """
        CustomException

        *Params:
        message: string required
        statusCode: int, required
    """
    status_code = 400
    
    def __init__(self, message):
        self.status_code = status_code
        if "UNIQUE" in str(message):
            
            if("username" in str(message)):
                self.message = "Usuario ya existe"
            elif("dni" in str(message)):
                self.message = "Dni ya existe"
            elif("phone" in str(message)):
                self.message = "Celular ya existe"
                                
        elif "FOREIGN" in str(err):
            self.message = "ya eciste llave forenea ya existe"
        else:
            self.message = "Error"

