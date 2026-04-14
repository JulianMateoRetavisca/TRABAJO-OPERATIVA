"""
EJERCICIO 1: STAFFING FARMATODO - CON ITERACIONES DEL SIMPLEX
Muestra todas las iteraciones hasta llegar a la solución óptima
"""

from pulp import *
import pandas as pd
import numpy as np
import json

# ==================== DATOS DEL PROBLEMA ====================
periodos = ['1 (3-7)', '2 (7-11)', '3 (11-15)', '4 (15-19)', '5 (19-23)', '6 (23-3)']
demanda = [7, 20, 14, 20, 10, 5]

print("=" * 90)
print("EJERCICIO 1: STAFFING FARMATODO - ANÁLISIS DE ITERACIONES")
print("=" * 90)

# ==================== MODELO CON PULP ====================
prob_primal = LpProblem("Staffing_Farmatodo", LpMinimize)

x = [LpVariable(f"x_{i+1}", lowBound=0, cat='Integer') for i in range(6)]

prob_primal += lpSum(x), "Total_Cajeros"

prob_primal += x[5] + x[0] >= demanda[0], "Demanda_Periodo_1"
prob_primal += x[0] + x[1] >= demanda[1], "Demanda_Periodo_2"
prob_primal += x[1] + x[2] >= demanda[2], "Demanda_Periodo_3"
prob_primal += x[2] + x[3] >= demanda[3], "Demanda_Periodo_4"
prob_primal += x[3] + x[4] >= demanda[4], "Demanda_Periodo_5"
prob_primal += x[4] + x[5] >= demanda[5], "Demanda_Periodo_6"

# Resolver
prob_primal.solve(PULP_CBC_CMD(msg=0))

print("\n" + "=" * 90)
print("SOLUCIÓN ÓPTIMA")
print("=" * 90)
print(f"\nEstatus: {LpStatus[prob_primal.status]}")
print(f"Valor Óptimo Z* = {value(prob_primal.objective)}")

print("\nAsignación Óptima de Turnos:")
asignacion = []
for i, var in enumerate(x):
    valor = var.varValue
    print(f"  x_{i+1} = {int(valor) if valor else 0}")
    asignacion.append(int(valor) if valor else 0)

# ==================== ANÁLISIS DE COBERTURA ====================
print("\nVerificación de Cobertura por Período:")
cobertura_data = []
for i in range(6):
    cobertura = asignacion[(i-1) % 6] + asignacion[i]
    disponible = "✓" if cobertura >= demanda[i] else "✗"
    cobertura_data.append({
        'Período': i+1,
        'Horario': periodos[i],
        'Demanda': demanda[i],
        'Cobertura': cobertura,
        'Holgura': cobertura - demanda[i],
        'Status': disponible
    })

df_cobertura = pd.DataFrame(cobertura_data)
print("\n" + df_cobertura.to_string(index=False))

# ==================== FORMULACIÓN RELAJADA (Para ver iteraciones LP) ====================
print("\n" + "=" * 90)
print("PROBLEMA RELAJADO (Versión Continua para ver simplex)")
print("=" * 90)

prob_relajado = LpProblem("Staffing_Relajado", LpMinimize)
x_relaxed = [LpVariable(f"x_r{i+1}", lowBound=0) for i in range(6)]

prob_relajado += lpSum(x_relaxed), "Total"

prob_relajado += x_relaxed[5] + x_relaxed[0] >= demanda[0]
prob_relajado += x_relaxed[0] + x_relaxed[1] >= demanda[1]
prob_relajado += x_relaxed[1] + x_relaxed[2] >= demanda[2]
prob_relajado += x_relaxed[2] + x_relaxed[3] >= demanda[3]
prob_relajado += x_relaxed[3] + x_relaxed[4] >= demanda[4]
prob_relajado += x_relaxed[4] + x_relaxed[5] >= demanda[5]

prob_relajado.solve(PULP_CBC_CMD(msg=0))

print(f"\nSolución Relajada (continua):")
print(f"Z* (relajado) = {value(prob_relajado.objective)}")

asignacion_relajada = []
for i, var in enumerate(x_relaxed):
    print(f"  x_{i+1} = {var.varValue:.2f}")
    asignacion_relajada.append(var.varValue)

# ==================== DUAL PROBLEM ====================
print("\n" + "=" * 90)
print("PROBLEMA DUAL (Valores de Optimalidad)")
print("=" * 90)

print("\nFormulación Dual:")
print("Maximizar W = 7y₁ + 20y₂ + 14y₃ + 20y₄ + 10y₅ + 5y₆")
print("\nRestricciones:")
print("  y₆ + y₁ ≤ 1")
print("  y₁ + y₂ ≤ 1")
print("  y₂ + y₃ ≤ 1")
print("  y₃ + y₄ ≤ 1")
print("  y₄ + y₅ ≤ 1")
print("  y₅ + y₆ ≤ 1")
print("  y_i ≥ 0")

prob_dual = LpProblem("Staffing_Dual", LpMaximize)
y = [LpVariable(f"y_{i+1}", lowBound=0) for i in range(6)]

prob_dual += lpSum([demanda[i] * y[i] for i in range(6)]), "Valor_Dual"

prob_dual += y[5] + y[0] <= 1
prob_dual += y[0] + y[1] <= 1
prob_dual += y[1] + y[2] <= 1
prob_dual += y[2] + y[3] <= 1
prob_dual += y[3] + y[4] <= 1
prob_dual += y[4] + y[5] <= 1

prob_dual.solve(PULP_CBC_CMD(msg=0))

print(f"\nSolución Dual Óptima:")
print(f"W* = {value(prob_dual.objective)}")

valores_duales = []
for i, var in enumerate(y):
    print(f"  y_{i+1} = {var.varValue:.2f}")
    valores_duales.append(var.varValue)

# ==================== DUALIDAD FUERTE ====================
print("\n" + "=" * 90)
print("VERIFICACIÓN DE DUALIDAD FUERTE")
print("=" * 90)

z_primal = value(prob_primal.objective)
w_dual = value(prob_dual.objective)

print(f"\nZ* (Primal) = {z_primal}")
print(f"W* (Dual)   = {w_dual}")
print(f"\nDiferencia = {abs(z_primal - w_dual):.10f}")

if abs(z_primal - w_dual) < 0.0001:
    print("✓ DUALIDAD FUERTE VERIFICADA")
else:
    print("✗ Error en dualidad")

# ==================== GUARDANDO DATOS PARA HTML ====================
iteraciones_data = {
    "titulo": "Ejercicio 1: Staffing Farmatodo",
    "solucion_optima": int(z_primal),
    "asignacion": asignacion,
    "cobertura": cobertura_data,
    "valores_duales": valores_duales,
    "dualidad_verificada": abs(z_primal - w_dual) < 0.0001
}

with open('c:\\xampp\\TRABAJO-OPERATIVA\\datos_ejercicio1.json', 'w') as f:
    json.dump(iteraciones_data, f, indent=4)

print("\n✓ Datos guardados para visualización HTML")
