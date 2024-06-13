from fastapi import FastAPI, HTTPException, status
from models import Animal, Shelter, UpdateShelterRequest, PatchShelterRequest

# Make the pydantic model `Shelter` that will represent this data, then manually
# change this list to be a list[Shelter]. You don't need to write code to convert
# this list, just manually change it by hand.
shelters: list[Shelter] = [
    Shelter(
        id=1,
        name="St. George Animal Shelter",
        address= "605 Waterworks Dr, St. George, UT 84770",
        animals= Animal(
            id=1,
            cats=13,
            dogs=15
            )
        ),
    Shelter(
        id=2,
        name= "St. George Paws",
        address= "1125 W 1130 N, St. George, UT 84770",
        animals= Animal(
            id=2,
            cats=12,
            dogs=9
        )
    ),
    Shelter(
        id=3,
        name= "Animal Rescue Team",
        address= "1838 W 1020 N Ste. B, St. George, UT 84770",
        animals= Animal(
            id=3,
            cats= 4,
            dogs= 7,
        )
    )
]

app = FastAPI()

@app.get("/shelters", response_model=list[Shelter], status_code=status.HTTP_200_OK, tags=["Shelters"])
async def get_shelters() -> list[Shelter]:
    return shelters

@app.get("/shelters/{shelter_id}", response_model=Shelter, status_code=status.HTTP_200_OK, tags=["Shelters"])
async def get_shelter(shelter_id: int) -> Shelter:
    try:
        shelter = [shelter for shelter in shelters if shelter.id == shelter_id].pop(0)
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Shelter ID: {shelter_id} not found.")
    return shelter

@app.post("/shelters", response_model=Shelter, status_code=status.HTTP_201_CREATED, tags=["Shelters"])
async def add_shelter(add_shelter_request: Shelter) -> Shelter:
    if add_shelter_request.id in [shelter.id for shelter in shelters]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Shelter ID {add_shelter_request.id} already exists. Please try again with a new shelter ID.")
    if add_shelter_request.animals.id in [shelter.animals.id for shelter in shelters]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Animal ID: {add_shelter_request.animals.id} already exists. Please try again with a new animal ID.")
    shelter = add_shelter_request
    shelters.append(shelter)
    return shelter

@app.put("/shelters/{shelter_id}", response_model=Shelter, status_code=status.HTTP_200_OK, tags=["Shelters"]) 
async def update_shelter(shelter_id: int, update_shelter_request: UpdateShelterRequest) -> Shelter:
    if shelter_id not in [shelter.id for shelter in shelters]:
        shelter = Shelter(id=shelter_id, **update_shelter_request.model_dump())
        shelters.append(shelter)
        return shelter
    for i, shelter in enumerate(shelters):
        if shelter_id == shelter.id:
            if update_shelter_request.animals.id in [shelt.animals.id for shelt in shelters if update_shelter_request.animals.id != shelter.animals.id]:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Animal ID: {update_shelter_request.animals.id} already exists. Please try again with a new animal ID.")
            for attr, value in update_shelter_request.model_dump(exclude={"animals"}).items():
                setattr(shelter, attr, value) 
            if update_shelter_request.animals:
                shelter.animals = Animal.model_validate(update_shelter_request.animals)
            shelters[i] = Shelter.model_validate(shelter)
            return shelters[i]
    
@app.patch("/shelters/{shelter_id}", response_model=Shelter, status_code=status.HTTP_200_OK, tags=["Shelters"])
async def patch_shelter(shelter_id: int, patch_shelter_request: PatchShelterRequest) -> Shelter:
    if shelter_id not in [shelter.id for shelter in shelters]:
        raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST, detail=f"Shelter ID: {shelter_id} not found.")
    for i, shelter in enumerate(shelters):
        if shelter_id == shelter.id:
            for attr, value in patch_shelter_request.model_dump(exclude_unset=True, exclude={"animals"}).items():
                setattr(shelter, attr, value) 
            if patch_shelter_request.animals:
                if patch_shelter_request.animals.id in [shelt.animals.id for shelt in shelters if patch_shelter_request.animals.id != shelter.animals.id] and patch_shelter_request.animals.id is not None:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Animal ID: {patch_shelter_request.animals.id} already exists. Please try again with a new animal ID.")
                shelter.animals = Animal.model_validate(patch_shelter_request.animals)
            shelters[i] = shelter
            return shelters[i]
            
@app.delete("/shelters/{shelter_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Shelters"]) 
async def delete_shelter(shelter_id: int):
    if shelter_id not in [shelter.id for shelter in shelters]:
        raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST, detail=f"Shelter ID: {shelter_id} not found.")
    for i, shelter in enumerate(shelters):
        if shelter_id == shelter.id:
            shelters.pop(i)