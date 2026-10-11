class Pokemon:

    def __init__(self, id_pokemon=None, nombre="", imagen="", entrenador=""):
        self.id_pokemon = id_pokemon
        self.nombre = nombre
        self.imagen = imagen
        self.entrenador = entrenador

    def __str__(self):
        return f"{self.nombre} - Entrenador: {self.entrenador}"