from typing import Dict
from ollama import chat
from pydantic import BaseModel

class Endpoint(BaseModel):
    endpoints: list[str]

class APISpec(BaseModel):
    endpoint_name: str
    params: list[Dict]
    returns: list[Dict]
    code: str

class OpenAPISpecGenerator:
    def __init__(self):
        self.model = 'devstral:24b'
        self.endpoints = []
        self.api_specs = {}
    
    async def generate_spec(self, code: str) -> Dict:
        response = chat(
            messages=[{
                'role': 'user',
                'content': f'Extract all API endpoint names defined in the following code: {code}'
            }],
            model=self.model,
            format=Endpoint.model_json_schema(),
        )
        endpoints = Endpoint.model_validate_json(response.message.content)
        self.endpoints.append(endpoints.endpoints)

        api_specs = {}

        for endpoint in endpoints.endpoints:
            response = chat(
                messages=[{
                    'role': 'user',
                    'content': f'Analyze the {endpoint} endpoint implementation in the following code: {code}'
                }],
                model=self.model,
                format=APISpec.model_json_schema(),
            )
            api_specs[endpoint] = APISpec.model_validate_json(response.message.content)
            self.api_specs[endpoint] = api_specs[endpoint]

        return api_specs
    
    async def return_api_specs(self) -> Dict:
        return self.api_specs