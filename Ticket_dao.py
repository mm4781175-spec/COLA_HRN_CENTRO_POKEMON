from conexion import Conexion
from Ticket import Ticket


class TicketDAO:

    def insertar(self, ticket):
        conexion = Conexion().conectar()

        if conexion is None:
            return False

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                INSERT INTO TICKET
                (
                    ID_POKEMON,
                    ID_ENFERMEDAD,
                    TIEMPO_ESPERA,
                    PRIORIDAD
                )
                VALUES (?, ?, ?, ?)
            """,
                ticket.id_pokemon,
                ticket.id_enfermedad,
                ticket.tiempo_espera,
                ticket.prioridad
            )

            conexion.commit()
            return True

        except Exception as e:
            print("Error al insertar ticket:")
            print(e)
            conexion.rollback()
            return False

        finally:
            conexion.close()


    def obtener_todos(self):
        conexion = Conexion().conectar()

        if conexion is None:
            return []

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    ID_TICKET,
                    ID_POKEMON,
                    ID_ENFERMEDAD,
                    TIEMPO_ESPERA,
                    PRIORIDAD
                FROM TICKET
                ORDER BY PRIORIDAD DESC
            """)

            tickets = []

            for fila in cursor.fetchall():

                ticket = Ticket(
                    id_ticket=fila.ID_TICKET,
                    id_pokemon=fila.ID_POKEMON,
                    id_enfermedad=fila.ID_ENFERMEDAD,
                    tiempo_espera=fila.TIEMPO_ESPERA,
                    prioridad=float(fila.PRIORIDAD)
                )

                tickets.append(ticket)

            return tickets

        except Exception as e:
            print("Error al obtener tickets:")
            print(e)
            return []

        finally:
            conexion.close()


    def obtener_por_id(self, id_ticket):
        conexion = Conexion().conectar()

        if conexion is None:
            return None

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    ID_TICKET,
                    ID_POKEMON,
                    ID_ENFERMEDAD,
                    TIEMPO_ESPERA,
                    PRIORIDAD
                FROM TICKET
                WHERE ID_TICKET = ?
            """, id_ticket)

            fila = cursor.fetchone()

            if fila is None:
                return None

            return Ticket(
                id_ticket=fila.ID_TICKET,
                id_pokemon=fila.ID_POKEMON,
                id_enfermedad=fila.ID_ENFERMEDAD,
                tiempo_espera=fila.TIEMPO_ESPERA,
                prioridad=float(fila.PRIORIDAD)
            )

        except Exception as e:
            print("Error al obtener ticket:")
            print(e)
            return None

        finally:
            conexion.close()


    def obtener_tickets_completos(self):
        conexion = Conexion().conectar()

        if conexion is None:
            return []

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    T.ID_TICKET,

                    P.ID_POKEMON,
                    P.NOMBRE AS NOMBRE_POKEMON,
                    P.IMAGEN,
                    P.ENTRENADOR,

                    E.ID_ENFERMEDAD,
                    E.NOMBRE AS NOMBRE_ENFERMEDAD,
                    E.DESCRIPCION,
                    E.TIEMPO_DE_ATENCION,

                    T.TIEMPO_ESPERA,
                    T.PRIORIDAD

                FROM TICKET T

                INNER JOIN POKEMON P
                    ON T.ID_POKEMON = P.ID_POKEMON

                INNER JOIN ENFERMEDAD E
                    ON T.ID_ENFERMEDAD = E.ID_ENFERMEDAD

                ORDER BY T.PRIORIDAD DESC
            """)

            return cursor.fetchall()

        except Exception as e:
            print("Error al obtener tickets completos:")
            print(e)
            return []

        finally:
            conexion.close()


    def actualizar_tiempo(self, id_ticket, tiempo_espera):
        conexion = Conexion().conectar()

        if conexion is None:
            return False

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                UPDATE TICKET
                SET TIEMPO_ESPERA = ?
                WHERE ID_TICKET = ?
            """,
                tiempo_espera,
                id_ticket
            )

            conexion.commit()
            return True

        except Exception as e:
            print("Error al actualizar tiempo:")
            print(e)
            conexion.rollback()
            return False

        finally:
            conexion.close()


    def actualizar_prioridad(self, id_ticket, prioridad):
        conexion = Conexion().conectar()

        if conexion is None:
            return False

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                UPDATE TICKET
                SET PRIORIDAD = ?
                WHERE ID_TICKET = ?
            """,
                prioridad,
                id_ticket
            )

            conexion.commit()
            return True

        except Exception as e:
            print("Error al actualizar prioridad:")
            print(e)
            conexion.rollback()
            return False

        finally:
            conexion.close()


    def actualizar_tiempo_prioridad(self, ticket):
        conexion = Conexion().conectar()

        if conexion is None:
            return False

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                UPDATE TICKET
                SET
                    TIEMPO_ESPERA = ?,
                    PRIORIDAD = ?
                WHERE ID_TICKET = ?
            """,
                ticket.tiempo_espera,
                ticket.prioridad,
                ticket.id_ticket
            )

            conexion.commit()
            return True

        except Exception as e:
            print("Error al actualizar ticket:")
            print(e)
            conexion.rollback()
            return False

        finally:
            conexion.close()


    def eliminar(self, id_ticket):
        conexion = Conexion().conectar()

        if conexion is None:
            return False

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                DELETE FROM TICKET
                WHERE ID_TICKET = ?
            """, id_ticket)

            conexion.commit()
            return True

        except Exception as e:
            print("Error al eliminar ticket:")
            print(e)
            conexion.rollback()
            return False

        finally:
            conexion.close()

    def actualizar_hrn(self):
        conexion = Conexion().conectar()

        if conexion is None:
            return False

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                           UPDATE T
                           SET T.TIEMPO_ESPERA = T.TIEMPO_ESPERA + 1,

                               T.PRIORIDAD     =
                                   CAST(
                                           (T.TIEMPO_ESPERA + 1) + E.TIEMPO_DE_ATENCION
                                       AS DECIMAL(10, 2)
                                   )
                                       /
                                   E.TIEMPO_DE_ATENCION FROM TICKET T

                INNER JOIN ENFERMEDAD E
                           ON T.ID_ENFERMEDAD = E.ID_ENFERMEDAD
                           """)

            conexion.commit()
            return True

        except Exception as e:
            print("Error al actualizar HRN:")
            print(e)

            conexion.rollback()
            return False

        finally:
            conexion.close()

    def actualizar_hrn_excepto(self, id_ticket_atencion):
        conexion = Conexion().conectar()

        if conexion is None:
            return False

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                           UPDATE T
                           SET T.TIEMPO_ESPERA = T.TIEMPO_ESPERA + 1,

                               T.PRIORIDAD     =
                                   CAST(
                                           (T.TIEMPO_ESPERA + 1) + E.TIEMPO_DE_ATENCION
                                       AS DECIMAL(10, 2)
                                   )
                                       /
                                   E.TIEMPO_DE_ATENCION FROM TICKET T

                INNER JOIN ENFERMEDAD E
                           ON T.ID_ENFERMEDAD = E.ID_ENFERMEDAD

                           WHERE T.ID_TICKET <> ?
                           """, id_ticket_atencion)

            conexion.commit()

            return True

        except Exception as e:
            print("Error al actualizar HRN:")
            print(e)

            conexion.rollback()

            return False

        finally:
            conexion.close()