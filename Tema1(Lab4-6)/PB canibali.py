import copy
import time

class Problema:
	def __init__(self):
		self.N = 3
		self.M = 2
		# (nr_can_vest, nr_mis_vest, nr_can_est, nr_mis_est, mal_unde_e_barca)
		self.date_init = [0, 0, self.N, self.N, 'est']
		self.scop = [self.N, self.N, 0, 0, 'vest']

	# nr de oameni pe malul de est /(M-1)
	# timp 0.001
	def calc_h(self, date):
		count = (date[2] + date[3]) // (self.M - 1)
		return count


# Sfarsit definire problema

# Clase folosite in algoritmul A*


class NodParcurgere:
	"""O clasa care cuprinde informatiile asociate unui nod din listele open/closed
		Cuprinde o referinta catre nodul in sine (din graf)
		dar are ca proprietati si valorile specifice algoritmului A* (f si g).
		Se presupune ca h este proprietate a nodului din graf
	"""
	problema = None  # atribut al clasei

	def __init__(self, date, parinte=None, g=0, f=float("inf")):
		self.date = date
		self.parinte = parinte  # obiect de tip NodParcurgere
		self.g = g  # costul drumului de la radacina pana la nodul curent
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
		m = self.problema.M

		# cauta malul curent
		if self.date[4] == 'est':
			poz_cur = 2
			poz_noua = 0
		else:
			poz_cur = 0
			poz_noua = 2

		# luam toate posibilitatile de combinatii de oameni de pe malul curent
		for CAN in range(self.date[poz_cur]+1):
			for MIS in range(self.date[poz_cur + 1]+1):
				# aplicam regulile barcii
				if (MIS + CAN == 0) or (MIS + CAN) > m:
					continue
				# aplicam regulile mancarii pe barca
				if CAN > MIS and MIS != 0:
					continue
				# aplicam regulile mancarii pe malul de start
				if self.date[poz_cur] - CAN > self.date[poz_cur + 1] - MIS and (self.date[poz_cur + 1] - MIS) != 0:
					continue
				# aplicam regulile mancarii pe malul de sosire
				if self.date[poz_noua] + CAN > self.date[poz_noua + 1] + MIS and (self.date[poz_noua + 1] + MIS) != 0:
					continue
				# copiem configuratia
				date_nou = copy.deepcopy(self.date)
				# scadem persoanele care pleaza
				date_nou[poz_cur] -= CAN
				date_nou[poz_cur + 1] -= MIS
				# adunam persoanele care se duc
				date_nou[poz_noua] += CAN
				date_nou[poz_noua + 1] += MIS
				# mutam barca
				if date_nou[4] == 'est':
					date_nou[4] = 'vest'
				else:
					date_nou[4] = 'est'
				# calculam noul h
				noul_h = self.problema.calc_h(date_nou)
				# construim nodul
				lista.append(NodParcurgere(date_nou, self, self.g + 1, self.g + 1 + noul_h))
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
		sir += str(x) + "  "
	sir += "]"
	return sir


def str_simpla(lista):
	"""
		o functie folosita strict in afisari - poate fi modificata in functie de problema
	"""
	pas = 0
	sir = "\n"
	for x in lista:
		sir += "Pas " + str(pas) + ":\n"
		pas += 1
		sir += "EST: C:" + str(x.date[2]) + " M: " + str(x.date[3]) + "\n"
		sir += "VEST: C:" + str(x.date[0]) + " M:" + str(x.date[1]) + "\n"
		sir += "BARCA: " + str(x.date[4])
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
	rad_arbore = NodParcurgere(NodParcurgere.problema.date_init)
	lopen = [rad_arbore]  # open va contine elemente de tip NodParcurgere
	lclosed = []  # closed va contine elemente de tip NodParcurgere
	nod_curent = None
	start_time = time.time()
	while len(lopen) != 0:
		nod_curent = lopen[0]
		lclosed.append(nod_curent)
		if nod_curent.test_scop():
			break  # am gasit cel mai bun drum
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
	print("Timp trecut:" + str(time.time() - start_time))

if __name__ == "__main__":
	problema = Problema()
	NodParcurgere.problema = problema
	a_star()
