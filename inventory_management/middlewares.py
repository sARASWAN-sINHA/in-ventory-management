import json


class CustomResponseMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.excluded_paths = ["api", "login", "profile", "admin"]

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_response(self, request, json_response):
        if (
            any(request.path.startswith(path) for path in self.excluded_paths)
            or json_response.get("Content-Type", "") != "application/json"
        ):
            return json_response

        if json_response.get("Content-Type", "") == "application/json":
            dict_response_data = json.loads(json_response.content)

            modified_response = {
                "status": json_response.status_code,
                "message": json_response.reason_phrase,
                **dict_response_data,
            }

            modified_json_response = json.dumps(modified_response)

            modified_json_response.get("Content-Type", "application/json")
            modified_json_response.get("Content-Length", len(modified_json_response))

            return modified_json_response
