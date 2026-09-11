from pydantic import BaseModel, Field

class GuardrailResponse(BaseModel):
    allowed: bool = Field(..., description="True if the request is valid, otherwise Fasle.")
    reason: str = Field(..., description="If the request is not allowed mention the reason, if request is allowed set to NA.")

