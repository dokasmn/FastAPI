# fastapi libs

from fastapi import FastAPI, HTTPException
from typing import List, Optional
from sqlalchemy.exc import IntegrityError
import sqlite3
from typing import Any, Dict

# project

from model import Club, database, clubs

# myapp

app = FastAPI()

# database settings

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# endpoints

@app.get("/clubs/", response_model=List[Club])
async def read_clubs():
    query = clubs.select()
    return await database.fetch_all(query)


@app.post("/clubs/", response_model=Club, status_code=201)
async def create_club(club: Club):
    try:
        query = clubs.insert().values(
            soccer_name=club.soccer_name,
            foundation_date=club.foundation_date,
            amount_titles=club.amount_titles,
            stadium=club.stadium
        )
        last_record_id = await database.execute(query)
        return {**club.dict(), "id": last_record_id}
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            raise HTTPException(status_code=400, detail="Club with this name already exists")
        else:
            raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@app.put("/clubs/{club_id}", response_model=Club)
async def update_club(club_id: int, updated_club: Club):
    query = clubs.select().where(clubs.c.id == club_id)
    existing_club = await database.fetch_one(query)
    
    if existing_club is None:
        raise HTTPException(status_code=404, detail="Club not found")
    
    query = clubs.update().where(clubs.c.id == club_id).values(
        soccer_name=updated_club.soccer_name,
        foundation_date=updated_club.foundation_date,
        amount_titles=updated_club.amount_titles,
        stadium=updated_club.stadium
    )
    await database.execute(query)
    
    return {**updated_club.dict(), "id": club_id}


@app.patch("/clubs/{club_id}", response_model=Club)
async def partial_update_club(club_id: int, partial_club: Dict[str, Any]):
    query = clubs.select().where(clubs.c.id == club_id)
    existing_club = await database.fetch_one(query)
    
    if existing_club is None:
        raise HTTPException(status_code=404, detail="Club not found")
    
    updated_values = {
        "soccer_name": existing_club["soccer_name"],
        "foundation_date": existing_club["foundation_date"],
        "amount_titles": existing_club["amount_titles"],
        "stadium": existing_club["stadium"]
    }
    
    if "soccer_name" in partial_club:
        updated_values["soccer_name"] = partial_club["soccer_name"]
    if "foundation_date" in partial_club:
        updated_values["foundation_date"] = partial_club["foundation_date"]
    if "amount_titles" in partial_club:
        updated_values["amount_titles"] = partial_club["amount_titles"]
    if "stadium" in partial_club:
        updated_values["stadium"] = partial_club["stadium"]
        
    query = clubs.update().where(clubs.c.id == club_id).values(updated_values)
    await database.execute(query)
    
    return {**updated_values, "id": club_id}
    


@app.delete("/clubs/{club_id}", response_model=Club)
async def delete_club(club_id: int):
    query = clubs.select().where(clubs.c.id == club_id)
    existing_club = await database.fetch_one(query)
    
    if existing_club is None:
        raise HTTPException(status_code=404, detail="Club not found")
    
    query = clubs.delete().where(clubs.c.id == club_id)
    await database.execute(query)
    
    return existing_club
