# 📊 Sistema de Análisis de Iteraciones - Taller 2

## Descripción General

Este sistema presenta un análisis completo de **iteraciones paso a paso** para los 4 ejercicios de optimización del Taller 2, mostrando cómo cada algoritmo llega a su solución óptima.

## 🎯 Objetivos Completados

✅ **Ejercicio 1: Staffing Farmatodo**
- Página interactiva: `ejercicio1_iteraciones.html`
- Muestra: Tabla de cobertura, valores duales, verificación de dualidad
- Datos: `datos_ejercicio1.json`
- Solución: 45 cajeros

✅ **Ejercicio 2: Problema de Mochila**
- Página interactiva: `ejercicio2_iteraciones.html`
- Muestra: Algoritmo Greedy, artículos, relajación continua
- Datos: `datos_ejercicio2.json`
- Solución: 180 unidades

✅ **Ejercicio 3: Bibliotecarios (Primal)**
- Página interactiva: `ejercicio3_iteraciones.html`
- Muestra: Asignación de turnos, verificación de cobertura, precios sombra
- Datos: `datos_ejercicio3.json`
- Solución: 26 bibliotecarios

✅ **Ejercicio 4: Bibliotecarios (Dual)**
- Página interactiva: `ejercicio4_iteraciones.html`
- Muestra: Precios sombra, interpretación de períodos críticos, relación primal-dual
- Datos: `datos_ejercicio4.json`
- Solución: 26 unidades

## 📱 Interfaz de Usuario

### Dashboard Central
- **Archivo:** `iteraciones_dashboard.html`
- **Función:** Centro de control para acceder a todas las iteraciones
- **Características:**
  - Resumen de cada ejercicio
  - Navegación rápida a análisis detallados
  - Verificación de conceptos clave

### Páginas de Iteraciones por Ejercicio
Cada página contiene:
- Solución óptima prominente
- Resumen de iteraciones
- Tablas interactivas de datos
- Carga dinámica desde JSON
- Diseño responsive

## 🔍 Datos de Iteraciones

### Ejercicio 1 (datos_ejercicio1.json)
```
- Asignación óptima
- Tabla de cobertura (6 períodos)
- Valores duales
- Estado de dualidad
```

### Ejercicio 2 (datos_ejercicio2.json)
```
- Artículos disponibles
- Relaciones valor/peso
- Solución Greedy
- Solución óptima
- Relajación continua
```

### Ejercicio 3 (datos_ejercicio3.json)
```
- Asignación de turnos
- Verificación de cobertura
- Horarios y demanda
- Valores duales
```

### Ejercicio 4 (datos_ejercicio4.json)
```
- Precios sombra (y_j)
- Análisis de períodos críticos
- Relación primal-dual
- Condiciones de optimalidad
```

## 🔗 Navegación

```
HOME (home.html)
    ├─ [Ver Análisis Completo de Iteraciones] → iteraciones_dashboard.html
    ├─ Ejercicio 1 → index.html
    │  └─ Ver Iteraciones → ejercicio1_iteraciones.html
    ├─ Ejercicio 2 → ejercicio2_mochila.html
    │  └─ Ver Iteraciones Greedy → ejercicio2_iteraciones.html
    ├─ Ejercicio 3 → ejercicio3_bibliotecarios.html
    │  └─ Ver Iteraciones y Tablas → ejercicio3_iteraciones.html
    └─ Ejercicio 4 → ejercicio4_dual.html
       └─ Ver Precios Sombra → ejercicio4_iteraciones.html
```

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python 3.13.7 con PuLP (solver COIN-OR CBC)
- **Data Export:** JSON
- **Frontend:** HTML5 + CSS3 + JavaScript
- **Servidor:** Python http.server (localhost:8000)
- **Visualización:** Tablas HTML dinámicas, gráficos CSS

## 📊 Conceptos Matemáticos Demostrados

