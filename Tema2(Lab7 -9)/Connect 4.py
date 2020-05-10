import time
import copy


def elem_identice(lista):
	mt = set(lista)
	if len(mt) == 1:
		castigator = list(mt)[0]
		if castigator != Joc.GOL:
			return castigator
		else:
			return False
	else:
		return False


def interval_deschis(interval, jucator):
	for piesa in interval:
		if piesa != jucator and piesa != Joc.GOL:
			return False
	return True


class Joc:
	"""
	Clasa care defineste jocul. Se va schimba de la un joc la altul.
	"""
	NR_COLOANE = 7
	NR_LINII = 6
	NR_CONNECT = 4  # cu cate simboluri adiacente se castiga
	SIMBOLURI_JUC = ['G', 'R']  # ['G', 'R'] sau ['X', '0']
	JMIN = None  # 'R'
	JMAX = None  # 'G'
	GOL = '.'

	def __init__(self, tabla=None):
		self.matr = tabla or [[Joc.GOL for i in range(Joc.NR_COLOANE)] for i in range(Joc.NR_LINII)]

	def final(self):
		# returnam simbolul jucatorului castigator daca are 4 piese adiacente
		# pe linie, coloana, diagonala \ sau diagonala /
		# sau returnam 'remiza'
		# sau 'False' daca nu s-a terminat jocul

		# verificam linii
		for i in range(Joc.NR_LINII):
			for j in range(Joc.NR_COLOANE - Joc.NR_CONNECT):
				if elem_identice([self.matr[i][j + x] for x in range(Joc.NR_CONNECT)]):
					return self.matr[i][j]

		# verificam coloane
		for i in range(Joc.NR_LINII - Joc.NR_CONNECT):
			for j in range(Joc.NR_COLOANE):
				if elem_identice([self.matr[i + x][j] for x in range(Joc.NR_CONNECT)]):
					return self.matr[i][j]

		# verificam diagonale \
		for i in range(Joc.NR_LINII - Joc.NR_CONNECT):
			for j in range(Joc.NR_COLOANE - Joc.NR_CONNECT):
				if elem_identice([self.matr[i + x][j + x] for x in range(Joc.NR_CONNECT)]):
					return self.matr[i][j]

		# verificam diagonale /
		for i in range(Joc.NR_CONNECT - 1, Joc.NR_LINII, 1):
			for j in range(Joc.NR_CONNECT - 1, Joc.NR_COLOANE, 1):
				if elem_identice([self.matr[i - x][j - x] for x in range(Joc.NR_CONNECT)]):
					return self.matr[i][j]

		if Joc.GOL not in (item for sublist in self.matr for item in sublist):
			return 'remiza'
		else:
			return False

	def mutari_joc(self, jucator):
		l_mutari = []

		# incercam sa punem piesa in orice coloana
		for j in range(Joc.NR_COLOANE):
			# cautam prima linie goala
			for i in range(Joc.NR_LINII):
				if self.matr[i][j] == Joc.GOL and (i == Joc.NR_LINII - 1 or self.matr[i + 1][j] != Joc.GOL):
					matr_noua = copy.deepcopy(self.matr)
					matr_noua[i][j] = jucator
					l_mutari.append(Joc(matr_noua))
					break

		return l_mutari

	def nr_intervale_deschise(self, jucator):
		# un interval de 4 pozitii adiacente (pe linie, coloana, diag \ sau diag /)
		# este deschis pt "jucator" daca nu contine "juc_opus"

		juc_opus = Joc.JMIN if jucator == Joc.JMAX else Joc.JMAX
		rez = 0

		# verificam linii
		for i in range(Joc.NR_LINII):
			for j in range(Joc.NR_COLOANE - Joc.NR_CONNECT):
				if interval_deschis([self.matr[i][j + x] for x in range(Joc.NR_CONNECT)], jucator):
					rez += 1

		# verificam coloane
		for i in range(Joc.NR_LINII - Joc.NR_CONNECT):
			for j in range(Joc.NR_COLOANE):
				if interval_deschis([self.matr[i + x][j] for x in range(Joc.NR_CONNECT)], jucator):
					rez += 1

		# verificam diagonale \
		for i in range(Joc.NR_LINII - Joc.NR_CONNECT):
			for j in range(Joc.NR_COLOANE - Joc.NR_CONNECT):
				if interval_deschis([self.matr[i + x][j + x] for x in range(Joc.NR_CONNECT)], jucator):
					rez += 1

		# verificam diagonale /
		for i in range(Joc.NR_CONNECT - 1, Joc.NR_LINII, 1):
			for j in range(Joc.NR_CONNECT - 1, Joc.NR_COLOANE, 1):
				if interval_deschis([self.matr[i - x][j - x] for x in range(Joc.NR_CONNECT)], jucator):
					rez += 1

		return rez

	def fct_euristica(self):
		# TO DO: alte variante de euristici? .....

		# intervale_deschisa(juc) = cate intervale de 4 pozitii
		# (pe linii, coloane, diagonale) nu contin juc_opus
		return self.nr_intervale_deschise(Joc.JMAX) - self.nr_intervale_deschise(Joc.JMIN)

	def estimeaza_scor(self, adancime):
		t_final = self.final()
		if t_final == Joc.JMAX:
			return 999 + adancime
		elif t_final == Joc.JMIN:
			return -999 - adancime
		elif t_final == 'remiza':
			return 0
		else:
			return self.fct_euristica()

	def __str__(self):
		sir = ''
		for nr_col in range(self.NR_COLOANE):
			sir += str(nr_col) + ' '
		sir += '\n'

		for i in range(self.NR_LINII):
			for j in range(self.NR_COLOANE):
				sir += str(self.matr[i][j]) + " "
			sir += "\n"
		return sir


