#!/bin/bash

LOG_FILE="../data/log_muestra_app.log"
OUT_DIR="../out"
JSON_REPORT="$OUT_DIR/reporte_log.json"
LOG_LEVEL=""

VALID_REPORT=""

function logSelector() {
    local opt="$1"

    case $opt in
        1) LOG_LEVEL="INFO";;
        2) LOG_LEVEL="WARN";;
        3) LOG_LEVEL="ERROR";;
        4) LOG_LEVEL="DEBUG";;
        *) echo -e  " \n\tGracias por usar el sistema, hasta luego!\n"
           exit 0
           ;;
    esac
}


function greeting() {
    echo ""
    echo -e " ---- Bienvenido al sistema de análsis de logs ---- \n"
    echo ""

    while true; do
        echo "Seleccione el nivel de log que quiere revisar"
        echo " 1.- INFO"
        echo " 2.- WARN"
        echo " 3.- ERROR"
        echo " 4.- DEBUG"
        echo " 5.- Salir del sistema"
        read opt

        if [ "$opt" -gt 5 ] || [ "$opt" -lt 1 ]; then
            echo -e "\n\tOpción inválida, intente de nuevo\n"
        else
            logSelector "$opt"
            break
        fi
    done
}

function read_log() {
    VALID_REPORT="$OUT_DIR/${LOG_LEVEL}_validos.txt"

    echo -e "\n Leyendo archivo con logs para el nivel [$LOG_LEVEL]... "
    grep -E "\[$LOG_LEVEL\] [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} .+" "$LOG_FILE" > "$VALID_REPORT"
    echo -e "\n Se han guardado las líneas válidas en: $VALID_REPORT. "
}

function generate_metrics() {
    local non_empty=$(grep -c -v '^$' "$LOG_FILE")
    local validated=$(grep -c "^" "$VALID_REPORT" )
    
    local suspicious=$(grep "\[${LOG_LEVEL}\]" "$LOG_FILE" | grep -E -v -c "\[$LOG_LEVEL\] [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} .+")

    echo -e "\n\tTotal de líneas no vacías: $non_empty"
    echo -e "\tTotal de líneas válidas para el nivel [$LOG_LEVEL]: $validated"
    echo -e "\tTotal de líneas que tienen el nivel [$LOG_LEVEL] pero no el formato: $suspicious\n\n"

    create_json "$non_empty" "$validated" "$suspicious"
}

function create_json() {
    local fecha_actual=$(date '+%Y-%m-%d %H:%M:%S')
    
    local json_template='{
    "reporte": {
        "nivel": "%s",
        "fecha": "%s",
        "metricas": {
        "no_vacias": %d,
        "validas": %d,
        "sospechosas": %d
        }
    }
}\n'

    echo -e "\n Generando reporte para el nivel [$LOG_LEVEL]"
    printf "$json_template" "$LOG_LEVEL" "$fecha_actual" "$1" "$2" "$3" > "$JSON_REPORT"
    echo -e "\n Se ha guardado el reporte en: $JSON_REPORT.\n\n"
}

greeting
read_log
generate_metrics

