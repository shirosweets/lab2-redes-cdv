# Laboratorio N°2

- [Laboratorio N°2](#laboratorio-n2)
- [Integrantes](#integrantes)
- [Enunciado](#enunciado)
  - [Protocolo HFTP](#protocolo-hftp)
  - [Comandos y Respuestas](#comandos-y-respuestas)
- [Entrega](#entrega)
  - [Comprendiendo el código](#comprendiendo-el-código)
  - [Comprendiendo](#comprendiendo)
  - [Implementación](#implementación)
- [Preguntas](#preguntas)
  - [Pregunta 1](#pregunta-1)
  - [Pregunta 2](#pregunta-2)
- [Nuestra forma de trabajar](#nuestra-forma-de-trabajar)

# Integrantes
- Carrizo, Ernesto.
- Domínguez, Agustín.
- Vispo, Valentina.

# Enunciado

## Protocolo HFTP
Llamaremos **Home-made File Transfer Protocol** (`HFTP`) a un protocolo de transferencia de archivos casero, creado por nosotros específicamente para este laboratorio. **HFTP** es un protocolo de capa de aplicación que usa `TCP` como protocolo de transporte. `TCP` garantiza una entrega segura, libre de errores y en orden de todas las transacciones hechas con HFTP. Un servidor de HFTP escucha pedidos en el puerto TCP 19500.

## Comandos y Respuestas
El cliente HFTP inicia el intercambio de mensajes mediante pedidos o comandos al servidor. El
servidor envía una respuesta a cada uno antes de procesar el siguiente hasta que el cliente
envía un comando de fin de conexión. En caso de que el cliente envíe varios pedidos
consecutivos, el servidor HFTP los responde en el orden en que se enviaron. El protocolo
HFTP es un protocolo ASCII, no binario, por lo que todo lo enviado (incluso archivos binarios)
será legible por humanos como strings.

- Comandos: consisten en una cadena de caracteres compuesta por elementos separados por un único espacio y terminadas con un fin de línea estilo DOS (\r\n) **(Nota 1)** . El 1 primer elemento del comando define el **tipo de acción esperada por el comando** y los elementos que siguen son **argumentos necesarios para realizar la acción**.

- Respuestas: comienzan con una cadena terminada en \r\n, y pueden tener una continuación dependiendo el comando que las origina. La cadena inicial comienza con una secuencia de dígitos (código de respuesta), seguida de un espacio, seguido de un texto describiendo el resultado de la operación. Por ejemplo, una cadena indicando un resultado exitoso tiene código `0` y con su texto descriptivo podría ser 0 OK.

**(Nota 1)**
```
Ver End of Line (EOL) en https://en.wikipedia.org/wiki/Newline:
\r = CR (Carriage Return) Usado como un carácter de nueva línea en Mac OS.
\n = LF (Line Feed) Usado como un carácter de nueva línea en Unix/Mac OS X.
\r\n = CR + LF Usado como un carácter de nueva línea en Windows/DOS y varios protocolos.
```


| Comandos | Descripción y Respuesta |
|-|-|
| `get_file_listing` | Este comando no recibe argumentos y busca obtener la lista de archivos que están actualmente disponibles. El servidor responde con una secuencia de líneas terminadas en \r\n, cada una con el nombre de uno de los archivos disponible. Una línea sin texto indica el fin de la lista. <br>Comando: <br>`get_file_listing` <br>Respuesta: <br>`0 OK\r\n` <br>`archivo1.txt\r\n` <br>`archivo2.jpg\r\n` <br> `\r\n` |
| `get_metadata FILENAME` | Este comando recibe un argumento `FILENAME` especificando un nombre de archivo del cual se pretende averiguar el tamaño **(Nota 2)** . El servidor responde con una cadena indicando su valor en bytes. <br>Comando: <br>`get_metadata archivo.txt`<br> Respuesta: <br>`0 OK\r\n ` <br>`3199\r\n` |
| `get_slice FILENAME OFFSET SIZE` | Este comando recibe en el argumento `FILENAME` el nombre de archivo del que se pretende obtener un slice o parte. La parte se especifica con un `OFFSET` (byte de inicio) y un `SIZE` (tamaño de la parte esperada, en bytes), ambos no negativos . El servidor **(Nota 3)** responde con el fragmento de archivo pedido codificado en [base64](https://es.wikipedia.org/wiki/Base64) y un `\r\n`. <br>Byte: <br>`0 5 10 15 20 25 30 35 40`<br>`v v v v v v v v v` <br>Archivo: <br>`!Que calor que hace hoy, pinta una birra!` <br>Comando **(Nota 4)**: <br>`get_slice archivo.txt 5 20` <br>Respuesta:<br> `0 OK\r\n` <br>`Y2Fsb3IgcXVlIGhhY2UgaG95LCA=\r\n`
| `quit` | Este comando no recibe argumentos y busca terminar la conexión. El servidor responde con un resultado exitoso (`0 OK`) y luego cierra la conexión. |


**(Nota 2)**
Los nombres de archivos no deberán contener espacios, de lo contrario, el protocolo no puede
diferenciar si un espacio corresponde al nombre del archivo o al comienzo de un argumento.

**(Nota 3)**
Atención que de acuerdo a la codificación [ASCII](https://es.wikipedia.org/wiki/ASCII), algunos caracteres fuera del lenguaje Inglés se representan con dos Bytes. En el archivo del ejemplo, de haber usado `¡` en lugar de `!` al
comienzo de la frase, la respuesta hubiese sido “ calor que hace hoy,” (con espacio al principio en lugar de al final) ya que el carácter `¡` ocupa dos bytes.

**(Nota 4)**
Esta es la codificación base64 de “calor que hace hoy, ”. El sentido de utilizar base64 es que al enviar el
archivo posiblemente binario, se codifica en una cadena ASCII.

En caso de algún error, el servidor responderá con códigos de respuestas diferentes a 0, más algún texto descriptivo a definir por el implementador. En particular:

* `0` La operación se realizó con éxito.
* `100` Se encontró un carácter \n fuera de un terminador de pedido \r\n.
* `101` Alguna malformación del pedido impidió procesarlo **(Nota 5)**
* `199` El servidor tuvo algún fallo interno al intentar procesar el pedido.
* `200` El comando no está en la lista de comandos aceptados.
* `201` La cantidad de argumentos no corresponde o no tienen la forma correcta.
* `202` El pedido se refiere a un archivo inexistente.
* `203` El pedido se refiere a una posición inexistente en un archivo **(Nota 6)**

Los errores con código iniciado en 1 son considerados fatales y derivan en el cierre de la conexión una vez reportados por el servidor.

Los errores que inician con 2 permiten continuar con la conexión y recibir pedidos posteriores.

**(Nota 5)**
A diferencia de los errores no fatales 200 y 201, este error es producto de alguna malformación crítica a
criterio del implementador. Por ejemplo, un comando malintencionado, de gran longitud, podría provocar
un [DoS](https://es.wikipedia.org/wiki/Ataque_de_denegaci%C3%B3n_de_servicio) o disminución de performance en el server y podría ser intervenido por un error fatal de este tipo

**(Nota 6)**
Se aplica particularmente al comando get_slice y debe generarse cuando no se cumple la condición
OFFSET + SIZE ≤ filesize.

# Entrega

## Comprendiendo el código

- `server.py`
Se encarga de aceptar y administar la conexion dada una peticion del cliente.
Este mismo llama al procedimiento que atiende las peticiones.

- `connection.py`
Atiende a los comandos dado por el cliente y devuelve una respuesta coherente con el resultado.

`directory` -> directorio virtual del usuario que se encuentra en ese momento.

## Comprendiendo

ASCII, no binario -> strings
Consecutivos: pedidos en orden, hasta que finaliza sesión

Comandos y respuetas
'response.status'+' '+'response.message'+'\r\n'

Para correr el servidor (consola 1):

```bash
python server.py
```

Para correr el cliente se debe colocar lo siguiente (consola 2):

```bash
python client.py -p 19500 -v ERROR 0.0.0.0
```
dónde 0.0.0.0 es el dominio, en este caso es lo mismo colocar 0.0.0.0 que `localhost`

## Implementación

[socket.recv](https://docs.python.org/3/library/socket.html#socket.socket.recv)

- `command.py`
Clase especializada en darle formato especifico a las consultas del cliente.

- `parser.py`
Clase encargada de realizar el analisis sintaxico de la consulta.

- `handler.py`
Clase encargada de ejecutar las consultas.

- `response_manager.py`
Clase encargada de realizar las respuestas al cliente.

- `hftp_exception.py`
Clase encargada de manejar las excepciones sobre nuestro protocolo.

# Preguntas

## Pregunta 1
> ¿Qué estrategias existen para poder implementar este mismo servidor pero con
capacidad de atender múltiples clientes simultáneamente? Investigue y responda
brevemente qué cambios serían necesario en el diseño del código.

Hay 3 maneras naturales de resolver este problema:

**Con procesos hijos (forks)**

Crear procesos hijos que atiendan a los diferentes clientes, esta manera genera mucha sobrecarga debido a que por cada cliente existirá un nuevo proceso que ocupa los mismos recursos que el proceso padre. Se puede utilizar la libreria `os` para crear procesos hijos. Este metodo no es escalable.

**Con hilos de ejecución (threads)**

La idea seria lanzar hilos de ejecución donde cada uno responde a un cliente en particular. Existen librerías que proveen estas abstracciones en Python, como `threading`, `subprocess`, `_threads`, etc. Este método es menos costoso que la idea de forks debido a que usa los recursos del único proceso corriendo.

**Con Corrutinas**

De la misma forma se podría manejar las distintas ejecuciones con corrutinas, donde cada corrutina maneja una conexión. Esto tendría el beneficio de solo manejarse en un thread, lo cual ahorraría aún más los recursos. La desventaja que tiene este método es que el manejo de control con corrutinas combinado con los sockets puede ser más complejo que como se manjea con threads. Esta complejidad no vale la pena a menos que sean muchos clientes para manejar concurrentemente.

## Pregunta 2
> Pruebe ejecutar el servidor en una máquina del laboratorio, mientras utiliza el cliente desde otra, hacia la ip de la máquina servidor. ¿Qué diferencia hay si se corre el servidor desde la IP “`localhost`”, “`127.0.0.1`” o la ip “`0.0.0.0`”?

Tanto "`localhost`" y "`127.0.0.1`" refieren a la misma dirección de IP, se utiliza para crear una conexión con la misma computadora.
"`0.0.0.0`" es un caso particular donde se utiliza como "ninguna dirección en particular". El valor de esta dirección dependerá del contexto en que se use.

# Importante
Para correr todos los test es necesario levantar el servidor con el siguiente comando:

```bash
python3 server.py -v INFO -d testGlobal
```

La parte importante es que la verbosidad esté puesta como `INFO`. Si está puesta como `DEBUG`, se crea un cuello de botella en la consola, ya que intenta escribir múltiples veces cada byte del filename y tarda más tiempo haciendo eso que manejando el pedido por socket. Este cuello de botella es tan notable que termina lanzando el Timeout del socket, y así fallando el test.

También tener en cuenta que el directorio de los test es *testGlobal*, mientras que el default del server es *testdata*, por lo que es importante que el servidor esté sirviendo el directorio *testGlobal*.

Cambiamos la carpeta que se utiliza para los test porque como este los eliminaba dificultaba la disponibilidad de los archivos al levantar el servidor.
En `tests/test_base.py` se encuentra el código con la varible `DATADIR` que hace referencia a la carpeta para los test.

# Nuestra forma de trabajar

Los commits que empiezan con *"Pair Programming"* son aquellos commits que fueron realizados de manera conjunta remota, mientras que los commits realizados por el usuario *"Visita"* son aquellos commits que fueron realizados de manera conjunta presencial durante el horario del laboratorio.

Cuando se realizan cambios individuales se van a realizar **Pull Request** a la branch principal (`master`).

## Modificaciones a los test

### Separación

Ya que algunos de los test (`big_file`, `big_filename`, `command_in_pieces`) tardaban considerablamente bastante en comparación con los demás, y para el debuggeo sería mejor aislar los test, **separamos** la suite de test en diferentes archivos para poder correrlos individualmente.

Para correrlos a todos como antes se puede levantar el server en una consola y correr:

```bash
python -m unittest discover -s tests
```

O simplemente correr el comando

```bash
make
```

ya que hicimos un **Makefile** que automáticamente levantar el server y corre todos los test.

También está

```bash
make short
```

para correr los tests que se ejecutan muy rápido

### Cambios individuales

Se modificaron dos test de manera superficial. Primero `test_multiple_commands` donde una variable llamada `len` generaba problemas ya que len es una función ya de la librería de Python.

```python
     def test_multiple_commands(self):
         client = self.new_client()
-        len = client.s.send(
+        socket_message_len = client.s.send(
             'get_file_listing\r\nget_file_listing\r\n'.encode("ascii"))
-        assert len == len(
+        assert socket_message_len == len(
             'get_file_listing\r\nget_file_listing\r\n'.encode("ascii"))
         status, message = client.read_response_line(TIMEOUT)
```

y otro fue acortar un poco el largo del filename

```python
    def test_big_filename(self):
        c = self.new_client()
-       c.send('get_metadata ' + 'x' * (5 * 2 ** 20), timeout=120)
+       c.send('get_metadata ' + 'x' * (5 * 2 ** 12), timeout=120)
        # Le damos 4 minutos a esto
        status, message = c.read_response_line(TIMEOUT * 6)
```

ya que conceptualmente testean lo mismo solo que una tarda muchísimo más tiempo que la otra.

---

## PEP8

[PEP8](https://peps.python.org/pep-0008/) es una guía que indica las convenciones estilísticas a seguir para escribir código Python. Se trata de un conjunto de recomendaciones cuyo objetivo es ayudar a escribir código más legible y abarca desde cómo nombrar variables, al número máximo de caracteres que una línea debe tener.

**Comando para corroborar que se cumpla PEP8**

```bash
pycodestyle .
```

# Puertos

## Cómo ubicar un puerto de escucha

```bash
sudo ss -tulwn | grep LISTEN
```

o

```bash
sudo lsof -t -i:19500
```

o

```bash
fuser -n tcp 19500
```


## Cómo cerrar un puerto

Durante la implementación del laboratorio se nos presentó el problema de que cuando se cerraba el servidor de manera correcta el socket permanece reservado por el OS. Utilizábamos los siguientes comandos para cerrar el puerto:

```bash
sudo kill $(sudo lsof -t -i:19500)
```

o

```bash
fuser -k -n tcp 19500
```

Pero aún así hay que esperar un tiempo para que el OS devuelva el socket (5s a 1min).

> https://poesiabinaria.net/2017/07/cerrar-puerto-tcp-ocupado-una-aplicacion-gnulinux/

# Implementaciones

- [x] Manejador de excepciones propias.
- [x] Configuración del logger del lado del server con distintos niveles.
- [x] Implementación de un buffer del lado del parser para optimizar el uso del socket.
- [x] Manejo de múltiples clientes concurrentes por medio del uso de threads.
