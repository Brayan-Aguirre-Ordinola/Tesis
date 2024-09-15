def crear_separador(texto, longitud_total):
    # Convertimos el texto a mayúsculas
    texto = texto.upper()
    
    # Calculamos la longitud del separador a ambos lados del texto
    separador = '-'
    longitud_texto = len(texto)
    
    if longitud_texto >= longitud_total:
        return texto[:longitud_total]  # Si el texto es más largo que la longitud total, lo truncamos
    
    longitud_guiones = longitud_total - longitud_texto
    guiones_izquierda = longitud_guiones // 2
    guiones_derecha = longitud_guiones - guiones_izquierda
    
    # Creamos el separador con el texto centrado
    return separador * guiones_izquierda + texto + separador * guiones_derecha

# Ejemplo de uso:
separador = crear_separador("GUARDAR EL ARCHIVO", 90)
print(separador)