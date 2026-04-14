"""
EJERCICIO 2: PROBLEMA DE MOCHILA - CON ITERACIONES
Muestra el proceso paso a paso hasta llegar a la solución óptima
"""

from pulp import *
import pandas as pd
import json

# ==================== DATOS DEL PROBLEMA ====================
print("=" * 90)
print("EJERCICIO 2: PROBLEMA DE MOCHILA 0/1 - ANÁLISIS DE ITERACIONES")
print("=" * 90)

articulos = ['Artículo 1', 'Artículo 2', 'Artículo 3', 'Artículo 4', 'Artículo 5']
valores = [40, 60, 50, 70, 30]
pesos = [10, 20, 15, 25, 12]
capacidad = 60

print("\nDATA DEL PROBLEMA:")
df_items = pd.DataFrame({
    'Artículo': articulos,
    'Valor': valores,
    'Peso': pesos,
    'Relación V/P': [v/p for v,p in zip(valores, pesos)]
})
print(df_items.to_string(index=False))
print(f"\nCapacidad de la Mochila: {capacidad} libras")

# ==================== HEURÍSTICA GREEDY (para comparación) ====================
print("\n" + "=" * 90)
print("HEURÍSTICA GREEDY (Solución por Relación Valor/Peso)")
print("=" * 90)

# Ordenar por relación valor/peso
indices_greedy = sorted(range(len(articulos)), key=lambda i: valores[i]/pesos[i], reverse=True)

print("\nOrdenamienti por Relación V/P:")
greedy_data = []
peso_actual = 0
valor_actual = 0
seleccionados_greedy = [0] * len(articulos)

for i, idx in enumerate(indices_greedy):
    ratio = valores[idx] / pesos[idx]
    print(f"  Paso {i+1}: {articulos[idx]} (V/P = {ratio:.2f})")
    
    if peso_actual + pesos[idx] <= capacidad:
        peso_actual += pesos[idx]
        valor_actual += valores[idx]
        seleccionados_greedy[idx] = 1
        print(f"    → ✓ Añadido (peso total: {peso_actual}, valor: {valor_actual})")
    else:
        print(f"    → ✗ No cabe (peso total sería: {peso_actual + pesos[idx]})")

print(f"\nResultado Greedy:")
print(f"  Valor Total: {valor_actual}")
print(f"  Peso Total: {peso_actual}/{capacidad}")
print(f"  Artículos: {[articulos[i] for i in range(len(articulos)) if seleccionados_greedy[i]]}")

# ==================== SOLUCIÓN ÓPTIMA (Programación Lineal Entera) ====================
print("\n" + "=" * 90)
print("SOLUCIÓN ÓPTIMA (Programación Lineal Entera con Simplex)")
print("=" * 90)

prob = LpProblem("Mochila_Excursionista", LpMaximize)

# Variables de decisión: x_i = 1 si se lleva artículo i, 0 si no
x = [LpVariable(f"x_{i+1}", cat='Binary') for i in range(len(articulos))]

# Función objetivo: Maximizar valor total
prob += lpSum([valores[i] * x[i] for i in range(len(articulos))]), "Valor_Total"

# Restricción: Peso total no debe exceder capacidad
prob += lpSum([pesos[i] * x[i] for i in range(len(articulos))]) <= capacidad, "Capacidad"

# Resolver
prob.solve(PULP_CBC_CMD(msg=0))

print(f"\nEstatus: {LpStatus[prob.status]}")
print(f"\nValor Óptimo: {value(prob.objective)}")

seleccionados_optimo = [x[i].varValue for i in range(len(articulos))]
print("\nArtículos Seleccionados:")
valor_opt = 0
peso_opt = 0
for i in range(len(articulos)):
    if seleccionados_optimo[i] == 1:
        print(f"  ✓ {articulos[i]}: Valor={valores[i]}, Peso={pesos[i]}")
        valor_opt += valores[i]
        peso_opt += pesos[i]

print(f"\nResumen Óptimo:")
print(f"  Valor Total: {valor_opt}")
print(f"  Peso Total: {peso_opt}/{capacidad}")
print(f"  Holgura: {capacidad - peso_opt} libras")

# ==================== COMPARACIÓN ====================
print("\n" + "=" * 90)
print("COMPARACIÓN: GREEDY vs ÓPTIMA")
print("=" * 90)

comparison = pd.DataFrame({
    'Método': ['Greedy (V/P)', 'Óptimo'],
    'Valor': [valor_actual, valor_opt],
    'Peso': [peso_actual, peso_opt],
    'Eficiencia': [valor_actual/peso_actual if peso_actual > 0 else 0, 
                   valor_opt/peso_opt if peso_opt > 0 else 0]
})

print("\n" + comparison.to_string(index=False))
print(f"\nMejora: {((valor_opt - valor_actual) / valor_actual * 100):.1f}%")

# ==================== TABLEAU SIMPLEX (Versión Continua) ====================
print("\n" + "=" * 90)
print("ANÁLISIS DE RELAJACIÓN CONTINUA")
print("=" * 90)

prob_relaxed = LpProblem("Mochila_Relajada", LpMaximize)
x_r = [LpVariable(f"x_r{i+1}", lowBound=0, upBound=1) for i in range(len(articulos))]

prob_relaxed += lpSum([valores[i] * x_r[i] for i in range(len(articulos))]), "Valor"
prob_relaxed += lpSum([pesos[i] * x_r[i] for i in range(len(articulos))]) <= capacidad

prob_relaxed.solve(PULP_CBC_CMD(msg=0))

print(f"\nSolución Relajada (continua):")
print(f"  Valor máximo (cota superior): {value(prob_relaxed.objective):.2f}")

print("\n  Selección por artículo:")
for i in range(len(articulos)):
    print(f"    x_{i+1} = {x_r[i].varValue:.3f} ({articulos[i]})")

# ==================== GUARDANDO DATOS PARA HTML ====================
iteraciones_mochila = {
    "titulo": "Ejercicio 2: Problema de Mochila 0/1",
    "articulos": articulos,
    "valores": valores,
    "pesos": pesos,
    "capacidad": capacidad,
    "solucion_optima": int(valor_opt),
    "peso_optimo": peso_opt,
    "seleccionados": [int(x) for x in seleccionados_optimo],
    "greedy_valor": valor_actual,
    "greedy_peso": peso_actual,
    "mejora_porcentaje": round(((valor_opt - valor_actual) / valor_actual * 100), 1) if valor_actual > 0 else 0
}

with open('c:\\xampp\\TRABAJO-OPERATIVA\\datos_ejercicio2.json', 'w') as f:
    json.dump(iteraciones_mochila, f, indent=4)

print("\n✓ Datos guardados para visualización HTML")
