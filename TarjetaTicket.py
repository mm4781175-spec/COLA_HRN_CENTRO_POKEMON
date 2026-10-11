import tkinter as tk
from PIL import Image, ImageTk


class TarjetaTicket(tk.Frame):

    def __init__(
        self,
        padre,
        pokemon,
        entrenador,
        imagen_pokemon,
        enfermedad,
        tiempo_atencion,
        tiempo_espera,
        prioridad
    ):
        super().__init__(
            padre,
            width=700,
            height=250,
            bg="white"
        )

        self.pack_propagate(False)

        self.pokemon = pokemon
        self.entrenador = entrenador
        self.imagen_pokemon = imagen_pokemon
        self.enfermedad = enfermedad
        self.tiempo_atencion = tiempo_atencion
        self.tiempo_espera = tiempo_espera
        self.prioridad = prioridad

        self.crear_tarjeta()


    def crear_tarjeta(self):

        # ==============================
        # FONDO DEL TICKET
        # ==============================

        imagen_fondo = Image.open(
            "resources/marco_medico_ticket.png"
        )

        imagen_fondo = imagen_fondo.resize(
            (700, 250)
        )

        self.fondo = ImageTk.PhotoImage(imagen_fondo)

        label_fondo = tk.Label(
            self,
            image=self.fondo,
            borderwidth=0
        )

        label_fondo.place(
            x=0,
            y=0,
            width=700,
            height=250
        )


        # ==============================
        # IMAGEN DEL POKEMON
        # ==============================

        try:
            imagen = Image.open(self.imagen_pokemon)

            imagen.thumbnail(
                (140, 140),
                Image.Resampling.LANCZOS
            )

            self.imagen_pokemon_tk = ImageTk.PhotoImage(
                imagen
            )

            label_imagen = tk.Label(
                self,
                image=self.imagen_pokemon_tk,
                bg="white",
                borderwidth=0
            )

            label_imagen.place(
                x=55,
                y=55,
                width=140,
                height=140
            )

        except Exception as e:
            print("Error al cargar imagen del Pokemon:")
            print(e)


        # ==============================
        # NOMBRE DEL POKEMON
        # ==============================

        label_pokemon = tk.Label(
            self,
            text=self.pokemon.upper(),
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#299667"
        )

        label_pokemon.place(
            x=220,
            y=40,
            width=200,
            height=35
        )


        # ==============================
        # ENTRENADOR
        # ==============================

        label_entrenador = tk.Label(
            self,
            text=f"Entrenador: {self.entrenador}",
            font=("Arial", 11),
            bg="white",
            fg="#3A3A3A",
            anchor="w"
        )

        label_entrenador.place(
            x=220,
            y=80,
            width=250,
            height=25
        )


        # ==============================
        # ENFERMEDAD
        # ==============================

        label_enfermedad = tk.Label(
            self,
            text=f"Enfermedad: {self.enfermedad}",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#3A3A3A",
            anchor="w"
        )

        label_enfermedad.place(
            x=220,
            y=110,
            width=300,
            height=25
        )


        # ==============================
        # TIEMPO DE ATENCION
        # ==============================

        label_atencion = tk.Label(
            self,
            text=f"Tiempo de atención: {self.tiempo_atencion} s",
            font=("Arial", 11),
            bg="white",
            fg="#3A3A3A",
            anchor="w"
        )

        label_atencion.place(
            x=220,
            y=145,
            width=250,
            height=25
        )


        # ==============================
        # TIEMPO DE ESPERA
        # ==============================

        self.label_espera = tk.Label(
            self,
            text=f"Espera: {self.tiempo_espera} s",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#277858"
        )

        self.label_espera.place(
            x=490,
            y=75,
            width=160,
            height=30
        )


        # ==============================
        # PRIORIDAD HRN
        # ==============================

        self.label_prioridad = tk.Label(
            self,
            text=f"Prioridad: {self.prioridad:.2f}",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#299667"
        )

        self.label_prioridad.place(
            x=490,
            y=125,
            width=160,
            height=35
        )


    def actualizar_datos(
        self,
        tiempo_espera,
        prioridad
    ):

        self.tiempo_espera = tiempo_espera
        self.prioridad = prioridad

        self.label_espera.config(
            text=f"Espera: {self.tiempo_espera} s"
        )

        self.label_prioridad.config(
            text=f"Prioridad: {self.prioridad:.2f}"
        )