from prisma import Prisma
from prisma.models import User, Bookmark

prisma = Prisma()

async def connect():
    await prisma.connect()

async def disconnect():
    await prisma.disconnect()

async def get_db():
    try:
        yield prisma
    finally:
        pass 