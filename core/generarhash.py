from getpass import getpass

from core.auth import hash_password


if __name__ == "__main__":
    clave_plana = getpass("Contraseña a convertir en hash: ")
    print(hash_password(clave_plana))
