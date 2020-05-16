import time
import copy

def scor(tabla, jucator):
    s = 0
    for linie in tabla:
        for casuta in linie:
            if casuta == jucator:
                s += 1
    return s


def jucator_op(jucator):
    if jucator == Joc.JMIN:
        return Joc.JMAX
    else:
        return Joc.JMIN


class Joc:
    # clasa cu datele pentru joc
    # tabla trebuie sa fie de dimensiuni pare!
    NR_COLOANE = 8
    NR_LINII = 8
    SIMBOLURI_JUC = ['A', 'N']  # alb si negru
    JMIN = None
    JMAX = None
    GOL = '#'

    def __init__(self, tabla=None):
        self.matr = tabla or [[Joc.GOL for i in range(Joc.NR_COLOANE)] for i in range(Joc.NR_LINII)]
        # adaugam cele 4 piese initiale daca tabla e noua
        if tabla is None:
            self.matr[int(Joc.NR_LINII/2) - 1][int(Joc.NR_COLOANE/2) - 1] = 'A'
            self.matr[int(Joc.NR_LINII/2) - 1][int(Joc.NR_COLOANE/2)] = 'N'
            self.matr[int(Joc.NR_LINII/2)][int(Joc.NR_COLOANE/2) - 1] = 'N'
            self.matr[int(Joc.NR_LINII/2)][int(Joc.NR_COLOANE/2)] = 'A'

    def final(self):
        # returnam simbolul jucatorului castigator
        # sau returnam 'remiza'
        # sau 'False' daca nu s-a terminat jocul\

        # verificam daca nu se mai pot face miscari
        if (not self.exista_miscare(Joc.JMAX)) and (not self.exista_miscare(Joc.JMIN)):
            # numaram cate piese are fiecare jucator
            scor_min = scor(self.matr, Joc.JMIN)
            scor_max = scor(self.matr, Joc.JMAX)
            if scor_min == scor_max:
                return 'remiza'
            elif scor_max > scor_min:
                return Joc.JMAX
            else:
                return Joc.JMIN
        else:
            # daca se mai pot face miscari jocul nu s-a terminat
            return False

    def exista_miscare(self, jucator):
        # verificam fiecare casuta daca e miscare valida
        # functia miscare_valida verifica initial daca casuta e goala, deci nu trebuie sa mai verificam noi
        for i in range(self.NR_LINII):
            for j in range(self.NR_COLOANE):
                if self.miscare_valida((i, j), jucator):
                    return True
        # nu am gasit casute pentru miscare valida
        return False

    def miscare_valida(self, miscare, jucator):
        (x, y) = miscare
        # verificare pozitie goala
        if self.matr[x][y] != Joc.GOL:
            return False

        opus = jucator_op(jucator)

        # verificare coloana
        for i in range(x+1, Joc.NR_LINII-1, 1):
            if self.matr[i][y] == opus and self.matr[i+1][y] == jucator:
                return True
            if self.matr[i][y] == jucator or self.matr[i][y] == Joc.GOL:
                break
        for i in range(x-1, 0, -1):
            if self.matr[i][y] == opus and self.matr[i-1][y] == jucator:
                return True
            if self.matr[i][y] == jucator or self.matr[i][y] == Joc.GOL:
                break

        # verificare linie
        for j in range(y + 1, Joc.NR_COLOANE - 1, 1):
            if self.matr[x][j] == opus and self.matr[x][j + 1] == jucator:
                return True
            if self.matr[x][j] == jucator or self.matr[x][j] == Joc.GOL:
                break
        for j in range(y - 1, 0, -1):
            if self.matr[x][j] == opus and self.matr[x][j-1] == jucator:
                return True
            if self.matr[x][j] == jucator or self.matr[x][j] == Joc.GOL:
                break

        # verificare diagonala \
        for i in range(1, min(Joc.NR_LINII - x, Joc.NR_COLOANE - y) - 1, 1):
            if self.matr[x+i][y+i] == opus and self.matr[x+i+1][y+i+1] == jucator:
                return True
            if self.matr[x+i][y+i] == jucator or self.matr[x+i][y+i] == Joc.GOL:
                break
        for i in range(1, min(x, y), 1):
            if self.matr[x-i][y-i] == opus and self.matr[x-i-1][y-i-1] == jucator:
                return True
            if self.matr[x-i][y-i] == jucator or self.matr[x-i][y-i] == Joc.GOL:
                break

        # verificare diagonala /
        for i in range(1, min(x + 1, Joc.NR_COLOANE - y) - 1, 1):
            if self.matr[x - i][y + i] == opus and self.matr[x - i - 1][y + i + 1] == jucator:
                return True
            if self.matr[x - i][y + i] == jucator or self.matr[x - i][y + i] == Joc.GOL:
                break
        for i in range(1, min(Joc.NR_LINII - x, y + 1) - 1, 1):
            if self.matr[x + i][y - i] == opus and self.matr[x + i + 1][y - i - 1] == jucator:
                return True
            if self.matr[x + i][y - i] == jucator or self.matr[x + i][y - i] == Joc.GOL:
                break
        # nu am gasit potriviri
        return False

    def aplica_miscare(self, miscare, jucator):
        (x, y) = miscare
        opus = jucator_op(jucator)

        # cautare coloana
        for i in range(x + 1, Joc.NR_LINII - 1, 1):
            if self.matr[i][y] == opus and self.matr[i + 1][y] == jucator:
                for k in range(x+1, i + 1, 1):
                    self.matr[k][y] = jucator
            if self.matr[i][y] == jucator or self.matr[i][y] == Joc.GOL:
                break
        for i in range(x - 1, 0, -1):
            if self.matr[i][y] == opus and self.matr[i - 1][y] == jucator:
                for k in range(x-1, i - 1, -1):
                    self.matr[k][y] = jucator
            if self.matr[i][y] == jucator or self.matr[i][y] == Joc.GOL:
                break

        # verificare linie
        for j in range(y + 1, Joc.NR_COLOANE - 1, 1):
            if self.matr[x][j] == opus and self.matr[x][j + 1] == jucator:
                for k in range(y+1, j + 1, 1):
                    self.matr[x][k] = jucator
            if self.matr[x][j] == jucator or self.matr[x][j] == Joc.GOL:
                break
        for j in range(y - 1, 0, -1):
            if self.matr[x][j] == opus and self.matr[x][j - 1] == jucator:
                for k in range(y-1, j + 1, 1):
                    self.matr[x][k] = jucator
            if self.matr[x][j] == jucator or self.matr[x][j] == Joc.GOL:
                break

        # verificare diagonala \
        for i in range(1, min(Joc.NR_LINII - x, Joc.NR_COLOANE - y) - 1, 1):
            if self.matr[x + i][y + i] == opus and self.matr[x + i + 1][y + i + 1] == jucator:
                for k in range(1, i+1, 1):
                    self.matr[x + k][y + k] = jucator
            if self.matr[x + i][y + i] == jucator or self.matr[x + i][y + i] == Joc.GOL:
                break
        for i in range(1, min(x, y), 1):
            if self.matr[x - i][y - i] == opus and self.matr[x - i - 1][y - i - 1] == jucator:
                for k in range(1, i + 1, 1):
                    self.matr[x - k][y - k] = jucator
            if self.matr[x - i][y - i] == jucator or self.matr[x - i][y - i] == Joc.GOL:
                break

        # verificare diagonala /
        for i in range(1, min(x + 1, Joc.NR_COLOANE - y) - 1, 1):
            if self.matr[x - i][y + i] == opus and self.matr[x - i - 1][y + i + 1] == jucator:
                for k in range(1, i + 1, 1):
                    self.matr[x - k][y + k] = jucator
            if self.matr[x - i][y + i] == jucator or self.matr[x - i][y + i] == Joc.GOL:
                break
        for i in range(1, min(Joc.NR_LINII - x, y + 1) - 1, 1):
            if self.matr[x + i][y - i] == opus and self.matr[x + i + 1][y - i - 1] == jucator:
                for k in range(1, i + 1, 1):
                    self.matr[x + k][y - k] = jucator
            if self.matr[x + i][y - i] == jucator or self.matr[x + i][y - i] == Joc.GOL:
                break
        # punem si piesa curenta
        self.matr[x][y] = jucator

    def mutari_joc(self, jucator):
        l_mutari = []

        # cautam toate miscarile valide
        for i in range(Joc.NR_LINII):
            for j in range(Joc.NR_COLOANE):
                if not self.miscare_valida((i, j), jucator):
                    continue
                # miscarea e valida creeaza un Joc nou si apoi aplica miscarea
                joc_nou = Joc(copy.deepcopy(self.matr))
                joc_nou.aplica_miscare((i, j), jucator)
                l_mutari.append(joc_nou)

        # verificam cazul in care nu am generat miscari noi adaugam o stare cu tabla identica
        if len(l_mutari) == 0:
            joc_nou = Joc(copy.deepcopy(self.matr))
            l_mutari.append(joc_nou)
        return l_mutari

    def fct_euristica(self):
        # numarul de piese JMAX - JMIN
        return scor(self.matr, Joc.JMAX) - scor(self.matr, Joc.JMIN)

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
        sir = '   '
        for nr_col in range(self.NR_COLOANE):
            sir += chr(ord('a') + nr_col) + ' '
        sir += '\n'
        sir += '  '
        for nr_col in range(self.NR_COLOANE-1):
            sir += '--'
        sir += '-\n'

        for i in range(self.NR_LINII):
            sir += str(i) + ' |'
            for j in range(self.NR_COLOANE):
                sir += str(self.matr[i][j]) + " "
            sir += "\n"
        return sir

    def afis_smart(self, jucator):
        sir = '   '
        for nr_col in range(self.NR_COLOANE):
            sir += chr(ord('a') + nr_col) + ' '
        sir += '\n'
        sir += '  '
        for nr_col in range(self.NR_COLOANE - 1):
            sir += '--'
        sir += '-\n'

        for i in range(self.NR_LINII):
            sir += str(i) + ' |'
            for j in range(self.NR_COLOANE):
                if self.matr[i][j] == Joc.GOL and self.miscare_valida((i,j), jucator):
                    sir += "* "
                else:
                    sir += str(self.matr[i][j]) + " "
            sir += "\n"
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

    # creare stare initiala (negru joaca primul)
    stare_curenta = Stare(tabla_curenta, Joc.SIMBOLURI_JUC[1], Stare.ADANCIME_MAX)

    linie = -1
    coloana = -1
    while True:
        # verificare daca poate juca(nu se poate ca ambii sa fie blocati, altfel se termina jocul si afisam castigator)
        if not stare_curenta.tabla_joc.exista_miscare(stare_curenta.j_curent):
            # dam tura celuilalt
            stare_curenta.j_curent = stare_curenta.jucator_opus()

        if stare_curenta.j_curent == Joc.JMIN:
            # afisare tabla ajutatoare
            print("* sunt pozitii valide")
            print(stare_curenta.tabla_joc.afis_smart(stare_curenta.j_curent))
            # muta jucatorul
            raspuns_valid = False
            while not raspuns_valid:
                try:
                    linie = int(input("linia = "))
                    coloana = input("coloana = ")
                    if not coloana.isalpha():
                        raise ValueError('Coloana nu e caracter')

                    # verificare linie,coloana in interval corect
                    if linie < 0 or linie >= Joc.NR_LINII:
                        print("Linie invalida (trebuie sa fie un numar intre 0 si {}).".format(Joc.NR_COLOANE - 1))
                    elif coloana < 'a' or coloana >= chr(ord('a') + Joc.NR_COLOANE):
                        print("Coloana invalida (trebuie sa fie un caracter intre a si {}).".format(chr(ord('a') + Joc.NR_COLOANE)))
                    else:
                        coloana = ord(coloana) - ord('a')
                        # cautare si verificare pozitie valida
                        if not stare_curenta.tabla_joc.miscare_valida((linie, coloana), Joc.JMIN):
                            print("Miscare invalida")
                        else:
                            raspuns_valid = True

                except ValueError:
                    print("Linia trebuie sa fie un numar intreg, coloana un caracter.")

            # dupa iesirea din while sigur am valida coloana
            # facem miscarea
            stare_curenta.tabla_joc.aplica_miscare((linie, coloana), Joc.JMIN)

            # afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            # print(str(stare_curenta))
            print(stare_curenta.tabla_joc.afis_smart(stare_curenta.jucator_opus()))
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
