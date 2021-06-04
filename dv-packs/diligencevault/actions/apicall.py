import json
import requests

from st2common.runners.base_action import Action

__all__ = [
    'ApiCallAction'
]

class ApiCallAction(Action):
    def run(self, payload, endpoint, method, page_url, content_type=None):
        token = payload.get("token")
        if not token:
            msg = ("Failed to call endpoint=%s): %s" %
                   (endpoint, "Token is not present in payload."))
            raise Exception(msg)

        if not content_type:
            content_type = "application/json;charset=UTF-8"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json;charset=UTF-8",
            "page-url": page_url,
        }

        request_payload = payload.get("body")
        if request_payload is None:
            msg = ("Failed to call endpoint=%s): %s" %
                   (endpoint, "Request body is not present in payload."))
            raise Exception(msg)

        if "application/json" in content_type:
            request_payload = json.dumps(request_payload)

        if method == "GET":
            response = requests.get(endpoint, headers=headers)
        elif method == "POST":
            response = requests.post(endpoint, headers=headers, data=request_payload)
        elif method == "PUT":
            response = requests.put(endpoint, headers=headers, data=request_payload)
        elif method == "PATCH":
            response = requests.patch(endpoint, headers=headers, data=request_payload)
        else:
            response = requests.delete(endpoint, headers=headers)

        if response.status_code != requests.codes.ok:  # pylint: disable=no-member
            msg = ('Failed to call endpoint=%s (status_code=%s): %s' %
                   (endpoint, response.status_code, response.text))
            raise Exception(msg)

        return response.json()