import requests
from st2common.runners.base_action import Action

from utils import get_environment_info_using_payload, validate_payload

__all__ = [
    'CreateWorkflowAction'
]

def get_workflow_definition(env_info, api_token, entity_id, entity_type, workflow_id):
    url = env_info["base_api_url"] + '/api/workflow_audits/preview'
    headers = {
        'Authorization': f'Bearer {api_token}',
        'page-url': '/workflows'
    }
    params = {
        'entity_id': entity_id,
        'entity_type': entity_type,
        'workflow_id': workflow_id
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != requests.codes.ok:
            msg = ('Failed to call endpoint=%s (status_code=%s): %s' %
                   (url, response.status_code, response.text))
            raise Exception(msg)

    return response.json()


def trigger_workflow(env_info, api_token, payload):
    url = env_info["base_api_url"] + '/api/workflow_audits'
    headers = {
        'Authorization': f'Bearer {api_token}',
        'page-url': '/workflow_automation'
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != requests.codes.ok:
            msg = ('Failed to call endpoint=%s (status_code=%s): %s' %
                   (url, response.status_code, response.text))
            raise Exception(msg)

    return response.json()


class CreateWorkflowAction(Action):
    def run(self, payload, workflow_id, entity_type, entity_id):
        validate_payload(payload=payload)
        token = payload.get("token")
        if not token:
            msg = ("Failed to execute action=create_workflow): %s" %
                   ("Token is not present in payload."))
            raise Exception(msg)

        env_info = get_environment_info_using_payload(payload=payload)
        entity_type = entity_type.lower().strip()

        workflow_definition = get_workflow_definition(
            env_info=env_info,
            api_token=token,
            entity_id=entity_id,
            entity_type=entity_type,
            workflow_id=workflow_id
        )

        response = trigger_workflow(
            env_info=env_info,
            api_token=token,
            payload=workflow_definition
        )

        return response
