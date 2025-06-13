from typing import Dict
from ollama import chat
from pydantic import BaseModel

class Endpoint(BaseModel):
    endpoint: list[str]

class APISpec(BaseModel):
    endpoint: str
    params: list[Dict]
    returns: list[Dict]
    code: str

class OpenAPISpecGenerator:
    def __init__(self):
        self.endpoints = []
        self.code = ""
        self.api_specs = []
    
    async def generate_spec(self, code: str) -> Dict:
        response = chat(
            messages=[{
                'role': 'user',
                'content': f'Extract all API endpoint names from the following code: {code}'
            }],
            model='devstral:24b',
            format=Endpoint.model_json_schema(),
        )
        endpoints = Endpoint.model_validate_json(response.message.content)

        for endpoint in endpoints.endpoint:
            response = chat(
                messages=[{
                    'role': 'user',
                    'content': f'Extract information about the {endpoint} endpoint from the following code: {code}'
                }],
                model='devstral:24b',
                format=APISpec.model_json_schema(),
            )
            api_spec = APISpec.model_validate_json(response.message.content)
            self.api_specs.append(api_spec)

        return self.api_specs