# GUÍA RÁPIDA - PROBLEMA STAFFING FARMATODO

## 📌 RESUMEN EJECUTIVO

**Problema:** Una tienda Farmatodo abierta 24 horas necesita determinar cuántos cajeros contratar.

**Respuesta:** **45 cajeros** distribuidos así:
- 2 comienzan a las 3 AM (período 1)
- 18 comienzan a las 7 AM (período 2)
- 20 comienzan a las 3 PM (período 4)
- 5 comienzan a las 11 PM (período 6)

---

## 🎯 EL MODELO PRIMAL (Problema de Decisión)

### ¿QUÉ SE BUSCA?
Decidir cuántos cajeros enviar a trabajar en cada período.

### VARIABLES PRIMAL
```
x₁ = Cajeros que comienzan turno a las 3-7 AM
x₂ = Cajeros que comienzan turno a las 7-11 AM
x₃ = Cajeros que comienzan turno a las 11-15 (11 AM-3 PM)
x₄ = Cajeros que comienzan turno a las 15-19 (3 PM-7 PM)
x₅ = Cajeros que comienzan turno a las 19-23 (7 PM-11 PM)
x₆ = Cajeros que comienzan turno a las 23-3 (11 PM-3 AM)
```

### FUNCIÓN OBJETIVO (Minimizar)
```
Z = x₁ + x₂ + x₃ + x₄ + x₅ + x₆

Minimizar el TOTAL de cajeros
```

### RESTRICCIONES
Cada restricción **garantiza que la demanda se satisface en cada período**:

| Período | Restricción | Significado |
|---------|------------|-------------|
| 3-7 AM | x₆ + x₁ ≥ 7 | Los turnos que comenzaron ayer a las 11 PM + hoy a las 3 AM cubren la demanda de 7 |
| 7-11 AM | x₁ + x₂ ≥ 20 | Los turnos que comenzaron a las 3 AM + 7 AM cubren la demanda de 20 |
| 11-15 (11 AM-3 PM) | x₂ + x₃ ≥ 14 | Los turnos que comenzaron a las 7 AM + 11 AM cubren la demanda de 14 |
| 15-19 (3 PM-7 PM) | x₃ + x₄ ≥ 20 | Los turnos que comenzaron a las 11 AM + 3 PM cubren la demanda de 20 |
| 19-23 (7 PM-11 PM) | x₄ + x₅ ≥ 10 | Los turnos que comenzaron a las 3 PM + 7 PM cubren la demanda de 10 |
| 23-3 (11 PM-3 AM) | x₅ + x₆ ≥ 5 | Los turnos que comenzaron a las 7 PM + 11 PM cubren la demanda de 5 |

**Nota:** Cada cajero trabaja 8 horas consecutivas = 2 períodos de 4 horas

---

## 🔄 EL MODELO DUAL (Problema de Valoración)

### ¿QUÉ SE BUSCA?
Encontrar el "precio sombra" o "valor marginal" de la demanda en cada período.

### VARIABLES DUAL
```
y₁ = ¿Cuántos cajeros ahorraríamos si la demanda del período 1 bajara en 1?
y₂ = ¿Cuántos cajeros ahorraríamos si la demanda del período 2 bajara en 1?
y₃ = ¿Cuántos cajeros ahorraríamos si la demanda del período 3 bajara en 1?
y₄ = ¿Cuántos cajeros ahorraríamos si la demanda del período 4 bajara en 1?
y₅ = ¿Cuántos cajeros ahorraríamos si la demanda del período 5 bajara en 1?
y₆ = ¿Cuántos cajeros ahorraríamos si la demanda del período 6 bajara en 1?
```

### FUNCIÓN OBJETIVO (Maximizar)
```
W = 7y₁ + 20y₂ + 14y₃ + 20y₄ + 10y₅ + 5y₆

Maximizar el VALOR TOTAL de la cobertura
```

### RESTRICCIONES DUALES
Cada restricción **limita cuánto puede servir cada variable dual**:

