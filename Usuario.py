import mysql.connector
from mysql.connector import Error
from databaseConnection import DatabaseConnection  # Asegúrate de que DatabaseConnection esté en el mismo directorio o la ruta correcta.
import bcrypt  # Necesitarás instalar la librería bcrypt: pip install bcrypt

class User:
    def __init__(self, db_connection):
        """
        Inicializa la clase User con una instancia de DatabaseConnection.
        
        :param db_connection: Instancia de la clase DatabaseConnection para conectar a la base de datos.
        """
        self.db_connection = db_connection
        self.user = None
        self.password = None
        self.user_id = None

    def login(self, usuario, password):
        """
        Verifica las credenciales del usuario (usuario y contraseña) y autentica el inicio de sesión.

        :param usuario: Nombre de usuario del administrador.
        :param password: Contraseña proporcionada por el administrador.
        :return: True si el inicio de sesión es exitoso, False en caso contrario.
        """
        # Consulta para obtener los datos del usuario con el nombre de usuario proporcionado.
        query = "SELECT ID, usuario, contrasena FROM administrador WHERE usuario = %s"
        params = (usuario,)  # Asegúrate de pasar `params` como una tupla, nota la coma al final.

        # Obtener los datos del usuario desde la base de datos.
        user_data = self.db_connection.fetch_results(query, params)

        # Si se encuentran resultados, verifica la contraseña.
        if user_data and len(user_data) > 0:
            stored_password = user_data[0][2]  # La contraseña almacenada en la base de datos.

            # Verificar la contraseña utilizando bcrypt.
            if password.encode('utf-8') == stored_password.encode('utf-8'):
                print("Inicio de sesión exitoso.")
                # Guardar la información del usuario en la instancia de la clase.
                self.user_id, self.usuario, _, = user_data[0]
                return True
            else:
                print("Contraseña incorrecta.")
                return False
        else:
            print("Usuario no encontrado.")
            return False


    def register(self, email, password, first_name, last_name):
        """
        Registra un nuevo usuario en la base de datos con la información proporcionada.
        
        :param email: Correo electrónico del nuevo usuario.
        :param password: Contraseña del nuevo usuario.
        :param first_name: Nombre del nuevo usuario.
        :param last_name: Apellido del nuevo usuario.
        :return: True si el registro fue exitoso, False de lo contrario.
        """
        # Cifrar la contraseña usando bcrypt.
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Consulta de inserción.
        query = "INSERT INTO users (email, password, first_name, last_name) VALUES (%s, %s, %s, %s)"
        params = (email, hashed_password.decode('utf-8'), first_name, last_name)

        # Ejecutar la consulta.
        if self.db_connection.execute_query(query, params):
            print("Usuario registrado con éxito.")
            return True
        else:
            print("Error al registrar el usuario.")
            return False

    def get_user_data(self, email):
        """
        Obtiene los datos del usuario basado en el correo proporcionado.
        
        :param email: Correo electrónico del usuario.
        :return: Diccionario con los datos del usuario si se encuentra, None de lo contrario.
        """
        query = "SELECT id, email, first_name, last_name FROM users WHERE email = %s"
        params = (email,)
        user_data = self.db_connection.fetch_results(query, params)

        if user_data:
            return {
                'id': user_data[0][0],
                'email': user_data[0][1],
                'first_name': user_data[0][2],
                'last_name': user_data[0][3]
            }
        else:
            print("No se encontró el usuario con el correo proporcionado.")
            return None

# Ejemplo de uso de la clase User
if __name__ == "__main__":
    # Crear una instancia de la conexión a la base de datos.
    db = DatabaseConnection()
    db.connect()

    # Crear una instancia de User y pasarle la conexión de la base de datos.
    user = User(db)
    
    # Registrar un nuevo usuario (opcional, para probar).
    # user.register('test@example.com', 'securepassword123', 'John', 'Doe')

    # Intentar iniciar sesión con un usuario existente.
    if user.login('test@example.com', 'securepassword123'):
        print(f"Bienvenido {user.first_name} {user.last_name}!")
    else:
        print("Error al iniciar sesión.")
    
    db.disconnect()
