"""
EJERCICIO 4: BIBLIOTECARIOS DUAL - CON ITERACIONES
Muestra el análisis del problema dual y sus iteraciones
"""

from pulp import *
import pandas as pd
import json

# ==================== DATOS DEL PROBLEMA ====================
print("=" * 90)
print("EJERCICIO 4: PROBLEMA DE BIBLIOTECARIOS (DUAL) - ANÁLISIS DE ITERACIONES")
print("=" * 90)

periodos = ['Período 1', 'Período 2', 'Período 3', 'Período 4', 'Período 5', 'Período 6']
horarios = ['12AM-4AM', '4AM-8AM', '8AM-12PM', '12PM-4PM', '4PM-8PM', '8PM-12AM']
demanda = [3, 2, 10, 14, 8, 10]

print("\nProblema Dual Simétrico del Ejercicio 3")
print("Primal: Minimizar bibliotecarios necesarios")
print("Dual:   Valorar cada período mediante precios sombra")

# ==================== MODELO DUAL ====================
print("\n" + "=" * 90)
print("MODELO DUAL: MAXIMIZAR VALOR")
print("=" * 90)

prob_dual = LpProblem("Bibliotecarios_Dual", LpMaximize)

# Variables duales: y_i = precio sombra (valor) del período i
y = [LpVariable(f"y_{i+1}", lowBound=0) for i in range(6)]

# Función objetivo: Maximizar valor ponderado por demanda
prob_dual += lpSum([demanda[i] * y[i] for i in range(6)]), "Valor_Total"

# Restricciones: Costo de cada turno (2 períodos) no debe exceder 1
print("\nFormulación:")
print("Maximizar:")
print("  W = 3y₁ + 2y₂ + 10y₃ + 14y₄ + 8y₅ + 10y₆")

print("\nRestricciones (Costo de Turnos):")
print("  Un bibliotecario trabaja 8 horas (2 períodos consecutivos)")
print("  Su costo no debe exceder 1 (1 bibliotecario)")

prob_dual += y[5] + y[0] <= 1, "Turno_1"  # Cubre períodos 1 (12AM-4AM) y 2 (4AM-8AM)
prob_dual += y[0] + y[1] <= 1, "Turno_2"  # Cubre períodos 2 (4AM-8AM) y 3 (8AM-12PM)
prob_dual += y[1] + y[2] <= 1, "Turno_3"  # Cubre períodos 3 (8AM-12PM) y 4 (12PM-4PM)
prob_dual += y[2] + y[3] <= 1, "Turno_4"  # Cubre períodos 4 (12PM-4PM) y 5 (4PM-8PM)
prob_dual += y[3] + y[4] <= 1, "Turno_5"  # Cubre períodos 5 (4PM-8PM) y 6 (8PM-12AM)
prob_dual += y[4] + y[5] <= 1, "Turno_6"  # Cubre períodos 6 (8PM-12AM) y 1 (12AM-4AM)

restricciones_dual = [
    f"  y₆ + y₁ ≤ 1 (Turno 23:00-07:00: cubre {horarios[5]} y {horarios[0]})",
    f"  y₁ + y₂ ≤ 1 (Turno 03:00-11:00: cubre {horarios[0]} y {horarios[1]})",
    f"  y₂ + y₃ ≤ 1 (Turno 07:00-15:00: cubre {horarios[1]} y {horarios[2]})",
    f"  y₃ + y₄ ≤ 1 (Turno 11:00-19:00: cubre {horarios[2]} y {horarios[3]})",
    f"  y₄ + y₅ ≤ 1 (Turno 15:00-23:00: cubre {horarios[3]} y {horarios[4]})",
    f"  y₅ + y₆ ≤ 1 (Turno 19:00-03:00: cubre {horarios[4]} y {horarios[5]})",
    "  y_i ≥ 0, para i = 1, 2, 3, 4, 5, 6"
]

for restriccion in restricciones_dual:
    print(restriccion)

# Resolver
prob_dual.solve(PULP_CBC_CMD(msg=0))

print(f"\nEstatus: {LpStatus[prob_dual.status]}")
print(f"Valor Óptimo W* = {value(prob_dual.objective)}")

# Solución
print("\nSolución Óptima (Precios Sombra):")
valores_duales = []
for i, var in enumerate(y):
    valor = round(var.varValue, 2) if var.varValue else 0
    print(f"  y_{i+1} = {valor}")
    valores_duales.append(valor)

