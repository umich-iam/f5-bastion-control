#!/usr/bin/python3

from ansible.module_utils.basic import AnsibleModule
import logging
import requests

def retrieve_credential(module):
    api_base_url = module.params["api_base_url"]
    validate_certs = module.params["validate_certs"]
    app_id = module.params["app_id"]
    query = module.params["query"]
    connection_timeout = module.params["connection_timeout"]
    query_format = module.params["query_format"]
    fail_request_on_password_change = module.params["fail_request_on_password_change"]
    client_cert = module.params.get("client_cert")
    client_key = module.params.get("client_key")
    reason = module.params.get("reason")

    endpoint_params = {
        "AppId": app_id,
        "Query": query,
        "ConnectionTimeout": connection_timeout,
        "QueryFormat": query_format,
        "FailRequestOnPasswordChange": fail_request_on_password_change,
    }

    if reason:
        endpoint_params["reason"] = reason

    endpoint = "/AIMWebService/api/Accounts?" + "&".join([f"{key}={value}" for key, value in endpoint_params.items()])

    url = f"{api_base_url}{endpoint}"

    try:
        response = requests.get(url, verify=validate_certs, cert=(client_cert, client_key))
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        module.fail_json(msg=f"Error while retrieving credential: {e}", status_code=response.status_code)

    result = response.json()

    return result, response.status_code

def main():
    fields = {
        "api_base_url": {"required": True, "type": "str"},
        "app_id": {"required": True, "type": "str"},
        "query": {"required": True, "type": "str"},
        "reason": {"required": False, "type": "str"},
        "connection_timeout": {"required": False, "type": "int", "default": 30},
        "query_format": {"required": False, "type": "str", "choices": ["Exact", "Regexp"], "default": "Exact"},
        "fail_request_on_password_change": {"required": False, "type": "bool", "default": False},
        "validate_certs": {"type": "bool", "default": True},
        "client_cert": {"type": "str", "required": False},
        "client_key": {"type": "str", "required": False},
        "state": {"type": "str", "choices": ["present"], "default": "present"},
    }

    module = AnsibleModule(argument_spec=fields, supports_check_mode=True)

    result, status_code = retrieve_credential(module)

    module.exit_json(changed=False, result=result, status_code=status_code)

if __name__ == '__main__':
    main()

