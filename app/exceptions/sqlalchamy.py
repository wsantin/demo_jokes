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
            self.message = "Error UNIQUE"
        elif "FOREIGN" in str(err):
            self.message = "Error FOREIGN"
        else:
            self.message = "Error"