| Restricción | Significado |
|-------------|-------------|
| y₆ + y₁ ≤ 1 | El valor de cubrir los períodos 6 y 1 ≤ 1 cajero |
| y₁ + y₂ ≤ 1 | El valor de cubrir los períodos 1 y 2 ≤ 1 cajero |
| y₂ + y₃ ≤ 1 | El valor de cubrir los períodos 2 y 3 ≤ 1 cajero |
| y₃ + y₄ ≤ 1 | El valor de cubrir los períodos 3 y 4 ≤ 1 cajero |
| y₄ + y₅ ≤ 1 | El valor de cubrir los períodos 4 y 5 ≤ 1 cajero |
| y₅ + y₆ ≤ 1 | El valor de cubrir los períodos 5 y 6 ≤ 1 cajero |

**Razón:** Un cajero cubre EXACTAMENTE 2 períodos consecutivos, entonces su valor no puede ser > 1.

---

## ✅ SOLUCIONES ÓPTIMAS

### Primal
```
x₁* = 2
x₂* = 18
x₃* = 0
x₄* = 20
x₅* = 0
x₆* = 5

Z* = 2 + 18 + 0 + 20 + 0 + 5 = 45 cajeros
```

### Dual
```
y₁* = 0.0
y₂* = 1.0
y₃* = 0.0
y₄* = 1.0
y₅* = 0.0
y₆* = 1.0

W* = 7(0) + 20(1) + 14(0) + 20(1) + 10(0) + 5(1) = 45
```

**IMPORTANTE:** Z* = W* = 45 (Se cumple la dualidad fuerte ✓)

---

## 🔗 RELACIÓN PRIMAL-DUAL: HOLGURA COMPLEMENTARIA

### LA REGLA
1. **Si x_i > 0** → su restricción dual **debe ser = 1** (restricción activa)
2. **Si restricción primal tiene holgura** → su variable dual **debe ser 0**

### VERIFICACIÓN

```
VARIABLES PRIMALES POSITIVAS:
✓ x₁ = 2 > 0  →  y₆ + y₁ = 1.0 + 0.0 = 1.0 ✓ ACTIVA
✓ x₂ = 18 > 0 →  y₁ + y₂ = 0.0 + 1.0 = 1.0 ✓ ACTIVA  
✓ x₄ = 20 > 0 →  y₃ + y₄ = 0.0 + 1.0 = 1.0 ✓ ACTIVA
✓ x₆ = 5 > 0  →  y₅ + y₆ = 0.0 + 1.0 = 1.0 ✓ ACTIVA

RESTRICCIONES CON HOLGURA:
✓ Período 3: Cobertura 18 > Demanda 14 (holgura=4) → y₃ = 0 ✓
✓ Período 5: Cobertura 20 > Demanda 10 (holgura=10) → y₅ = 0 ✓

RESTRICCIONES ACTIVAS (sin holgura):
✓ Período 1: Cobertura = Demanda = 7 → y₁ puede ser > 0 (es 0)
✓ Período 2: Cobertura = Demanda = 20 → y₂ puede ser > 0 (es 1) ✓
✓ Período 4: Cobertura = Demanda = 20 → y₄ puede ser > 0 (es 1) ✓
✓ Período 6: Cobertura = Demanda = 5 → y₆ puede ser > 0 (es 1) ✓
```

✓ **TODAS LAS CONDICIONES DE COMPLEMENTARIEDAD SE CUMPLEN**

---

## 📊 INTERPRETACIÓN DE VALORES DUALES

### Precios Sombra

```
y₁ = 0.0  → Reducir demanda período 1 en 1 NO ahorraría cajeros
y₂ = 1.0  → Reducir demanda período 2 en 1 ahorraría 1 CAJERO ⭐
y₃ = 0.0  → Reducir demanda período 3 en 1 NO ahorraría cajeros
y₄ = 1.0  → Reducir demanda período 4 en 1 ahorraría 1 CAJERO ⭐
y₅ = 0.0  → Reducir demanda período 5 en 1 NO ahorraría cajeros
y₆ = 1.0  → Reducir demanda período 6 en 1 ahorraría 1 CAJERO ⭐
```

### Clasificación de Períodos

**CRÍTICOS (y > 0):** Períodos 2, 4, 6
- Aumentar demanda → aumenta personal total
- Reducir demanda → reduce personal total
- Son "cuellos de botella"

