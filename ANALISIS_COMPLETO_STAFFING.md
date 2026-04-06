# ANÁLISIS COMPLETO: PROBLEMA DE PLANIFICACIÓN DE PERSONAL (STAFFING) - FARMATODO

## 📋 DESCRIPCIÓN DEL PROBLEMA

**Contexto:** Una tienda Farmatodo abierta 24 horas necesita determinar el número mínimo de cajeros que debe contratar para satisfacer la demanda de cada período.

**Características del problema:**
- La tienda funciona 24 horas divididas en 6 períodos de 4 horas cada uno
- Los cajeros trabajan 8 horas consecutivas (cubriendo exactamente 2 períodos)
- Cada cajero puede comenzar su turno al inicio de cualquier período
- Se debe satisfacer la demanda mínima de cajeros en cada período
- Objetivo: **Minimizar el número total de cajeros contratados**

---

## 📊 DATA DEL PROBLEMA

| Período | Horario | Demanda Mínima | Duración |
|---------|---------|----------------|----------|
| 1 | 3-7 | 7 | 4 horas |
| 2 | 7-11 | 20 | 4 horas |
| 3 | 11-15 | 14 | 4 horas |
| 4 | 15-19 | 20 | 4 horas |
| 5 | 19-23 | 10 | 4 horas |
| 6 | 23-3 | 5 | 4 horas |

---

## 🎯 MODELO PRIMAL (PROBLEMA ORIGINAL)

### Definición de Variables

Cada variable $x_i$ representa el número de cajeros que **comienzan su turno** al inicio del período $i$ (0 ≤ i ≤ 5):

$$x_i = \text{Número de cajeros que comienzan turno en período } i$$

Los turnos son de 8 horas consecutivas:
- Turno que comienza en período 1 (3-7): trabaja 3-7 y 7-11 (períodos 1 y 2)
- Turno que comienza en período 2 (7-11): trabaja 7-11 y 11-15 (períodos 2 y 3)
- Turno que comienza en período 3 (11-15): trabaja 11-15 y 15-19 (períodos 3 y 4)
- Turno que comienza en período 4 (15-19): trabaja 15-19 y 19-23 (períodos 4 y 5)
- Turno que comienza en período 5 (19-23): trabaja 19-23 y 23-3 (períodos 5 y 6)
- Turno que comienza en período 6 (23-3): trabaja 23-3 y 3-7 (períodos 6 y 1)

### Función Objetivo (Minimizar)

$$Z = x_1 + x_2 + x_3 + x_4 + x_5 + x_6$$

**Interpretación:** Minimizar el número total de cajeros contratados.

### Restricciones de Cobertura

Cada restricción asegura que la demanda de cada período sea satisfecha:

| Período | Restricción | Interpretación |
|---------|------------|-----------------|
| 1 (3-7) | $x_6 + x_1 \geq 7$ | Cubierto por turnos iniciados en período 6 y período 1 |
| 2 (7-11) | $x_1 + x_2 \geq 20$ | Cubierto por turnos iniciados en período 1 y período 2 |
| 3 (11-15) | $x_2 + x_3 \geq 14$ | Cubierto por turnos iniciados en período 2 y período 3 |
| 4 (15-19) | $x_3 + x_4 \geq 20$ | Cubierto por turnos iniciados en período 3 y período 4 |
| 5 (19-23) | $x_4 + x_5 \geq 10$ | Cubierto por turnos iniciados en período 4 y período 5 |
| 6 (23-3) | $x_5 + x_6 \geq 5$ | Cubierto por turnos iniciados en período 5 y período 6 |

### Restricciones de No-negatividad e Integralidad

$$x_i \geq 0 \text{ y enteros, } \forall i = 1,2,3,4,5,6$$

### Formulación Completa (Forma Estándar)

```
Minimizar:  Z = x₁ + x₂ + x₃ + x₄ + x₅ + x₆

Sujeto a:
  x₆ + x₁ ≥ 7      (Período 1)
  x₁ + x₂ ≥ 20     (Período 2)
  x₂ + x₃ ≥ 14     (Período 3)
  x₃ + x₄ ≥ 20     (Período 4)
  x₄ + x₅ ≥ 10     (Período 5)
  x₅ + x₆ ≥ 5      (Período 6)
  
  xᵢ ≥ 0 y enteros, ∀ i
```

---

