SOUBOR = open("kandidatka.txt", "r")
MANDATY = 15


def nacti_kandidatku(soubor):
    kandidatka = []
    strana_jmeno = ""
    strana_kandidati = []
    for radek in soubor:
        if str(radek[0]) not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"] and len(radek) > 5:
            strana_jmeno = radek
        elif len(radek) > 5:
            strana_kandidati.append(radek)
        else:
            kandidatka.append((strana_jmeno, strana_kandidati))
            strana_jmeno = ""
            strana_kandidati = []
    return kandidatka


def zpracuj_volice(kandidatka, MANDATY):
    volic = []
    zakrizkoval_stranu = False
    krizky_celkem = 0
    for strana in kandidatka:
        print(strana[0][:-1])
        strana_hlasy = [False] * len(strana[1])
        if krizky_celkem == MANDATY:
            volic.append((strana[0], False, strana_hlasy))
            continue
        if not zakrizkoval_stranu:
            krizek = input("Přejete si dát křížek straně: " + strana[0])
            if krizek:
                zakrizkoval_stranu = True
                krizky_celkem += 1
                volic.append((strana[0], True, strana_hlasy))
                continue
        for index_kandidata in range(len(strana[1])):
            krizek = input("Přejete si dát křížek: " +
                           strana[1][index_kandidata])
            if krizek:
                krizky_celkem += 1
                strana_hlasy[index_kandidata] = True
            if krizky_celkem == MANDATY:
                break
        volic.append((strana[0], False, strana_hlasy))
    upravene_strany = []
    for strana in volic:
        if strana[1]:
            pocet_krizku = max([(len(strana[2]) - krizky_celkem + 1), 0])
            strana = (strana[0], False, [True] * pocet_krizku
                      + [False] * (len(strana[2]) - pocet_krizku))
        upravene_strany.append((strana[0], strana[2]))
    return upravene_strany


def secti_strany(volici, kandidatka):
    hlasy = kandidatka.copy()
    for i in range(len(hlasy)):
        hlasy[i] = (hlasy[i][0], [("", 0)] * len(hlasy[i][1]))

    for volic in volici:
        for index_strany in range(len(kandidatka)):
            for index_kandidata in range(len(hlasy[index_strany][1])):
                hlasy[index_strany][1][index_kandidata] = (
                    kandidatka[index_strany][1][index_kandidata],
                    hlasy[index_strany][1][index_kandidata][1] +
                    (1 if volic[index_strany][1][index_kandidata] else 0)
                )
    return [(strana[0], sum(map(lambda x: x[1], strana[1])), strana[1]) for strana in hlasy]


def odstran_pod_5_procent(strany, hlasy_celkem):
    serazene_strany = sorted(strany, key=lambda x: x[1], reverse=True)
    strany = list(filter(lambda x: x[1] > hlasy_celkem*0.05, serazene_strany))
    return strany if len(strany) > 1 else serazene_strany[:2]


def dhondtova_metoda(hlasy, MANDATY):
    mandaty_stran = [0] * len(hlasy)
    nezmene_hlasy = hlasy.copy()
    for _ in range(MANDATY):
        nejvice_hlasu = max(hlasy, key=lambda x: x[1])
        index = hlasy.index(nejvice_hlasu)
        mandaty_stran[index] += 1
        hlasy[index] = (hlasy[index][0], nezmene_hlasy[index][1] /
                        (1 + mandaty_stran[index]), hlasy[index][2])
    return [(nezmene_hlasy[i][0], nezmene_hlasy[i][1], nezmene_hlasy[i][2], mandaty_stran[i]) for i in range(len(hlasy))]


def serad_strany(strany):
    nove_strany = []
    for strana in strany:
        kandidati = strana[2].copy()
        prumer_hlasu = strana[1] / len(kandidati)
        nad_110_procent = []
        for kandidat in kandidati:
            if kandidat[1] > prumer_hlasu*1.1:
                nad_110_procent.append(kandidat)
        for kandidat in nad_110_procent:
            kandidati.remove(kandidat)
        nad_110_procent = sorted(nad_110_procent, key=lambda x: x[1] + (
            1 - int(x[0].partition(".")[0])/len(strana[2])), reverse=True)  # takovy tricek
        kandidati = nad_110_procent + kandidati
        nove_strany.append((strana[0], strana[1], kandidati, strana[3]))
    return nove_strany


def vygeneruj_vysledky(strany):
    vysledky = []
    for strana in strany:
        strana_postupjici = []
        for i in range(strana[3]):
            strana_postupjici.append(strana[2][i])
        vysledky.append((strana[0], strana_postupjici))
    return vysledky


def zpracuj_vsechny_volice(kandidatka, MANDATY):
    volici = []
    while True:
        vstup = input("Přejete si sečíst hlasy?")
        if vstup:
            break
        volici.append(zpracuj_volice(kandidatka, MANDATY))
    strany = secti_strany(volici, kandidatka)
    print()

    for strana in strany:
        print(strana[0][:-1])
        for kandidat in strana[2]:
            print(kandidat[0][:-1] + ": " + str(kandidat[1]))
        print("Celkem hlasů pro stranu: " + str(strana[1]) + "\n")
    return strany


def zpracuj_zadani_souctu(kandidatka):
    volici = []
    for strana in kandidatka:
        print(strana[0][:-1])
        hlasy = []
        for kandidat in strana[1]:
            while True:
                pocet_hlasu = input(kandidat[:-1] + ": ")
                try:
                    if pocet_hlasu == "":
                        pocet_hlasu = 0
                    elif int(pocet_hlasu) < 0:
                        raise TypeError("Pouze kladná čísla jsou povolena.")
                    hlasy.append((kandidat, int(pocet_hlasu)))
                    break
                except:
                    print("Počet hlasů musí být nezáporné celé číslo.")
        volici.append((strana[0], sum(map(lambda x: x[1], hlasy)), hlasy))
        print()
    return volici


def main():
    kandidatka = nacti_kandidatku(SOUBOR)

    vstup = input("Chcete zahájit sbírání hlasů (enter), nebo zadat součet? ")
    if vstup:
        strany = zpracuj_zadani_souctu(kandidatka)
    else:
        strany = zpracuj_vsechny_volice(kandidatka, MANDATY)

    hlasy_celkem = sum(map(lambda x: x[1], strany))
    bez_5_procent = odstran_pod_5_procent(strany, hlasy_celkem)

    print("Strany po odstranění těch, které nedosáhly 5 %: ")
    for strana in bez_5_procent:
        print(strana[0][:-1])
    print()

    s_mandaty = dhondtova_metoda(bez_5_procent, MANDATY)

    print("Počty mandátů stran: ")
    for strana in s_mandaty:
        print(strana[0][:-1] + ": " + str(strana[3]))
    print()

    serazene_strany = serad_strany(s_mandaty)
    vysledky = vygeneruj_vysledky(serazene_strany)
    print("Mandáty získali: ")
    for strana in vysledky:
        print("Za stranu " + strana[0][:-1])
        for kandidat in strana[1]:
            print(kandidat[0][:-1] + ": " + str(kandidat[1]))
        print()
    return vysledky


if __name__ == "__main__":
    main()
