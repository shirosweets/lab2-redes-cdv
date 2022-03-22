# Laboratorio N°2

# Integrantes

# Comprendiendo el código

- `server.py`

`directory` -> directorio virtual del usuario que se encuentra en ese momento. 

# Comprendiendo

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

# Preguntas
1. ¿Qué estrategias existen para poder implementar este mismo servidor pero con
capacidad de atender múltiples clientes simultáneamente? Investigue y responda
brevemente qué cambios serían necesario en el diseño del código.
2. Pruebe ejecutar el servidor en una máquina del laboratorio, mientras utiliza el cliente
desde otra, hacia la ip de la máquina servidor. ¿Qué diferencia hay si se corre el
servidor desde la IP “localhost”, “127.0.0.1” o la ip “0.0.0.0”?