## 🔄 MODELO DUAL (PROBLEMA ASOCIADO)

### Transformación de Primal a Dual

Para obtener el dual, aplicamos las reglas de transformación:

| Aspecto | Primal | Dual |
|--------|--------|------|
| **Sentido de optimización** | Minimizar | Maximizar |
| **Restricciones primales** | ≥ (desigualdades) | 6 variables duales |
| **Variables primales** | 6 variables | 6 restricciones ≤ |
| **Matriz de coeficientes** | A | $A^T$ (transpuesta) |
| **Vector RHS** | b (demanda) | c (coeficientes objetivo) |
| **Vector c** | coef. objetivo | b (demanda) |

### Definición de Variables Duales

Cada variable $y_j$ representa el **valor marginal** (precio sombra) de relajar la restricción de demanda en el período $j$:

$$y_j = \text{Valor dual asociado a la restricción de demanda en período } j$$

Interpretación económica: $y_j$ representa el número máximo de cajeros que se ahorraría por reducir en 1 la demanda del período $j$.

### Función Objetivo (Maximizar)

$$W = 7y_1 + 20y_2 + 14y_3 + 20y_4 + 10y_5 + 5y_6$$

**Interpretación:** Maximizar el valor total de la cobertura de demanda.

### Restricciones Duales

Cada restricción dual está asociada a una variable primal y garantiza que el valor dual nunca sea "demasiado grande":

| Variable Primal | Restricción Dual | Interpretación |
|-----------------|------------------|-----------------|
| $x_1$ | $y_6 + y_1 \leq 1$ | El cajero que comienza en período 1 cubre períodos 6 y 1 |
| $x_2$ | $y_1 + y_2 \leq 1$ | El cajero que comienza en período 2 cubre períodos 1 y 2 |
| $x_3$ | $y_2 + y_3 \leq 1$ | El cajero que comienza en período 3 cubre períodos 2 y 3 |
| $x_4$ | $y_3 + y_4 \leq 1$ | El cajero que comienza en período 4 cubre períodos 3 y 4 |
| $x_5$ | $y_4 + y_5 \leq 1$ | El cajero que comienza en período 5 cubre períodos 4 y 5 |
| $x_6$ | $y_5 + y_6 \leq 1$ | El cajero que comienza en período 6 cubre períodos 5 y 6 |

### Restricciones de No-negatividad

$$y_j \geq 0, \text{ pero pueden ser libres de signo (sin restricción de signo)}$$

### Formulación Completa (Forma Estándar)

```
Maximizar:  W = 7y₁ + 20y₂ + 14y₃ + 20y₄ + 10y₅ + 5y₆

Sujeto a:
  y₆ + y₁ ≤ 1     (Restricción dual para x₁)
  y₁ + y₂ ≤ 1     (Restricción dual para x₂)
  y₂ + y₃ ≤ 1     (Restricción dual para x₃)
  y₃ + y₄ ≤ 1     (Restricción dual para x₄)
  y₄ + y₅ ≤ 1     (Restricción dual para x₅)
  y₅ + y₆ ≤ 1     (Restricción dual para x₆)
  
  yⱼ ≥ 0, ∀ j (pueden ser libres)
```

---

## ✅ SOLUCIÓN ÓPTIMA

### Solución del Modelo Primal

```
Valor Óptimo: Z* = 45 cajeros

Asignación óptima:
  x₁ = 2   cajeros comienzan en período 1 (3-7)
  x₂ = 18  cajeros comienzan en período 2 (7-11)
  x₃ = 0   cajeros comienzan en período 3 (11-15)
  x₄ = 20  cajeros comienzan en período 4 (15-19)
  x₅ = 0   cajeros comienzan en período 5 (19-23)
  x₆ = 5   cajeros comienzan en período 6 (23-3)
```

### Verificación de Cobertura

| Período | Demanda | Cobertura | Turnos que cubren | Estado |
|---------|---------|-----------|-------------------|--------|
| 1 (3-7) | 7 | 7 | x₆ + x₁ = 5 + 2 | ✓ Exacto |
| 2 (7-11) | 20 | 20 | x₁ + x₂ = 2 + 18 | ✓ Exacto |
| 3 (11-15) | 14 | 18 | x₂ + x₃ = 18 + 0 | ✓ Exceso +4 |
| 4 (15-19) | 20 | 20 | x₃ + x₄ = 0 + 20 | ✓ Exacto |
| 5 (19-23) | 10 | 20 | x₄ + x₅ = 20 + 0 | ✓ Exceso +10 |
| 6 (23-3) | 5 | 5 | x₅ + x₆ = 0 + 5 | ✓ Exacto |

