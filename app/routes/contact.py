from fastapi import APIRouter, HTTPException
from app.models.schemas import ContactRequest, ContactResponse, ServiceInfo, ServiceType
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
import uuid
from config import settings

router = APIRouter()

class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.sender_email = settings.SENDER_EMAIL
        self.sender_password = settings.SENDER_PASSWORD
    
    def send_contact_email(self, contact_data: ContactRequest) -> bool:
        """
        Envia email com os dados do formulário de contato
        """
        try:
            if not self.sender_email or not self.sender_password:
                print("Configurações de email não definidas. Simulando envio...")
                return True
            
            message = MimeMultipart()
            message["From"] = self.sender_email
            message["To"] = "email@lexdatafinance.com"
            message["Subject"] = f"Novo Contato - {contact_data.company}"
            
            body = f"""
            Nova mensagem de contato recebida via website:
            
            Nome: {contact_data.name}
            Email: {contact_data.email}
            Empresa: {contact_data.company}
            Telefone: {contact_data.phone or 'Não informado'}
            Tipo de Serviço: {contact_data.service_type.value}
            
            Mensagem:
            {contact_data.message}
            
            Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
            ID: {str(uuid.uuid4())[:8]}
            """
            
            message.attach(MIMEText(body, "plain"))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            return True
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return False

@router.post("/contact", response_model=ContactResponse)
async def submit_contact_form(contact_data: ContactRequest):
    """
    Processa formulário de contato da LexData & Finance Solutions
    """
    try:
        email_service = EmailService()
        
        # Envia email com os dados do contato
        email_sent = email_service.send_contact_email(contact_data)
        
        if email_sent:
            return ContactResponse(
                success=True,
                message="Mensagem enviada com sucesso! Entraremos em contato em breve.",
                contact_id=str(uuid.uuid4())
            )
        else:
            return ContactResponse(
                success=False,
                message="Erro ao enviar mensagem. Tente novamente mais tarde."
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro interno do servidor: {str(e)}"
        )

@router.get("/services", response_model=dict)
async def get_services():
    """
    Retorna lista completa de serviços oferecidos pela LexData
    """
    services = {
        "consultoria": ServiceInfo(
            name="Consultoria Estratégica & Inteligência de Negócios",
            description="Dashboards e BI integrados, análise preditiva e planejamento estratégico baseado em dados",
            features=[
                "Dashboards e BI integrados",
                "Análise preditiva para decisões estratégicas",
                "Planejamento estratégico baseado em dados"
            ]
        ),
        "legaltech": ServiceInfo(
            name="Soluções Jurídico-Tecnológicas (LegalTech)",
            description="Automação de processos jurídicos, IA para previsão de resultados e compliance digital",
            features=[
                "Automação de cálculos trabalhistas e contratos",
                "Previsão de resultados judiciais com IA",
                "Compliance digital e LGPD"
            ]
        ),
        "financas": ServiceInfo(
            name="Finanças & Investimentos",
            description="Planejamento financeiro, análise de risco e estudos preditivos de mercado",
            features=[
                "Planejamento financeiro e tributário",
                "Modelos de análise de risco e scoring",
                "Estudos preditivos de mercado"
            ]
        ),
        "tecnologia": ServiceInfo(
            name="Tecnologia & Cloud",
            description="Soluções em nuvem AWS, integração de dados e aplicativos web",
            features=[
                "Aplicativos web e automações em nuvem AWS",
                "Integração de dados através de ETL, APIs e Data Lakes",
                "Segurança e escalabilidade garantidas"
            ]
        ),
        "treinamento": ServiceInfo(
            name="Educação & Treinamentos",
            description="Capacitação profissional em LegalTech, Big Data e Inteligência Competitiva",
            features=[
                "Workshops e mentorias especializadas",
                "Cursos em LegalTech e Big Data",
                "Treinamentos em Inteligência Competitiva"
            ]
        )
    }
    return services

@router.get("/services/{service_type}")
async def get_service_detail(service_type: ServiceType):
    """
    Retorna detalhes de um serviço específico
    """
    services_data = await get_services()
    
    if service_type.value in services_data:
        return services_data[service_type.value]
    else:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")