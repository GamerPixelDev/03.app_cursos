import bcrypt

hash_guardado = "$2b$12$7vA7oFkbmEqlzC7Lb0WZZu7Gv1Pp8NQpdaMWJMyPS4PtT3hr/XpH2"
password_correcta = "admin123"
password_incorrecta = "otra"

print("Hash en bytes:", hash_guardado.encode())

print("✓ Coincide admin123:", bcrypt.checkpw(password_correcta.encode(), hash_guardado.encode()))
print("✗ Coincide otra:", bcrypt.checkpw(password_incorrecta.encode(), hash_guardado.encode()))
