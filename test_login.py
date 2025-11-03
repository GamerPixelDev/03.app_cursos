from models.usuarios import autenticar_usuario

usuario = input("Nombre de usuario: ")
contraseña = input("Contraseña: ")

valido, rol = autenticar_usuario(usuario, contraseña)
if valido:
    print(f"Autenticación exitosa. Rol: {rol}")
else:
    print("Autenticación fallida. Usuario o contraseña incorrectos.")