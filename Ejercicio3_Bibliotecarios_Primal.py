"""
EJERCICIO 3: PROBLEMA DE BIBLIOTECARIOS - TURNO DE 8 HORAS
Biblioteca universitaria abierta 24 horas
Cada bibliotecario trabaja 8 horas consecutivas
Objetivo: Minimizar número total de bibliotecarios
"""

from pulp import *
import pandas as pd

# ==================== DATA DEL PROBLEMA ====================
periodos = ['Período 1\n(12 AM - 4 AM)', 'Período 2\n(4 AM - 8 AM)', 'Período 3\n(8 AM - 12 PM)', 
            'Período 4\n(12 PM - 4 PM)', 'Período 5\n(4 PM - 8 PM)', 'Período 6\n(8 PM - 12 AM)']
demanda = [3, 2, 10, 14, 8, 10]  # Demanda en cada período
turno_duracion = 8  # horas
periodo_duracion = 4  # horas
periodos_por_turno = turno_duracion // periodo_duracion  # 2 períodos

print("=" * 90)
print("EJERCICIO 3: PROBLEMA DE BIBLIOTECARIOS - TURNOS DE 8 HORAS")
print("=" * 90)

print("\n📚 DATA DEL PROBLEMA:")
data_df = pd.DataFrame({
    'Período': ['1', '2', '3', '4', '5', '6'],
    'Horario': ['12 AM - 4 AM', '4 AM - 8 AM', '8 AM - 12 PM', '12 PM - 4 PM', '4 PM - 8 PM', '8 PM - 12 AM'],
    'Demanda Mínima': demanda
})
print(data_df.to_string(index=False))
print(f"\n🕒 Cada bibliotecario trabaja {turno_duracion} horas consecutivas ({periodos_por_turno} períodos)")
print(f"📅 Total de períodos en el día: 6")

# ==================== MODELO PRIMAL ====================
print("\n" + "=" * 90)
print("MODELO PRIMAL: MINIMIZAR TOTAL DE BIBLIOTECARIOS")
print("=" * 90)

prob_primal = LpProblem("Bibliotecarios_Primal", LpMinimize)

# Variables de decisión: x_i = bibliotecarios que comienzan turno en período i
x = [LpVariable(f"x_{i+1}", lowBound=0, cat='Integer') for i in range(6)]

# Función objetivo: Minimizar total de bibliotecarios
prob_primal += lpSum(x), "Total_Bibliotecarios"

# Restricciones: Cobertura por período
# Un bibliotecario que comienza en período i trabaja en períodos i e (i+1)%6
prob_primal += x[5] + x[0] >= demanda[0], "Demanda_Periodo_1"  # 12 AM - 4 AM
prob_primal += x[0] + x[1] >= demanda[1], "Demanda_Periodo_2"  # 4 AM - 8 AM
prob_primal += x[1] + x[2] >= demanda[2], "Demanda_Periodo_3"  # 8 AM - 12 PM
prob_primal += x[2] + x[3] >= demanda[3], "Demanda_Periodo_4"  # 12 PM - 4 PM
prob_primal += x[3] + x[4] >= demanda[4], "Demanda_Periodo_5"  # 4 PM - 8 PM
prob_primal += x[4] + x[5] >= demanda[5], "Demanda_Periodo_6"  # 8 PM - 12 AM

print("\nFORMULACIÓN PRIMAL:")
print("\nVariables de decisión:")
print("x_i = Número de bibliotecarios que comienzan turno en período i")

print("\nFunción Objetivo (Minimizar):")
print("Z = x₁ + x₂ + x₃ + x₄ + x₅ + x₆")

print("\nRestricciones (cobertura de demanda):")
restricciones = [
    "x₆ + x₁ ≥ 3   (Período 1: 12 AM - 4 AM)",
    "x₁ + x₂ ≥ 2   (Período 2: 4 AM - 8 AM)",
    "x₂ + x₃ ≥ 10  (Período 3: 8 AM - 12 PM)",
    "x₃ + x₄ ≥ 14  (Período 4: 12 PM - 4 PM)",
    "x₄ + x₅ ≥ 8   (Período 5: 4 PM - 8 PM)",
    "x₅ + x₆ ≥ 10  (Período 6: 8 PM - 12 AM)"
]
for r in restricciones:
    print(f"  {r}")

# Resolver
prob_primal.solve(PULP_CBC_CMD(msg=0))

