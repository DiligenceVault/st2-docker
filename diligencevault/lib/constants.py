ENV_VALUE = {
    "prod": {},
    "dev": {
        "base_api_url": "https://dv-feature-api.diligencevault.com/"
    },
    "test": {},
    "beta": {}
}

SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "env": {
            "type": "string",
            "enum": ["prod", "dev", "beta", "test"],
        },
        "token": {"$ref": "#/definitions/non-empty-string"},
        "body": {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "id": {"$ref": "#/definitions/greater-than-zero"},
                        "email": {"$ref": "#/definitions/email-field"}
                    },
                    "required": ["id", "email"]
                },
                "firm": {
                    "type": "object",
                    "properties": {
                        "id": {"$ref": "#/definitions/greater-than-zero"},
                        "name": {"$ref": "#/definitions/non-empty-string"}
                    },
                    "required": ["id", "name"]
                },
            },
            "required": ["user", "firm"]
        },
        "event": {
            "type": "object",
            "properties": {
                "uuid": {"$ref": "#/definitions/uuid-field"}
            },
            "required": ["uuid"]
        }
    },
    "required": ["token", "body", "event", "env"],
    "definitions": {
        "non-empty-string": {
            "type": "string",
            "minLength": 1
        },
        "greater-than-zero": {
            "type": "number",
            "minimum": 1
        },
        "email-field": {
            "type": "string",
            "format": "email",
            "minLength": 1,
        },
        "uuid-field": {
            "type": "string",
            # "format": "uuid", # this isn't working for some reason.
            "minLength": 1,
            "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
        }
    }
}

SCHEMA_TYPE_TO_ENTITY_TYPE = {
    "vehicle": 1217,
    "contact": 1218,
    "fund": 1219,
    "firm": 1220,
    "duediligence": 1105,
    "project": 1105,
    "strategy": 5004,
}