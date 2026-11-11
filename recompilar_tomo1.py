# -*- coding: utf-8 -*-
"""Recompila SOLO el Tomo I (con las fuentes HTML actuales), protegiendo Tomo II y Separata.

construir_suite.generar_tomos_y_separata() también regenera Tomo II (versión vieja de 160 págs.)
y la Separata, por eso se respaldan antes y se restauran al terminar.
"""
import importlib.util
import os
import shutil
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(BASE, "_trabajo", "backup_recompilar_t1")
PROTEGIDOS = [
    "Tomo_2_Kernel_e_Internals.pdf",
    "Separata_Escritorio.pdf",
    "Tomo_3_LLVM_Rust_Contenedores_IA.pdf",
    "Tomo_1_Tronco_y_Apoyo.pdf",
    "Tomo_1_Parte_A_pags_1-178.pdf",
    "Tomo_1_Parte_B_pags_179-410.pdf",
    "CLS_Curso_Reversing.pdf",
]

os.makedirs(BACKUP, exist_ok=True)
for f in PROTEGIDOS:
    p = os.path.join(BASE, f)
    if os.path.exists(p):
        shutil.copy2(p, os.path.join(BACKUP, f))
print(f"Respaldo creado en {BACKUP}")

spec = importlib.util.spec_from_file_location("construir_suite_root", os.path.join(BASE, "construir_suite.py"))
cs = importlib.util.module_from_spec(spec)
sys.modules["construir_suite_root"] = cs
spec.loader.exec_module(cs)

try:
    ctx = cs.generar_pdf_completo()
    cs.generar_tomos_y_separata(ctx)
finally:
    # Restaurar volúmenes que NO deben cambiar
    for f in ["Tomo_2_Kernel_e_Internals.pdf", "Separata_Escritorio.pdf", "Tomo_3_LLVM_Rust_Contenedores_IA.pdf"]:
        b = os.path.join(BACKUP, f)
        if os.path.exists(b):
            shutil.copy2(b, os.path.join(BASE, f))
            if cs.ARTIFACT_DIR and os.path.isdir(cs.ARTIFACT_DIR):
                shutil.copy2(b, os.path.join(cs.ARTIFACT_DIR, f))
    print("Tomo II, Tomo III y Separata restaurados desde el respaldo.")

import pypdf
r = pypdf.PdfReader(os.path.join(BASE, "Tomo_1_Tronco_y_Apoyo.pdf"))
print(f"\nTomo I recompilado: {len(r.pages)} páginas")