print("\n" + "-" * 90)
print("SOLUCIÓN ÓPTIMA - MODELO PRIMAL")
print("-" * 90)
print(f"\nEstatus: {LpStatus[prob_primal.status]}")
print(f"\nValor Óptimo (Total mínimo de bibliotecarios): {int(value(prob_primal.objective))}")

print("\nAsignación óptima:")
solucion_x = []
for i in range(6):
    val = int(value(x[i]))
    solucion_x.append(val)
    periodo_siguiente = ((i+1) % 6) + 1
    print(f"  x_{i+1} = {val:2} bibliotecarios comienzan en período {i+1}")

# Verificar cobertura
print("\nVerificación de cobertura:")
cobertura = []
for j in range(6):
    cob = solucion_x[(j-1) % 6] + solucion_x[j]
    cobertura.append(cob)

resultado_df = pd.DataFrame({
    'Período': ['1', '2', '3', '4', '5', '6'],
    'Horario': ['12 AM - 4 AM', '4 AM - 8 AM', '8 AM - 12 PM', '12 PM - 4 PM', '4 PM - 8 PM', '8 PM - 12 AM'],
    'Demanda': demanda,
    'Cobertura': cobertura,
    'Diferencia': [c - d for c, d in zip(cobertura, demanda)]
})
print(resultado_df.to_string(index=False))

# ==================== MODELO DUAL ====================
print("\n" + "=" * 90)
print("MODELO DUAL: VALORACIÓN DE RESTRICCIONES")
print("=" * 90)

prob_dual = LpProblem("Bibliotecarios_Dual", LpMaximize)

# Variables duales
y = [LpVariable(f"y_{i+1}", cat='Continuous') for i in range(6)]

# Función objetivo dual
prob_dual += lpSum([demanda[i] * y[i] for i in range(6)]), "Beneficio_Dual"

# Restricciones duales
prob_dual += y[5] + y[0] <= 1, "Restriccion_x1"
prob_dual += y[0] + y[1] <= 1, "Restriccion_x2"
prob_dual += y[1] + y[2] <= 1, "Restriccion_x3"
prob_dual += y[2] + y[3] <= 1, "Restriccion_x4"
prob_dual += y[3] + y[4] <= 1, "Restriccion_x5"
prob_dual += y[4] + y[5] <= 1, "Restriccion_x6"

print("\nFORMULACIÓN DUAL:")
print("\nVariables duales:")
print("y_j = Valor de cobertura de demanda en período j")

print("\nFunción Objetivo (Maximizar):")
print("W = 3y₁ + 2y₂ + 10y₃ + 14y₄ + 8y₅ + 10y₆")

print("\nRestricciones duales:")
print("  y₆ + y₁ ≤ 1")
print("  y₁ + y₂ ≤ 1")
print("  y₂ + y₃ ≤ 1")
print("  y₃ + y₄ ≤ 1")
print("  y₄ + y₅ ≤ 1")
print("  y₅ + y₆ ≤ 1")

# Resolver dual
prob_dual.solve(PULP_CBC_CMD(msg=0))

print("\n" + "-" * 90)
print("SOLUCIÓN ÓPTIMA - MODELO DUAL")
print("-" * 90)
print(f"\nEstatus: {LpStatus[prob_dual.status]}")
print(f"\nValor Óptimo: {value(prob_dual.objective):.2f}")

print("\nVariables duales óptimas:")
solucion_y = []
for i in range(6):
    val = value(y[i])
    solucion_y.append(val)
    print(f"  y_{i+1} = {val:.4f}")

# ==================== ANÁLISIS ====================
print("\n" + "=" * 90)
print("ANÁLISIS Y CONCLUSIÓN")
print("=" * 90)

print(f"""
✓ RESPUESTA:
  Total MÍNIMO de bibliotecarios requeridos: {int(value(prob_primal.objective))}
  
  Distribución óptima:""")

total_check = 0
for i in range(6):
    if solucion_x[i] > 0:
        print(f"    • {solucion_x[i]:2} bibliotecarios comienzan turno en período {i+1}")
        total_check += solucion_x[i]

print(f"\n  Total: {total_check} bibliotecarios")
print(f"\n✓ Dualidad Fuerte: Z* = W* = {int(value(prob_primal.objective))}")

# Exportar datos para página web
print("\n" + "=" * 90)
print("DATOS PARA PÁGINA WEB")
print("=" * 90)
print(f"Total: {int(value(prob_primal.objective))}")
print(f"Solución x: {solucion_x}")
print(f"Cobertura: {cobertura}")
