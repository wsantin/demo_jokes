from marshmallow import fields
from datetime import datetime

class DateTime(fields.DateTime):
    """
    Class extends marshmallow standard DateTime with "timestamp" format.
    """

    SERIALIZATION_FUNCS = \
        fields.DateTime.SERIALIZATION_FUNCS.copy()
    DESERIALIZATION_FUNCS = \
        fields.DateTime.DESERIALIZATION_FUNCS.copy()

    SERIALIZATION_FUNCS['timestamp'] = lambda x: int(x.timestamp()) * 1000
    DESERIALIZATION_FUNCS['timestamp'] = datetime.fromtimestamp