### Solución del Modelo Dual

```
Valor Óptimo: W* = 45 (igual al primal ✓)

Valores duales óptimos:
  y₁ = 0.0    (Período 1: 3-7)
  y₂ = 1.0    (Período 2: 7-11)
  y₃ = 0.0    (Período 3: 11-15)
  y₄ = 1.0    (Período 4: 15-19)
  y₅ = 0.0    (Período 5: 19-23)
  y₆ = 1.0    (Período 6: 23-3)
```

---

## 🔗 TEOREMA DE DUALIDAD FUERTE

### Enunciado

Para un par de problemas primal-dual, si ambos tienen soluciones óptimas finitas, entonces:

$$Z^*_{\text{primal}} = W^*_{\text{dual}}$$

### Verificación en Nuestro Problema

```
Valor óptimo del Primal:  Z* = 45 cajeros
Valor óptimo del Dual:    W* = 45
Diferencia:               |Z* - W*| = 0 ✓

=> Se cumple la DUALIDAD FUERTE
```

---

## 📐 CONDICIONES DE HOLGURA COMPLEMENTARIA

### Teorema: Complementariedad

Para soluciones óptimas $x^*$ e $y^*$, se cumple:

1. **Si $x_i^* > 0$**, entonces la restricción dual $i$ es **activa** (se cumple con igualdad):
   $$\sum_j a_{ji} y_j^* = c_i$$

2. **Si la restricción primal $j$ tiene holgura** (cobertura > demanda), entonces:
   $$y_j^* = 0$$

### Análisis en Nuestro Problema

#### Variables Primales Positivas

```
x₁ = 2 > 0  → Restricción dual 1: y₆ + y₁ = 1
             Verificación: 1.0 + 0.0 = 1.0 ✓ ACTIVA

x₂ = 18 > 0 → Restricción dual 2: y₁ + y₂ = 1
             Verificación: 0.0 + 1.0 = 1.0 ✓ ACTIVA

x₄ = 20 > 0 → Restricción dual 4: y₃ + y₄ = 1
             Verificación: 0.0 + 1.0 = 1.0 ✓ ACTIVA

x₆ = 5 > 0  → Restricción dual 6: y₅ + y₆ = 1
             Verificación: 0.0 + 1.0 = 1.0 ✓ ACTIVA
```

#### Variables Primales Cero

```
x₃ = 0      → Restricción dual 3: y₂ + y₃ ≤ 1
             Verificación: 1.0 + 0.0 = 1.0 ✓ Se cumple

x₅ = 0      → Restricción dual 5: y₄ + y₅ ≤ 1
             Verificación: 1.0 + 0.0 = 1.0 ✓ Se cumple
```

#### Restricciones Primales con Holgura

```
Período 3: Cobertura 18 - Demanda 14 = Holgura 4
           → y₃ = 0.0 ✓ Cumple complementariedad

Período 5: Cobertura 20 - Demanda 10 = Holgura 10
           → y₅ = 0.0 ✓ Cumple complementariedad
```

#### Restricciones Primales Activas (sin holgura)

```
Período 1: Cobertura 7 = Demanda 7 (ACTIVA)
           → y₁ puede ser > 0 ✓ y₁ = 0.0

Período 2: Cobertura 20 = Demanda 20 (ACTIVA)
           → y₂ puede ser > 0 ✓ y₂ = 1.0

Período 4: Cobertura 20 = Demanda 20 (ACTIVA)
           → y₄ puede ser > 0 ✓ y₄ = 1.0

Período 6: Cobertura 5 = Demanda 5 (ACTIVA)
           → y₆ puede ser > 0 ✓ y₆ = 1.0
```

**Conclusión:** Todas las condiciones de holgura complementaria se cumplen perfectamente ✓

---

## 💡 INTERPRETACIÓN ECONÓMICA

### Significado de los Valores Duales

$$y_j = \text{Precio sombra del período } j$$

Representa cuántos cajeros menos necesitaríamos si pudiéramos reducir la demanda del período $j$ en 1 unidad.

