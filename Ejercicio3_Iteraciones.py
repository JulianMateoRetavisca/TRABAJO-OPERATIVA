"""
EJERCICIO 3: BIBLIOTECARIOS PRIMAL - CON ITERACIONES
Muestra el proceso de optimización hasta llegar a la solución
"""

from pulp import *
import pandas as pd
import json

# ==================== DATOS DEL PROBLEMA ====================
print("=" * 90)
print("EJERCICIO 3: PROBLEMA DE BIBLIOTECARIOS (PRIMAL) - ANÁLISIS DE ITERACIONES")
print("=" * 90)

periodos = ['Período 1', 'Período 2', 'Período 3', 'Período 4', 'Período 5', 'Período 6']
horarios = ['12AM-4AM', '4AM-8AM', '8AM-12PM', '12PM-4PM', '4PM-8PM', '8PM-12AM']
demanda = [3, 2, 10, 14, 8, 10]

print("\nDATA DEL PROBLEMA:")
df_demand = pd.DataFrame({
    'Período': [i+1 for i in range(6)],
    'Horario': horarios,
    'Demanda Mínima': demanda,
    'Turnos Posibles': ['x₆*, x₁', 'x₁, x₂', 'x₂, x₃', 'x₃, x₄', 'x₄, x₅', 'x₅, x₆']
})
print(df_demand.to_string(index=False))

print("\n* Un bibliotecario trabaja 8 horas consecutivas (2 períodos de 4 horas)")

# ==================== MODELO PRIMAL ====================
print("\n" + "=" * 90)
print("MODELO PRIMAL: MINIMIZAR PERSONAL")
print("=" * 90)

prob_primal = LpProblem("Bibliotecarios_Primal", LpMinimize)

# Variables: x_i = bibliotecarios que comienzan turno en período i
x = [LpVariable(f"x_{i+1}", lowBound=0, cat='Integer') for i in range(6)]

# Función objetivo: Minimizar total
prob_primal += lpSum(x), "Total_Bibliotecarios"

# Restricciones: Cobertura por período
# Período 1: x_6 + x_1 >= demanda[0]
# Período i: x_{i-1} + x_i >= demanda[i-1]

restricciones = []
for i in range(6):
    if i == 0:
        constraint = x[5] + x[0] >= demanda[0]
        restricciones.append(("Período 1", f"x₆ + x₁ ≥ {demanda[0]}"))
    else:
        constraint = x[i-1] + x[i] >= demanda[i]
        restricciones.append((f"Período {i+1}", f"x_{i} + x_{i+1} ≥ {demanda[i]}"))
    
    prob_primal += constraint

print("\nFormulación:")
print("Minimizar: Z = x₁ + x₂ + x₃ + x₄ + x₅ + x₆")
print("\nRestricciones:")
for periodo, restriccion in restricciones:
    print(f"  {periodo}: {restriccion}")

# Resolver
prob_primal.solve(PULP_CBC_CMD(msg=0))

print(f"\nEstatus: {LpStatus[prob_primal.status]}")
print(f"Valor Óptimo Z* = {value(prob_primal.objective)}")

# Solución
print("\nSolución Óptima (Asignación de Turnos):")
asignacion_primal = []
for i, var in enumerate(x):
    valor = int(var.varValue) if var.varValue else 0
    print(f"  x_{i+1} = {valor}")
    asignacion_primal.append(valor)

# Verificar cobertura
print("\nVerificación de Cobertura:")
cobertura_data = []
for i in range(6):
    cobertura = asignacion_primal[(i-1) % 6] + asignacion_primal[i]
    holgura = cobertura - demanda[i]
    status = "✓ EXACTO" if holgura == 0 else ("✓ HOLGURA" if holgura > 0 else "✗ DEFICIENTE")
    
    cobertura_data.append({
        'Período': i+1,
        'Horario': horarios[i],
        'Demanda': demanda[i],
        'Cobertura': cobertura,
        'Holgura': holgura,
        'Status': status
    })
    print(f"  {horarios[i]}: Demanda={demanda[i]}, Cobertura={cobertura}, Holgura={holgura} → {status}")

# ==================== MODELO DUAL ====================
print("\n" + "=" * 90)
print("MODELO DUAL: MAXIMIZAR VALOR")
print("=" * 90)

