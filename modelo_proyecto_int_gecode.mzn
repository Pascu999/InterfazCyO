include "globals.mzn";

% Parámetros del modelo
int: n;
int: m;
array[1..m, 1..2] of 0..n: ciudades;
int: precision = 1000;

% Manhattan
function var int: manhattan(var int: x1, var int: y1, var int: x2, var int: y2) = abs(x1 - x2) + abs(y1 - y2);

% Coordenadas basurero
var 0..n*precision: x;
var 0..n*precision: y;

% Distancias
array[1..m] of var 0..2*n*precision: distancias;
var int: min_distancia = min(distancias);

% Restricciones

array[1..m, 1..2] of var int: ciudades_m;
constraint forall(i in 1..m, j in 1..2) (ciudades_m[i,j] = ciudades[i,j] * precision);


constraint forall(i in 1..m) (distancias[i] = manhattan(ciudades_m[i,1], ciudades_m[i,2], x, y));
  
constraint forall(i in 1..m) (x = ciudades_m[i,1] -> y != ciudades_m[i,2]);

solve maximize min_distancia / precision;

output ["x = \(x / precision) \ny = \(y / precision)\nDistancia = \(min_distancia / precision)"]