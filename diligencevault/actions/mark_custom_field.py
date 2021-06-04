import requests

from st2common.runners.base_action import Action

from utils import get_environment_info_using_payload, validate_payload
from constants import SCHEMA_TYPE_TO_ENTITY_TYPE

__all__ = [
    'MarkCustomFieldAction'
]


"""
{
    "entity_type":1220,
    "schema_type":"firm",
    "entity_id":0,
    "custom_fields":[
        {
            "type":"text",
            "has_multiple":false,
            "has_href":false,
            "is_mandatory":false,
            "status":true,
            "visible":1,
            "alias":"st2_tag",
            "value":""
        }
    ]
}
"""

"""
{
    "entity_id":8649,
    "owner_user_id":71363,
    "entity_type":1219,
    "schema_type":"fund",
    "custom_fields":[
        {
            "type":"int",
            "has_multiple":false,
            "has_href":false,
            "is_mandatory":false,
            "description":"just a random integer here",
            "status":true,
            "visible":1,
            "alias":"integer",
            "value":[{"value":1}],
            "order":1,
            "field_unique_key":"fn_1"
        },{
            "type":"text",
            "has_multiple":false,
            "has_href":false,
            "is_mandatory":false,
            "description":"Just a random text field",
            "status":true,
            "visible":1,
            "alias":"text field",
            "value":[{"value":"dd"}],
            "order":2,
            "field_unique_key":"fn_2"
        }
    ]
}
"""

def get_custom_fields(env_info, api_token, schema_type):
    url = env_info["base_api_url"] + 'api/service/dvapi_service/get_custom_fields'
    headers = {
        'Authorization': f'Bearer {api_token}',
        'page-url': f'/app/firm/settings/{schema_type}_tags'
    }
    body = {
        'entity_id': 0,
        'schema_type': schema_type,
    }

    response = requests.post(url, json=body, headers=headers)
    if response.status_code != requests.codes.ok:
            msg = ('Failed to call endpoint=%s (status_code=%s): %s' %
                   (url, response.status_code, response.text))
            raise Exception(msg)

    custom_fields = response.json()["custom_fields"][schema_type]
    return custom_fields


def create_custom_fields(env_info, api_token, schema_type, field_name):
    url = env_info["base_api_url"] + 'api/service/dvapi_service/create_custom_fields'
    headers = {
        'Authorization': f'Bearer {api_token}',
        'page-url': f'/app/firm/settings/{schema_type}_tags'
    }

    body = {
        "entity_type": SCHEMA_TYPE_TO_ENTITY_TYPE[schema_type],
        "schema_type": schema_type,
        "entity_id": 0,
        "custom_fields": [
            {
                "type": "text",
                "has_multiple": False,
                "has_href": False,
                "is_mandatory": False,
                "status": True,
                "visible": 1,
                "alias": field_name,
                "value": ""
            }
        ]
    }

    response = requests.post(url, json=body, headers=headers)
    if response.status_code != requests.codes.ok:
            msg = ('Failed to call endpoint=%s (status_code=%s): %s' %
                   (url, response.status_code, response.text))
            raise Exception(msg)

    custom_fields = response.json()["custom_fields"]
    return custom_fields


def update_custom_field_value(custom_fields, field_name, value):
    for field in custom_fields:
        if field["alias"] == field_name:
            if field["type"] == "text":
                field["value"] = [{
                    "value": value,
                    "value_url": None,
                    "dynamic_url": None
                }]
            else:
                field["value"] = [{
                    "value": value
                }]

    return custom_fields


def post_custom_field_data(
    env_info,
    api_token,
    user_id,
    firm_id,
    entity_id,
    schema_type,
    custom_fields,
    field_name,
    field_value
):
    url = env_info["base_api_url"] + 'api/service/dvapi_service/post_custom_fields_data'
    headers = {
        'Authorization': f'Bearer {api_token}',
        'page-url': f'/app/firms/{firm_id}/{schema_type}s/{entity_id}/profile/monitor' # TODO fix: schema_type formatting is wrong.
    }

    custom_fields = update_custom_field_value(
        custom_fields=custom_fields,
        field_name=field_name,
        value=field_value
    )

    body = {
        "entity_type": SCHEMA_TYPE_TO_ENTITY_TYPE[schema_type],
        "schema_type": schema_type,
        "entity_id": entity_id,
        "owner_user_id": user_id,
        "custom_fields": custom_fields
    }

    response = requests.post(url, json=body, headers=headers)
    if response.status_code != requests.codes.ok:
            msg = ('Failed to call endpoint=%s (status_code=%s): %s' %
                   (url, response.status_code, response.text))
            raise Exception(msg)

    return response.json()


class MarkCustomFieldAction(Action):
    def run(self, payload, field_name, field_value, schema_type, entity_id):
        validate_payload(payload=payload)
        token = payload.get("token")
        if not token:
            msg = ("Failed to call endpoint=/post_custom_fields_data): %s" %
                   ("Token is not present in payload."))
            raise Exception(msg)

        env_info = get_environment_info_using_payload(payload=payload)
        api_body = payload["body"]

        schema_type = schema_type.lower().strip()
        field_name = field_name.strip()
        field_value = field_value.strip()

        custom_fields = get_custom_fields(
            env_info=env_info,
            api_token=token,
            schema_type=schema_type
        )

        is_field_present = [field for field in custom_fields if field["alias"] == field_name]
        if not custom_fields or not is_field_present:
            custom_fields = create_custom_fields(
                env_info=env_info,
                api_token=token,
                schema_type=schema_type,
                field_name=field_name
            )

        response = post_custom_field_data(
            env_info=env_info,
            api_token=token,
            user_id=api_body["user"]["id"],
            firm_id=api_body["firm"]["id"],
            entity_id=entity_id,
            schema_type=schema_type,
            custom_fields=custom_fields,
            field_name=field_name,
            field_value=field_value
        )

        return response
