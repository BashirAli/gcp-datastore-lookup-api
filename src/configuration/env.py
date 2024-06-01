from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gcp_project_id: str = Field(..., alias="GCP_PROJECT_ID")
    api_name: str = "gcp-datastore-lookup-api"



settings = Settings()
