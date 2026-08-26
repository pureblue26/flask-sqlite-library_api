from pydantic import BaseModel, ConfigDict

class schemasModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)