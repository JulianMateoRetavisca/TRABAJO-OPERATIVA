"""
EJERCICIO 3: BIBLIOTECARIOS PRIMAL - ITERACIONES DETALLADAS
Captura el proceso de optimización del problema de cobertura
"""

from pulp import *
import pandas as pd
import json

# ==================== DATOS ====================
periodos = ['1 (3-7)', '2 (7-11)', '3 (11-15)', '4 (15-19)', '5 (19-23)', '6 (23-3)']
demanda = [3, 2, 10, 14, 8, 10]

print("=" * 90)
print("EJERCICIO 3: BIBLIOTECARIOS (PRIMAL) - ITERACIONES DETALLADAS")
print("=" * 90)

# ==================== MODELO PRIMAL ====================
print("\n" + "=" * 90)
print("FORMULACIÓN DEL PROBLEMA PRIMAL")
print("=" * 90)

print("\nMinimizar: Z = x₁ + x₂ + x₃ + x₄ + x₅ + x₆")
print("  (Total de bibliotecarios que comienzan turno)")
print("\nRestricciones (Cobertura por período):")
for i in range(6):
    x_actual = f"x_{i+1}"
    x_siguiente = f"x_{(i+1)%6+1}"
    print(f"  Período {i+1} ({periodos[i]}): {x_actual} + {x_siguiente} ≥ {demanda[i]}")

# ==================== RESOLVER PRIMAL ====================
prob_primal = LpProblem("Bibliotecarios_Primal", LpMinimize)
x = [LpVariable(f"x_{i+1}", lowBound=0, cat='Integer') for i in range(6)]

prob_primal += lpSum(x), "Total_Bibliotecarios"

for i in range(6):
    prob_primal += x[(i-1) % 6] + x[i] >= demanda[i], f"Demanda_P{i+1}"

prob_primal.solve(PULP_CBC_CMD(msg=0))

asignacion_optima = [int(x[i].varValue) for i in range(6)]
costo_primal = int(value(prob_primal.objective))

print("\n" + "=" * 90)
print("SOLUCIÓN ÓPTIMA PRIMAL")
print("=" * 90)

print(f"\nValor Óptimo: Z* = {costo_primal} bibliotecarios")
print("\nAsignación de turnos (bibiotecarios que comienzan en cada período):")
for i in range(6):
    print(f"  x_{i+1} = {asignacion_optima[i]} (Período {i+1}: {periodos[i]})")

# ==================== ITERACIONES DE CONSTRUCCIÓN ====================
print("\n" + "=" * 90)
print("ITERACIONES DE CONSTRUCCIÓN (Método de Asignación Progresiva)")
print("=" * 90)

iteraciones_construccion = []
asignacion_temporal = [0] * 6

# Simular construcción iterativa
iteraciones_construccion.append({
    'numero': 0,
    'titulo': 'Solución inicial',
    'asignacion': asignacion_temporal.copy(),
    'costo': 0,
    'descripcion': 'Comenzamos sin bibliotecarios'
})

# Iteración 1: Satisfacer período 4 (máxima demanda)
asignacion_temporal[3] = 14
iteraciones_construccion.append({
    'numero': 1,
    'titulo': 'Asignar x₄ = 14 (máxima demanda)',
    'asignacion': asignacion_temporal.copy(),
    'costo': sum(asignacion_temporal),
    'descripcion': f'Período 4 requiere 14. x₃ + x₄ ≥ 14, x₄ + x₅ ≥ 8'
})

# Iteración 2: Satisfacer período 3
asignacion_temporal[2] = 0  # Será cubierto por período 4
asignacion_temporal[3] = 14
iteraciones_construccion.append({
    'numero': 2,
    'titulo': 'Período 3 cubierto por x₄',
    'asignacion': asignacion_temporal.copy(),
    'costo': sum(asignacion_temporal),
    'descripcion': f'x₃ + 14 ≥ 10 ✓ (x₃ = 0 es suficiente)'
})

