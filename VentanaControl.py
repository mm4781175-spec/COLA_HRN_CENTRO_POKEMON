import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from Pokemon_dao import PokemonDAO
from Enfermedad_dao import EnfermedadDAO
from Ticket_dao import TicketDAO
from Ticket import Ticket


class VentanaControl:

    def __init__(self, padre):

        self.ventana = tk.Toplevel(padre)

        self.ventana.title("Centro Pokemon - Control")
        self.ventana.geometry("600x900")
        self.ventana.resizable(False, False)

        self.pokemon_dao = PokemonDAO()
        self.enfermedad_dao = EnfermedadDAO()
        self.ticket_dao = TicketDAO()

        self.pokemones = self.pokemon_dao.obtener_todos()
        self.enfermedades = self.enfermedad_dao.obtener_todas()

        self.crear_interfaz()


    def crear_interfaz(self):

        imagen = Image.open("resources/marco_medico_tableta.png")
        imagen = imagen.resize((600, 900))

        self.fondo = ImageTk.PhotoImage(imagen)

        fondo_label = tk.Label(
            self.ventana,
            image=self.fondo
        )

        fondo_label.place(
            x=0,
            y=0,
            width=600,
            height=900
        )


        titulo = tk.Label(
            self.ventana,
            text="CENTRO POKEMON",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="#289965"
        )

        titulo.place(
            x=150,
            y=150,
            width=300,
            height=50
        )


        label_pokemon = tk.Label(
            self.ventana,
            text="Selecciona Pokemon",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#3A785B"
        )

        label_pokemon.place(
            x=150,
            y=280,
            width=300,
            height=35
        )


        self.combo_pokemon = ttk.Combobox(
            self.ventana,
            state="readonly",
            font=("Arial", 13)
        )

        self.combo_pokemon["values"] = [
            pokemon.nombre
            for pokemon in self.pokemones
        ]

        self.combo_pokemon.place(
            x=150,
            y=325,
            width=300,
            height=35
        )


        label_enfermedad = tk.Label(
            self.ventana,
            text="Selecciona Enfermedad",
            font=("Arial", 15, "bold"),
            bg="white",
            fg="#3A785B"
        )

        label_enfermedad.place(
            x=150,
            y=410,
            width=300,
            height=35
        )


        self.combo_enfermedad = ttk.Combobox(
            self.ventana,
            state="readonly",
            font=("Arial", 13)
        )

        self.combo_enfermedad["values"] = [
            enfermedad.nombre
            for enfermedad in self.enfermedades
        ]

        self.combo_enfermedad.place(
            x=150,
            y=455,
            width=300,
            height=35
        )


        boton_crear = tk.Button(
            self.ventana,
            text="CREAR TICKET",
            font=("Arial", 15, "bold"),
            bg="#66D49C",
            fg="white",
            activebackground="#4BB981",
            command=self.crear_ticket
        )

        boton_crear.place(
            x=175,
            y=570,
            width=250,
            height=55
        )


    def crear_ticket(self):

        indice_pokemon = self.combo_pokemon.current()
        indice_enfermedad = self.combo_enfermedad.current()

        if indice_pokemon == -1:
            messagebox.showwarning(
                "Aviso",
                "Selecciona un Pokemon"
            )
            return

        if indice_enfermedad == -1:
            messagebox.showwarning(
                "Aviso",
                "Selecciona una enfermedad"
            )
            return


        pokemon = self.pokemones[indice_pokemon]
        enfermedad = self.enfermedades[indice_enfermedad]


        ticket = Ticket(
            id_pokemon=pokemon.id_pokemon,
            id_enfermedad=enfermedad.id_enfermedad,
            tiempo_espera=0,
            prioridad=1.0
        )


        resultado = self.ticket_dao.insertar(ticket)


        if resultado:

            messagebox.showinfo(
                "Centro Pokemon",
                "Ticket creado correctamente"
            )

            self.combo_pokemon.set("")
            self.combo_enfermedad.set("")

        else:

            messagebox.showerror(
                "Error",
                "No se pudo crear el ticket"
            )