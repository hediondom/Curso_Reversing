# -*- coding: utf-8 -*-
"""Corta el Tomo I en Parte A / Parte B justo antes de la portadilla 'PARTE B',
verificando paridad par en ambas partes. Elimina los cortes viejos del directorio."""
import os, glob, pypdf

BASE = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(BASE, "Tomo_1_Tronco_y_Apoyo.pdf")
r = pypdf.PdfReader(src)
total = len(r.pages)

corte = None
for i, pg in enumerate(r.pages):
    t = pg.extract_text() or ""
    if "PARTE B" in t and "Reversing Avanzado" in t:
        corte = i
        break
assert corte is not None, "No se encontró la portadilla de la Parte B"
assert corte % 2 == 0 and (total - corte) % 2 == 0, f"Paridad impar: A={corte}, B={total - corte}"

nom_a = f"Tomo_1_Parte_A_pags_1-{corte}.pdf"
nom_b = f"Tomo_1_Parte_B_pags_{corte + 1}-{total}.pdf"

# Borrar cortes anteriores para no dejar duplicados
for viejo in glob.glob(os.path.join(BASE, "Tomo_1_Parte_A_pags_*.pdf")) + glob.glob(os.path.join(BASE, "Tomo_1_Parte_B_pags_*.pdf")):
    if os.path.basename(viejo) not in (nom_a, nom_b):
        os.remove(viejo)
        print("Eliminado corte viejo:", os.path.basename(viejo))

for nombre, rango in [(nom_a, (0, corte)), (nom_b, (corte, total))]:
    w = pypdf.PdfWriter()
    w.append(r, pages=rango)
    with open(os.path.join(BASE, nombre), "wb") as f:
        w.write(f)
    n = rango[1] - rango[0]
    print(f"{nombre}: {n} págs. = {n // 2} hojas (par: {n % 2 == 0})")
