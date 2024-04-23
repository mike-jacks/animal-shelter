from pydantic import BaseModel

class Animal(BaseModel):
    id: int
    cats: int
    dogs: int

class Shelter(BaseModel):
    id: int
    name: str
    address: str
    animals: Animal

class UpdateShelterRequest(BaseModel):
    name: str
    address: str
    animals: Animal

class PatchShelterRequest(BaseModel):
    name: str | None = None
    address: str | None = None
    animals: Animal | None = None
    