import pyodbc


class Conexion:

    def __init__(self):
        self.servidor = "localhost"
        self.base_datos = "CENTRO_POKEMON"

    def conectar(self):
        try:
            conexion = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={self.servidor};"
                f"DATABASE={self.base_datos};"
                f"Trusted_Connection=yes;"
            )

            print("Conexion exitosa a CENTRO_POKEMON")
            return conexion

        except Exception as e:
            print("Error al conectar con la base de datos:")
            print(e)
            return None