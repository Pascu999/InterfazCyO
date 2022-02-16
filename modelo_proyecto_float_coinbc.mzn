include "globals.mzn";

% Parámetros del modelo
int: n;
int: m;
array[1..m, 1..2] of 0..n: ciudades;

% Manhattan
function var float: manhattan(int: x1, int: y1, var float: x2, var float: y2) = abs(x1 - x2) + abs(y1 - y2);

% Coordenadas basurero
var 0.0..n: x;
var 0.0..n: y;

% Distancias
array[1..m] of var 0.0..2*n: distancias;
var float: min_distancia = min(distancias);

% Restricciones


constraint forall(i in 1..m) (distancias[i] = manhattan(ciudades[i,1], ciudades[i,2], x, y));

constraint forall(i in 1..m) (x = ciudades[i,1] -> y != ciudades[i,2]);

solve maximize min_distancia;

output ["x = \(show_float(1,1,x)) \ny = \(show_float(1,1,y))\nDistancia = \(show_float(1,1,min_distancia))"]
