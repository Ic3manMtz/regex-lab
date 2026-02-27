#!/bin/bash

PASSWORD_FILE="../data/passwords_muestra.txt"
OUT_DIR="../out"
VALID_REPORT="$OUT_DIR/validas.txt"
INVALID_REPORT="$OUT_DIR/invalidas.txt"

function password_validator() {
    > "$VALID_REPORT"
    > "$INVALID_REPORT"

    while IFS= read -r pass || [[ -n "$pass" ]]; do
        reason=""
        is_valid=true

        # 1. Validar caracteres inválidos (solo alfanuméricos)
        if [[ "$pass" =~ [^a-zA-Z0-9] ]]; then
            reason+="tiene caracteres inválidos"
            is_valid=false
        fi

        # 2. Validar longitud
        if [[ ${#pass} -lt 8 ]]; then
            reason+="longitud insuficiente"
            is_valid=false
        fi

        # 3. Validar mayúscula
        if [[ ! "$pass" =~ [A-Z] ]]; then
            reason+="no tiene mayúscula"
            is_valid=false
        fi

        # 4. Validar dígito
        if [[ ! "$pass" =~ [0-9] ]]; then
            reason+="no tiene dígito"
            is_valid=false
        fi

        if [ "$is_valid" = true ]; then
            echo "$pass" >> "$VALID_REPORT"
            ((val_count++))
        else
            echo "$pass -> Razones: $reason" >> "$INVALID_REPORT"
            ((inv_count++))
        fi
    done < "$PASSWORD_FILE"

    echo -e "\n Se guardaron $val_count contraseñans válidas en: $VALID_REPORT"
    echo -e " Se guardaron $inv_count contraseñas inválidas guadada en: $INVALID_REPORT\n\n"
}

function greeting() {
    echo ""
    echo -e " ---- Bienvenido al sistema de validación de contraseñas ---- \n"
    echo ""

    echo -e "\nEspera un momento estamos analizando el archivo $PASSWORD_FILE...\n\n"
    sleep 1
    password_validator
}

greeting