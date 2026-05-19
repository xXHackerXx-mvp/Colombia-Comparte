# Dashboard de Simulación · Colombia Comparte

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

## Descripción

Dashboard interactivo que aplica **Cadenas de Márkov de tiempo discreto** al flujo de navegación y registro de usuarios en la plataforma de **Colombia Comparte**, específicamente al proceso de inscripción al **Programa EDIFICA** de emprendimiento social.

El modelo comprende **33 estados** (pantallas y acciones de la plataforma), **66 recorridos base** de 5 perfiles de usuario y calcula las matrices de conteos y probabilidades de transición para simular el comportamiento de N usuarios, identificar el estado crítico de abandono y proponer intervenciones de mejora.

### Funcionalidades principales

- Visualización de estados y recorridos base del modelo
- Matrices de transición: conteos y probabilidades (con mapa de calor)
- Simulación Monte Carlo con parámetros ajustables (N usuarios, estado inicial, máximo de pasos)
- Análisis de resultados: tasa de éxito, abandono y error técnico
- Diagnóstico del estado crítico y generación de recomendaciones ejecutivas
- Comparación de escenarios inicial vs. mejorado

---

## Cómo ejecutar localmente

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPO>
cd colombia-comparte-simulacion
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

```bash
streamlit run app_colombia_comparte.py
```

La aplicación se abrirá automáticamente en `http://localhost:8501`.

---

## Despliegue en Streamlit Cloud

Esta aplicación está lista para desplegarse en **[Streamlit Cloud](https://share.streamlit.io)** sin configuración adicional.

**Pasos:**

1. Sube el repositorio a GitHub (todos los archivos de esta carpeta).
2. Ve a [https://share.streamlit.io](https://share.streamlit.io) e inicia sesión con tu cuenta de GitHub.
3. Haz clic en **"New app"**.
4. Selecciona el repositorio y la rama (`main` o `master`).
5. En el campo **"Main file path"**, escribe: `app_colombia_comparte.py`
6. Haz clic en **"Deploy"**.

Streamlit Cloud instalará las dependencias de `requirements.txt` e iniciará la aplicación automáticamente.

---

## Tecnologías usadas

| Tecnología | Versión mínima | Uso |
|---|---|---|
| **Python** | 3.10+ | Lenguaje principal |
| **Streamlit** | 1.32.0 | Framework de dashboard web |
| **Pandas** | 2.0.0 | Manipulación de matrices y datos tabulares |
| **NumPy** | 1.24.0 | Cálculo numérico y simulación Monte Carlo |
| **Matplotlib** | 3.7.0 | Visualizaciones y gráficas estadísticas |

---

## Universidad

**Universidad Santo Tomás · Seccional Tunja · 2026**

Proyecto académico desarrollado para la asignatura de Simulación, aplicando teoría de Cadenas de Márkov a un caso real de la organización social [Colombia Comparte](https://colombiacomparte.org) y su Programa EDIFICA de emprendimiento.

---

## Licencia

MIT — libre para uso académico y educativo.
