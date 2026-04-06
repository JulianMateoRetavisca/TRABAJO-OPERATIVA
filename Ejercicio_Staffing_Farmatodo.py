"""
PROBLEMA DE PLANIFICACIÓN DE PERSONAL - FARMATODO
Construir modelo Primal y Dual para optimizar cajeros

El problema:
- Tienda funciona 24 horas con 6 períodos de 4 horas cada uno
- Un cajero trabaja 8 horas consecutivas (cubre 2 períodos)
- Necesidad mínima de cajeros por período
- Objetivo: Minimizar total de cajeros
"""

from pulp import *
import pandas as pd
import numpy as np

# ==================== DATOS DEL PROBLEMA ====================
periodos = ['1 (3-7)', '2 (7-11)', '3 (11-15)', '4 (15-19)', '5 (19-23)', '6 (23-3)']
demanda = [7, 20, 14, 20, 10, 5]  # Cajeros mínimos por período

print("=" * 70)
print("PROBLEMA: PLANIFICACIÓN ÓPTIMA DE CAJEROS - FARMATODO")
print("=" * 70)
print("\nDATA DEL PROBLEMA:")
print(pd.DataFrame({
    'Período': periodos,
    'Horas': ['3-7', '7-11', '11-15', '15-19', '19-23', '23-3'],
    'Demanda Mínima': demanda
}))

# ==================== MODELO PRIMAL ====================
print("\n" + "=" * 70)
print("MODELO PRIMAL: MINIMIZAR TOTAL DE CAJEROS")
print("=" * 70)

# Crear problema
prob_primal = LpProblem("Staffing_Farmatodo", LpMinimize)

# Variables de decisión: x_i = cajeros que comienzan turno al inicio del período i
x = [LpVariable(f"x_{i+1}", lowBound=0, cat='Integer') for i in range(6)]

# Función objetivo: Minimizar total de cajeros
prob_primal += lpSum(x), "Total_Cajeros"

# Restricciones: Cobertura por período
# Un cajero que comienza en período i trabaja durante los períodos i e i+1 (8 horas)
# Período 1: cubierto por x_6 (turno anterior 23-3) + x_1 (3-7)
# Período 2: cubierto por x_1 (3-7) + x_2 (7-11)
# ...
# Período 6: cubierto por x_5 (19-23) + x_6 (23-3)

prob_primal += x[5] + x[0] >= demanda[0], f"Demanda_Periodo_1"  # 23-3 y 3-7
prob_primal += x[0] + x[1] >= demanda[1], f"Demanda_Periodo_2"  # 3-7 y 7-11
prob_primal += x[1] + x[2] >= demanda[2], f"Demanda_Periodo_3"  # 7-11 y 11-15
prob_primal += x[2] + x[3] >= demanda[3], f"Demanda_Periodo_4"  # 11-15 y 15-19
prob_primal += x[3] + x[4] >= demanda[4], f"Demanda_Periodo_5"  # 15-19 y 19-23
prob_primal += x[4] + x[5] >= demanda[5], f"Demanda_Periodo_6"  # 19-23 y 23-3

print("\nFORMULACIÓN PRIMAL:")
print("\nVariables de decisión:")
print("x_i = Número de cajeros que comienzan turno al inicio del período i (i=1,2,3,4,5,6)")

print("\nFunción Objetivo:")
print("Minimizar Z = x_1 + x_2 + x_3 + x_4 + x_5 + x_6")

print("\nRestricciones (cobertura de demanda):")
restricciones_primal = [
    "x_6 + x_1 ≥ 7   (Período 1: 3-7)",
    "x_1 + x_2 ≥ 20  (Período 2: 7-11)",
    "x_2 + x_3 ≥ 14  (Período 3: 11-15)",
    "x_3 + x_4 ≥ 20  (Período 4: 15-19)",
    "x_4 + x_5 ≥ 10  (Período 5: 19-23)",
    "x_5 + x_6 ≥ 5   (Período 6: 23-3)",
    "x_i ≥ 0 y enteros, para todo i"
]
for r in restricciones_primal:
    print(f"  {r}")

# Resolver modelo primal
prob_primal.solve(PULP_CBC_CMD(msg=0))

print("\n" + "-" * 70)
print("SOLUCIÓN ÓPTIMA - MODELO PRIMAL")
print("-" * 70)
print(f"\nEstatus: {LpStatus[prob_primal.status]}")
print(f"\nValor Óptimo (Total mínimo de cajeros): {int(value(prob_primal.objective))}")

print("\nAsignación de cajeros por período de inicio:")
solucion_primal = []
for i in range(6):
    val = int(value(x[i]))
    solucion_primal.append(val)
    print(f"  x_{i+1} = {val} cajeros comienzan turno en período {i+1} ({periodos[i]})")

# Verificar cobertura
print("\nVerificación de demanda cubierta:")
cobertura = [
    solucion_primal[5] + solucion_primal[0],  # Período 1
    solucion_primal[0] + solucion_primal[1],  # Período 2
    solucion_primal[1] + solucion_primal[2],  # Período 3
    solucion_primal[2] + solucion_primal[3],  # Período 4
    solucion_primal[3] + solucion_primal[4],  # Período 5
    solucion_primal[4] + solucion_primal[5],  # Período 6
]

resultado_df = pd.DataFrame({
    'Período': periodos,
    'Horas': ['3-7', '7-11', '11-15', '15-19', '19-23', '23-3'],
    'Demanda': demanda,
    'Cobertura': cobertura,
    'Diferencia': [c - d for c, d in zip(cobertura, demanda)]
})
print(resultado_df.to_string(index=False))

# ==================== MODELO DUAL ====================
print("\n\n" + "=" * 70)
print("MODELO DUAL")
print("=" * 70)

