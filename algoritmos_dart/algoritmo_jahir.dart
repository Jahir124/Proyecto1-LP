int binarySearch(List<int> listIntegers, int target) {
 int start = 0;
 int end = listIntegers.length - 1;
 while (start <= end) {
 int half = (start + end) ~/ 2; // ~/ It's integer division
 if (listIntegers[half] == target) {
 return half; // Found, return the index
 } else if (listIntegers[medio] < target) {
 start = half + 1;
 } else {
 end = half - 1;
 }
 }
 return -1; // Not found
