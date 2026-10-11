from conexion import Conexion
from Enfermedad import Enfermedad


class EnfermedadDAO:

    def obtener_todas(self):
        conexion = Conexion().conectar()

        if conexion is None:
            return []

        try:
            cursor = conexion.cursor()

            cursor.execute("""
                SELECT
                    ID_ENFERMEDAD,
                    NOMBRE,
                    DESCRIPCION,
                    TIEMPO_DE_ATENCION
                FROM ENFERMEDAD
            """)

            enfermedades = []

            for fila in cursor.fetchall():
                enfermedad = Enfermedad(
                    id_enfermedad=fila.ID_ENFERMEDAD,
                    nombre=fila.NOMBRE,
                    descripcion=fila.DESCRIPCION,
                    tiempo_de_atencion=fila.TIEMPO_DE_ATENCION
                )

                enfermedades.append(enfermedad)

            return enfermedades

        except Exception as e:
            print("Error al obtener las enfermedades:")
            print(e)
            return []

        finally:
            conexion.close()