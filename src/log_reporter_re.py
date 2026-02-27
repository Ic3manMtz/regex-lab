import re
import os
from datetime import datetime
import json

def greeting():
    print(" ---- Bienvenido al sistema de análisis de logs ---- \n")
    log_level=""
    while True:
        print("Seleccione el nivel de log que quiere revisar")
        print(" 1.- INFO")
        print(" 2.- WARN")
        print(" 3.- ERROR")
        print(" 4.- DEBUG")
        print(" 5.- Salir del sistema")
        opt = input("")

        if not opt.isdigit():
            print("\n\tPor favor, ingrese un número válido\n")
            continue

        opt_int = int(opt)

        if opt_int>5 or opt_int<1:
            print("\n\tOpción inválida, intente de nuevo\n")
        else:
            log_level=logSelector(opt_int)
            readLog(log_level)
            continue

def logSelector(opt):
    print(f"Opción seleccionada {opt}")
    match opt:
        case 1: return "INFO"
        case 2: return "WARN"
        case 3: return "ERROR"
        case 4: return "DEBUG"
        case 5: 
            print("\n\tGracias por usar el sistema, hasta luego!\n")
            exit(0)

def readLog(log_level):
    valid_report=os.path.join("../out", f"{log_level}_validos.txt")
    log_file="../data/log_muestra_app.log"
    pattern = rf"\[{log_level}\] [0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}} [0-9]{{2}}:[0-9]{{2}}:[0-9]{{2}} .+"
    
    print(f"\n Leyendo archivo con logs para el nivel [{log_level}]...")

    try:
        with open(log_file, 'r') as f_in, open(valid_report, 'w') as f_out:
            for line in f_in:
                if re.search(pattern, line):
                    f_out.write(line)
                    
        print(f"\n Se han guardado las líneas válidas en: {valid_report}. ")
        generateMetrics(log_level,log_file,valid_report)
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {log_file}")

def generateMetrics(log_level,log_file,valid_report):
    non_empty=0
    validated=0
    suspicious=0

    pattern_valid = rf"\[{log_level}\] [0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}} [0-9]{{2}}:[0-9]{{2}}:[0-9]{{2}} .+"

    try:
        with open(valid_report, 'r') as f_val:
            validated = sum(1 for line in f_val if line.strip())

        with open(log_file, 'r') as f_log:
            for line in f_log:
                clean_line = line.strip()
                
                if clean_line:
                    non_empty += 1
                    
                    if f"[{log_level}]" in clean_line:
                        if not re.search(pattern_valid, clean_line):
                            suspicious += 1

        print(f"\n\tTotal de líneas no vacías: {non_empty}")
        print(f"\tTotal de líneas válidas para el nivel [{log_level}]: {validated}")
        print(f"\tTotal de líneas que tienen el nivel [{log_level}] pero no el formato: {suspicious}\n\n")
        createJson(log_level,non_empty,validated,suspicious)
    except FileNotFoundError as e:
        print(f"Error al procesar archivos: {e}")


def createJson(log_level,non_empty,validated,suspicious):
    json_report="../out/reporte_log.json"
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    data = {
        "reporte": {
            "nivel": log_level,
            "fecha": fecha_actual,
            "metricas": {
                "no_vacias": non_empty,
                "validas": validated,
                "sospechosas": suspicious
            }
        }
    }

    print(f"\n Generando reporte para el nivel [{log_level}]")
    with open(json_report, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"\n Se ha guardado el reporte en: {json_report}.\n")

if __name__ == "__main__":
    greeting()