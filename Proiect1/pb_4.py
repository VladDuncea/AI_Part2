import copy
import time

# 1 pentru euristica optima,2 pentru euristica secundara
EURISTICA = 1


class Problema:

    def __init__(self, adancime, suparati, matrice, pers_initiala, scop):
        # adancimea e egala pe toate randurile
        self.adancime = adancime
        # lista de perechi de persoane suparate
        self.suparati = suparati
        # matricea cu numele elevilor
        self.matrice = matrice
        # pozitia celui care detine mesajul initial
        self.pers_initiala = pers_initiala
        # pozitia din matrice la care trebuie sa ajunga mesajul
        self.scop = scop

    # calculam distanta manhattan intre pozitia mesajului si pozitia din scop
    # pasi: 439
    # timp: 0.06
    def calc_h1(self, date):
        return abs(self.scop[0] - date[0]) + abs(self.scop[1] - date[1])

    # calculam distanta manhatan, dar trecand prin penultima/ultima banca
    # pasi: 2323
    # timp: 1.08
    def calc_h2(self, date):
        count = 0
        return count

    def verif_pozitie(self,sursa,dest):
        # verif loc liber
        if self.matrice[dest[0]][dest[1]] == "liber":
            return False

        # verificare suparati
        for (pers1,pers2) in self.suparati:
            if (pers1 == self.matrice[sursa[0]][sursa[1]] and pers2 == self.matrice[dest[0]][dest[1]]) or\
                    (pers2 == self.matrice[sursa[0]][sursa[1]] and pers1 == self.matrice[dest[0]][dest[1]]):
                return False
        return True


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

    def calc_euristica(self,date):
        # calculam noul h
        if EURISTICA == 1:
            noul_h = self.problema.calc_h1(date)
        else:
            noul_h = self.problema.calc_h2(date)
        return noul_h

    def creeaza_nod(self,noua_poz):
        return NodParcurgere(noua_poz, self, self.g + 1, self.g + 1 + self.calc_euristica(noua_poz))

    # se modifica in functie de problema
    def expandeaza(self):
        # Expandeaza nodul curent, intoarce lista de succesori
        # Construieste direct succesorii ca un nodParcurgere, pare mult mai simplu asa
        lista = []
        adancime = self.problema.adancime
        # avem maxim 4 directii, le testam pe toate
        i = self.date[0]
        j = self.date[1]

        # poate sa dea jos daca nu e capat
        if i > 0 and self.problema.verif_pozitie((i, j), (i - 1, j)):
            lista.append(self.creeaza_nod((i - 1, j)))
        # poate sa dea sus daca nu e capat
        if i < adancime-1 and self.problema.verif_pozitie((i, j), (i+1, j)):
            lista.append(self.creeaza_nod((i+1, j)))

        # separam cazurile pentru coloana para/impara(numarat de la 0)
        # (par poate sa dea oriunde spre dreapta, impar spre stanga)

        # PAR
        if j % 2==0 and self.problema.verif_pozitie((i,j), (i,j+1)):
            lista.append(self.creeaza_nod((i, j+1)))
        # poate sa dea doar la capete spre stanga, si daca nu e ultima coloana in stanga
        if j % 2==0 and j != 0 and i >= adancime-2 and self.problema.verif_pozitie((i,j), (i,j-1)):
            lista.append(self.creeaza_nod((i, j-1)))

        # IMPAR
        # poate sa dea doar la capete spre dreapta, si daca nu e ultima coloana in dreapta
        if j % 2 != 0 and j != 5 and i >= adancime - 2 and self.problema.verif_pozitie((i, j), (i, j + 1)):
            lista.append(self.creeaza_nod((i, j + 1)))
        if j % 2 != 0 and self.problema.verif_pozitie((i, j), (i, j - 1)):
            lista.append(self.creeaza_nod((i, j - 1)))

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

    problema = NodParcurgere.problema
    sir = str(problema.matrice[lista[0].date[0]][lista[0].date[1]]) + " "
    for i in range(len(lista)-1):
        sursa = lista[i].date
        dest = lista[i+1].date
        # v
        if sursa[0] + 1 == dest[0]:
            sir += "v"
        # ^
        if sursa[0] - 1 == dest[0]:
            sir += "^"
        # < sau <<
        if sursa[1] - 1 == dest[1]:
            if sursa[1] % 2 == 0:
                sir += "<<"
            else:
                sir += "<"
        # > sau >>
        if sursa[1] + 1 == dest[1]:
            if sursa[1] % 2 != 0:
                sir += ">>"
            else:
                sir += ">"
        sir += " " + str(problema.matrice[dest[0]][dest[1]]) + " "
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
    """
    for i in range(len(lista)):
        if lista[i].date == nod_parc.date:
            return lista[i]
    return None


def a_star():
    # contor pt pasi, pentru statistici
    pasi = 0
    rad_arbore = NodParcurgere(NodParcurgere.problema.pers_initiala)
    lopen = [rad_arbore]  # open va contine elemente de tip NodParcurgere
    lclosed = []  # closed va contine elemente de tip NodParcurgere
    nod_curent = None
    start_time = time.time()
    while len(lopen) != 0:
        nod_curent = lopen[0]
        pasi += 1
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
        print("Numar de pasi incercati: " + str(pasi))
    print("Timp trecut:" + str(time.time() - start_time))


def main():
    try:
        # citire date intrare si prelucrare
        adancime = 0
        matrice = []
        suparati = []
        with open('date_intrare_1.txt', 'r') as fisier:
            # citim primul rand
            linie = fisier.readline()
            nume = linie.split()
            # citim toti copii pana la suparati
            while nume[0] != "suparati":
                adancime += 1
                matrice.append(nume)
                linie = fisier.readline()
                nume = linie.split()
            # citim copii suparati
            linie = fisier.readline()
            nume = linie.split()
            while nume[0] != "mesaj:":
                suparati.append((nume[0], nume[1]))
                linie = fisier.readline()
                nume = linie.split()
            # citim persoana initiala si persoana finala
            initial = nume[1]
            scop = nume[3]
            # cauta persoana initiala, finala
            gasit = False
            for i, linie in enumerate(matrice):
                for k, val in enumerate(linie):
                    if val == initial:
                        initial = (i, k)
                        gasit = True
                        break
                if gasit:
                    break
            gasit = False
            for i, linie in enumerate(matrice):
                for k, val in enumerate(linie):
                    if val == scop:
                        scop = (i, k)
                        gasit = True
                        break
                if gasit:
                    break
    except:
        print("Fisierul de input nu este formatat corect!")
        exit(1)
    problema = Problema(adancime, suparati, matrice, initial, scop)
    NodParcurgere.problema = problema
    a_star()


if __name__ == "__main__":
    main()
