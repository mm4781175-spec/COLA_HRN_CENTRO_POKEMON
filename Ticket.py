class Ticket:

    def __init__(
        self,
        id_ticket=None,
        id_pokemon=None,
        id_enfermedad=None,
        tiempo_espera=0,
        prioridad=1.0
    ):
        self.id_ticket = id_ticket
        self.id_pokemon = id_pokemon
        self.id_enfermedad = id_enfermedad
        self.tiempo_espera = tiempo_espera
        self.prioridad = prioridad

    def calcular_prioridad(self, tiempo_atencion):

        if tiempo_atencion > 0:
            self.prioridad = (
                self.tiempo_espera + tiempo_atencion
            ) / tiempo_atencion

        return self.prioridad

    def aumentar_tiempo_espera(self):
        self.tiempo_espera += 1

    def __str__(self):
        return (
            f"Ticket {self.id_ticket} | "
            f"Pokemon: {self.id_pokemon} | "
            f"Espera: {self.tiempo_espera}s | "
            f"Prioridad: {self.prioridad:.2f}"
        )