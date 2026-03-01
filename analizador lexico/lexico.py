import re

class AnalizadorLexico:
    tabla_tokens = {}

    palabras_reservadas = {
        "if", "else", "while", "for", "int", "float", "double", "string", "return"
    }

    @staticmethod
    def leer_archivo():
        ubicacion = input("Ingrese Archivo: ")
        try:
            with open(ubicacion, 'r', encoding='utf-8') as archivo:
                return archivo.read()
        except FileNotFoundError:
            print("Archivo no encontrado.")
            return ""

    @staticmethod
    def obtener_token(lexema):
        if lexema in AnalizadorLexico.palabras_reservadas:
            return "PALABRA_RESERVADA"

        if re.match(r'^".*"$', lexema):
            return "CADENA"

        if re.match(r'^\d+$', lexema):
            return "NUM_ENTERO"

        if re.match(r'^\d+\.\d+$', lexema):
            return "NUM_REAL"

        if re.match(r'^[a-zA-Z_]\w*$', lexema):
            return "IDENTIFICADOR"
        operadores = {
            "=": "OP_ASIGNACION", "+": "OP_SUMA", "-": "OP_RESTA",
            "*": "OP_MULTIPLICACION", "/": "OP_DIVISION", "<": "OP_MENOR",
            ">": "OP_MAYOR", "<=": "OP_MENOR_IGUAL", ">=": "OP_MAYOR_IGUAL",
            "==": "OP_IGUAL", "!=": "OP_DIFERENTE", ";": "PUNTO_COMA",
            "(": "PARENTESIS_ABRE", ")": "PARENTESIS_CIERRA",
            "{": "LLAVE_ABRE", "}": "LLAVE_CIERRA"
        }
        return operadores.get(lexema, "TOKEN_DESCONOCIDO")

    @classmethod
    def analizar(cls, codigo):
        codigo = re.sub(r'//.*', '', codigo)
        codigo = re.sub(r'/\*[\s\S]*?\*/', '', codigo)

        patron = r'".*?"|(<=|>=|==|!=|[{}();=+\-*/<>])|\b\d+(\.\d+)?\b|\b[a-zA-Z_]\w*\b'
        
        coincidencias = re.finditer(patron, codigo)

        for match in coincidencias:
            lexema = match.group(0)
            if lexema and lexema not in cls.tabla_tokens:
                cls.tabla_tokens[lexema] = cls.obtener_token(lexema)

    @classmethod
    def mostrar_tabla(cls):
        print("\nTABLA LEXEMA | TOKEN\n")
        for lexema, token in cls.tabla_tokens.items():
            print(f"{lexema:15} | {token}")

if __name__ == "__main__":
    analizador = AnalizadorLexico()
    contenido = analizador.leer_archivo()
    
    if contenido:
        analizador.analizar(contenido)
        analizador.mostrar_tabla()