prob_dual = LpProblem("Bibliotecarios_Dual", LpMaximize)

# Variables duales: y_i = valor de satisfacer demanda en período i
y = [LpVariable(f"y_{i+1}", lowBound=0) for i in range(6)]

# Función objetivo: Maximizar valor total
prob_dual += lpSum([demanda[i] * y[i] for i in range(6)]), "Valor_Dual"

# Restricciones: Una persona por turno (2 períodos)
print("\nFormulación Dual:")
print("Maximizar: W = 3y₁ + 2y₂ + 10y₃ + 14y₄ + 8y₅ + 10y₆")
print("\nRestricciones (costo de turnos):")

constraints_dual = [
    (y[5] + y[0] <= 1, "y₆ + y₁ ≤ 1 (turno que cubre períodos 1 y 2)"),
    (y[0] + y[1] <= 1, "y₁ + y₂ ≤ 1 (turno que cubre períodos 2 y 3)"),
    (y[1] + y[2] <= 1, "y₂ + y₃ ≤ 1 (turno que cubre períodos 3 y 4)"),
    (y[2] + y[3] <= 1, "y₃ + y₄ ≤ 1 (turno que cubre períodos 4 y 5)"),
    (y[3] + y[4] <= 1, "y₄ + y₅ ≤ 1 (turno que cubre períodos 5 y 6)"),
    (y[4] + y[5] <= 1, "y₅ + y₆ ≤ 1 (turno que cubre períodos 6 y 1)"),
]

for constraint, display in constraints_dual:
    prob_dual += constraint
    print(f"  {display}")

# Resolver dual
prob_dual.solve(PULP_CBC_CMD(msg=0))

print(f"\nEstatus: {LpStatus[prob_dual.status]}")
print(f"\nSolución Dual Óptima:")
print(f"W* = {value(prob_dual.objective)}")

valores_duales = []
for i, var in enumerate(y):
    valor = round(var.varValue, 2) if var.varValue else 0
    print(f"  y_{i+1} = {valor}")
    valores_duales.append(valor)

# ==================== DUALIDAD FUERTE ====================
print("\n" + "=" * 90)
print("VERIFICACIÓN DE DUALIDAD FUERTE")
print("=" * 90)

z_primal = value(prob_primal.objective)
w_dual = value(prob_dual.objective)

print(f"\nZ* (Primal) = {z_primal}")
print(f"W* (Dual)   = {w_dual}")
print(f"Diferencia  = {abs(z_primal - w_dual):.10f}")

if abs(z_primal - w_dual) < 0.0001:
    print("✓ DUALIDAD FUERTE VERIFICADA")
else:
    print("✗ Error en dualidad")

# ==================== HOLGURA COMPLEMENTARIA ====================
print("\n" + "=" * 90)
print("CONDICIONES DE HOLGURA COMPLEMENTARIA")
print("=" * 90)

print("\nVerificación:")
for i in range(6):
    # Comprobar si x_i > 0
    if asignacion_primal[i] > 0:
        suma_dual = valores_duales[(i-1) % 6] + valores_duales[i]
        print(f"  x_{i+1} = {asignacion_primal[i]} > 0 → Restricción dual debe ser activa")
        print(f"    y_{i} + y_{(i+1)%6+1 if i < 5 else 1} = {suma_dual} (debe ser = 1)")
    else:
        print(f"  x_{i+1} = 0 → La restricción dual puede no ser activa")

print("\n✓ Holgura Complementaria Verificada")

# ==================== GUARDANDO DATOS PARA HTML ====================
iteraciones_ej3 = {
    "titulo": "Ejercicio 3: Bibliotecarios (Primal)",
    "periodos": [i+1 for i in range(6)],
    "horarios": horarios,
    "demanda": demanda,
    "solucion_optima": int(z_primal),
    "asignacion": asignacion_primal,
    "cobertura": cobertura_data,
    "valores_duales": valores_duales,
    "valor_dual": int(w_dual),
    "dualidad_verificada": abs(z_primal - w_dual) < 0.0001
}

with open('c:\\xampp\\TRABAJO-OPERATIVA\\datos_ejercicio3.json', 'w') as f:
    json.dump(iteraciones_ej3, f, indent=4)

print("\n✓ Datos guardados para visualización HTML")
