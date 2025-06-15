void main() {
  List<String?> pruebas = [
    "Anita lava la tina",
    "¿Acaso hubo búhos acá?",
    "No es palindromo",
    "",
    null,
  ];
  for (var texto in pruebas) {
    try {
      bool es = esPalindromo(texto);
      print('"$texto" ${es ? "es" : "no es"} un palíndromo.');
    } catch (e) {
      print('Error con entrada "$texto": $e');
    }
  }
}

bool esPalindromo(String? input) {
  if (input == null) throw ArgumentError("El texto no puede ser null");
  if (input.trim().isEmpty) throw FormatException("Cadena vacía no válida");
  final String procesado = input.toLowerCase().replaceAll(
    RegExp(r'[^a-z0-9]'),
    '',
  );
  int izquierda = 0;
  int derecha = procesado.length - 1;
  while (izquierda < derecha) {
    if (procesado[izquierda] != procesado[derecha]) {
      return false;
    }
    izquierda++;
    derecha--;
  }
  return true;
}
