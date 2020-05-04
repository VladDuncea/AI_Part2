import copy


class Problema:
	def __init__(self):
		self.dim_tabla = 3
		self.date_init = [[2, 4, 3], [8, 7, 5], [1, 0, 6]]
		self.scop = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

	# calculam distanta manhattan intre pozitia placutei si pozitia din scop
	# pasi: 14
	def calc_h1(self, date):
		count = 0
		# pentru fiecare placuta(nu 0) calculeaza dist manhattan cu unde ar trebui sa fie
		for i in range(len(date)):
			for j in range(len(date[i])):
				# sari spatiul
				if date[i][j] == 0:
					continue
				# gaseste pozitia in scop
				for ii, e in enumerate(self.scop):
					for jj, ee in enumerate(e):
						if date[i][j] == ee:
							count += abs(i - ii) + abs(j-jj)
							break
		return count

	# calculam numarul de placute care nu se afla la locul corect
	# pasi: 38
	def calc_h2(self, date):
		count = 0
		# pentru fiecare placuta(nu 0) calculeaza dist manhattan cu unde ar trebui sa fie
		for i in range(len(date)):
			for j in range(len(date[i])):
				# sari spatiul
				if date[i][j] == 0:
					continue
				# gaseste pozitia in scop
				if date[i][j] != self.scop[i][j]:
					count += 1
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

	# se modifica in functie de problema
	def expandeaza(self):
		# Expandeaza nodul curent, intoarce lista de succesori
		# Construieste direct succesorii ca un nodParcurgere, pare mult mai simplu asa
		lista = []
		dim = self.problema.dim_tabla
		# cautam placuta 0
		for i, e in enumerate(self.date):
			for j, ee in enumerate(e):
				if ee == 0:
					# luam cele 4 mutari posibile
					for (ii, jj) in [[-1,0],[1,0],[0,-1],[0,1]]:
						# verificam sa fie o miscare valida
						if (i + ii) < 0 or (j + jj) <0 or (i + ii) >= dim or (j + jj) >= dim:
							continue
						# copiem configuratia
						date_nou = copy.deepcopy(self.date)
						# punem valoarea in locul lui 0
						date_nou[i][j] = date_nou[i + ii][j + jj]
						# puneam 0 in locul valorii
						date_nou[i + ii][j + jj] = 0
						# calculam noul h
						noul_h = self.problema.calc_h2(date_nou)
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


def str_simpla(lista):
	"""
		o functie folosita strict in afisari - poate fi modificata in functie de problema
	"""
	pas = 0
	sir = "\n"
	for x in lista:
		sir += "Pas" + str(pas) + ":\n"
		pas += 1
		for rand in x.date:
			for val in rand:
				sir += str(val) + " "
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
