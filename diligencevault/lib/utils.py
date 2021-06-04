from jsonschema import validate, draft7_format_checker

import constants


def validate_payload(payload):
    validate(
        instance=payload,
        schema=constants.SCHEMA,
        format_checker=draft7_format_checker
    )
    return

def get_environment_info_using_payload(payload):
    env = payload.get("env")
    if not env:
        msg = ("Failed to execute action=create_workflow): %s" %
                ("Environment info is not present in payload."))
        raise Exception(msg)

    if env not in ("prod", "dev", "beta", "test"):
        msg = ("Failed to execute action=create_workflow): %s" %
                ("Invalid environment info is passed in payload."))
        raise Exception(msg)

    return constants.ENV_VALUE[env]
