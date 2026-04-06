"""
ANÁLISIS VISUAL Y DE SENSIBILIDAD - PROBLEMA STAFFING FARMATODO
Incluye: Gráficos, análisis de sensibilidad, casos alternos
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pulp import *

# ==================== CONFIGURACIÓN DE VISUALIZACIÓN ====================
plt.style.use('seaborn-v0_8-darkgrid')
fig = plt.figure(figsize=(18, 12))

# ==================== DATA DEL PROBLEMA ====================
periodos = ['P1 (3-7)', 'P2 (7-11)', 'P3 (11-15)', 'P4 (15-19)', 'P5 (19-23)', 'P6 (23-3)']
demanda = [7, 20, 14, 20, 10, 5]
solucion_x = [2, 18, 0, 20, 0, 5]  # x_i óptimos
solucion_y = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]  # y_j óptimos

cobertura = [
    solucion_x[5] + solucion_x[0],  # Período 1
    solucion_x[0] + solucion_x[1],  # Período 2
    solucion_x[1] + solucion_x[2],  # Período 3
    solucion_x[2] + solucion_x[3],  # Período 4
    solucion_x[3] + solucion_x[4],  # Período 5
    solucion_x[4] + solucion_x[5],  # Período 6
]

# ==================== GRÁFICO 1: DEMANDA vs COBERTURA ====================
ax1 = plt.subplot(2, 3, 1)
x_pos = np.arange(len(periodos))
width = 0.35

bars1 = ax1.bar(x_pos - width/2, demanda, width, label='Demanda Mínima', color='#FF6B6B', alpha=0.8)
bars2 = ax1.bar(x_pos + width/2, cobertura, width, label='Cobertura Real', color='#4ECDC4', alpha=0.8)

ax1.set_xlabel('Período', fontsize=10, fontweight='bold')
ax1.set_ylabel('Número de Cajeros', fontsize=10, fontweight='bold')
ax1.set_title('Demanda vs Cobertura por Período', fontsize=12, fontweight='bold')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(periodos, fontsize=9)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Añadir valores en las barras
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}', ha='center', va='bottom', fontsize=8)
for bar in bars2:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}', ha='center', va='bottom', fontsize=8)

# ==================== GRÁFICO 2: ASIGNACIÓN DE TURNOS ====================
ax2 = plt.subplot(2, 3, 2)
colores = ['#FF6B6B' if x > 0 else '#E8E8E8' for x in solucion_x]
bars = ax2.bar(periodos, solucion_x, color=colores, alpha=0.8, edgecolor='black', linewidth=1.5)

ax2.set_xlabel('Período de Inicio de Turno', fontsize=10, fontweight='bold')
ax2.set_ylabel('Número de Cajeros', fontsize=10, fontweight='bold')
ax2.set_title('Asignación Óptima de Turnos (x_i)', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3, axis='y')

# Añadir valores
for i, (bar, val) in enumerate(zip(bars, solucion_x)):
    if val > 0:
        ax2.text(bar.get_x() + bar.get_width()/2., val,
                 f'{int(val)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    else:
        ax2.text(bar.get_x() + bar.get_width()/2., 0.5,
                 '0', ha='center', va='bottom', fontsize=9, color='gray')

# ==================== GRÁFICO 3: VALORES DUALES ====================
ax3 = plt.subplot(2, 3, 3)
colores_dual = ['#95E1D3' if y > 0 else '#E8E8E8' for y in solucion_y]
bars = ax3.bar(periodos, solucion_y, color=colores_dual, alpha=0.8, edgecolor='black', linewidth=1.5)

ax3.set_xlabel('Período', fontsize=10, fontweight='bold')
ax3.set_ylabel('Valor Dual (y_j)', fontsize=10, fontweight='bold')
ax3.set_title('Precios Sombra - Valores Duales (y_j)', fontsize=12, fontweight='bold')
ax3.set_ylim(0, 1.2)
ax3.grid(True, alpha=0.3, axis='y')

# Añadir valores
for bar, val in zip(bars, solucion_y):
    ax3.text(bar.get_x() + bar.get_width()/2., val + 0.05,
             f'{val:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# ==================== GRÁFICO 4: HOLGURA DE RESTRICCIONES ====================
ax4 = plt.subplot(2, 3, 4)
holgura = [c - d for c, d in zip(cobertura, demanda)]
colores_holgura = ['#4ECDC4' if h == 0 else '#FFE66D' for h in holgura]
bars = ax4.bar(periodos, holgura, color=colores_holgura, alpha=0.8, edgecolor='black', linewidth=1.5)

ax4.set_xlabel('Período', fontsize=10, fontweight='bold')
ax4.set_ylabel('Holgura (Cobertura - Demanda)', fontsize=10, fontweight='bold')
ax4.set_title('Holgura de Restricciones Primales', fontsize=12, fontweight='bold')
ax4.axhline(y=0, color='red', linestyle='--', linewidth=2, label='Restricción Activa')
ax4.grid(True, alpha=0.3, axis='y')
ax4.legend()

# Añadir valores
for bar, val in zip(bars, holgura):
    ax4.text(bar.get_x() + bar.get_width()/2., val + 0.3,
             f'{int(val)}', ha='center', va='bottom', fontsize=9, fontweight='bold')

# ==================== GRÁFICO 5: COMPLEMENTARIEDAD ====================
ax5 = plt.subplot(2, 3, 5)

# Correlación entre variables primales y restricciones duales
restricciones_duales_eval = [
    solucion_y[5] + solucion_y[0],  # Para x_1
    solucion_y[0] + solucion_y[1],  # Para x_2
    solucion_y[1] + solucion_y[2],  # Para x_3
    solucion_y[2] + solucion_y[3],  # Para x_4
    solucion_y[3] + solucion_y[4],  # Para x_5
    solucion_y[4] + solucion_y[5],  # Para x_6
]

x_pos = np.arange(len(periodos))
width = 0.35

# Variables primales (normalizadas)
bars1 = ax5.bar(x_pos - width/2, [min(x/5, 1) for x in solucion_x], width, 
               label='x_i (normalizado)', color='#FF6B6B', alpha=0.8)

# Restricciones duales
bars2 = ax5.bar(x_pos + width/2, restricciones_duales_eval, width,
               label='y_{i-1} + y_i', color='#4ECDC4', alpha=0.8)

ax5.set_xlabel('Índice', fontsize=10, fontweight='bold')
ax5.set_ylabel('Valor', fontsize=10, fontweight='bold')
ax5.set_title('Holgura Complementaria: Si x_i > 0 entonces Σy = 1', fontsize=12, fontweight='bold')
ax5.set_xticks(x_pos)
ax5.set_xticklabels([f'i={i+1}' for i in range(6)], fontsize=9)
ax5.set_ylim(0, 1.2)
ax5.legend()
ax5.grid(True, alpha=0.3, axis='y')

# ==================== GRÁFICO 6: FLUJO DE PERSONAL DURANTE EL DÍA ====================
ax6 = plt.subplot(2, 3, 6)

# Crear flujo acumulativo
hora_inicio = [3, 7, 11, 15, 19, 23]
cajeros_periodo = [[] for _ in range(6)]

# Llenar con turnos
for periodo in range(6):
    for turno_inicio in range(6):
        # Un turno iniciado en turno_inicio cubre los períodos turno_inicio y (turno_inicio+1)%6
        siguiente = (turno_inicio + 1) % 6
        if turno_inicio == periodo or siguiente == periodo:
            cajeros_periodo[periodo].append((turno_inicio, solucion_x[turno_inicio]))

# Crear gráfico de Gantt simplificado
y_offset = 0
for periodo in range(6):
    for turno_inicio, cantidad in cajeros_periodo[periodo]:
        color_mapa = plt.cm.Set3(turno_inicio)
        ax6.barh(periodo, 2, left=turno_inicio, height=0.6, color=color_mapa, alpha=0.7, edgecolor='black')
        ax6.text(turno_inicio + 1, periodo, f'x{turno_inicio+1}={int(cantidad)}', 
                ha='center', va='center', fontsize=8, fontweight='bold')

ax6.set_yticks(range(6))
ax6.set_yticklabels(periodos)
ax6.set_xlabel('Período de Turno', fontsize=10, fontweight='bold')
ax6.set_title('Solapamiento de Turnos (Diagrama de Gantt)', fontsize=12, fontweight='bold')
ax6.set_xlim(0, 6)
ax6.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('c:\\xampp\\TRABAJO-OPERATIVA\\Analisis_Staffing_Grafico.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico guardado: Analisis_Staffing_Grafico.png")
plt.show()

# ==================== ANÁLISIS DE SENSIBILIDAD ====================
print("\n" + "="*80)
print("ANÁLISIS DE SENSIBILIDAD")
print("="*80)

print("\n1. RANGO DE OPTIMALIDAD DE COEFICIENTES OBJETIVO")
print("-" * 80)
print("\nPregunta: ¿Cuánto pueden cambiar los coeficientes de la función objetivo")
print("sin que cambie la base óptima (la estructura de la solución)?")

# Simulación de sensibilidad
print("\nSimulación: Cambios en el costo por cajero por período")
print("\nSerie: Cambio en coeficiente de función objetivo vs Valor Óptimo")

cambios = np.linspace(-0.5, 0.5, 11)
valores_obj = []

for cambio in cambios:
    # Resolver con coeficientes modificados
    prob_sensibilidad = LpProblem("Sensibilidad", LpMinimize)
    x_sens = [LpVariable(f"x_{i+1}", lowBound=0, cat='Integer') for i in range(6)]
    
    # Función objetivo con cambio en x_1
    prob_sensibilidad += lpSum([x_sens[i] for i in range(6)]) + cambio * x_sens[0], "Obj"
    
    # Restricciones
    prob_sensibilidad += x_sens[5] + x_sens[0] >= demanda[0], f"D_1"
    prob_sensibilidad += x_sens[0] + x_sens[1] >= demanda[1], f"D_2"
    prob_sensibilidad += x_sens[1] + x_sens[2] >= demanda[2], f"D_3"
    prob_sensibilidad += x_sens[2] + x_sens[3] >= demanda[3], f"D_4"
    prob_sensibilidad += x_sens[3] + x_sens[4] >= demanda[4], f"D_5"
    prob_sensibilidad += x_sens[4] + x_sens[5] >= demanda[5], f"D_6"
    
    prob_sensibilidad.solve(PULP_CBC_CMD(msg=0))
    valores_obj.append(value(prob_sensibilidad.objective))

# Gráfico de sensibilidad
fig_sens, ax_sens = plt.subplots(figsize=(10, 6))
ax_sens.plot(cambios, valores_obj, 'o-', linewidth=2.5, markersize=8, color='#FF6B6B')
ax_sens.axvline(x=0, color='green', linestyle='--', linewidth=2, label='Valor original (0)')
ax_sens.set_xlabel('Cambio en Coeficiente de x₁ (ΔC₁)', fontsize=12, fontweight='bold')
ax_sens.set_ylabel('Valor Óptimo de la Función Objetivo', fontsize=12, fontweight='bold')
ax_sens.set_title('Análisis de Sensibilidad: Variación de Coeficiente en x₁', fontsize=13, fontweight='bold')
ax_sens.grid(True, alpha=0.3)
ax_sens.legend(fontsize=11)
plt.tight_layout()
plt.savefig('c:\\xampp\\TRABAJO-OPERATIVA\\Sensibilidad_Coeficientes.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico guardado: Sensibilidad_Coeficientes.png")
plt.show()

# ==================== ANÁLISIS DE RANGO DE VIABILIDAD (RHS) ====================
print("\n2. RANGO DE VIABILIDAD DE RESTRICCIONES (RHS)")
print("-" * 80)
print("\nPregunta: ¿Cuánto pueden cambiar los valores de demanda (RHS)")
print("sin que aumente el número total de cajeros?")

print("\nAlgoritmo: Incrementar demanda de cada período y ver cómo crece el total")

resultados_rango = []

for periodo in range(6):
    demandas_alt = demanda.copy()
    incrementos = range(0, 21, 2)
    valores_z = []
    
    for incremento in incrementos:
        demandas_alt[periodo] = demanda[periodo] + incremento
        
        prob_alt = LpProblem("RHS_Sensitivity", LpMinimize)
        x_alt = [LpVariable(f"x_{i+1}", lowBound=0, cat='Integer') for i in range(6)]
        
        prob_alt += lpSum(x_alt), "Obj"
        
        prob_alt += x_alt[5] + x_alt[0] >= demandas_alt[0], f"D_1"
        prob_alt += x_alt[0] + x_alt[1] >= demandas_alt[1], f"D_2"
        prob_alt += x_alt[1] + x_alt[2] >= demandas_alt[2], f"D_3"
        prob_alt += x_alt[2] + x_alt[3] >= demandas_alt[3], f"D_4"
        prob_alt += x_alt[3] + x_alt[4] >= demandas_alt[4], f"D_5"
        prob_alt += x_alt[4] + x_alt[5] >= demandas_alt[5], f"D_6"
        
        prob_alt.solve(PULP_CBC_CMD(msg=0))
        valores_z.append(value(prob_alt.objective))
        
        demandas_alt = demanda.copy()  # Reset
    
    resultados_rango.append(valores_z)
    print(f"\nPeríodo {periodo+1} ({periodos[periodo]}):")
    print(f"  Demanda original: {demanda[periodo]}")
    print(f"  Incrementos: {list(incrementos)}")
    print(f"  Valor objetivo: {valores_z}")
    print(f"  Tasa de incremento: {(valores_z[-1] - valores_z[0]) / (incrementos[-1] - incrementos[0]):.2f} cajeros/unidad demanda")

# ==================== TABLA RESUMEN ====================
print("\n" + "="*80)
print("TABLA RESUMEN: SOLUCIÓN ÓPTIMA")
print("="*80)

resumen_df = pd.DataFrame({
    'Período': periodos,
    'Demanda': demanda,
    'Cobertura': cobertura,
    'Holgura': [c - d for c, d in zip(cobertura, demanda)],
    'x_i (Turnos)': solucion_x,
    'y_j (Dual)': [f"{y:.2f}" for y in solucion_y],
    'Restricción Activa': ['Sí' if h == 0 else 'No' for h in [c - d for c, d in zip(cobertura, demanda)]]
})

print(resumen_df.to_string(index=False))

# ==================== CONCLUSIONES ====================
print("\n" + "="*80)
print("CONCLUSIONES DEL ANÁLISIS")
print("="*80)

print(f"""
✓ SOLUCIÓN ÓPTIMA GENERAL:
  - Total de cajeros: 45
  - Este es el MÍNIMO NECESARIO para satisfacer la demanda

