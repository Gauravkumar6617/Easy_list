from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import StaticPool
from src.server.core.config import settings

database_url = make_url(settings.DATABASE_URL)
engine_options = {
    "echo": settings.DB_ECHO,
    "pool_pre_ping": settings.DB_POOL_PRE_PING,
}

if database_url.get_backend_name() == "sqlite":
    engine_options["connect_args"] = {"check_same_thread": False}

if database_url.get_backend_name() == "sqlite" and database_url.database in (None, "", ":memory:"):
    engine_options["poolclass"] = StaticPool
else:
    engine_options.update(
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_timeout=settings.DB_POOL_TIMEOUT,
        pool_recycle=settings.DB_POOL_RECYCLE,
    )
engine = create_engine(settings.DATABASE_URL, **engine_options)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass
#This function creates a database session for each FastAPI request.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def HealthCheck():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Database health check failed: {e}")
        return False