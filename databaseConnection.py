import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self, host='localhost', user='root', password='', database='gimsaber'):
        """
        Inicializa la clase con los parámetros de conexión.
        
        :param host: Dirección del servidor (por defecto es 'localhost').
        :param user: Nombre de usuario de la base de datos (por defecto es 'root').
        :param password: Contraseña del usuario.
        :param database: Nombre de la base de datos a la cual conectarse.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """
        Establece la conexión con la base de datos y la almacena en el atributo `self.connection`.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Conexión a la base de datos establecida con éxito.")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def disconnect(self):
        """
        Cierra la conexión con la base de datos.
        """
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            print("Conexión a la base de datos cerrada.")

    def execute_query(self, query, params=None):
        """
        Ejecuta una consulta en la base de datos.

        :param query: Consulta SQL a ejecutar.
        :param params: Parámetros opcionales para la consulta.
        :return: True si la consulta se ejecuta correctamente, False de lo contrario.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            print("Consulta ejecutada exitosamente.")
            return True
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return False

    def fetch_results(self, query, params=None):
        """
        Ejecuta una consulta de selección y devuelve los resultados.

        :param query: Consulta SQL a ejecutar.
        :param params: Parámetros opcionales para la consulta.
        :return: Resultados de la consulta como una lista de tuplas.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Error al obtener resultados: {e}")
            return None

# Ejemplo de uso de la clase DatabaseConnection
if __name__ == "__main__":
    db = DatabaseConnection()
    db.connect()  # Establecer la conexión con la base de datos.
    
    # Ejemplo de consulta para seleccionar usuarios.
    query = "SELECT * FROM users;"
    results = db.fetch_results(query)
    if results:
        for row in results:
            print(row)

    db.disconnect()  # Cerrar la conexión con la base de datos.
