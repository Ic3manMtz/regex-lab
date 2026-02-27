import re
import os

INPUT_FILE = "../data/passwords_muestra.txt"
OUT_DIR = "../out"
VALID_REPORT = os.path.join(OUT_DIR, "validas.txt")
INVALID_REPORT = os.path.join(OUT_DIR, "invalidas.txt")

def password_validator():
    os.makedirs(OUT_DIR, exist_ok=True)
    
    val_count = 0
    inv_count = 0

    try:
        with open(INPUT_FILE, 'r') as input_file, \
             open(VALID_REPORT, 'w') as valid_report, \
             open(INVALID_REPORT, 'w') as invalid_report:

            for line in input_file:
                password = line.strip()
                if not password:
                    continue

                reason = ""
                
                # 1. Validar caracteres inválidos (solo alfanuméricos)
                if re.search(r'[^a-zA-Z0-9]', password):
                    reason+="tiene caracteres inválidos"
                
                # 2. Validar longitud
                if len(password) < 8:
                    reason+="longitud insuficiente"
                
                # 3. Validar mayúscula
                if not re.search(r'[A-Z]', password):
                    reason+="no tiene mayúscula"
                
                # 4. Validar dígito
                if not re.search(r'[0-9]', password):
                    reason+="no tiene dígito"

                if not reason:
                    valid_report.write(f"{password}\n")
                    val_count += 1
                else:
                    invalid_report.write(f"{password} -> Razón: {reason}\n")
                    inv_count += 1

        print(f"\nSe guardaron {val_count} contraseñas válidas en: {VALID_REPORT}")
        print(f"Se guardaron {inv_count} contraseñas inválidas en: {INVALID_REPORT}\n")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {INPUT_FILE}")

if __name__ == "__main__":
    print("\n---- Bienvenido al sistema de validación de contraseñas (Python) ----")
    password_validator()