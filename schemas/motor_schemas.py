from pydantic import BaseModel

class MotorCreate(BaseModel):
     Motor: int
     potencia_cv:int
     potencia_kw: float
     torque_nm:int
     velocidade_maxima: int