kandidatka = open("kandidatka.txt", "r")
MANDATY = 3
inputarray = [("StranaA", [("petr novotny", 5), ("ludek novotny", 10)]), ("StranaB", [
    ("petr novak", 1)]), ("StranaC", [("alois cerny", 0), ("petr cerny", 12)])]
jmena_stran = []
nadpetprocent = []
celkemkrizku = 0
for strana in inputarray:
    jmena_stran.append(strana[0])
# vypocitava krizky jednotlivych stran----------------------------------------------------------
krizkystrany = []
j = 0
for j in range(len(inputarray)):  # tolikrat, kolik je stran prida nulu do arraye
    krizkystrany.append(0)
    for i in range(len(inputarray[j][1])):  # pocet kandidatu ve strane
        # pricitani krizku od jednotlivych kandidatu ke spravne strane
        krizkystrany[j] += inputarray[j][1][i][1]
        i += 1
    i = 0
    j += 1
print(krizkystrany)
# Pocita krizky celkem------------------------------------------------------------------------
for j in range(len(inputarray)):  # pocet stran
    celkemkrizku += krizkystrany[j]
    j += 1
print(celkemkrizku)
# vypocitava 5% a vyhazuje strany pod 5%----------------------------------------------------------
petprocent = round(celkemkrizku/100*5, 3)
nadpetprocent_strany = []
j = 0
print(len(krizkystrany))
while len(nadpetprocent) < 2:
    for j in range(len(krizkystrany)):  # zjistim jestli vsechny strany presahli 5%
        if krizkystrany[j] >= petprocent:
            nadpetprocent.append(krizkystrany[j])
            nadpetprocent_strany.append(inputarray[j])
        j += 1
    petprocent -= 0.001
print("nadpetprocent")
print(nadpetprocent)
# #D'Hondtova metoda------------------------------------------------------------------------------

mandatystrany = []
for j in range(len(nadpetprocent)):  # tolikrat, kolik je stran prida nulu do arraye
    mandatystrany.append(0)
nejvic = 0
while MANDATY > 0:  # Rozdava mandaty
    max = nadpetprocent[0]
    j = 0
    for j in range(0, len(nadpetprocent)):
        if nadpetprocent[j] > max:
            max = nadpetprocent[j]
        j += 1
    nejvic = nadpetprocent.index(max)
    MANDATY -= 1
    mandatystrany[nejvic] += 1
    nadpetprocent[nejvic] /= 2
# print(nadpetprocent)
# print(mandatystrany)

pocetkandidatu = []
pocetkandidatuvestrane = 0
j = 0
for j in range(len(nadpetprocent)):  # vypocitava pocty kandidatu ve stranach nad 5%
    pocetkandidatuvestrane = len(nadpetprocent_strany[j][1])
    pocetkandidatu.append(pocetkandidatuvestrane)
print(pocetkandidatu)
# poradi kandidatu -------------------------------------------------------------------------------------------------------------
j = 0
for j in range(len(nadpetprocent_strany)):
    i = 0
    # projde vsechny kandidaty, jestli nemaji vice nez 10% nad prumerem a prohazi poradi na kandidatce
    for i in range(pocetkandidatu[j]):
        prumerstrany = krizkystrany[j]/pocetkandidatu[j]
        if nadpetprocent_strany[j][1][i][1] >= prumerstrany*1.1:
            naprvnimisto = nadpetprocent_strany[j][1][i]
            nadpetprocent_strany[j][1].remove(naprvnimisto)
            nadpetprocent_strany[j][1].insert(0, naprvnimisto)
        i += 1
    j += 1
j = 0
# vyhozeni ostatnich kandidatu -------------------------------------------------------------------------------------------------------
KONECNEPORADI = nadpetprocent_strany
for j in range(len(nadpetprocent_strany)):  # vyhazuje nadbytecne kandidaty
    pocetpop = pocetkandidatu[j]-mandatystrany[j]
    for pocetpop in range(pocetpop, 0, -1):
        KONECNEPORADI[j][1].pop()

print(KONECNEPORADI)
