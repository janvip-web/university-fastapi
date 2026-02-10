from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

db_url = "postgresql+asyncpg://user:admin@localhost:5000/university_db"

engine = create_async_engine(db_url, echo = True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
    )

# Base = declarative_base()

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
            #except rollback
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
