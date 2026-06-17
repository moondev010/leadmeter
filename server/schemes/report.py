from pydantic import BaseModel

class ReportScheme(BaseModel):
    score: int
    reason: str
    confidence: int