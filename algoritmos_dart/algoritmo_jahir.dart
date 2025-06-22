class Estudiante {
  final String nombre;
  final List<double> notas;

  Estudiante(this.nombre, this.notas) {
    if (notas.any((n) => n < 0 || n > 10)) {
      throw ArgumentError("Las notas deben estar entre 0 y 10.");
    }
  }

  double get promedio => notas.reduce((a, b) => a + b) / notas.length;

  String get estado => promedio >= 7 ? "Aprobado" : "Reprobado";

  String clasificacion() {
    if (promedio >= 9.0) return "Excelente";
    if (promedio >= 8.0) return "Bueno";
    if (promedio >= 7.0) return "Regular";
    return "Insuficiente";
  }
}

void main() {
  List<Estudiante> estudiantes = [
    Estudiante("Ana", [9.0, 8.5, 9.2]),
    Estudiante("Luis", [6.5, 7.0, 6.8]),
    Estudiante("María", [10.0, 9.8, 9.5]),
    Estudiante("Carlos", [5.0, 4.5, 6.0]),
  ];

  print("=== Reporte Académico ===\n");
  for (var estudiante in estudiantes) {
    print("Nombre: ${estudiante.nombre}");
    print("Notas: ${estudiante.notas.join(', ')}");
    print("Promedio: ${estudiante.promedio.toStringAsFixed(2)}");
    print("Estado: ${estudiante.estado}");
    print("Clasificación: ${estudiante.clasificacion()}");
    print("-----------------------------");
  }

  // Búsqueda por nombre
  String nombreBuscado = "Luis";
  Estudiante? buscado = buscarEstudiante(estudiantes, nombreBuscado);

  if (buscado != null) {
    print("\n🔍 Estudiante encontrado: ${buscado.nombre}");
    print("Promedio: ${buscado.promedio}");
  } else {
    print("\n Estudiante '$nombreBuscado' no encontrado.");
  }
}

Estudiante? buscarEstudiante(List<Estudiante> lista, String nombre) {
  for (var est in lista) {
    if (est.nombre.toLowerCase() == nombre.toLowerCase()) {
      return est;
    }
  }
  return null;
}
