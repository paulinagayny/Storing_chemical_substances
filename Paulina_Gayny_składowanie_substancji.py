# -*- coding: utf-8 -*-

from collections import defaultdict
import numpy

#jesli chodzi o niemozliwosc sasiadowania to zakladam kazdy z kazdym ze nie moze z podanej grupy
class Graf:
    #Lista sąsiedztwa jako pythonowski słownik defaultdict
    
    def __init__(self, V) :
        self.lista_sasiedztwa = defaultdict(list) #na początku pusta lista - będę tu przechowywać nazwy substancji jako klucze do list sąsiadów (okreslonych swoimi nazwami)
        self.kolory = defaultdict(int) #również jako słownik implementuję, kluczem będą tu nazwy substancji a wartosciami ich kolory
        self.V = V #liczba wierzchołków
        self.ile_zaj = 0 #ile zajętych kolorów
        self.grupy = defaultdict(list) #przydzielone grupom poszczególnych list nazw subst.
        
        #dodaję krawędź tylko jesli wierzchołki już nie są sąsiadami
        #żeby uniknąć powtórzeń.
        #(jest sens sprawdzać tylko dla istniejących już w słowniku elementów)
    def Dodaj_krawedz(self, nazwa_subst_1, nazwa_subst_2) :
        
            if nazwa_subst_1 in self.lista_sasiedztwa and nazwa_subst_2 in self.lista_sasiedztwa:
                
                sasiedzi_1 = self.lista_sasiedztwa[nazwa_subst_1]
                for s in range(len(sasiedzi_1)):
                    
                    if nazwa_subst_2 == sasiedzi_1[s]:
                        return
                        
                sasiedzi_2 = self.lista_sasiedztwa[nazwa_subst_2]
                for k in range(len(sasiedzi_2)):
                    
                    if nazwa_subst_1 == sasiedzi_2[k]:
                        return
                
                self.lista_sasiedztwa[nazwa_subst_1].append(nazwa_subst_2)
                self.lista_sasiedztwa[nazwa_subst_2].append(nazwa_subst_1)
                
            else:
                self.lista_sasiedztwa[nazwa_subst_1].append(nazwa_subst_2)
                self.lista_sasiedztwa[nazwa_subst_2].append(nazwa_subst_1)
                

    def Narysuj_graf(self) :
        for wezel in self.lista_sasiedztwa.items() :
            print(wezel)


    #obliczenie najwyższego stopnia wierzchołka
    def Najw_Stopien(self):
        s_max = -1
        for wezel in self.lista_sasiedztwa:
            sasiedzi = self.lista_sasiedztwa[wezel]
            s = len(sasiedzi)
            if s > s_max:
                s_max = s
        return s_max
    
    def Kolory_dost(self):
        #zakładam tyle dostępnych kolorów jak k - kolorowalny jest graf
        #zgodnie z tw. dla grafu prostego o najw. stopniu wierzchołka s graf jest (s + 1) - kolorowalny
        C = []
        
        for i in range(self.Najw_Stopien() + 1):
            C.append(i) #kolory (grupy substancji) 0, 1, 2, ..., s  czyli (s + 1) kolorów

        return C
    
    
    def Koloruj_wezel(self, nazwa_subst):
        
        #jesli to w ogole jest substancja w naszym grafie
        if nazwa_subst in self.lista_sasiedztwa:
            
            if nazwa_subst in self.kolory:
                #już ma kolor, więc już nic nie robimy
                return
            
            else:
                #jesli nie ma swojego koloru
                
                C = self.Kolory_dost()
                sasiedzi = self.lista_sasiedztwa[nazwa_subst]
                    
                while nazwa_subst not in self.kolory:
                    #dla każdego koloru
                    for k in range(len(C)):
                        if nazwa_subst not in self.kolory:
                            kolor = C[k] #tymczasowo
                                
                            #sprawdzamy kolory sąsiadów
                            for l in range(len(sasiedzi)):
                                #jesli sasiad ma w ogóle kolor
                                if sasiedzi[l] in self.kolory:
                                    if self.kolory[sasiedzi[l]] == kolor:
                                        kolor = -1
                                
                            #pierwszy kolor nierowny kolorowi żadnego z sąsiadów
                            if kolor != -1:
                                self.kolory[nazwa_subst] = kolor
                    
        else:
            return "substancji nie ma w liscie sasiedztwa"
        
    
    def Kolorowanie_grafu(self):

        for substancja in self.lista_sasiedztwa: 
            #dla każdej substancji
            self.Koloruj_wezel(substancja)
            self.ile_zaj = self.ile_zaj + 1 #aktualizacja liczby zajętych kolorów/grup
        
        self.Wyswietl_podzial_na_grupy()

    def Dodaj_do_grupy(self, nazwa_subst):
        
        #można odkomentować żeby zobaczyć podział na kolory jeszcze bez uporządkowania do ładniejszego wyswietlenia
        #for nazwa_subst in self.kolory:
            #print(nazwa_subst, "grupa", self.kolory[nazwa_subst])
        
        for i in range(self.ile_zaj):
            if nazwa_subst in self.lista_sasiedztwa and nazwa_subst in self.kolory:
                if self.kolory[nazwa_subst] == i:
                    self.grupy[i].append(nazwa_subst)
    
    def Dodaj_do_grup(self):
         
        for substancja in self.lista_sasiedztwa:
            self.Dodaj_do_grupy(substancja)
            
    def Wyswietl_podzial_na_grupy(self):
        
        self.Dodaj_do_grup()
        
        ile_grup = len(self.grupy.items())
        print("Graf jest", ile_grup, "- kolorowalny. Podział substancji nie mogących ze sobą sąsiadować na", ile_grup, "grup (kolorów) tak by można było je bezpiecznie składować:\n")
        
        for grupa in self.grupy:
            print("grupa", grupa, self.grupy[grupa])
        

