# Simulador de Refrigeración con CoolProp

## Descripción

Este script simula el comportamiento térmico de una cámara de refrigeración utilizando mangos como carga térmica. El programa evalúa el intercambio de calor entre la cámara, la fruta, el ambiente y el sistema de refrigeración basado en un evaporador y un condensador. Las funciones de convección y calor generado en el evaporador son modeladas usando las propiedades del refrigerante **R134A** a través de la librería **CoolProp**. Los resultados son presentados gráficamente y almacenados en archivos de texto.

## Requisitos

- Python 3.x
- Librerías necesarias:
  - CoolProp (`pip install CoolProp`)
  - Matplotlib (`pip install matplotlib`)
  - Numpy (`pip install numpy`)

## Estructura del Código

### 1. **Importación de Librerías**
   - **CoolProp**: Para obtener propiedades termodinámicas del aire y refrigerante.
   - **Matplotlib**: Para generar gráficas de los resultados.
   - **Numpy**: Para manipulación de arreglos numéricos.
   - **Datetime y OS**: Para crear y guardar archivos con la fecha y hora actual.

### 2. **Configuración del Simulador**
   - Variables como el tiempo de simulación, masa de la fruta, y la temperatura de entrada del evaporador se configuran aquí.

### 3. **Condiciones Iniciales**
   - Se definen las condiciones iniciales de la simulación, incluyendo las temperaturas del ambiente, la cámara y la fruta.

### 4. **Funciones Principales**
   - `fruit_area(mass_fruit)`: Calcula el área superficial efectiva de los mangos en función de la masa.
   - `Conv_fruit_room(T_fruit, T_room)`: Calcula el calor de convección entre la fruta y la cámara.
   - `Conv_amb_room(T_amb, T_room)`: Calcula el calor de convección entre el ambiente y la cámara.
   - `Id_T_room(...)`: Actualiza la temperatura de la cámara en función de las ganancias/pérdidas de calor.
   - `Id_T_fruit(...)`: Calcula la nueva temperatura de la fruta en función del calor intercambiado.
   - `Q_dot_evaporador(T_e, T_c)`: Calcula el calor extraído en el evaporador usando las propiedades del refrigerante **R134A**.

### 5. **Bucle Principal**
   - Realiza la simulación a través del tiempo, calculando en cada paso los calores de convección y las nuevas temperaturas tanto del aire en la cámara como de la fruta.

### 6. **Generación de Gráficas**
   - Se generan gráficas de temperatura a lo largo del tiempo para la cámara, el evaporador y la fruta, si corresponde.

### 7. **Guardado de Resultados**
   - Los resultados de la simulación se guardan en una carpeta que incluye:
     - Una imagen con las gráficas de la simulación.
     - Un archivo `.txt` que detalla las condiciones iniciales y los parámetros usados.

## Ejecución del Código

1. Configura las variables en la sección **Configuración del Simulador**.
2. Ejecuta el script.
3. Revisa los resultados generados en la carpeta creada automáticamente.

## Resultados

- El script generará gráficos que muestran cómo evolucionan las temperaturas de la cámara, fruta y evaporador con el tiempo.
- Los datos se guardarán en una carpeta con la fecha y hora de la simulación.

## Notas

- El simulador actualmente soporta un sistema de refrigeración basado en **R134A**.
- La masa de la fruta debe ser configurada en la sección inicial. Si se establece a 0 kg, el script simulará una cámara vacía.

## Ejemplo de Salida

Al ejecutar el script, se espera obtener gráficos como:
- **Temperatura en el evaporador** (°C)
- **Temperatura en la cámara** (°C)
- **Temperatura de la fruta** (°C) (si hay carga térmica).

Los resultados de la simulación se guardarán en una carpeta con el formato:  
`Intento_DD-MM-YYYY_HH-MM-SS/`.

---
