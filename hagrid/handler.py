import json
import uuid


def get_uuid(event, context):
    body = {'uuid': str(uuid.uuid4()), 'source': 'native'}

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
