from models import usuarios

def test_usuarios():
    print("\n🧩 Probando módulo usuarios...")
    
    print("➕ Creando usuario de prueba...")
    usuarios.crear_usuario("test_user", "1234", "usuario")

    print("🔍 Verificando login...")
    ok, rol = usuarios.autenticar_usuario("test_user", "1234")
    print(f"Resultado login: {ok}, rol: {rol}")

    print("🔑 Cambiando contraseña...")
    usuarios.cambiar_contrasena("test_user", "5678")
    ok, _ = usuarios.autenticar_usuario("test_user", "5678")
    print(f"Login con nueva contraseña: {ok}")

    print("🗑️ Eliminando usuario de prueba...")
    usuarios.eliminar_usuario("test_user")
    ok, _ = usuarios.autenticar_usuario("test_user", "5678")
    print(f"Login tras borrado (debe ser False): {ok}")

if __name__ == "__main__":
    test_usuarios()