✓ PERÍODOS CRÍTICOS (y_j = 1.0):
  - Período 2 (7-11): 20 cajeros mínimos
  - Período 4 (15-19): 20 cajeros mínimos  
  - Período 6 (23-3): 5 cajeros mínimos
  → Aumentar demanda en estos períodos → aumenta personal total

✓ PERÍODOS NO CRÍTICOS (y_j = 0.0):
  - Período 1 (3-7): Tiene cierta flexibilidad
  - Período 3 (11-15): Cobertura excedente de 4 cajeros
  - Período 5 (19-23): Cobertura excedente de 10 cajeros
  → Reducir demanda en estos períodos → No reduce personal total (hay holgura)

✓ INTERPRETACIÓN DE HOLGURA COMPLEMENTARIA:
  - 4 variables positivas (x₁, x₂, x₄, x₆) ↔ 4 restricciones duales activas
  - Las restricciones activas son exactamente donde se necesita la demanda
  - Esto garantiza que la solución es ÓPTIMA

✓ RECOMENDACIONES PRÁCTICAS:
  1. Contratar 45 cajeros en total
  2. Enfoque en períodos 2 y 4 (máxima intensidad)
  3. Mantener flexibilidad en períodos 3 y 5 (pueden cubrirse con otros turnos)
  4. Priorizar horarios: período 1 (2), período 2 (18), período 4 (20), período 6 (5)
""")

print("\n" + "="*80)
print("ANÁLISIS COMPLETADO")
print("="*80)