class Stare:
	"""
	Clasa folosita de algoritmii minimax si alpha-beta
	Are ca proprietate tabla de joc
	Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
	De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari_joc() care ofera lista cu
	configuratiile posibile in urma mutarii unui jucator
	"""

	ADANCIME_MAX = None

	def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
		self.tabla_joc = tabla_joc
		self.j_curent = j_curent

		# adancimea in arborele de stari
		self.adancime = adancime

		# scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
		self.scor = scor

		# lista de mutari posibile din starea curenta
		self.mutari_posibile = []

		# cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
		self.stare_aleasa = None

	def jucator_opus(self):
		if self.j_curent == Joc.JMIN:
			return Joc.JMAX
		else:
			return Joc.JMIN

	def mutari_stare(self):
		l_mutari = self.tabla_joc.mutari_joc(self.j_curent)
		juc_opus = self.jucator_opus()
		l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

		return l_stari_mutari

	def __str__(self):
		sir = str(self.tabla_joc) + "(Juc curent: " + self.j_curent + ")\n"
		return sir


""" Algoritmul MinMax """


def min_max(stare):
	if stare.adancime == 0 or stare.tabla_joc.final():
		stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
		return stare

	# calculez toate mutarile posibile din starea curenta
	stare.mutari_posibile = stare.mutari_stare()

	# aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
	mutari_scor = [min_max(mutare) for mutare in stare.mutari_posibile]

	if stare.j_curent == Joc.JMAX:
		# daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
		stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
	else:
		# daca jucatorul e JMIN aleg starea-fiica cu scorul minim
		stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)

	stare.scor = stare.stare_aleasa.scor
	return stare


def alpha_beta(alpha, beta, stare):
	if stare.adancime == 0 or stare.tabla_joc.final():
		stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
		return stare

	if alpha >= beta:
		return stare  # este intr-un interval invalid deci nu o mai procesez

	stare.mutari_posibile = stare.mutari_stare()

	if stare.j_curent == Joc.JMAX:
		scor_curent = float('-inf')

		for mutare in stare.mutari_posibile:
			# calculeaza scorul
			stare_noua = alpha_beta(alpha, beta, mutare)

			if (scor_curent < stare_noua.scor):
				stare.stare_aleasa = stare_noua
				scor_curent = stare_noua.scor
			if (alpha < stare_noua.scor):
				alpha = stare_noua.scor
				if alpha >= beta:
					break

	elif stare.j_curent == Joc.JMIN:
		scor_curent = float('inf')

		for mutare in stare.mutari_posibile:
			stare_noua = alpha_beta(alpha, beta, mutare)

			if (scor_curent > stare_noua.scor):
				stare.stare_aleasa = stare_noua
				scor_curent = stare_noua.scor

			if (beta > stare_noua.scor):
				beta = stare_noua.scor
				if alpha >= beta:
					break

	stare.scor = stare.stare_aleasa.scor

	return stare