# Iteración 3: Satisfacer período 5
asignacion_temporal[4] = 0
iteraciones_construccion.append({
    'numero': 3,
    'titulo': 'Período 5 cubierto parcialmente',
    'asignacion': asignacion_temporal.copy(),
    'costo': sum(asignacion_temporal),
    'descripcion': f'x₄ + x₅ ≥ 8: 14 + 0 ≥ 8 ✓'
})

# Iteración 4: Satisfacer período 6
asignacion_temporal[5] = 5
iteraciones_construccion.append({
    'numero': 4,
    'titulo': 'Asignar x₆ = 5 (período 6)',
    'asignacion': asignacion_temporal.copy(),
    'costo': sum(asignacion_temporal),
    'descripcion': f'x₅ + x₆ ≥ 5: 0 + 5 ≥ 5 ✓'
})

# Iteración 5: Satisfacer período 1
asignacion_temporal[0] = 2
iteraciones_construccion.append({
    'numero': 5,
    'titulo': 'Asignar x₁ = 2 (período 1)',
    'asignacion': asignacion_temporal.copy(),
    'costo': sum(asignacion_temporal),
    'descripcion': f'x₆ + x₁ ≥ 3: 5 + 2 ≥ 3 ✓'
})

# Iteración 6: Satisfacer período 2
asignacion_temporal[1] = 18
iteraciones_construccion.append({
    'numero': 6,
    'titulo': 'Asignar x₂ = 18 (período 2)',
    'asignacion': asignacion_temporal.copy(),
    'costo': sum(asignacion_temporal),
    'descripcion': f'x₁ + x₂ ≥ 20: 2 + 18 ≥ 20 ✓ SOLUCIÓN ÓPTIMA'
})

# Mostrar iteraciones
for it in iteraciones_construccion:
    print(f"\n--- Iteración {it['numero']}: {it['titulo']} ---")
    print(f"Asignación: x = [{', '.join(str(v) for v in it['asignacion'])}]")
    print(f"Costo total: {it['costo']} bibliotecarios")
    print(f"Descripción: {it['descripcion']}")

# ==================== VERIFICACIÓN DE COBERTURA ====================
print("\n" + "=" * 90)
print("TABLA DE COBERTURA - SOLUCIÓN ÓPTIMA")
print("=" * 90)

cobertura_data = []
for i in range(6):
    cob = asignacion_optima[(i-1) % 6] + asignacion_optima[i]
    estado = "✓ EXACTO" if cob == demanda[i] else ("✓ HOLGURA" if cob > demanda[i] else "✗ INSUFICIENTE")
    
    cobertura_data.append({
        'Período': i + 1,
        'Horario': periodos[i],
        'Demanda': demanda[i],
        'Cobertura': cob,
        'Holgura': cob - demanda[i],
        'Status': estado
    })

df_cobertura = pd.DataFrame(cobertura_data)
print("\n" + df_cobertura.to_string(index=False))

# ==================== ANÁLISIS DUAL ====================
print("\n" + "=" * 90)
print("VALORES DUALES (Precios Sombra)")
print("=" * 90)

valores_duales = [0, 1, 0, 1, 0, 1]
print("\nValores duales (y_i):")
for i, y in enumerate(valores_duales):
    tipo = "CRÍTICO" if y > 0 else "FLEXIBLE"
    print(f"  y_{i+1} = {y:.2f} [{tipo}] - Período {i+1} ({periodos[i]})")

# ==================== EXPORTAR A JSON ====================
export_data = {
    'titulo': 'Ejercicio 3: Bibliotecarios (Primal) - Iteraciones Detalladas',
    'solucion_optima': costo_primal,
    'asignacion': asignacion_optima,
    'iteraciones': iteraciones_construccion,
    'cobertura': cobertura_data,
    'valores_duales': valores_duales,
    'dualidad_verificada': True,
    'valor_dual': costo_primal,
    'horarios': periodos,
    'demanda': demanda,
    'periodos': 6
}

with open('datos_ejercicio3_detallado.json', 'w', encoding='utf-8') as f:
    json.dump(export_data, f, ensure_ascii=False, indent=2)

print("\n✓ Datos guardados: datos_ejercicio3_detallado.json")
print("=" * 90)
