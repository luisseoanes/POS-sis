# Importar las clases necesarias
from databaseConnection import DatabaseConnection  # Asegúrate de que este archivo contenga la clase DatabaseConnection.
from Usuario import User  # Asegúrate de que este archivo contenga la clase User.

def main():
    """
    Función principal del programa que permite al usuario iniciar sesión.
    """
    # Establecer conexión con la base de datos
    db = DatabaseConnection()
    db.connect()  # Conectar a la base de datos

    # Crear una instancia de la clase User pasando la conexión de la base de datos
    user = User(db)

    print("=== Sistema de Inicio de Sesión ===")
    email = input("Ingrese su correo electrónico: ")
    password = input("Ingrese su contraseña: ")

    # Intentar iniciar sesión
    if user.login(email, password):
        print(f"Bienvenido ")
        # Aquí se puede agregar la lógica adicional que debería ejecutarse después de iniciar sesión.
    else:
        print("Error al iniciar sesión. Verifique su correo y/o contraseña.")

    # Cerrar la conexión a la base de datos
    db.disconnect()

# Verificar si el script se está ejecutando como el programa principal
if __name__ == "__main__":
    main()
