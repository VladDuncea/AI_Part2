import time
import copy


# TODO: inca o functie de scor
def scor(tabla, jucator):
    # functia simpla de scor, intoarce numarul de patrate acumulate de jucator
    s = 0
    for linie in tabla:
        for casuta in linie:
            if casuta == jucator:
                s += 1
    return s


def scor_max(tabla, jucator):
    # functia de scor 2, intoarce scorul maxim pe care il poate acumula jucatorul
    # si daca  trece de jumatate cu scorul curent intoarce 9999(castig sigur)
    s = 0
    for linie in tabla:
        for casuta in linie:
            if casuta == jucator:
                s += 1

    # verificare castig sigur
    if s > (Joc.NR_COLOANE * Joc.NR_LINII)/2:
        return 9999
    for linie in tabla:
        for casuta in linie:
            if casuta == Joc.GOL:
                s += 1
    return s


def jucator_op(jucator):
    if jucator == Joc.JMIN:
        return Joc.JMAX
    else:
        return Joc.JMIN


class Joc:
    # clasa cu datele pentru joc
    # dimensiuni default, se citesc date noi de la tastatura
    NR_COLOANE = 3
    NR_LINII = 3
    SIMBOLURI_JUC = ['A', 'B']  # alb si negru
    POZ_VALIDE = ['L', 'R', 'T', 'B']  # left, right, top, bottom
    JMIN = None
    JMAX = None
    GOL = ' '

    def __init__(self, vertical=None, orizontal=None, scor=None):
        self.matr_scor = scor or [[Joc.GOL for i in range(Joc.NR_COLOANE)] for i in range(Joc.NR_LINII)]
        # in matricea verticala avem nr_coloane+1 coloane si nr_linii linii
        self.matr_vertic = vertical or [[0 for i in range(Joc.NR_COLOANE + 1)] for i in range(Joc.NR_LINII)]
        # in matricea orizontala avem nr_coloane coloane si nr_linii+1 linii
        self.matr_orizon = orizontal or [[0 for i in range(Joc.NR_COLOANE)] for i in range(Joc.NR_LINII + 1)]

    # functie de testare a starii finale si de stabilire a castigatorului
    def final(self):
        # returnam simbolul jucatorului castigator
        # sau returnam 'remiza'
        # sau 'False' daca nu s-a terminat jocul

        # verificam daca se mai pot pune linii
        if not self.exista_miscare():
            # numaram cate piese are fiecare jucator
            scor_min = scor(self.matr_scor, Joc.JMIN)
            scor_max = scor(self.matr_scor, Joc.JMAX)
            if scor_min == scor_max:
                return 'remiza'
            elif scor_max > scor_min:
                return Joc.JMAX
            else:
                return Joc.JMIN
        else:
            # daca se mai pot face miscari jocul nu s-a terminat
            return False

    # functia care verifica daca mai exista miscari posibile
    def exista_miscare(self):
        # verificam daca mai exista linii necompletate
        for i in range(len(self.matr_vertic)):
            for j in range(len(self.matr_vertic[0])):
                if not self.matr_vertic[i][j]:
                    return True
        for i in range(len(self.matr_orizon)):
            for j in range(len(self.matr_orizon[0])):
                if not self.matr_orizon[i][j]:
                    return True
        # nu am gasit linii libere
        return False

    # functie care verifica daca o miscare e valida
    def miscare_valida(self, miscare):
        (x, y, z) = miscare

        # verificam daca linia e disponibila
        # stanga
        if z == "L":
            if self.matr_vertic[x][y] == 1:
                return False
        # dreapta
        if z == "R":
            if self.matr_vertic[x][y + 1] == 1:
                return False
        # sus
        if z == "T":
            if self.matr_orizon[x][y] == 1:
                return False
        # jos
        if z == "B":
            if self.matr_orizon[x + 1][y] == 1:
                return False
        return True

    # adaugam linia si intoarcem numarul de casute castigate intoarce -1 daca miscarea nu e valida
    def aplica_linie(self, miscare, jucator):
        (x, y, z) = miscare

        # verificam(redundant, dar nu poti avea incredere in calculator(poate triseaza))
        if not self.miscare_valida(miscare):
            return -1

        # actualizam matricea de linii
        # stanga
        if z == "L":
            self.matr_vertic[x][y] = 1
        # dreapta
        if z == "R":
            self.matr_vertic[x][y + 1] = 1
        # sus
        if z == "T":
            self.matr_orizon[x][y] = 1
        # jos
        if z == "B":
            self.matr_orizon[x + 1][y] = 1

        # numaram cate patrate a facut si le actualizam
        contor = 0
        # cazuri pentru linie verticala
        if z == "L" or z == "R":
            # ne purtam de parca linia este in stanga coordonatelor
            i = x
            if z == "L":
                j = y
            else:
                j = y + 1

            # verificam la stanga daca nu e prima linie verticala
            if j != 0:
                if self.matr_orizon[i][j - 1] and self.matr_orizon[i + 1][j - 1] and self.matr_vertic[i][j - 1]:
                    contor += 1
                    self.matr_scor[i][j - 1] = jucator

            # verificam la dreapta daca nu e ultima linie verticala
            if j != Joc.NR_COLOANE:
                if self.matr_orizon[i][j] and self.matr_orizon[i + 1][j] and self.matr_vertic[i][j]:
                    contor += 1
                    self.matr_scor[i][j] = jucator

        # cazuri pentru linie orizontala
        if z == "T" or z == "B":
            # ne purtam de parca linia este deasupra coordonatelor
            if z == "T":
                i = x
            else:
                i = x + 1
            j = y

            # verificam la sus daca nu e prima linie orizontala
            if i != 0:
                if self.matr_orizon[i - 1][j] and self.matr_vertic[i - 1][j] and self.matr_vertic[i - 1][j + 1]:
                    contor += 1
                    self.matr_scor[i - 1][j] = jucator

            # verificam la jos daca nu e ultima linie orizontala
            if i != Joc.NR_LINII:
                if self.matr_orizon[i + 1][j] and self.matr_vertic[i][j] and self.matr_vertic[i][j + 1]:
                    contor += 1
                    self.matr_scor[i][j] = jucator

        return contor

    # functia de generare a miscarilor (succesorilor)
    def mutari_joc(self, jucator):
        l_mutari = []

        # incercam toate miscarile
        for i in range(Joc.NR_LINII):
            for j in range(Joc.NR_COLOANE):
                for poz in Joc.POZ_VALIDE:
                    if not self.miscare_valida((i, j, poz)):
                        continue
                    # miscarea e valida creeaza un Joc nou si apoi aplica miscarea
                    joc_nou = copy.deepcopy(self)
                    if joc_nou.aplica_linie((i, j, poz), jucator) == 2:
                        # daca a facut doua patrate poate sa joace iar
                        lista = joc_nou.mutari_joc(jucator)
                        if len(lista) != 0:
                            l_mutari.extend(lista)
                        else:
                            l_mutari.append(joc_nou)
                    else:
                        l_mutari.append(joc_nou)

        return l_mutari

    def fct_euristica(self):
        # numarul de piese JMAX - JMIN
        return scor_max(self.matr_scor, Joc.JMAX) - scor_max(self.matr_scor, Joc.JMIN)

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
        # afisare codul coloanelor
        sir = '   '
        for nr_col in range(self.NR_COLOANE):
            sir += chr(ord('a') + nr_col) + ' '
        sir += '\n'
        # afisare separator
        sir += '  -'
        for nr_col in range(self.NR_COLOANE):
            sir += '--'
        sir += '\n'

        # afisare tabla
        # pe linii pare afisam liiniile orizontale si puncte
        # pe linii impare afisam cutiile si liniile verticale
        i1 = 0
        i2 = 0
        for i in range(self.NR_LINII * 2 + 1):
            # afisare pt linie para
            if i % 2 == 0:
                sir += '  .'
                for j in range(self.NR_COLOANE):
                    if self.matr_orizon[i1][j]:
                        sir += '-.'
                    else:
                        sir += ' .'
                sir += "\n"
                i1 += 1
            # afisare pt linie impara
            if i % 2 != 0:
                sir += str(i2) + ' '
                if self.matr_vertic[i2][0]:
                    sir += '|'
                else:
                    sir += ' '
                for j in range(self.NR_COLOANE):
                    sir += self.matr_scor[i2][j]
                    if self.matr_vertic[i2][j + 1]:
                        sir += '|'
                    else:
                        sir += ' '
                sir += "\n"
                i2 += 1
        return sir


