import requests
from db import SessionLocal, engine, Base
from models import Pokemon
from schema import PokemonSchema

Base.metadata.create_all(bind=engine)


def fetch_pokemon_data(pokemon_id: int):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        types = ", ".join([type["type"]["name"] for type in data["types"]])
        return PokemonSchema(name=data["name"], type=types)
    else:
        return None


def add_pokemon_to_db(pokemon_schema: PokemonSchema) -> Pokemon:
    with SessionLocal() as session:
        db_pokemon = Pokemon(name=pokemon_schema.name, type=pokemon_schema.type)
        session.add(db_pokemon)
        session.commit()
        session.refresh(db_pokemon)
    return db_pokemon
