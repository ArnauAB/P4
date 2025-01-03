PAV - P4: reconocimiento y verificación del locutor
===================================================

Obtenga su copia del repositorio de la práctica accediendo a [Práctica 4](https://github.com/albino-pav/P4)
y pulsando sobre el botón `Fork` situado en la esquina superior derecha. A continuación, siga las
instrucciones de la [Práctica 2](https://github.com/albino-pav/P2) para crear una rama con el apellido de
los integrantes del grupo de prácticas, dar de alta al resto de integrantes como colaboradores del proyecto
y crear la copias locales del repositorio.

También debe descomprimir, en el directorio `PAV/P4`, el fichero [db_8mu.tgz](https://atenea.upc.edu/mod/resource/view.php?id=3654387?forcedownload=1)
con la base de datos oral que se utilizará en la parte experimental de la práctica.

Como entrega deberá realizar un *pull request* con el contenido de su copia del repositorio. Recuerde
que los ficheros entregados deberán estar en condiciones de ser ejecutados con sólo ejecutar:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~.sh
  make release
  run_spkid mfcc train test classerr verify verifyerr
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recuerde que, además de los trabajos indicados en esta parte básica, también deberá realizar un proyecto
de ampliación, del cual deberá subir una memoria explicativa a Atenea y los ficheros correspondientes al
repositorio de la práctica.

A modo de memoria de la parte básica, complete, en este mismo documento y usando el formato *markdown*, los
ejercicios indicados.

## Ejercicios.

### SPTK, Sox y los scripts de extracción de características.

- Analice el script `wav2lp.sh` y explique la misión de los distintos comandos involucrados en el *pipeline*
  principal (`sox`, `$X2X`, `$FRAME`, `$WINDOW` y `$LPC`). Explique el significado de cada una de las 
  opciones empleadas y de sus valores.
> `sox`: El comando sox sirve para realizar múltiples tareas sobre un fichero de audio, como cambiar su formato, y realizar operaciones de procesado de señal (transformada o reducción de ruido por ejemplo). En nuestro caso, lo usaremos para transformar el fichero WAV raw a un stream de int16.
>
> `$X2X`: Programa de SPTK que permite la conversión entre distintos formatos de datos. En nuestro caso, convierte el stream de formato int16 a float32.
>
> `$FRAME`: Sirve para dividir la señal en tramas y extraer frame a frame toda una secuencia. En nuestro caso, hemos elegido tramas de longitud 240 (-l 240) y con un periodo de 80 (-p 80).
>
> `$WINDOW`: Enventana los datos extraidos anteriormente (mantiene la longitud de 240 muestras), usa la ventana de Hamming por defecto si no se define de otra manera.
>
> `$LPC`: Calcula los `-m` coeficientes (orden **$lpc_order**) LPC de cada frame (240 muestras).  

- Explique el procedimiento seguido para obtener un fichero de formato *fmatrix* a partir de los ficheros de
  salida de SPTK (líneas 49 a 55 del script `wav2lp.sh`).
> Calculamos el numero de columnas según el orden de predicción lineal que usamos (lpc_order+1), y el de filas según las líneas del fichero de salida entre el número de columnas. Luego generamos un archivo con las dimensiones calculadas y luego agregamos los coeficientes LPC calculados anteriormente al archivo.

  * ¿Por qué es más conveniente el formato *fmatrix* que el SPTK?
> Utilizando el formato fmatrix podemos transformar nuestro vector de entrada a matriz, teniendo un rápido acceso a los datos de nuestra señal. Además, su cabecera ofrece información sobre número de tramas y coeficientes calculados.

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales de predicción lineal
  (LPCC) en su fichero <code>scripts/wav2lpcc.sh</code>:
> ```bash
> sox $inputfile -t raw -e signed -b 16 - |
>     $X2X +sf |
>     $FRAME -l 240 -p 80 |
>     $WINDOW -l 240 -L 240 |
>     $LPC -l 240 -m $lpc_order |
>     $LPCC -m $lpc_order -M $lpcc_order > $base.lpcc || exit 1
> ```

- Escriba el *pipeline* principal usado para calcular los coeficientes cepstrales en escala Mel (MFCC) en su
  fichero <code>scripts/wav2mfcc.sh</code>:
> ```bash
> sox $inputfile -t raw -e signed -b 16 - |
>     $X2X +sf |
>     $FRAME -l 240 -p 80 |
>     $WINDOW -l 240 -L 240 |
>     $MFCC -w 1 -s 8 -l 240 -m $mfcc_order -n $mfcc_banks > $base.mfcc || exit 1
> ```

### Extracción de características.

- Inserte una imagen mostrando la dependencia entre los coeficientes 2 y 3 de las tres parametrizaciones
  para todas las señales de un locutor.
  
  **LP:**  
  
  ![image](https://github.com/user-attachments/assets/3e3c4808-9f3d-40e8-adfe-d61a6c36e7e3)


  **LPCC:**  
  
  ![image](https://github.com/user-attachments/assets/fbe9d3f5-7956-49c7-9631-d6daf0dd6209)


  **MFCC:**  
  
  ![image](https://github.com/user-attachments/assets/cd7cc866-5707-4632-b830-1ea70bc40f0f)



  + Indique **todas** las órdenes necesarias para obtener las gráficas a partir de las señales 
    parametrizadas.
    > Empezamos ejecutando el programa run_spkid para las 3 parametrizaciones (lp,lpcc,mfcc) y después generamos los ficheros de texto:
    > 
    > ![image](https://github.com/user-attachments/assets/8d0c3f22-16d9-420c-abc0-6b86a0f7636d)
    >
    > Finalmente, mostramos por pantalla los diferentes tipos de predicción usando MATLAB:
    > 
    > ![image](https://github.com/user-attachments/assets/d695217c-eb44-4e77-9c49-acc0dd66c7bd)


  + ¿Cuál de ellas le parece que contiene más información?
    > Cuanto más incorrelados estén los coeficientes, más separados estarán los puntos en las gráficas, esos son los casos que nos proporcionan más información. Podemos deducir entonces mirando las gráficas que la de mfcc y lpcc tendrán significativamente más información que la de lp, debido a que tiene más dependencia, como vemos en su gráfica donde sus puntos se alinean sobre el eje diagonal.  
    
- Usando el programa <code>pearson</code>, obtenga los coeficientes de correlación normalizada entre los
  parámetros 2 y 3 para un locutor, y rellene la tabla siguiente con los valores obtenidos.

  |                        | LP        | LPCC      | MFCC       |
  |------------------------|:---------:|:---------:|:----------:|
  | &rho;<sub>x</sub>[2,3] | -0.692576 | -0.170836 | -0.0504945 |
  
  + Compare los resultados de <code>pearson</code> con los obtenidos gráficamente.
    
  > Efectivamente comprobamos (analizando los resultados en valor absoluto) que LP es la más incorrelada de los 3 tipos de predicción ya que su valor es el más alto y sus puntos parecían una recta con pendiente negativo, de ahí que su coeficiente de correlación sea negativo. Por otro lado, confirmamos también la baja correlación de los otros dos tipos LPCC y MFCC, viendo numéricamente que MFCC es más incorrelado aún que LPCC.
  
- Según la teoría, ¿qué parámetros considera adecuados para el cálculo de los coeficientes LPCC y MFCC?

> Se suele considerar adecuado escoger alrededor de 12-16 coeficientes para ambos LPCC y MFCC. Para MFCC, además, se suelen usar entre 20-40 filtros en la escala Mel, buscando un equilibrio entre la resolución en esta escala y el coste computacional necesario para ello. 

### Entrenamiento y visualización de los GMM.

Complete el código necesario para entrenar modelos GMM.

- Inserte una gráfica que muestre la función de densidad de probabilidad modelada por el GMM de un locutor
  para sus dos primeros coeficientes de MFCC.

- Inserte una gráfica que permita comparar los modelos y poblaciones de dos locutores distintos (la gŕafica
  de la página 20 del enunciado puede servirle de referencia del resultado deseado). Analice la capacidad
  del modelado GMM para diferenciar las señales de uno y otro.

### Reconocimiento del locutor.

Complete el código necesario para realizar reconociminto del locutor y optimice sus parámetros.

- Inserte una tabla con la tasa de error obtenida en el reconocimiento de los locutores de la base de datos
  SPEECON usando su mejor sistema de reconocimiento para los parámetros LP, LPCC y MFCC.

### Verificación del locutor.

Complete el código necesario para realizar verificación del locutor y optimice sus parámetros.

- Inserte una tabla con el *score* obtenido con su mejor sistema de verificación del locutor en la tarea
  de verificación de SPEECON. La tabla debe incluir el umbral óptimo, el número de falsas alarmas y de
  pérdidas, y el score obtenido usando la parametrización que mejor resultado le hubiera dado en la tarea
  de reconocimiento.
 
### Test final

- Adjunte, en el repositorio de la práctica, los ficheros `class_test.log` y `verif_test.log` 
  correspondientes a la evaluación *ciega* final.

### Trabajo de ampliación.

- Recuerde enviar a Atenea un fichero en formato zip o tgz con la memoria (en formato PDF) con el trabajo 
  realizado como ampliación, así como los ficheros `class_ampl.log` y/o `verif_ampl.log`, obtenidos como 
  resultado del mismo.
