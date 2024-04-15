import requests
from PIL import Image
from io import BytesIO
import os

def get_pokemon_info(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        pokemon_data = response.json()
        pokemon_info = {
            "name": pokemon_data["name"],
            "height": pokemon_data["height"],
            "weight": pokemon_data["weight"],
            "abilities": [ability["ability"]["name"] for ability in pokemon_data["abilities"]],
            "types": [type_data["type"]["name"] for type_data in pokemon_data["types"]]
        }
        if 'sprites' in pokemon_data and 'front_default' in pokemon_data['sprites']:
            pokemon_info['sprites'] = pokemon_data['sprites']['front_default']
        else:
            pokemon_info['sprites'] = None
        return pokemon_info
    else:
        return None

def save_pokemon_info_to_file(pokemon_info):
    file_path = f"C:\\Users\\melin\\downloads\\pokemon_info_{pokemon_info['name']}.txt"
    with open(file_path, "w") as file:
        file.write("Pokemon Information:\n")
        file.write(f"Name: {pokemon_info['name']}\n")
        file.write(f"Height: {pokemon_info['height']}\n")
        file.write(f"Weight: {pokemon_info['weight']}\n")
        file.write("Abilities: " + ', '.join(pokemon_info['abilities']) + "\n")
        file.write("Types: " + ', '.join(pokemon_info['types']) + "\n")
    return file_path


def main():
    pokemon_name = input("Enter the Pokémon name: ")
    pokemon_info = get_pokemon_info(pokemon_name)

    if pokemon_info:
        print(f"Name: {pokemon_info['name']}")
        print(f"Height: {pokemon_info['height']}")
        print(f"Weight: {pokemon_info['weight']}")
        print(f"Abilities: {', '.join(pokemon_info['abilities'])}")
        print(f"Types: {', '.join(pokemon_info['types'])}")

        file_path = save_pokemon_info_to_file(pokemon_info)
        print(f"\nPokemon information saved to: {file_path}")

        if pokemon_info['sprites']:
            image_response = requests.get(pokemon_info['sprites'])
            if image_response.status_code == 200:
                image = Image.open(BytesIO(image_response.content))
                # Redimensionar la imagen a un tamaño específico (por ejemplo, 400x400 píxeles)
                image = image.resize((400, 400))
                image_path = "pokemon_image.png"
                image.save(image_path)
                os.system(f"start {image_path}")
                print(f"Image saved as {image_path}")
            else:
                print("Failed to download image.")
        else:
            print("No image available for this Pokémon.")
    else:
        print("Pokémon not found!")

if __name__ == "__main__":
    main()
