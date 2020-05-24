# Grupa 244 Duncea Vlad Alexandru

import copy
import time


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
        # setam euristica default
        self.euristica = 1

    # functie ca sa setam euristica curenta(valoare intre 1 si 3)
    def set_euristica(self, euristica):
        self.euristica = euristica

    # in calcul euristici 'date' este pozitia pentru care se aproximeaza distanta
    # euristica admisibila, nu e consistenta pentru ca ne putem indeparta de scop pentru a ocoli blocaje
    # calculam distanta manhatan
    """
    Admisibilitate: distanta manhatan nu poate sa fie mai lunga decat drumul in sine(miscarile se fac
    doar stanga-dreapta sau sus-jos)
    """
    def calc_h1(self, date):
        return abs(self.scop[0] - date[0]) + abs(self.scop[1] - date[1])

    # euristica admisibila, nu e consistenta pentru ca ne putem indeparta de scop pentru a ocoli blocaje
    # calculam distanta intre coloane
    """
        Admisibilitate: distanta dintre coloane in modul nu poate sa fie mai lunga decat drumul in sine
        (va trebui sa faca cel putin 'n'(dif dintre coloane) miscari pentru a ajunge pe pozitia scop)
    """
    def calc_h2(self, date):
        return abs(self.scop[1] - date[1])

    # euristica nu indeplineste conditia de admisibilitate
    # calculam triplul distantei intre randuri
    """
        Nu e admisibila: Daca avem scopul pe aceeasi coloana si nu avem blocaje va intoarce triplul distantei reale
    """
    def calc_h3(self, date):
        return 3 * abs(self.scop[0] - date[0])

    # intoarce true daca persoanele nu sunt suparate si locul nu e liber, fals altfel
    # sursa,dest sunt coordonatele sursei/destinatiei
    def verif_pozitie(self, sursa, dest):
        # verif loc liber
        if self.matrice[dest[0]][dest[1]] == "liber":
            return False

        # verificare suparati
        for (pers1, pers2) in self.suparati:
            if (pers1 == self.matrice[sursa[0]][sursa[1]] and pers2 == self.matrice[dest[0]][dest[1]]) or \
                    (pers2 == self.matrice[sursa[0]][sursa[1]] and pers1 == self.matrice[dest[0]][dest[1]]):
                return False
        return True


# Sfarsit definire problema

# Clase folosite in algoritmul A*
class NodParcurgere:
    """O clasa care cuprinde informatiile asociate unui nod din listele open/closed
        Cuprinde o referinta catre nodul in sine (din graf)
        dar are ca proprietati si valorile specifice algoritmului A* (f si g).
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

    # functie care calculeaza aproximarea in functie de euristica aleasa
    def calc_euristica(self, date):
        # calculam noul h
        if NodParcurgere.problema.euristica == 1:
            noul_h = self.problema.calc_h1(date)
        elif NodParcurgere.problema.euristica == 2:
            noul_h = self.problema.calc_h2(date)
        else:
            noul_h = self.problema.calc_h3(date)
        return noul_h

    # functie care sa creeze nodul(asa apar mai putine linii duplicat)
    def creeaza_nod(self, noua_poz):
        return NodParcurgere(noua_poz, self, self.g + 1, self.g + 1 + self.calc_euristica(noua_poz))

    # functia de generare a succesorilor
    def expandeaza(self):
        # Expandeaza nodul curent, intoarce lista de succesori
        # Construieste direct succesorii ca un nodParcurgere, pare mult mai simplu asa
        lista = []
        # variabile ajutatoare
        adancime = self.problema.adancime   # numarul de coloane(cel de randuri e intotdeauna 6)
        i = self.date[0]    # randul
        j = self.date[1]    # coloana

        # avem maxim 4 directii in care putem da mesajul, le testam pe toate
        # in afara de verificarile speciale, la fiecare pas verificam daca nu sunt certate persoanele

        # poate sa dea mesajul in sus daca nu e in primul rand
        if i > 0 and self.problema.verif_pozitie((i, j), (i - 1, j)):
            lista.append(self.creeaza_nod((i - 1, j)))

        # poate sa dea mesajul in jos  daca nu e in ultimul rand
        if i < adancime - 1 and self.problema.verif_pozitie((i, j), (i + 1, j)):
            lista.append(self.creeaza_nod((i + 1, j)))

        # separam cazurile pentru coloana para/impara(numarat de la 0)
        # (par poate sa dea oricand spre dreapta, impar oricand spre stanga)

        # PAR
        if j % 2 == 0:
            # da la dreapta daca nu sunt suparati/loc liber
            if self.problema.verif_pozitie((i, j), (i, j + 1)):
                lista.append(self.creeaza_nod((i, j + 1)))
            # poate sa dea doar in ultimele 2 randuri spre stanga
            # si daca nu e ultima coloana din stanga
            if j != 0 and i >= adancime - 2 and self.problema.verif_pozitie((i, j), (i, j - 1)):
                lista.append(self.creeaza_nod((i, j - 1)))

        # IMPAR
        if j % 2 != 0:
            # poate sa dea doar in ultimele doua coloane spre dreapta
            # si daca nu e ultima coloana in dreapta
            if j != 5 and i >= adancime - 2 and self.problema.verif_pozitie((i, j), (i, j + 1)):
                lista.append(self.creeaza_nod((i, j + 1)))
            # da la stanga daca nu sunt suparati/loc liber
            if self.problema.verif_pozitie((i, j), (i, j - 1)):
                lista.append(self.creeaza_nod((i, j - 1)))
        return lista

    # functia de testare a scopului, verifica daca pozitia curenta este cea dorita
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
    # afisare in stilul problemei
    problema = NodParcurgere.problema
    # adaugam primul nume
    sir = str(problema.matrice[lista[0].date[0]][lista[0].date[1]]) + " "
    # pentru fiecare doua persoane adaugam intre ele caracterul corespunzator
    for i in range(len(lista) - 1):
        sursa = lista[i].date
        dest = lista[i + 1].date
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


def a_star(nume_output):
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

    with open(nume_output, 'a+') as fisier:
        fisier.write("\n------------- Euristica " + str(NodParcurgere.problema.euristica) + " -----------------\n")
        if len(lopen) == 0:
            fisier.write("Lista open e vida, nu avem drum de la nodul start la nodul scop")
        else:
            fisier.write("Drum de cost minim: " + str_simpla(nod_curent.drum_arbore()))
            fisier.write("\nNumar de pasi incercati: " + str(pasi))
        fisier.write("\nTimp trecut:" + str(time.time() - start_time) +"\n")


def citire(fisier):
    try:
        # citire date intrare si prelucrare
        adancime = 0
        matrice = []
        suparati = []
        with open(fisier, 'r') as fisier:
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
    return Problema(adancime, suparati, matrice, initial, scop)


def main():
    date_intrare = ['input_1.txt', 'input_2.txt', 'input_3.txt', 'input_4.txt']
    date_iesire = ['output_1.txt', 'output_2.txt', 'output_3.txt', 'output_4.txt']

    for i in range(len(date_intrare)):
        # golim fisierul de iesire
        f = open(date_iesire[i], "w")
        f.close()
        for euristica in range(1, 4, 1):
            NodParcurgere.problema = citire(date_intrare[i])
            NodParcurgere.problema.set_euristica(euristica)

            a_star(date_iesire[i])


if __name__ == "__main__":
    main()