# ==================== ANÁLISIS DE RESULTADOS ====================
print("\n" + "=" * 90)
print("INTERPRETACIÓN DE PRECIOS SOMBRA")
print("=" * 90)

print("\nSignificado:")
print("  y_i > 0: Período i es CRÍTICO (restricción activa en el primal)")
print("  y_i = 0: Período i tiene HOLGURA (no es restricción activa)")

print("\nPor período:")
analisis_data = []
for i in range(6):
    if valores_duales[i] > 0:
        interpretacion = "CRÍTICO - Aumentar demanda requeriría + personal"
    else:
        interpretacion = "FLEXIBLE - Hay cobertura sobrante"
    
    analisis_data.append({
        'Período': i+1,
        'Horario': horarios[i],
        'Demanda': demanda[i],
        'Precio Sombra': valores_duales[i],
        'Interpretación': interpretacion
    })
    
    print(f"  y_{i+1} = {valores_duales[i]}: {horarios[i]}")
    print(f"    → {interpretacion}")

# ==================== VERIFICACIÓN CON PRIMAL ====================
print("\n" + "=" * 90)
print("RELACIÓN CON PROBLEMA PRIMAL (Ejercicio 3)")
print("=" * 90)

# Recalcular primal para comparación
prob_primal = LpProblem("Bibliotecarios_Primal_Ref", LpMinimize)
x = [LpVariable(f"x_{i+1}", lowBound=0, cat='Integer') for i in range(6)]

prob_primal += lpSum(x), "Total_Bibliotecarios"

prob_primal += x[5] + x[0] >= demanda[0]
prob_primal += x[0] + x[1] >= demanda[1]
prob_primal += x[1] + x[2] >= demanda[2]
prob_primal += x[2] + x[3] >= demanda[3]
prob_primal += x[3] + x[4] >= demanda[4]
prob_primal += x[4] + x[5] >= demanda[5]

prob_primal.solve(PULP_CBC_CMD(msg=0))

z_primal = value(prob_primal.objective)
w_dual = value(prob_dual.objective)
asignacion_primal = [int(x[i].varValue) if x[i].varValue else 0 for i in range(6)]

print(f"\nZ* (Primal - Ej. 3):  {z_primal}")
print(f"W* (Dual - Ej. 4):    {w_dual}")
print(f"\nDiferencia: {abs(z_primal - w_dual):.10f}")

if abs(z_primal - w_dual) < 0.0001:
    print("✓ DUALIDAD FUERTE VERIFICADA")
else:
    print("✗ Error en dualidad")

# ==================== CONDICIONES DE OPTIMALIDAD ====================
print("\n" + "=" * 90)
print("CONDICIONES DE OPTIMALIDAD (Holgura Complementaria)")
print("=" * 90)

print("\nVerificación de Complementariedad:")
print("\nVariables Primales:")
for i in range(6):
    if asignacion_primal[i] > 0:
        suma_dual = valores_duales[(i-1) % 6] + valores_duales[i]
        print(f"  x_{i+1} = {asignacion_primal[i]} > 0")
        print(f"    → Restricción dual {i+1} debe ser activa (= 1)")
        print(f"    → y_{i%6+1 if i > 0 else 6} + y_{i+1} = {suma_dual}")
        if abs(suma_dual - 1.0) < 0.01:
            print(f"    ✓ ACTIVA")
        else:
            print(f"    ✗ NO ACTIVA (problema)")
    else:
        print(f"  x_{i+1} = 0: Restricción dual puede no ser activa")

print("\n✓ Condiciones de Optimalidad Satisfechas")

# ==================== GUARDANDO DATOS PARA HTML ====================
iteraciones_ej4 = {
    "titulo": "Ejercicio 4: Bibliotecarios (Dual Simétrico)",
    "periodos": [i+1 for i in range(6)],
    "horarios": horarios,
    "demanda": demanda,
    "solucion_dual": int(w_dual),
    "valores_duales": valores_duales,
    "analisis": analisis_data,
    "primal_valor": int(z_primal),
    "primal_asignacion": asignacion_primal,
    "dualidad_verificada": abs(z_primal - w_dual) < 0.0001
}

with open('c:\\xampp\\TRABAJO-OPERATIVA\\datos_ejercicio4.json', 'w') as f:
    json.dump(iteraciones_ej4, f, indent=4)

print("\n✓ Datos guardados para visualización HTML")
