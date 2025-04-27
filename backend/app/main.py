from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prisma import Prisma
from . import schemas, auth
from .database import get_db, connect, disconnect
from prisma.models import User, Bookmark
from .scraper.runner import ScrapySearchService 
from typing import List
from crochet._eventloop import TimeoutError
from comparator import group_hotels_by_name, organize_hotel_comparison

app = FastAPI()

scrapy_service = ScrapySearchService()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the hotel-compare API"}

@app.on_event("startup")
async def startup():
    await connect()

@app.on_event("shutdown")
async def shutdown():
    await disconnect()

@app.post("/register", response_model=schemas.User)
async def register(user: schemas.UserCreate, db: Prisma = Depends(get_db)):
    existing_user = await db.user.find_unique(where={"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = await db.user.create(
        data={
            "email": user.email,
            "username": user.username,
            "password": hashed_password
        }
    )
    return new_user

@app.post("/login", response_model=schemas.Token)
async def login(user: schemas.LoginSchema, db: Prisma = Depends(get_db)):
    db_user = await db.user.find_unique(where={"email": user.email})
    if not db_user or not auth.verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(data={"sub": user.email})
    refresh_token = auth.create_refresh_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.post("/search")
async def search_hotels(
    search_params: schemas.HotelSearch,
    current_user: schemas.User = Depends(auth.get_current_user),
    db: Prisma = Depends(get_db)
):
    try:
        # Convert search params to dict for the spider
        search_dict = search_params.dict()
        
        # Run spiders and wait for completion
        scrapy_service.run_spider(search_dict)
        
        # Get results
        scraped_hotels = scrapy_service.get_items()
        grouped_hotels = group_hotels_by_name(scraped_hotels)
        comparison_list = organize_hotel_comparison(grouped_hotels)
        
        return {"result": comparison_list}
    except TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="The search operation took too long to complete. Please try again."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during the search: {str(e)}"
        )

@app.post("/bookmarks", response_model=schemas.Bookmark)
async def create_bookmark(
    bookmark: schemas.BookmarkCreate,
    current_user: User = Depends(auth.get_current_user),
    db: Prisma = Depends(get_db)
):
    new_bookmark = await db.bookmark.create(
        data={
            "hotelName": bookmark.hotel_name,
            "image": bookmark.image,
            "price": bookmark.price,
            "rating": bookmark.rating,
            "bookingUrl": bookmark.booking_url,
            "userId": current_user.id
        }
    )
    return schemas.Bookmark(
        id=new_bookmark.id,
        hotel_name=new_bookmark.hotelName,
        image=new_bookmark.image,
        price=new_bookmark.price,
        rating=new_bookmark.rating,
        booking_url=new_bookmark.bookingUrl,
        user_id=new_bookmark.userId,
        created_at=new_bookmark.createdAt
    )

@app.get("/bookmarks/{bookmark_id}", response_model=schemas.Bookmark)
async def get_bookmark(
    bookmark_id: int,
    current_user: User = Depends(auth.get_current_user),
    db: Prisma = Depends(get_db)
):
    bookmark = await db.bookmark.find_unique(
        where={"id": bookmark_id},
        include={"user": True}
    )
    if not bookmark or bookmark.userId != current_user.id:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    return schemas.Bookmark(
        id=bookmark.id,
        hotel_name=bookmark.hotelName,
        image=bookmark.image,
        price=bookmark.price,
        rating=bookmark.rating,
        booking_url=bookmark.bookingUrl,
        user_id=bookmark.userId,
        created_at=bookmark.createdAt
    )

@app.get("/bookmarks", response_model=list[schemas.Bookmark])
async def get_user_bookmarks(
    current_user: User = Depends(auth.get_current_user),
    db: Prisma = Depends(get_db)
):
    bookmarks = await db.bookmark.find_many(
        where={"userId": current_user.id}
    )
    return [
        schemas.Bookmark(
            id=bookmark.id,
            hotel_name=bookmark.hotelName,
            image=bookmark.image,
            price=bookmark.price,
            rating=bookmark.rating,
            booking_url=bookmark.bookingUrl,
            user_id=bookmark.userId,
            created_at=bookmark.createdAt
        )
        for bookmark in bookmarks
    ]

@app.delete("/bookmarks/{bookmark_id}")
async def delete_bookmark(
    bookmark_id: int,
    current_user: User = Depends(auth.get_current_user),
    db: Prisma = Depends(get_db)
):
    # First check if the bookmark exists and belongs to the current user
    bookmark = await db.bookmark.find_unique(
        where={"id": bookmark_id},
        include={"user": True}
    )
    
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    if bookmark.userId != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this bookmark")
    
    # Delete the bookmark
    await db.bookmark.delete(
        where={"id": bookmark_id}
    )
    
    return {"message": "Bookmark deleted successfully"} 