```
y₁ = 0.0  → Reducir demanda del período 1 NO ahorraría cajeros
            (hay holgura, se usan recursos que podrían no usarse)

y₂ = 1.0  → Reducir demanda del período 2 en 1 ahorraría 1 cajero
            (crítico: demanda crítica)

y₃ = 0.0  → Reducir demanda del período 3 NO ahorraría cajeros
            (hay exceso de cobertura)

y₄ = 1.0  → Reducir demanda del período 4 en 1 ahorraría 1 cajero
            (crítico: demanda crítica)

y₅ = 0.0  → Reducir demanda del período 5 NO ahorraría cajeros
            (hay exceso de cobertura)

y₆ = 1.0  → Reducir demanda del período 6 en 1 ahorraría 1 cajero
            (crítico: demanda crítica)
```

### Períodos Críticos

Los períodos 2, 4 y 6 son **críticos** porque:
- Su valor dual es 1.0
- Cualquier aumento en su demanda requeriría contratar más cajeros
- Son los "cuellos de botella" del sistema

Los períodos 1, 3 y 5 son **no críticos** porque:
- Su valor dual es 0.0
- Tienen cierta flexibilidad en la cobertura
- Los recursos asignados pueden redistribuirse

---

## 📈 INTERPRETACIÓN DE LA SOLUCIÓN

### Distribución de Turnos

```
HORARIO DE OPERACIÓN: 24 horas (períodos de 4 horas)

Período 1 (3-7):      ████ 7 cajeros (5 de período 6 + 2 nuevos)
Período 2 (7-11):     ████████████████████ 20 cajeros (exacto)
Período 3 (11-15):    ██████████████████ 18 cajeros (14 requeridos + 4 exceso)
Período 4 (15-19):    ████████████████████ 20 cajeros (exacto)
Período 5 (19-23):    ████████████████████ 20 cajeros (10 requeridos + 10 exceso)
Período 6 (23-3):     █████ 5 cajeros (exacto)
```

### Flujo de Personal Acumulativo

| Período | Turnos que terminan | Cayeros en turno | Turnos que comienzan | Total |
|---------|-------------------|------------------|----------------------|--------|
| 1 | x₅=0 | 7 | - | 7 |
| 2 | x₆=5 | 7-5=2 (+18) | x₁=2 | 20 |
| 3 | x₁=2 | 20-2=18 (+0) | x₂=18 | 18 |
| 4 | x₂=18 | 18-18=0 (+20) | x₃=0 | 20 |
| 5 | x₃=0 | 20-0=20 (+0) | x₄=20 | 20 |
| 6 | x₄=20 | 20-20=0 (+5) | x₅=0 | 5 |

---

## 🎓 CONCLUSIONES

### Respuesta a la Pregunta Original

**"Determine qué grupo diario de empleados satisface las necesidades con el mínimo de personal."**

**RESPUESTA:** 
- **Número mínimo total de cajeros: 45**
- **Distribución óptima:**
  - 2 cajeros comienzan turno a las 3 AM (período 1)
  - 18 cajeros comienzan turno a las 7 AM (período 2)
  - 0 cajeros comienzan turno a las 11 AM (período 3)
  - 20 cajeros comienzan turno a las 3 PM (período 4)
  - 0 cajeros comienzan turno a las 7 PM (período 5)
  - 5 cajeros comienzan turno a las 11 PM (período 6)

### Ventajas de Este Modelo

1. ✓ Método sistemático y óptimo (no heurístico)
2. ✓ Garantiza satisfacer todas las restricciones
3. ✓ Proporciona el mínimo costo (menos personal)
4. ✓ Fácilmente adaptable a nuevos períodos o restricciones
5. ✓ Proporciona análisis de sensibilidad (valores duales)

### Períodos Prioritarios

- **Períodos 2, 4, 6:** Son críticos (y=1). Cualquier cambio en la demanda afecta el total de personal
- **Períodos 1, 3, 5:** Son válvulas de escape. Tienen cierta flexibilidad

---

## 📚 Referencias Teóricas

Este problema es un caso clásico de:
- **Programación Lineal Entera**
- **Problema de Cobertura de Turnos (Shift Scheduling)**
- **Teoría de Dualidad en Optimización**
- **Análisis de Sensibilidad Usando Precios Sombra**

Aplicaciones reales similares:
- Planificación de personal en hospitales, call centers, supermercados
- Asignación de recursos en manufactura
- Planificación de transporte público
- Asignación de turnos en seguridad

