import os
from google.auth.credentials import AnonymousCredentials

class ApiKeyCreds(AnonymousCredentials):
    def __init__(self, api_key:str):
        self.api_key = api_key
        self.project_id = os.getenv("PROJECT_ID")
        self.location = os.getenv("LOCATION")
        # print(self.api_key, self.project_id, self.location)

    def apply(self, headers,  token=None, **_):
        headers["X-Goog-Api-Key"] = self.api_key
