#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Formato: ClrMamePro
Notas: Esta rutina iguala el nombre del archivo ZIP al nombre del archivo rom de NEOGEO (.neo)
para archivos .dat de ClrMamePro. El script busca la línea 'rom ( name' y reemplaza el valor
del parámetro 'name' (si la línea contiene ÚNICAMENTE ese atributo) usando el nuevo valor, eliminando
la extensión '.neo' si está presente.
"""
__author__ = "Felipe Bonnemaison"
__python_ver__ = "IronPython 2.7.9"

# IMPORTS
import re
import sys

# FUNCTIONS
def process_game_block(block_lines):
    """
    Procesa un bloque 'game ( ... )':
    - Busca en la línea que comienza con 'rom ( name' el valor entre comillas.
    - Si lo encuentra, reemplaza el valor del parámetro 'name' (si la línea contiene ÚNICAMENTE ese atributo)
        usando el nuevo valor, eliminando la extensión '.neo' si está presente.
    """
    new_name = None
    # Buscamos la línea de "rom ( name ..." y extraemos su valor
    rom_regex = re.compile(r'^\s*rom\s*\(\s*name\s+"([^"]+)"', re.IGNORECASE)
    for line in block_lines:
        m = rom_regex.match(line)
        if m:
            new_name = m.group(1)
            break

    # Si el nombre finaliza en ".neo", removemos esa extensión
    if new_name and new_name.endswith(".neo"):
        new_name = new_name[:-4]

    if new_name:
        new_block = []
        # Sólo modificamos la línea 'name' si contiene ÚNICAMENTE ese atributo y nada más.
        name_regex = re.compile(r'^(\s*name\s+)"[^"]+"\s*$', re.IGNORECASE)
        for line in block_lines:
            m = name_regex.match(line)
            if m:
                # Reconstruimos la línea preservando la indentación
                new_line = m.group(1) + '"' + new_name + '"' + "\n"
                new_block.append(new_line)
            else:
                new_block.append(line)
        return new_block
    else:
        # Si no se encontró la línea "rom ( name", no se modifica el bloque.
        return block_lines

def process_file(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    new_lines = []
    inside_game = False
    block_lines = []
    game_start = re.compile(r'^\s*game\s*\(', re.IGNORECASE)
    game_end   = re.compile(r'^\s*\)\s*$', re.IGNORECASE)

    for line in lines:
        if game_start.match(line):
            inside_game = True
            block_lines = [line]
        elif inside_game:
            block_lines.append(line)
            if game_end.match(line):
                processed_block = process_game_block(block_lines)
                new_lines.extend(processed_block)
                inside_game = False
                block_lines = []
        else:
            new_lines.append(line)

    # Agrega cualquier bloque pendiente sin procesar
    if block_lines:
        new_lines.extend(block_lines)

    with open(output_file, 'w') as f:
        f.writelines(new_lines)

def main():
    if len(sys.argv) < 3:
        print("Uso: python script.py archivo_entrada.dat archivo_salida.dat")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    process_file(input_file, output_file)
    print("Archivo procesado y guardado en", output_file)

# MAIN
if __name__ == "__main__":
    main()