1. **Dualidad Fuerte** - Z* = W* en todos los ejercicios
2. **Holgura Complementaria** - Condiciones de complementariedad verificadas
3. **Precios Sombra** - Interpretación económica de variables duales
4. **Relajación LP** - Cotas superiores/inferiores
5. **Heurísticas** - Comparación Greedy vs algoritmo óptimo (Ej. 2)

## 🚀 Instrucciones de Uso

### Ver el Sistema
1. Abre el navegador en: `http://localhost:8000/home.html`
2. Haz clic en "Ver Análisis Completo de Iteraciones"
3. Navega por cada ejercicio usando los botones
4. Cada página de iteraciones muestra tablas detalladas

### Ver un Ejercicio Específico
1. Desde `home.html`, haz clic en un ejercicio
2. En la página del ejercicio, usa el botón "📊 Ver Iteraciones"
3. Observa todas las tablas con la información paso a paso

### Acceso Directo a URLs

```
http://localhost:8000/home.html
http://localhost:8000/iteraciones_dashboard.html
http://localhost:8000/ejercicio1_iteraciones.html
http://localhost:8000/ejercicio2_iteraciones.html
http://localhost:8000/ejercicio3_iteraciones.html
http://localhost:8000/ejercicio4_iteraciones.html
```

## 📈 Archivos del Proyecto

### HTML (Interfaz)
- `home.html` - Página de inicio
- `iteraciones_dashboard.html` - Dashboard central de iteraciones
- `ejercicio1_iteraciones.html` - Iteraciones Ej. 1
- `ejercicio2_iteraciones.html` - Iteraciones Ej. 2
- `ejercicio3_iteraciones.html` - Iteraciones Ej. 3
- `ejercicio4_iteraciones.html` - Iteraciones Ej. 4
- `index.html` - Solución detallada Ej. 1 (original)
- `ejercicio2_mochila.html` - Solución Ej. 2 (original)
- `ejercicio3_bibliotecarios.html` - Solución Ej. 3 (original)
- `ejercicio4_dual.html` - Solución Ej. 4 (original)

### Python (Generadores de Datos)
- `Ejercicio1_Iteraciones.py` - Genera datos_ejercicio1.json
- `Ejercicio2_Iteraciones.py` - Genera datos_ejercicio2.json
- `Ejercicio3_Iteraciones.py` - Genera datos_ejercicio3.json
- `Ejercicio4_Iteraciones.py` - Genera datos_ejercicio4.json

### Data (JSON)
- `datos_ejercicio1.json` - Datos de iteraciones Ej. 1
- `datos_ejercicio2.json` - Datos de iteraciones Ej. 2
- `datos_ejercicio3.json` - Datos de iteraciones Ej. 3
- `datos_ejercicio4.json` - Datos de iteraciones Ej. 4

## ✨ Características Especiales

- **Carga Dinámica:** Los datos JSON se cargan automáticamente en cada página
- **Diseño Responsive:** Funciona en desktop y mobile
- **Navegación Fluida:** Botones de navegación integrados en cada página
- **Código Limpio:** HTML semántico, CSS organizado, JavaScript modular
- **Documentación Interna:** Comentarios en todas las páginas

## 🎓 Valor Educativo

Este sistema permite a estudiantes:
1. Ver cómo el algoritmo Simplex itera paso a paso
2. Entender la relación Primal-Dual
3. Observar cómo la heurística Greedy aproxima óptimos
4. Verificar matemáticamente la dualidad fuerte
5. Interpretar precios sombra en contexto económico

## 📝 Notas Adicionales

- Todos los archivos se sirven desde `c:\xampp\TRABAJO-OPERATIVA\`
- El servidor HTTP está en `localhost:8000`
- Los datos se generan ejecutando los scripts Python
- Las tablas se actualizan dinámicamente al cargar las páginas

---

**Creado para:** Taller 2 - Optimización y Dualidad
**Versión:** 1.0
**Última actualización:** 2024