class Stare:
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

    def afisare_scor(self):
        print("Scor jucator:" + str(scor(self.tabla_joc.matr_scor, Joc.JMIN)))
        print("Scor calculator:" + str(scor(self.tabla_joc.matr_scor, Joc.JMAX)))

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

            if scor_curent < stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if alpha < stare_noua.scor:
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')

        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)

            if scor_curent > stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if beta > stare_noua.scor:
                beta = stare_noua.scor
                if alpha >= beta:
                    break
    stare.scor = stare.stare_aleasa.scor
    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if final:
        if final == "remiza":
            print("Remiza!")
        else:
            print("A castigat " + final)
        # afisare scor
        stare_curenta.afisare_scor()
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

    # initializare ADANCIME_MAX, intrabam user-ul greutatea
    # 2-Usor
    # 3-Mediu
    # 4-Greu
    raspuns_valid = False
    while not raspuns_valid:
        n = input("Greutatea jocului: (raspundeti cu 1,2 sau 3)\n 1.Usor\n 2.Mediu\n 3.Greu\n ")
        if n.isdigit() and 1 <= int(n) <= 3:
            n = int(n)
            if n == 1:
                Stare.ADANCIME_MAX = 2
            elif n == 2:
                Stare.ADANCIME_MAX = 3
            elif n == 3:
                Stare.ADANCIME_MAX = 4
            raspuns_valid = True
        else:
            print("Trebuie sa introduceti un numar natural nenul intre 1 si 3.")

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

    # initializare ADANCIME_MAX
    raspuns_valid = False
    while not raspuns_valid:
        x = input("Linii: ")
        y = input("Coloane: ")
        if x.isdigit() and y.isdigit():
            Joc.NR_LINII = int(x)
            Joc.NR_COLOANE = int(y)
            raspuns_valid = True
        else:
            print("Trebuie sa introduceti un numar natural nenul.")

    # initializare tabla
    tabla_curenta = Joc()
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala vietatea joaca prima
    stare_curenta = Stare(tabla_curenta, Joc.JMIN, Stare.ADANCIME_MAX)

    # Afisare informatie iesire
    print("Daca doriti sa iesiti scrieti \"exit\" cand sunteti intrebat \"linie=\"!")

    linie = -1
    coloana = -1
    while True:
        if stare_curenta.j_curent == Joc.JMIN:
            t_inainte = int(round(time.time() * 1000))
            # muta jucatorul
            raspuns_valid = False
            while not raspuns_valid:
                try:
                    linie = input("linia = ")
                    if linie == "exit":
                        print("Jocul a fost intrerupt")
                        stare_curenta.afisare_scor()
                        return 0
                    linie = int(linie)
                    coloana = input("coloana = ")
                    [a, b, c, d] = Joc.POZ_VALIDE
                    pozitia = str(input("Pozitii valide {},{},{},{}.\nPozitia:".format(a, b, c, d))).upper()
                    if not coloana.isalpha():
                        raise ValueError('Coloana nu e caracter')

                    # verificare linie,coloana in interval corect
                    if linie < 0 or linie >= Joc.NR_LINII:
                        print("Linie invalida (trebuie sa fie un numar intre 0 si {}).".format(Joc.NR_COLOANE - 1))
                    elif coloana < 'a' or coloana >= chr(ord('a') + Joc.NR_COLOANE):
                        print("Coloana invalida (trebuie sa fie un caracter intre a si {}).".format(
                            chr(ord('a') + Joc.NR_COLOANE)))
                    elif pozitia not in Joc.POZ_VALIDE:
                        print("Pozitia invalida!")
                    else:
                        coloana = ord(coloana) - ord('a')
                        # cautare si verificare pozitie valida
                        if not stare_curenta.tabla_joc.miscare_valida((linie, coloana, pozitia)):
                            print("Miscare invalida")
                        else:
                            raspuns_valid = True

                except ValueError:
                    print("Linia trebuie sa fie un numar intreg, coloana un caracter.")

            # dupa iesirea din while sigur am valida coloana
            # facem miscarea
            patrate = stare_curenta.tabla_joc.aplica_linie((linie, coloana, pozitia), Joc.JMIN)

            # afiseaza cat a gandit jucatorul:
            t_dupa = int(round(time.time() * 1000))
            print("Jucatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            # afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))
            # testez daca jocul a ajuns intr-o stare finala
            # si afisez un mesaj corespunzator in caz ca da
            if afis_daca_final(stare_curenta):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus (doar daca nu a facut 2 patrate)
            if patrate != 2:
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
            matr1 = stare_curenta.tabla_joc.matr_vertic
            matr2 = stare_curenta.tabla_joc.matr_orizon
            pasi = 0
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            for i in range(len(matr1)):
                for j in range(len(matr1[0])):
                    if matr1[i][j] != stare_curenta.tabla_joc.matr_vertic[i][j]:
                        pasi += 1
            for i in range(len(matr2)):
                for j in range(len(matr2[0])):
                    if matr2[i][j] != stare_curenta.tabla_joc.matr_orizon[i][j]:
                        pasi += 1
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
            print("Calculatorul a facut " + str(pasi) +" pasi!")

            if afis_daca_final(stare_curenta):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()


if __name__ == "__main__":
    main()