**NO CRÍTICOS (y = 0):** Períodos 1, 3, 5
- Hay holgura en la cobertura
- Pueden reducirse sin afectar el total
- Hay flexibilidad

---

## 💡 ANÁLISIS DE SENSIBILIDAD

### Efecto de cambios de demanda

```
Período 2 (crítico):
  Aumentar demanda en 1 → aumenta personal en 1 cajero
  Tasa: 1.0 cajeros/unidad

Período 3 (no crítico):
  Aumentar demanda en 1 → aumenta personal en ~0.3 cajeros
  (Porque hay holgura de 4 cajeros)
  Tasa: 0.3 cajeros/unidad
```

### Rangos de viabilidad (sin cambiar la solución)

```
Período 1: Demanda puede aumentar hasta en ~16 sin afectar personal
Período 2: Cada aumento de demanda requiere 1 cajero más
Período 3: Demanda puede aumentar hasta en ~4 sin afectar personal
Período 4: Cada aumento de demanda requiere 1 cajero más
Período 5: Demanda puede aumentar hasta en ~10 sin afectar personal
Período 6: Cada aumento de demanda requiere 1 cajero más
```

---

## 📋 TABLA COMPARATIVA PRIMAL vs DUAL

| Aspecto | Primal | Dual |
|---------|--------|------|
| **Objetivo** | Minimizar personal | Maximizar valor |
| **Variables** | x_i (decisiones) | y_j (precios) |
| **Restricciones** | Demanda (≥) | Restricciones duales (≤) |
| **Rango de valores** | x ≥ 0, enteros | y ≥ 0, reales |
| **Interpretación** | ¿Cuántos? | ¿Cuánto vale? |
| **Solución óptima** | 45 cajeros | Valor = 45 |

---

## 🎓 CONCEPTOS CLAVE

### 1. **Dualidad Fuerte**
> "Si un problema primal tiene solución óptima finita, su dual también la tiene, y son iguales."
>
> En nuestro caso: Z* = W* = 45 ✓

### 2. **Restricciones Activas vs Inactivas**
- **Activa:** Se cumple con igualdad (holgura = 0)
- **Inactiva:** Tiene holgura (cobertura > demanda)

### 3. **Holgura Complementaria**
> "Si una variable en el primal es positiva, su restricción dual debe ser activa."

### 4. **Precios Sombra**
> "Cuánto cambiaría el valor objetivo si relajáramos (modificáramos) una restricción en 1 unidad."

---

## 🚀 CÓMO USAR ESTA SOLUCIÓN EN PRÁCTICA

1. **Contrata 45 cajeros total**
2. **Horarios:**
   - 2 cajeros: Turno 3 AM - 11 AM
   - 18 cajeros: Turno 7 AM - 3 PM
   - 20 cajeros: Turno 3 PM - 11 PM
   - 5 cajeros: Turno 11 PM - 7 AM

3. **Verifica cobertura:**
   - 3-7 AM: 5 (turno noche) + 2 (turno mañana) = 7 ✓
   - 7-11 AM: 2 (turno mañana) + 18 (turno día) = 20 ✓
   - 11 AM-3 PM: 18 (turno día) + 0 (turno tarde) = 18 ✓ (14 requeridos + 4 extra)
   - 3-7 PM: 0 (turno día) + 20 (turno tarde) = 20 ✓
   - 7-11 PM: 20 (turno tarde) + 0 (turno noche) = 20 ✓ (10 requeridos + 10 extra)
   - 11 PM-3 AM: 0 (turno tarde) + 5 (turno noche) = 5 ✓

4. **Si hay cambios de demanda:**
   - Períodos 2, 4, 6: Cada aumento de 1 requiere 1 cajero más
   - Períodos 1, 3, 5: Hay flexibilidad de 4-16 cajeros

---

## 📝 ARCHIVO DE CÓDIGO

Consulta `Ejercicio_Staffing_Farmatodo.py` para ver la implementación completa con:
- Definición del modelo primal
- Definición del modelo dual
- Resolución con PuLP
- Análisis de holgura complementaria
- Verificación de dualidad fuerte

