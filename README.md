# 🐱 Agentes de IA — Demo en vivo

Demo construida para la píldora formativa **"De chatbot a gato autónomo"**.

Un agente ReAct implementado desde cero en Python usando Groq como LLM, sin frameworks como LangChain o CrewAI.

---

## ¿Qué es un agente ReAct?

ReAct es un patrón de razonamiento donde el agente alterna entre:

- **Thought** — razona sobre qué hacer
- **Action** — elige una herramienta y la ejecuta
- **Observation** — observa el resultado y decide el siguiente paso

Este ciclo se repite hasta que el agente considera que tiene la respuesta final.

```
Thought → Action → Observation → Thought → Action → Observation → Final Answer
```

---

## ¿Qué hace esta demo?

El agente recibe una misión, razona paso a paso y usa herramientas reales para completarla:

```
🎯 Misión: Calcula 15 * 4 y luego ponlo en mayúsculas con el texto 'el resultado es'

--- Paso 1 ---
Thought: Primero necesito calcular el producto de 15 y 4.
Action: calcular
Input: 15 * 4
⚙️  Observation: 60

--- Paso 2 ---
Thought: Ahora combino el resultado con el texto y lo paso a mayúsculas.
Action: mayusculas
Input: el resultado es 60
⚙️  Observation: EL RESULTADO ES 60

--- Paso 3 ---
Thought: Ya tengo la respuesta
Final Answer: EL RESULTADO ES 60

✅ Respuesta final: EL RESULTADO ES 60
```

---

## Estructura del proyecto

```
agentes-ia-demo/
├── agente_demo.py      # El agente ReAct completo
├── requirements.txt    # Dependencias
├── .env.example        # Plantilla para la API key
└── README.md
```

---

## Cómo funciona el código

### 1. Herramientas
Son funciones Python normales que el agente puede invocar:

```python
def calcular(expresion: str) -> str:
    return str(eval(expresion))

def mayusculas(texto: str) -> str:
    return texto.upper()
```

En un agente real serían llamadas a APIs, búsquedas web, consultas a bases de datos, etc.

### 2. System prompt
Le indica al LLM el formato exacto que debe seguir (patrón ReAct):

```
Thought: <lo que estás pensando>
Action: <nombre_herramienta>
Input: <argumento>
```

El modelo no "sabe" ser un agente por defecto — el prompt es lo que lo convierte en uno.

### 3. El loop
El núcleo del agente: llama al LLM, ejecuta la herramienta, devuelve la observación y repite:

```python
for paso in range(1, 6):
    respuesta = llm(mensajes)
    
    if "Final Answer:" in respuesta:
        break
    
    herramienta(input)
    mensajes.append(observation)
```

Eso es todo. Un loop, un prompt y herramientas.

---

## Instalación

### 1. Clona el repo
```bash
git clone https://github.com/karinaromerovasquez/agentes-ia-demo.git
cd agentes-ia-demo
```

### 2. Crea el entorno virtual
```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows (Git Bash)
# o
.venv\Scripts\activate          # Windows (cmd)
# o
source .venv/bin/activate       # Mac/Linux
```

### 3. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 4. Configura tu API key
Crea un archivo `.env` en la raíz del proyecto:
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

Consigue tu key gratis en [console.groq.com](https://console.groq.com)

### 5. Corre el agente
```bash
python agente_demo.py
```

---

## Tecnologías

- [Groq](https://groq.com) — LLM ultrarrápido
- [python-dotenv](https://pypi.org/project/python-dotenv/) — manejo de variables de entorno
- Python 3.10+

---

## ¿Por qué sin frameworks?

LangChain, CrewAI y similares son útiles en producción, pero ocultan la mecánica real.

Esta demo existe para mostrar que un agente es, en esencia, un loop con un prompt bien escrito. Una vez que entiendes esto, los frameworks tienen mucho más sentido.
