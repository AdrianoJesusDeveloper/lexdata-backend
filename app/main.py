from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import contact
from config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para integração entre direito, dados e finanças - LexData & Finance Solutions",
    version=settings.PROJECT_VERSION
)

# CORS middleware - ATUALIZADO PARA PRODUÇÃO
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://lexdata-frontend.vercel.app",  # Substitua pelo seu domínio Vercel
        "https://*.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(contact.router, prefix="/api/v1", tags=["contact"])

@app.get("/")
async def root():
    return {
        "message": "Bem-vindo à LexData & Finance Solutions API",
        "version": settings.PROJECT_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "LexData API"}