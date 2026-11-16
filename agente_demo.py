from dotenv import load_dotenv
from groq import Groq
import os
import time

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --- Herramientas disponibles ---
def calcular(expresion: str) -> str:
    return str(eval(expresion))

def mayusculas(texto: str) -> str:
    return texto.upper()

HERRAMIENTAS = {
    "calcular": calcular,
    "mayusculas": mayusculas,
}

SYSTEM_PROMPT = """Eres un agente que resuelve tareas paso a paso usando herramientas.

En cada paso debes responder EXACTAMENTE en este formato:
Thought: <lo que estás pensando>
Action: <nombre_herramienta>
Input: <argumento>

Cuando ya tengas la respuesta final, responde:
Thought: Ya tengo la respuesta
Final Answer: <respuesta>

Herramientas disponibles: calcular, mayusculas"""

def ejecutar_agente(mision: str):
    print(f"\n🎯 Misión: {mision}\n")
    mensajes = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": mision},
    ]

    for paso in range(1, 6):
        respuesta = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=mensajes,
        ).choices[0].message.content

        time.sleep(0.5)
        print(f"--- Paso {paso} ---")
        for linea in respuesta.splitlines():
            print(linea)
            time.sleep(0.05)

        if "Final Answer:" in respuesta:
            final = respuesta.split("Final Answer:")[-1].strip()
            print(f"\n✅ Respuesta final: {final}\n")
            break

        # Extraer acción e input
        if "Action:" in respuesta and "Input:" in respuesta:
            accion = respuesta.split("Action:")[-1].split("\n")[0].strip()
            entrada = respuesta.split("Input:")[-1].split("\n")[0].strip()

            if accion in HERRAMIENTAS:
                resultado = HERRAMIENTAS[accion](entrada)
                time.sleep(0.3)
                print(f"⚙️  Observation: {resultado}\n")
                mensajes.append({"role": "assistant", "content": respuesta})
                mensajes.append({"role": "user", "content": f"Observation: {resultado}"})
            else:
                print(f"❌ Herramienta '{accion}' no encontrada\n")
                break

# --- Misión de demo ---
ejecutar_agente("Calcula 15 * 4 y luego ponlo en mayúsculas con el texto 'el resultado es'")
