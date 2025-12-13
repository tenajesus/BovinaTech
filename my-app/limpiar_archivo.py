#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script para limpiar bytes nulos del archivo funciones_home.py"""

import os

archivo = 'controllers/funciones_home.py'

# Leer el archivo en modo binario
with open(archivo, 'rb') as f:
    content = f.read()

# Eliminar bytes nulos
content_limpio = content.replace(b'\x00', b'')

# Escribir el archivo limpio
with open(archivo, 'wb') as f:
    f.write(content_limpio)

print(f"Archivo {archivo} limpiado exitosamente")
print(f"Bytes nulos eliminados: {content.count(b'\\x00')}")
