#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Formato: ClrMamePro
Notas: Esta rutina conserva los bloques 'game' que contengan la palabra 'cloneof'
y descarta el resto. Adicionalmente, dentro de los bloques que contienen 'cloneof',
se descartan aquellos cuya descripción (línea que empieza con "description")
contenga (entre paréntesis) las palabras "hack", "bootleg" o "prototype".
"""
__author__ = "Felipe Bonnemaison"
__python_ver__ = "IronPython 2.7.9"

# IMPORTS
import re
import sys

# FUNCTIONS
def contar_parentesis(linea):
    """
    Cuenta los paréntesis de apertura y cierre en la línea,
    ignorando el contenido que esté entre comillas.
    """
    # Se elimina el contenido entre comillas dobles para evitar contar paréntesis que estén dentro.
    sin_comillas = re.sub(r'".*?"', '', linea)
    return sin_comillas.count('('), sin_comillas.count(')')

def descripcion_contiene_palabras(linea, palabras):
    """
    Revisa la línea de descripción extrayendo el contenido entre paréntesis
    y verifica si en alguno de ellos aparece alguna de las palabras clave.
    """
    grupos = re.findall(r'\((.*?)\)', linea)
    for grupo in grupos:
        texto = grupo.lower()
        for palabra in palabras:
            if palabra in texto:
                return True
    return False

def procesar_archivos(archivo_entrada, archivo_salida):
    # Leemos todas las líneas del archivo de entrada.
    with open(archivo_entrada, "r") as f:
        lineas = f.readlines()

    resultado = []
    dentro_bloque = False
    bloque_actual = []
    nivel = 0
    # Palabras clave a buscar en la línea "description"
    palabras_clave = ["hack", "bootleg", "prototype"]

    i = 0
    while i < len(lineas):
        linea = lineas[i]
        if not dentro_bloque:
            # Detectamos el inicio de un bloque game (
            if linea.lstrip().startswith("game ("):
                dentro_bloque = True
                bloque_actual = [linea]
                ab, ce = contar_parentesis(linea)
                nivel = ab - ce
            else:
                # Línea fuera de cualquier bloque game, se conserva.
                resultado.append(linea)
        else:
            bloque_actual.append(linea)
            ab, ce = contar_parentesis(linea)
            nivel += ab - ce

            # Cuando el balance de paréntesis vuelve a cero o es negativo, el bloque finaliza.
            if nivel <= 0:
                # Primero: verificar que el bloque contenga "cloneof"
                # Segundo: descartar si en la descripción se encuentra alguna palabra prohibida.
                tiene_cloneof = False
                desc_con_palabras_prohibidas = False
                for bline in bloque_actual:
                    if re.search(r'\bcloneof\b', bline):
                        tiene_cloneof = True
                    # Verificar solo en la línea description
                    if bline.lstrip().startswith("description"):
                        if descripcion_contiene_palabras(bline, palabras_clave):
                            desc_con_palabras_prohibidas = True
                # Solo se conserva el bloque si contiene "cloneof" y NO tiene palabras
                # prohibidas en la sección de descripción.
                if tiene_cloneof and not desc_con_palabras_prohibidas:
                    resultado.extend(bloque_actual)
                # Reiniciamos variables para procesar el siguiente bloque.
                dentro_bloque = False
                bloque_actual = []
                nivel = 0
        i += 1

    # Escribimos el resultado en el archivo de salida.
    with open(archivo_salida, "w") as f:
        f.writelines(resultado)

# MAIN
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: datOnlyClonesNeo.py archivo_entrada.dat archivo_salida.dat")
        sys.exit(1)
    procesar_archivos(sys.argv[1], sys.argv[2])
