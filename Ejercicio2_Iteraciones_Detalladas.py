"""
EJERCICIO 2: PROBLEMA DE MOCHILA - ITERACIONES DETALLADAS DEL GREEDY
Captura cada paso de la heurística Greedy y compara con óptimo
"""

from pulp import *
import pandas as pd
import json

# ==================== DATOS ====================
articulos = ['Artículo 1', 'Artículo 2', 'Artículo 3', 'Artículo 4', 'Artículo 5']
valores = [40, 60, 50, 70, 30]
pesos = [10, 20, 15, 25, 12]
capacidad = 60

print("=" * 90)
print("EJERCICIO 2: MOCHILA 0/1 - ITERACIONES DETALLADAS")
print("=" * 90)

# ==================== ITERACIONES DEL GREEDY ====================
print("\n" + "=" * 90)
print("HEURÍSTICA GREEDY - ITERACIONES PASO A PASO")
print("=" * 90)

# Calcular ratios
ratios = [(valores[i] / pesos[i], i) for i in range(len(articulos))]
ratios_sorted = sorted(ratios, reverse=True)

print("\nOrdenamiento inicial por relación Valor/Peso:")
for i, (ratio, idx) in enumerate(ratios_sorted, 1):
    print(f"  {i}. {articulos[idx]}: V/P = {ratio:.2f}")

# Iteraciones Greedy
iteraciones_greedy = []
peso_usado = 0
valor_total = 0
items_seleccionados = []

for iteracion, (ratio, idx) in enumerate(ratios_sorted, 1):
    articulo = articulos[idx]
    peso = pesos[idx]
    valor = valores[idx]
    
    if peso_usado + peso <= capacidad:
        estado = "✓ ACEPTADO"
        peso_usado += peso
        valor_total += valor
        items_seleccionados.append((idx, articulo, valor, peso))
        accion = f"Se añade {articulo}. Peso total: {peso_usado}/{capacidad}"
    else:
        estado = "✗ RECHAZADO (No cabe)"
        accion = f"No cabe. Capacidad disponible: {capacidad - peso_usado}, Peso del artículo: {peso}"
    
    iter_data = {
        'numero': iteracion,
        'articulo': articulo,
        'indice': idx,
        'ratio': float(ratio),
        'valor': valor,
        'peso': peso,
        'peso_usado_antes': peso_usado - peso if estado == "✓ ACEPTADO" else peso_usado,
        'peso_usado_despues': peso_usado if estado == "✓ ACEPTADO" else peso_usado,
        'valor_acumulado': valor_total,
        'estado': estado,
        'descripcion': accion,
        'capacidad_disponible': capacidad - (peso_usado if estado == "✓ ACEPTADO" else peso_usado)
    }
    
    iteraciones_greedy.append(iter_data)
    
    print(f"\n--- Iteración {iteracion}: {articulo} (V/P = {ratio:.2f}) ---")
    print(f"  Peso: {peso} libras, Valor: {valor}")
    print(f"  Peso total antes: {iter_data['peso_usado_antes']}/{capacidad}")
    print(f"  {estado}")
    print(f"  Peso total ahora: {iter_data['peso_usado_despues']}/{capacidad}")
    print(f"  Valor acumulado: {valor_total}")

print(f"\n--- RESULTADO GREEDY ---")
print(f"Valor total: {valor_total}")
print(f"Peso total: {peso_usado}/{capacidad}")
print(f"Articulos seleccionados: {', '.join([art[1] for art in items_seleccionados])}")

# ==================== SOLUCIÓN ÓPTIMA ====================
print("\n" + "=" * 90)
print("SOLUCIÓN ÓPTIMA (Programación Lineal Entera)")
print("=" * 90)

prob = LpProblem("Mochila", LpMaximize)
x = [LpVariable(f"x_{i+1}", cat='Binary') for i in range(len(articulos))]

prob += lpSum([valores[i] * x[i] for i in range(len(articulos))]), "Valor_Total"
prob += lpSum([pesos[i] * x[i] for i in range(len(articulos))]) <= capacidad, "Capacidad"

prob.solve(PULP_CBC_CMD(msg=0))

solucion_optima = [int(x[i].varValue) for i in range(len(articulos))]
valor_optimo = int(value(prob.objective))
peso_optimo = sum([pesos[i] * solucion_optima[i] for i in range(len(articulos))])

print(f"\nSolución Óptima:")
print(f"  Valor: {valor_optimo}")
print(f"  Peso: {peso_optimo}/{capacidad}")

articulos_optimos = [articulos[i] for i in range(len(articulos)) if solucion_optima[i] == 1]
print(f"  Artículos: {', '.join(articulos_optimos)}")

# ==================== COMPARACIÓN ====================
print("\n" + "=" * 90)
print("COMPARACIÓN: GREEDY vs ÓPTIMO")
print("=" * 90)

mejora = ((valor_optimo - valor_total) / valor_total) * 100 if valor_total > 0 else 0

print(f"\nHeurística Greedy:")
print(f"  Valor: {valor_total}")
print(f"  Peso: {peso_usado}/{capacidad}")
print(f"  Eficiencia: {valor_total/peso_usado:.2f}")

print(f"\nSolución Óptima:")
print(f"  Valor: {valor_optimo}")
print(f"  Peso: {peso_optimo}/{capacidad}")
print(f"  Eficiencia: {valor_optimo/peso_optimo:.2f}")

print(f"\nMejora del óptimo sobre Greedy: {mejora:.2f}%")

# ==================== EXPORTAR A JSON ====================
export_data = {
    'titulo': 'Ejercicio 2: Mochila 0/1 - Iteraciones Detalladas',
    'articulos': articulos,
    'valores': valores,
    'pesos': pesos,
    'capacidad': capacidad,
    
    'iteraciones_greedy': iteraciones_greedy,
    
    'greedy_valor': valor_total,
    'greedy_peso': peso_usado,
    'greedy_articulos': articulos_optimos if valor_total == valor_optimo else [art[1] for art in items_seleccionados],
    
    'solucion_optima': valor_optimo,
    'peso_optimo': peso_optimo,
    'seleccionados': solucion_optima,
    
    'mejora_porcentaje': float(mejora),
    
    'articulos_optimos': articulos_optimos,
    
    'comparacion': {
        'greedy': {
            'valor': valor_total,
            'peso': peso_usado,
            'eficiencia': round(valor_total/peso_usado, 2) if peso_usado > 0 else 0
        },
        'optimo': {
            'valor': valor_optimo,
            'peso': peso_optimo,
            'eficiencia': round(valor_optimo/peso_optimo, 2)
        }
    }
}

with open('datos_ejercicio2_detallado.json', 'w', encoding='utf-8') as f:
    json.dump(export_data, f, ensure_ascii=False, indent=2)

print("\n✓ Datos guardados: datos_ejercicio2_detallado.json")
print("=" * 90)
