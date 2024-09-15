import CoolProp.CoolProp as CP

def cal(temperatura, presion):
    try:
        calidad = CP.PropsSI('Q', 'T', temperatura, 'P', presion, 'R134A')
        if 0 <= calidad <= 1:
            return calidad  # Retorna la calidad si está entre 0 y 1
        else:
            return None  # No está en la región de mezcla (líquido comprimido o vapor sobrecalentado)
    except ValueError:
        return None  # Si CoolProp no puede calcular la calidad, significa que no está en la región de mezcla

# Definir condiciones
temperatura = 25.65 +273.15 # Temperatura en Kelvin
presion = 4.89e5  # Presión en Pascales

# Calcular la calidad
calidad = cal(temperatura, presion)

# Mostrar resultado
if calidad is not None:
    print(f"Calidad del refrigerante R134A a T={temperatura} K y P={presion} Pa: {calidad}")
else:
    print("El refrigerante no está en la región de mezcla (líquido o vapor).")
