from pydantic import BaseModel

class TransmissionCreate(BaseModel):
    Transmission: str
    num_marches : int
    traction : str