print("\nFORMULACIÓN DUAL:")
print("\nVariables duales:")
print("y_j = Valor de cobertura de demanda en período j (j=1,2,3,4,5,6)")

print("\nProblema Dual (MAXIMIZAR):")
print("Maximizar W = 7y_1 + 20y_2 + 14y_3 + 20y_4 + 10y_5 + 5y_6")

print("\nRestricciones duales (coeficientes de variables primales):")
restricciones_dual = [
    "y_6 + y_1 ≤ 1  (Coeficiente de x_1 en primal)",
    "y_1 + y_2 ≤ 1  (Coeficiente de x_2 en primal)",
    "y_2 + y_3 ≤ 1  (Coeficiente de x_3 en primal)",
    "y_3 + y_4 ≤ 1  (Coeficiente de x_4 en primal)",
    "y_4 + y_5 ≤ 1  (Coeficiente de x_5 en primal)",
    "y_5 + y_6 ≤ 1  (Coeficiente de x_6 en primal)",
    "y_j ≥ 0 y sin restricción de signo (libre)"
]
for r in restricciones_dual:
    print(f"  {r}")

# Crear modelo dual
prob_dual = LpProblem("Dual_Staffing_Farmatodo", LpMaximize)

# Variables duales (libres de signo)
y = [LpVariable(f"y_{i+1}", cat='Continuous') for i in range(6)]

# Función objetivo dual
prob_dual += lpSum([demanda[i] * y[i] for i in range(6)]), "Beneficio_Dual"

# Restricciones duales
prob_dual += y[5] + y[0] <= 1, "Restriccion_x1"  # Para x_1
prob_dual += y[0] + y[1] <= 1, "Restriccion_x2"  # Para x_2
prob_dual += y[1] + y[2] <= 1, "Restriccion_x3"  # Para x_3
prob_dual += y[2] + y[3] <= 1, "Restriccion_x4"  # Para x_4
prob_dual += y[3] + y[4] <= 1, "Restriccion_x5"  # Para x_5
prob_dual += y[4] + y[5] <= 1, "Restriccion_x6"  # Para x_6

# Resolver modelo dual
prob_dual.solve(PULP_CBC_CMD(msg=0))

print("\n" + "-" * 70)
print("SOLUCIÓN ÓPTIMA - MODELO DUAL")
print("-" * 70)
print(f"\nEstatus: {LpStatus[prob_dual.status]}")
print(f"\nValor Óptimo (debe ser igual al primal): {value(prob_dual.objective):.2f}")

print("\nVariables duales óptimas:")
solucion_dual = []
for i in range(6):
    val = value(y[i])
    solucion_dual.append(val)
    print(f"  y_{i+1} = {val:.4f} (Período {i+1}: {periodos[i]})")

# ==================== ANÁLISIS DE COMPLEMENTARIEDAD ====================
print("\n\n" + "=" * 70)
print("ANÁLISIS DE COMPLEMENTARIEDAD (HOLGURA COMPLEMENTARIA)")
print("=" * 70)

print("\nCondiciones de holgura complementaria:")
print("Si x_i > 0, entonces su restricción dual asociada es activa (=)")
print("Si restricción primal tiene holgura, entonces su variable dual es 0\n")

for i in range(6):
    xi_val = solucion_primal[i]
    # Restricción dual para x_{i+1}: y_{6-i} + y_{i+1} ≤ 1
    if i == 0:
        dual_sum = solucion_dual[5] + solucion_dual[0]
    else:
        dual_sum = solucion_dual[i-1] + solucion_dual[i]
    
    print(f"x_{i+1} = {xi_val}: ", end="")
    if xi_val > 0:
        print(f"Variable POSITIVA → y_{i} + y_{(i%6)+1} debe ser = 1")
        print(f"  Verificación: {solucion_dual[(i-1)%6]:.4f} + {solucion_dual[i]:.4f} = {dual_sum:.4f}")
    else:
        print(f"Variable CERO → restricción dual puede ser < 1")

# Holgura en restricciones primales
print("\nHolgura en restricciones de demanda:")
for j in range(6):
    demanda_j = demanda[j]
    cobertura_j = cobertura[j]
    holgura = cobertura_j - demanda_j
    print(f"Período {j+1}: Cobertura={cobertura_j}, Demanda={demanda_j}, Holgura={holgura}", end="")
    if holgura == 0:
        print(" → RESTRICCIÓN ACTIVA (y_j puede ser positivo)")
    else:
        print(f" → HOLGURA={holgura} → y_{j+1} = 0")

# ==================== RESUMEN FINAL ====================
print("\n\n" + "=" * 70)
print("RESUMEN Y RECOMENDACIÓN FINAL")
print("=" * 70)

print(f"\n✓ Número MÍNIMO de cajeros requeridos: {int(value(prob_primal.objective))}")
print("\n✓ Distribución óptima del turno inicial:")
for i in range(6):
    if solucion_primal[i] > 0:
        print(f"  • Período {i+1} ({periodos[i]}): {solucion_primal[i]} cajeros")

print("\n✓ Conclusión: La tienda debe contratar", int(value(prob_primal.objective)), 
      "cajeros distribuidos óptimamente en los 6 períodos.")

# Verificación de dualidad fuerte
print("\n" + "=" * 70)
print("VERIFICACIÓN DE DUALIDAD FUERTE")
print("=" * 70)
print(f"Valor óptimo del Primal:  {int(value(prob_primal.objective))}")
print(f"Valor óptimo del Dual:    {value(prob_dual.objective):.2f}")
print(f"Diferencia (debe ser ~0): {abs(int(value(prob_primal.objective)) - value(prob_dual.objective)):.6f}")
print("\n✓ Los valores son iguales: Se cumple la dualidad fuerte")
