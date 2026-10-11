from conexion import Conexion
from Pokemon import Pokemon


class PokemonDAO:

    def obtener_todos(self):
        conexion = Conexion().conectar()

        if conexion is None:
            return []

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT ID_POKEMON, NOMBRE, IMAGEN, ENTRENADOR
                FROM POKEMON
            """)

            pokemones = []

            for fila in cursor.fetchall():
                pokemon = Pokemon(
                    id_pokemon=fila.ID_POKEMON,
                    nombre=fila.NOMBRE,
                    imagen=fila.IMAGEN,
                    entrenador=fila.ENTRENADOR
                )

                pokemones.append(pokemon)

            return pokemones

        except Exception as e:
            print("Error al obtener los Pokemon:")
            print(e)
            return []

        finally:
            conexion.close()