# Convertir número decimal a formato IEE 754 de 32 bits.
# David Alejandro Puga Novoa
# GR2CC
def decimal_a_binario(decimal):
    signo = '0' if decimal > 0 else '1'
    decimal = abs(decimal)
    parte_entera = int(decimal)
    parte_fraccionaria = decimal - parte_entera

    # Convertir parte entera a binario
    binario_entero = ''
    if parte_entera == 0:
        binario_entero = '0'
    while parte_entera > 0:
        binario_entero = str(parte_entera % 2) + binario_entero
        parte_entera = parte_entera // 2

    # Convertir parte fraccionaria a binario
    binario_fraccionario = ''
    while parte_fraccionaria > 0:
        parte_fraccionaria *= 2
        if parte_fraccionaria >= 1:
            binario_fraccionario += '1'
            parte_fraccionaria -= 1
        else:
            binario_fraccionario += '0'
        if len(binario_fraccionario) > 23:  # IEEE 754 mantisa tiene 23 bits
            break

    binario = binario_entero + '.' + binario_fraccionario
    return signo, binario

def normalizar_binario(binario):
    if '.' not in binario:
        binario += '.0'
    
    parte_entera, parte_fraccionaria = binario.split('.')
    if '1' in parte_entera:
        exponente = len(parte_entera) - 1
        mantisa = parte_entera[1:] + parte_fraccionaria
    else:
        exponente = -parte_fraccionaria.find('1') - 1
        mantisa = parte_fraccionaria[parte_fraccionaria.find('1') + 1:]

    return exponente, mantisa

def obtener_exponente_y_mantisa(binario):
    exponente, mantisa = normalizar_binario(binario)
    sesgo_exponente = exponente + 127  # Sesgo para 32 bits
    mantisa = mantisa[:23].ljust(23, '0')  # Mantisa de 23 bits
    return exponente, sesgo_exponente, mantisa

def decimal_a_ieee754(decimal):
    signo, binario = decimal_a_binario(decimal)
    exponente, sesgo_exponente, mantisa = obtener_exponente_y_mantisa(binario)
    
    bit_signo = signo
    bits_exponente = f"{sesgo_exponente:08b}"
    bits_mantisa = mantisa
    
    ieee754 = f"{bit_signo}{bits_exponente}{bits_mantisa}"
    return signo, binario, exponente, sesgo_exponente, bits_exponente, bits_mantisa, ieee754

def main():
    decimal = float(input("Introduce un número decimal (positivo o negativo): "))
    if decimal == 0:
        print(f"IEE 754 completo: 00000000000000000000000000000000")
    else:
        signo, binario, exponente, sesgo_exponente, bits_exponente, bits_mantisa, ieee754 = decimal_a_ieee754(decimal)
        hexadecimal = hex(int(ieee754, 2))
        print(f"Decimal: {decimal}")
        print(f"Número en binario (sin signo): {binario}")
        print(f"Representación IEEE 754:")
        print(f"  Signo: {signo}")
        print(f"  Exponente (sin sesgo): {exponente}")
        print(f"  Sesgo del exponente (decimal): {sesgo_exponente}")
        print(f"  Sesgo del exponente (binario): {bits_exponente}")
        print(f"  Mantisa: {bits_mantisa}")
        print(f"  IEEE 754 completo: {ieee754}")
        print(f"Equivalente hexadecimal: {hexadecimal}")

if __name__ == "__main__":
    main()