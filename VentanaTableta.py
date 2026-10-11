import tkinter as tk
from PIL import Image, ImageTk

from Ticket_dao import TicketDAO
from TarjetaTicket import TarjetaTicket


class VentanaTableta:

    def __init__(self, padre):

        self.ventana = tk.Toplevel(padre)

        self.ventana.title("Centro Pokemon - Tableta")
        self.ventana.geometry("900x1000")
        self.ventana.resizable(False, False)

        self.ticket_dao = TicketDAO()

        self.tarjetas = []

        # Cronometro general
        self.segundos = 0

        # Ticket que actualmente esta siendo atendido
        self.ticket_actual_id = None
        self.ticket_actual_nombre = None

        # Tiempo restante de atencion
        self.tiempo_restante = 0

        self.crear_interfaz()

        # Mostrar tickets inicialmente
        self.cargar_tickets()

        # Elegir primer Pokemon
        self.seleccionar_siguiente_ticket()

        # La primera actualización ocurre despues de 1 segundo
        self.ventana.after(
            1000,
            self.actualizar_sistema
        )


    def crear_interfaz(self):

        # =====================================
        # FONDO
        # =====================================

        imagen = Image.open(
            "resources/marco_medico_tableta.png"
        )

        imagen = imagen.resize(
            (900, 1000)
        )

        self.fondo = ImageTk.PhotoImage(imagen)

        label_fondo = tk.Label(
            self.ventana,
            image=self.fondo,
            borderwidth=0
        )

        label_fondo.place(
            x=0,
            y=0,
            width=900,
            height=1000
        )


        # =====================================
        # TITULO
        # =====================================

        titulo = tk.Label(
            self.ventana,
            text="CENTRO POKEMON",
            font=("Arial", 23, "bold"),
            bg="white",
            fg="#289965"
        )

        titulo.place(
            x=250,
            y=85,
            width=400,
            height=40
        )


        # =====================================
        # CRONOMETRO GENERAL
        # =====================================

        self.label_cronometro = tk.Label(
            self.ventana,
            text="00:00:00",
            font=("Arial", 17, "bold"),
            bg="white",
            fg="#3A785B"
        )

        self.label_cronometro.place(
            x=350,
            y=125,
            width=200,
            height=35
        )


        # =====================================
        # POKEMON EN ATENCION
        # =====================================

        self.label_atendiendo = tk.Label(
            self.ventana,
            text="Esperando Pokemon...",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#289965"
        )

        self.label_atendiendo.place(
            x=200,
            y=160,
            width=500,
            height=30
        )


        # =====================================
        # TIEMPO RESTANTE
        # =====================================

        self.label_tiempo_restante = tk.Label(
            self.ventana,
            text="Tiempo restante: --",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#3A785B"
        )

        self.label_tiempo_restante.place(
            x=250,
            y=190,
            width=400,
            height=30
        )


        # =====================================
        # CANVAS
        # =====================================

        self.canvas = tk.Canvas(
            self.ventana,
            bg="white",
            highlightthickness=0
        )

        self.canvas.place(
            x=85,
            y=230,
            width=730,
            height=650
        )


        # =====================================
        # SCROLLBAR
        # =====================================

        self.scrollbar = tk.Scrollbar(
            self.ventana,
            orient="vertical",
            command=self.canvas.yview
        )

        self.scrollbar.place(
            x=815,
            y=230,
            width=18,
            height=650
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )


        # =====================================
        # FRAME DE TICKETS
        # =====================================

        self.frame_tickets = tk.Frame(
            self.canvas,
            bg="white"
        )

        self.canvas.create_window(
            (365, 0),
            window=self.frame_tickets,
            anchor="n"
        )

        self.frame_tickets.bind(
            "<Configure>",
            self.actualizar_scroll
        )


        # =====================================
        # SCROLL MOUSE
        # =====================================

        self.canvas.bind_all(
            "<MouseWheel>",
            self.scroll_mouse
        )


    def actualizar_scroll(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )


    def scroll_mouse(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )


    # =========================================
    # SELECCIONAR SIGUIENTE TICKET
    # =========================================

    def seleccionar_siguiente_ticket(self):

        tickets = self.ticket_dao.obtener_tickets_completos()

        if not tickets:

            self.ticket_actual_id = None
            self.ticket_actual_nombre = None
            self.tiempo_restante = 0

            self.label_atendiendo.config(
                text="No hay Pokemon en atención"
            )

            self.label_tiempo_restante.config(
                text="Tiempo restante: --"
            )

            return


        # El primero es el de mayor prioridad
        ticket = tickets[0]

        self.ticket_actual_id = ticket.ID_TICKET
        self.ticket_actual_nombre = ticket.NOMBRE_POKEMON

        self.tiempo_restante = (
            ticket.TIEMPO_DE_ATENCION
        )


        self.label_atendiendo.config(
            text=f"ATENDIENDO: {self.ticket_actual_nombre.upper()}"
        )

        self.label_tiempo_restante.config(
            text=f"Tiempo restante: {self.tiempo_restante} s"
        )


    # =========================================
    # MOSTRAR TICKETS EN COLA
    # =========================================

    def cargar_tickets(self):

        posicion_scroll = self.canvas.yview()

        if posicion_scroll:
            posicion = posicion_scroll[0]
        else:
            posicion = 0


        # Borrar tarjetas anteriores
        for widget in self.frame_tickets.winfo_children():
            widget.destroy()

        self.tarjetas.clear()


        tickets = self.ticket_dao.obtener_tickets_completos()


        # =====================================
        # FILTRAR EL QUE ESTA SIENDO ATENDIDO
        # =====================================

        tickets_en_espera = []

        for ticket in tickets:

            if ticket.ID_TICKET != self.ticket_actual_id:
                tickets_en_espera.append(ticket)


        # =====================================
        # NO HAY TICKETS ESPERANDO
        # =====================================

        if not tickets_en_espera:

            label_vacio = tk.Label(
                self.frame_tickets,
                text="No hay Pokemon esperando",
                font=("Arial", 18, "bold"),
                bg="white",
                fg="#67B98F"
            )

            label_vacio.pack(
                pady=100
            )

            self.ventana.update_idletasks()

            self.actualizar_scroll()

            return


        # =====================================
        # CREAR TARJETAS
        # =====================================

        for ticket in tickets_en_espera:

            tarjeta = TarjetaTicket(
                self.frame_tickets,

                pokemon=ticket.NOMBRE_POKEMON,

                entrenador=ticket.ENTRENADOR,

                imagen_pokemon=ticket.IMAGEN,

                enfermedad=ticket.NOMBRE_ENFERMEDAD,

                tiempo_atencion=ticket.TIEMPO_DE_ATENCION,

                tiempo_espera=ticket.TIEMPO_ESPERA,

                prioridad=float(ticket.PRIORIDAD)
            )

            tarjeta.pack(
                pady=10
            )

            self.tarjetas.append(tarjeta)


        self.ventana.update_idletasks()

        self.actualizar_scroll()

        self.canvas.yview_moveto(posicion)


    # =========================================
    # CRONOMETRO GENERAL
    # =========================================

    def actualizar_cronometro(self):

        horas = self.segundos // 3600

        minutos = (
            self.segundos % 3600
        ) // 60

        segundos = self.segundos % 60


        texto = (
            f"{horas:02d}:"
            f"{minutos:02d}:"
            f"{segundos:02d}"
        )

        self.label_cronometro.config(
            text=texto
        )


    # =========================================
    # SISTEMA HRN
    # =========================================

    def actualizar_sistema(self):

        # Cronometro general
        self.segundos += 1

        self.actualizar_cronometro()


        # =====================================
        # SI NO HAY NINGUNO EN ATENCION
        # =====================================

        if self.ticket_actual_id is None:

            self.seleccionar_siguiente_ticket()

            self.cargar_tickets()

            self.ventana.after(
                1000,
                self.actualizar_sistema
            )

            return


        # =====================================
        # ACTUALIZAR LOS QUE SIGUEN ESPERANDO
        # =====================================

        self.ticket_dao.actualizar_hrn_excepto(
            self.ticket_actual_id
        )


        # =====================================
        # RESTAR TIEMPO AL QUE ESTA EN ATENCION
        # =====================================

        self.tiempo_restante -= 1


        self.label_tiempo_restante.config(
            text=f"Tiempo restante: {self.tiempo_restante} s"
        )


        # =====================================
        # TERMINO SU ATENCION
        # =====================================

        if self.tiempo_restante <= 0:

            id_terminado = self.ticket_actual_id
            nombre_terminado = self.ticket_actual_nombre


            # Eliminar de BD
            self.ticket_dao.eliminar(
                id_terminado
            )


            print(
                f"{nombre_terminado} termino su atención"
            )


            # Ya no hay Pokemon siendo atendido
            self.ticket_actual_id = None
            self.ticket_actual_nombre = None
            self.tiempo_restante = 0


            # Elegir inmediatamente el siguiente
            self.seleccionar_siguiente_ticket()


        # =====================================
        # RECARGAR COLA
        # =====================================

        self.cargar_tickets()


        # =====================================
        # VOLVER A EJECUTAR EN 1 SEGUNDO
        # =====================================

        self.ventana.after(
            1000,
            self.actualizar_sistema
        )