def afis_daca_final(stare_curenta):
	# ?? TO DO:
	# de adagat parametru "pozitie", ca sa nu verifice mereu toata tabla,
	# ci doar linia, coloana, 2 diagonale pt elementul nou, de pe "pozitie"

	final = stare_curenta.tabla_joc.final()
	if final:
		if final == "remiza":
			print("Remiza!")
		else:
			print("A castigat " + final)

		return True

	return False


def main():
	# initializare algoritm
	raspuns_valid = False
	while not raspuns_valid:
		tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
		if tip_algoritm in ['1', '2']:
			raspuns_valid = True
		else:
			print("Nu ati ales o varianta corecta.")

	# initializare ADANCIME_MAX
	raspuns_valid = False
	while not raspuns_valid:
		n = input("Adancime maxima a arborelui: ")
		if n.isdigit():
			Stare.ADANCIME_MAX = int(n)
			raspuns_valid = True
		else:
			print("Trebuie sa introduceti un numar natural nenul.")

	# initializare jucatori
	[s1, s2] = Joc.SIMBOLURI_JUC.copy()  # lista de simboluri posibile
	raspuns_valid = False
	while not raspuns_valid:
		Joc.JMIN = str(input("Doriti sa jucati cu {} sau cu {}? ".format(s1, s2))).upper()
		if Joc.JMIN in Joc.SIMBOLURI_JUC:
			raspuns_valid = True
		else:
			print("Raspunsul trebuie sa fie {} sau {}.".format(s1, s2))
	Joc.JMAX = s1 if Joc.JMIN == s2 else s2

	# initializare tabla
	tabla_curenta = Joc()
	print("Tabla initiala")
	print(str(tabla_curenta))

	# creare stare initiala
	stare_curenta = Stare(tabla_curenta, Joc.SIMBOLURI_JUC[0], Stare.ADANCIME_MAX)

	linie = -1
	coloana = -1
	while True:
		if stare_curenta.j_curent == Joc.JMIN:
			# muta jucatorul
			raspuns_valid = False
			while not raspuns_valid:
				try:
					coloana = int(input("coloana = "))
					linie = -1

					# verificare coloana in interval corect
					if coloana < 0 or coloana >= Joc.NR_COLOANE:
						print("Coloana invalida (trebuie sa fie un numar intre 0 si {}).".format(Joc.NR_COLOANE - 1))
					else:
						# cautare linie
						for i in range(Joc.NR_LINII):
							if stare_curenta.tabla_joc.matr[i][coloana] == Joc.GOL and (
									i == Joc.NR_LINII - 1 or stare_curenta.tabla_joc.matr[i + 1][coloana] != Joc.GOL):
								linie = i
								break

						if linie == -1:
							print("Coloana este plina")
						else:
							raspuns_valid = True

				except ValueError:
					print("Coloana trebuie sa fie un numar intreg.")

			# dupa iesirea din while sigur am valida coloana
			# deci pot plasa simbolul pe "tabla de joc"
			stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMIN

			# afisarea starii jocului in urma mutarii utilizatorului
			print("\nTabla dupa mutarea jucatorului")
			print(str(stare_curenta))

			# testez daca jocul a ajuns intr-o stare finala
			# si afisez un mesaj corespunzator in caz ca da
			if afis_daca_final(stare_curenta):
				break

			# S-a realizat o mutare. Schimb jucatorul cu cel opus
			stare_curenta.j_curent = stare_curenta.jucator_opus()

		# --------------------------------
		else:  # jucatorul e JMAX (calculatorul)
			# Mutare calculator

			# preiau timpul in milisecunde de dinainte de mutare
			t_inainte = int(round(time.time() * 1000))
			if tip_algoritm == '1':
				stare_actualizata = min_max(stare_curenta)
			else:  # tip_algoritm==2
				stare_actualizata = alpha_beta(-5000, 5000, stare_curenta)
			stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
			print("Tabla dupa mutarea calculatorului")
			print(str(stare_curenta))

			# preiau timpul in milisecunde de dupa mutare
			t_dupa = int(round(time.time() * 1000))
			print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

			if afis_daca_final(stare_curenta):
				break

			# S-a realizat o mutare. Schimb jucatorul cu cel opus
			stare_curenta.j_curent = stare_curenta.jucator_opus()


if __name__ == "__main__":
	main()
