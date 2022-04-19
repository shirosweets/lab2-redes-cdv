
# python3 server.py -v INFO -d testGlobal

# python3 -m unittest tests/test_server.py

AUTORS = Carrizo Ernesto, Domínguez Agustín Marcelo, Vispo Valentina Solange.
NUM_LAB = 2
MAT = Redes y Sistemas Operativos - FAMAF - 2022
KILL_SERVER = lsof -i tcp:19500 | tail -n 1 | awk '{print $$2}' | xargs --no-run-if-empty kill
OTHER_KILL_SERVER = fuser -k -n tcp 19500
OTHER_KILL_SERVER_2 = ps | grep python3 | xargs kill || true

all: alltest

alltest: runServer
	@echo "---- START ALL TEST ----"
	python3 -m unittest discover -s tests/
	$(KILL_SERVER)
	@echo "---- END ALL TEST ----"

runServer:
	-@(python3 server.py -v ERROR -d testGlobal > /dev/null &)

short: runServer
	@echo "---- START SHORT TEST ----"
	python3 -m unittest tests/test_server.py
	python3 -m unittest tests/test_errors.py
	python3 -m unittest tests/test_hard.py
	-@$(KILL_SERVER) & -@$(OTHER_KILL_SERVER)
	@echo "---- END SHORT TEST ----"

autor: # Imprime el nombre de los autorres # Se usa con $ make autor # @echo silencia el echo en consola
	@echo $(AUTORS)

lab: # Imprime el número del laboratorio # Se usa con $ make lab
	@echo $(NUM_LAB)

materia: # Imprime el nombre de la materia, junto con su facultad y año # Se usa con $ make materia
	@echo $(MAT)