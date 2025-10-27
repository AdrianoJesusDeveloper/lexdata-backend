from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum

class ServiceType(str, Enum):
    CONSULTORIA = "consultoria"
    LEGALTECH = "legaltech"
    FINANCAS = "financas"
    TREINAMENTO = "treinamento"
    OUTRO = "outro"

class ContactRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nome completo")
    email: EmailStr = Field(..., description="E-mail válido")
    company: str = Field(..., min_length=2, max_length=100, description="Nome da empresa")
    service_type: ServiceType = Field(..., description="Tipo de serviço de interesse")
    message: str = Field(..., min_length=10, max_length=1000, description="Mensagem detalhada")
    phone: Optional[str] = Field(None, max_length=20, description="Telefone para contato")

class ContactResponse(BaseModel):
    success: bool
    message: str
    contact_id: Optional[str] = None

class ServiceInfo(BaseModel):
    name: str
    description: str
    features: list[str] = []