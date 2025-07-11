// Algoritmo de búsqueda con estadísticas básicas 
class Analizador { 
  Set<int> datos; 

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

  void probarReglas() { 
    Set<int> numeros = {1, 2, 3};
    var conjunto = {true, false};
    Set<String> palabras = {"hola", "mundo"};
    Set<double> vacio = {true, 1};
    var suma = 1 + 2;
    double o = 1.2;
    int retorn() {
      return 1;  
    }
    int i = 0;
    while (i < 3) {
      print(i);
      i++;
    }
  } 

  Map<String, dynamic> resumen;
} 

void main() { 
  Set<int> lista = {3, 6, 8, 12, 15, 20}; 
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