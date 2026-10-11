class Enfermedad:

    def __init__(
        self,
        id_enfermedad=None,
        nombre="",
        descripcion="",
        tiempo_de_atencion=0
    ):
        self.id_enfermedad = id_enfermedad
        self.nombre = nombre
        self.descripcion = descripcion
        self.tiempo_de_atencion = tiempo_de_atencion

    def __str__(self):
        return f"{self.nombre} - Tiempo: {self.tiempo_de_atencion} segundos"