#teraz funkcje bardziej specyficzne dla naszego zadania, mniej ogólne
    
#implementacja grafu w postaci listy sąsiedztwa implementowanej za pomocą słownika dla podanych przez użytkownika relacji między substancjami
def Graf_substancji(wejscie):
    tab_str = Oczysc_ze_sr(wejscie)
    
    tablice = Tablice(wejscie) #tablice to tablice tablic po rozdz. srednikami, tablica to tablica legendy
    rozmiar = len(tab_str)
    graf = Graf(rozmiar)
    
    for i in range(len(tablice)): #dla wszystkich tablic między srednikowych
        
        for k in range(len(tablice[i])): #dla każdej indywidualnej tablicy
            for l in range(k + 1, len(tablice[i])):
                graf.Dodaj_krawedz(tablice[i][k], tablice[i][l])
    
    return graf
                
#oczyszczenie wejscia ze sredników
def Oczysc_ze_sr(wejscie): 
    data = wejscie.split()
    rozmiar = len(data) - Ile_sredn(data)
    tab = []
    for i in range(len(data)):
        if data[i] != ";":
            tab.append(data[i])
    return tab

#ile sredników w podanym tekscie
def Ile_sredn(data):
    l = 0
    for g in range(len(data)):
        if data[g] == ";":
            l = l + 1
    return l

def Tablice(wejscie):
    
    data = wejscie.split()  
    
    rozmiar = Ile_sredn(data) + 1
    graf = Graf(rozmiar)
    
    tablice = []
    for r in range(rozmiar):
        tablice.append([])
    
    srednik = -1
    i = 0
    while i < rozmiar:
        l = srednik + 1   
        #print("l", l)
        while l < len(data) and data[l] != ";":

            tablice[i].append(data[l])
            l = l + 1
            
        if l < len(data) and data[l] == ";":
            srednik = l
            
        i = i + 1
            
    return tablice
        
#TESTY
print("Wpisz: nazwa substancji chemicznej [SPACJA] nazwa substancji z którą nie może sąsiadować [SPACJA] nazwa kolejnej substancji z którą nie może sąsiadować [SPACJA] (i tak dalej)\n") 
print("Kolejne podawane substancje których niemożliwości sąsiadowania podajemy rozdzielane są średnikiem ';'\n")
print("Przykład:")
print("amoniak cyjanek kadm ; kadm rtęć ołów ; formalina rtęć nikotyna jod strychnina ; nikotyna jod brom\n")
print("Zapis ten oznacza że amoniak nie może sąsiadować z cyjankiem i kadmem, kadm z rtęcią i ołowiem, formalina z rtęcią, nikotyną, jodem i strychniną, a nikotyna z jodem i bromem\n")

input_testowy = "amoniak cyjanek kadm ; kadm rtęć ołów ; formalina rtęć nikotyna jod strychnina ; nikotyna jod brom\n"

graf = Graf_substancji(input_testowy)

print("Otrzymany graf w postaci listy sąsiedztwa zaimplementowanej w postaci słownika defaultdict:\n")
graf.Narysuj_graf()

print("\n")
graf.Kolorowanie_grafu()