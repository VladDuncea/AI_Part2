import copy


# ASTA SE MODIFICA IN FUNCTIE DE PROBLEMA
class Problema:

	def __init__(self):
		self.date_init = [['a'], ['c', 'b'], ['d']]
		self.scop = [['b', 'c'], [], ['d', 'a']]

	# numarul de blocuri diferite
	# pasi: 4
	def calc_h1(self, date):
		count = 0
		for i in range(len(date)):
			for j in range(len(date[i])):
				if j < len(self.scop[i]):
					if date[i][j] != self.scop[i][j]:
						count += 1
				else:
					count += 1
		return count

	# numarul de stive diferite
	# pasi: 6
	def calc_h2(self, date):
		count = 0
		for i in range(len(date)):
			for j in range(len(date[i])):
				# daca avem o diferenta o contorizam si trecem la urmatoarea stiva
				if j < len(self.scop[i]):
					if date[i][j] != self.scop[i][j]:
						count += 1
						break
				else:
					count += 1
					break
		return count
# Sfarsit definire problema

# Clase folosite in algoritmul A*


class NodParcurgere:
	"""O clasa care cuprinde informatiile asociate unui nod din listele open/closed
		Cuprinde o referinta catre nodul in sine (din graf)
		dar are ca proprietati si valorile specifice algoritmului A* (f si g). 
		Se presupune ca h este proprietate a nodului din graf
	"""
	problema = None		# atribut al clasei

	def __init__(self, date, parinte=None, g=0, f=float("inf")):
		self.date = date
		self.parinte = parinte		# obiect de tip NodParcurgere
		self.g = g					# costul drumului de la radacina pana la nodul curent
		self.f = f

	def drum_arbore(self):
		"""Functie care calculeaza drumul asociat unui nod din arborele de cautare.
			Functia merge din parinte in parinte pana ajunge la radacina"""
		nod_c = self
		drum = [nod_c]
		while nod_c.parinte is not None:
			drum = [nod_c.parinte] + drum
			nod_c = nod_c.parinte
		return drum

	def contine_in_drum(self, nod_parc):
		# Verifica NodParcurgere cu NodParcurgere
		nod_c = self
		while nod_c is not None:
			if nod_c.date == nod_parc.date:
				return True
			nod_c = nod_c.parinte
		return False

	# ASTA SE MODIFICA IN FUNCTIE DE PROBLEMA
	def expandeaza(self):
		# Expandeaza nodul curent, intoarce lista de succesori
		# Construieste direct succesorii ca un nodParcurgere, pare mult mai simplu asa
		lista = []
		nr_stive = len(self.date)
		for i in range(nr_stive):
			if len(self.date[i]) > 0:
				for j in range(nr_stive):
					# sari peste aceeasi stiva
					if j == i:
						continue
					# copiam vechea stare
					date_nou = copy.deepcopy(self.date)
					# luam cubul
					val = date_nou[i].pop()
					# il punem in noua stiva
					date_nou[j].append(val)
					# calculam noul h
					noul_h = self.problema.calc_h1(date_nou)
					# construim nodul
					lista = lista + [NodParcurgere(date_nou, self, self.g + 1, self.g + 1 + noul_h)]
		return lista

	# se modifica in functie de problema
	def test_scop(self):
		return self.date == self.problema.scop

	def __str__(self):
		parinte = self.parinte if self.parinte is None else self.parinte.date
		return f"({self.date}, parinte={parinte}, f={self.f}, g={self.g})"


# Algoritmul A*
def str_info_noduri(lista):
	"""
		o functie folosita strict in afisari - poate fi modificata in functie de problema
	"""
	sir = "["
	for x in lista:
		sir += str(x)+"  "
	sir += "]"
	return sir


# ASTA SE MODIFICA IN FUNCTIE DE PROBLEMA
def str_simpla(lista):
	"""
		o functie folosita strict in afisari - poate fi modificata in functie de problema
	"""
	pas = 0
	sir = "\n"
	for x in lista:
		# afiseaza pasul, pasul 0 e ca avem dat
		sir += "Pas" + str(pas)+":\n"
		pas += 1
		# gaseste adancimea maxima
		maxx = 0
		for stiva in x.date:
			if len(stiva) > maxx:
				maxx = len(stiva)

		# afiseaza rand cu rand
		for i in range(maxx-1, -1, -1):
			for stiva in x.date:
				if len(stiva) > i:
					sir += str(stiva[i])
				else:
					sir += "-"
				sir += " "
			sir += "\n"
		sir += "\n"
	return sir


def afis_succesori_cost(lista):
	"""
		o functie folosita strict in afisari - poate fi modificata in functie de problema
	"""
	sir = ""
	for (x, cost) in lista:
		sir += "\nnod: " + str(x) + ", cost arc:" + str(cost)
	
	return sir


def in_lista(lista, nod_parc):
	"""
	lista "l" contine obiecte de tip NodParcurgere
	"nod" este de tip Nod
	"""
	for i in range(len(lista)):
		if lista[i].date == nod_parc.date:
			return lista[i]
	return None


def a_star():
	# contor pt pasi, pentru statistici
	pasi = 0
	rad_arbore = NodParcurgere(NodParcurgere.problema.date_init)
	lopen = [rad_arbore]		# open va contine elemente de tip NodParcurgere
	lclosed = []				# closed va contine elemente de tip NodParcurgere
	nod_curent = None
	while len(lopen) != 0:
		nod_curent = lopen[0]
		pasi += 1
		lclosed.append(nod_curent)
		if nod_curent.test_scop():
			break	  # am gasit cel mai bun drum
		lopen.remove(nod_curent)
		succesori = nod_curent.expandeaza()
		for s in succesori:
			nod_nou = None

			# daca apartine drumului sarim peste
			if nod_curent.contine_in_drum(s):
				continue

			# verificam daca apare in lopen
			aux = in_lista(lopen, s)
			if aux is not None:
				if aux.f > s.f:
					# nodul exista in open dar am gasit o valoare mai buna
					lopen.remove(aux)
					nod_nou = s
			else:
				# nu am gasit in open, cautam in closed
				aux = in_lista(lclosed, s)
				if aux is not None:
					# nodul exista in closed dar am gasit o valoare mai buna
					if aux.f > s.f:
						lclosed.remove(aux)
						nod_nou = s
				else:
					# nu e nici in open nici in closed
					nod_nou = s

			if nod_nou is not None:
				lopen.append(nod_nou)
		lopen.sort(key=lambda x: (x.f, -x.g))

	print("\n------------------ Concluzie -----------------------")
	if len(lopen) == 0:
		print("Lista open e vida, nu avem drum de la nodul start la nodul scop")
	else:
		print("Drum de cost minim: " + str_simpla(nod_curent.drum_arbore()))
		print("Numar de pasi incercati: " + str(pasi))
	

if __name__ == "__main__":
	problema = Problema()
	NodParcurgere.problema = problema
	a_star()
