# EvoSim

## Integrantes

* Alejandro Yero Valdes
* Leismael Sosa Hernandez
  
## Descripción del proyecto

El proyecto consistirá en una simulación de organismos simples que pueden interactuar entre ellos y con el medio. el comportamiento de estos estará definido por una cadena genética y otras características básicas, como pueden ser el tamaño de la especie, el tiempo de vida o el costo biológico (la cantidad de nutrientes que necesita para sobrevivir), estas últimas pueden ser modificadas por la cadena de genes. Los genes de un organismos podrán ser definidos al inicio de la simulación y redefinidos luego por mutaciones o recombinación de genes entre miembros de una misma especie dependiendo de características como el tipo de reproducción y se elidirán de un conjunto predefinido. La piscina de genes la modelaremos como un grafo dirigido para simular dependencia de funcionalidades, por ejemplo, para poder diferenciar colores primero el organismo debe haber desarrollado visión. También dividiremos los genes en distintos tipos, por ejemplo mientras algunos genes pueden aportar características físicas para que el organismo interactúe con el medio, como audición o visión, otros pueden permitirle procesar información obtenida mediante estos últimos o determinar como el organismo tomara decisiones a partir de información obtenida. El objetivo del proyecto es observar el comportamiento de este tipo de sistemas y ver como se desarrollan las especies a partir de la interacción entre los organismos y el medio.

## Inteligencia Artificial

En el proyecto utilizaremos inteligencia artificial como parte de los comportamientos que pueden desarrollar los algoritmos y para intentar generar organismos que logren sobrevivir durante mas tiempo. Para esto utilizaremos algoritmos genéticos para la evolución de los organismos, en los cuales se definirá la cadena genética de cada individuo y se definirá como se reproducen y mutan los genes. También utilizaremos algoritmos de búsqueda para determinar como los organismos interactúan con el medio y como toman decisiones. Por ejemplo, para determinar como un organismo se mueve en el medio, podemos utilizar un algoritmo de búsqueda para determinar el camino mas corto entre el organismo y el alimento.

## Compilación

Para la parte de compilación diseñaremos un DSL que facilite el control de la simulación, desde el establecimiento del estado inicial, el diseño de distintos organismos, acceso sencillo a los algoritmos de inteligencia artificial que tendremos implementados y la definición de las reglas de interacción entre los organismos, asi como características del ambiente y la implementación de funciones que permitan modelar event.
