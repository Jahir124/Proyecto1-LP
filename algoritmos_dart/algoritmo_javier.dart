// Algoritmo de búsqueda con estadísticas básicas 
class Analizador { 
  List<int> datos; 
  Map<String, dynamic> resumen; 

  Analizador(this.datos) { 
    resumen = {"min": 0, "max": 0, "promedio": 0.0, "existe": false}; 
  } 

  int busquedaBinaria(int objetivo) { 
    int ini = 0, fin = datos.length - 1; 
    while (ini <= fin) { 
      int mid = (ini + fin) ~/ 2; 
      if (datos[mid] == objetivo) { 
        resumen["existe"] = true; 
        return mid; 
      } else if (datos[mid] < objetivo) { 
        ini = mid + 1; 
      } else { 
        fin = mid - 1; 
      } 
    } 
    return -1; 
  } 

  void calcularResumen() { 
    int suma = 0, min = datos[0], max = datos[0]; 
    for (int val in datos) { 
      suma += val; 
      if (val < min) min = val; 
      if (val > max) max = val; 
    } 
    resumen["min"] = min; 
    resumen["max"] = max; 
    resumen["promedio"] = suma / datos.length; 
  } 

  void mostrarResumen() { 
    print("Resumen:"); 
    print("Min: ${resumen["min"]}, Max: ${resumen["max"]}, Promedio: ${resumen["promedio"]}"); 
    print("Elemento buscado existe: ${resumen["existe"]}"); 
  } 
} 

void main() { 
  List<int> lista = [3, 6, 8, 12, 15, 20]; 
  int objetivo = 12; 
  var analizador = Analizador(lista); 
  int pos = analizador.busquedaBinaria(objetivo); 
  analizador.calcularResumen(); 
  if (pos != -1) { 
    print("Elemento encontrado en posición $pos"); 
  } else { 
    print("Elemento no encontrado"); 
  } 
  analizador.mostrarResumen(); 
  var entrada = 2.34;
}