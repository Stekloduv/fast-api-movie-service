from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud import get_films, update_film, delete_film
from app.models import Film
from app.schemas import FilmCreate, FilmRead
from app.database import get_db
from app.models import Film
from app.schemas import FilmCreate, FilmUpdate

router = APIRouter()


@router.post("/movies/", response_model=FilmRead)
async def create_film(film: FilmCreate, db: AsyncSession = Depends(get_db)):
    new_film = Film(**film.dict())
    db.add(new_film)
    await db.commit()
    await db.refresh(new_film)
    return new_film


@router.get("/movies/{film_id}", response_model=FilmRead)
async def get_film(film_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Film).where(Film.id == film_id))
    film = result.scalar_one_or_none()
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    return film


@router.post("/movies/", response_model=FilmRead)
async def add_film(film: FilmCreate, db: AsyncSession = Depends(get_db)):
    new_film = await create_film(db, film)
    return new_film


@router.get("/movies/", response_model=list[FilmRead])
async def list_films(db: AsyncSession = Depends(get_db)):
    films = await get_films(db)
    return films


@router.get("/movies/{film_id}", response_model=FilmRead)
async def read_film(film_id: int, db: AsyncSession = Depends(get_db)):
    film = await get_film(db, film_id)
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    return film


@router.put("/movies/{film_id}", response_model=FilmRead)
async def edit_film(film_id: int, film: FilmUpdate, db: AsyncSession = Depends(get_db)):
    updated_film = await update_film(db, film_id, film)
    if not updated_film:
        raise HTTPException(status_code=404, detail="Film not found")
    return updated_film


@router.delete("/movies/{film_id}", response_model=FilmRead)
async def remove_film(film_id: int, db: AsyncSession = Depends(get_db)):
    deleted_film = await delete_film(db, film_id)
    if not deleted_film:
        raise HTTPException(status_code=404, detail="Film not found")
    return deleted_film
