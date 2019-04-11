import csv
import pandas as pd
import itertools
import math
import decimal
from Graph import *
import random
nodi=[]
tabdati=[]
d=[]
nodi_dict={}
g=""
graph={}
nij=[]
totsecondo=[]
totprimo=[]

class learn():

    def __init__(self, data):
        self.data=data
        self.createdataframe()
        self.inittab()


    def createdataframe(self):#funzione per creare il dataframe dal file passato in ingresso contenente i record
        with open(self.data) as filecsv:
            lettore=csv.reader(filecsv, delimiter=",")#legge file csv in cui ci sono i vari record


            global nodi #variabile globale in cui vengono inseriti i nomi dei nodi del grafo
            nodi=next(lettore) #inserimento nodi nella variabile globale


            global nodi_dict #dizionario con cui vengono codificati i vari nodi del grafo
            for riga in range(nodi.__len__()): #inserimento nodi codificati nel dizionario e nel grafo
                nodi_dict[nodi[riga]]=riga
                graph[nodi[riga]]=[]


            global g
            g=Graph(graph)#generazione del grafo con la classe Graph


            global d #array globale in cui vengono inseriti i vari record del file da studiare per arrivare a costruire il grafo
            for riga in lettore: #inserimento record nell'array globale
                d.append(riga)

            global dati
            dati=pd.DataFrame(d, columns=nodi) #inserisco i dati che ho in un dataframe sottoforma di tabella per poterli analizzare tramite pandas


    def inittab(self):#funzione per costruire la tabella del grafo
        tabella= []
        for i in range(nodi.__len__()): #costruisce la tabella vuota che sara poi il grafo cercato
            riga=[]
            for j in range(nodi.__len__()):
                riga.append(0)
            tabella.append(riga)
        self.rand_tab(tabella, None, None)#richiamo la funzione rand_tab
        massimo=self.alg(tabella,None)#richiamo la funzione alg per calcolare la scoring_function iniziale
        print tabella
        print massimo
        g.stampa()
        self.structure(tabella, massimo, False)#richiamo la funzione structure per massimizzare la scoring_function

    def rand_tab(self,tab,a,b):#crea un grafo inserendo archi in modo casuale garantendo l'aciclicita
        if (a!=None):
            g.add_edge(nodi[a],nodi[b])
            tab[a][b]=1
            controllo=g.find_cicle()#richiamo la funzione find_cicle della classe graph per controllare che il grafo sia aciclico
            if controllo!="DAG":#se aciclico ok
                g.delete_edge(nodi[a],nodi[b])
                tab[a][b]=0
        nodi_isolati=g.find_isolated_nodes()
        if (len(nodi_isolati)!=0):
            padre=random.randint(0,nodi.__len__()-1)
            figlio=random.randint(0,nodi.__len__()-1)
            while padre==figlio:
                figlio=random.randint(0,nodi.__len__()-1)
            self.rand_tab(tab,padre,figlio)

    def structure(self,tab,massimo,find):#funzione per generare tutte le possibili strutture del grafo
        poss_mosse=[]
        if find==False:#se find==true sono arrivato alla conclusione e stampo i risultati
            e=nodi.__len__()
            for i in range(e):#aggiungo tutte le possibili variazioni del grafo nell'array poss_mosse
                for j in range(e):
                    mossa=[]
                    if i!=j:
                        if tab[j][i]==1:
                            g.delete_edge(nodi[j],nodi[i])
                            controllo=g.find_cicle()#richiamo la funzione find_cicle della classe graph per controllare che il grafo sia aciclico
                            nodi_isolati=g.find_isolated_nodes()
                            if (len(nodi_isolati)==0):
                                if controllo=="DAG":#se aciclico ok
                                    mossa.append("D")
                                    mossa.append(j)
                                    mossa.append(i)
                            g.add_edge(nodi[j],nodi[i])
                        else:
                            if tab[i][j]==1:
                                g.delete_edge(nodi[i],nodi[j])
                                g.add_edge(nodi[j],nodi[i])
                                controllo=g.find_cicle()
                                nodi_isolati=g.find_isolated_nodes()
                                if controllo=="DAG":#se aciclico ok
                                    mossa.append("C")
                                    mossa.append(j)
                                    mossa.append(i)
                                g.delete_edge(nodi[j],nodi[i])
                                g.add_edge(nodi[i],nodi[j])
                            else:
                                g.add_edge(nodi[j],nodi[i])
                                controllo=g.find_cicle()#richiamo la funzione find_cicle della classe graph per controllare che il grafo sia aciclico
                                nodi_isolati=g.find_isolated_nodes()
                                if controllo=="DAG":#se aciclico ok
                                    mossa.append(j)
                                    mossa.append(i)
                                g.delete_edge(nodi[j],nodi[i])
                        if controllo=="DAG" and (len(nodi_isolati)==0):
                            poss_mosse.append(mossa)
            find,massimo,tab=self.maximize(tab,poss_mosse,massimo)#richiamo la funzione maximize per cercare il massimo tra le possibili variazioni
            self.structure(tab,massimo,find)#richiamo questa funzione per ripetere l'azione
        else:
            print(tab)
            g.stampa()
            print massimo

    def maximize(self,tab,poss_mosse,massimo):#cerca il massimo tra le possibili varizioni del grafo
        max=massimo
        mossa_max=[]
        for i in range(len(poss_mosse)):
            if len(poss_mosse[i])==3:
                control=poss_mosse[i][0]
                padre=poss_mosse[i][1]
                figlio=poss_mosse[i][2]
                if control=="D":
                    tab[padre][figlio]=0
                    temp, temp_totprimo, temp_totsecondo= self.alg(tab,figlio)
                    tab[padre][figlio]=1
                else:
                    tab[padre][figlio]=1
                    tab[figlio][padre]=0
                    temp, temp_totprimo, temp_totsecondo= self.alg(tab,figlio)
                    tab[padre][figlio]=0
                    tab[figlio][padre]=1
            else:
                padre=poss_mosse[i][0]
                figlio=poss_mosse[i][1]
                tab[padre][figlio]=1
                temp, temp_totprimo, temp_totsecondo=self.alg(tab,figlio)
                tab[padre][figlio]=0
            print temp
            if temp>max:
                mossa_max=[]
                max=temp
                mossa_max.append(padre)
                mossa_max.append(figlio)
                mossa_max.append(temp_totprimo)
                mossa_max.append(temp_totsecondo)
        print "nuova configurazione"
        print max
        print massimo
        if max!=massimo:
            global totprimo
            global totsecondo
            padre=mossa_max[0]
            figlio=mossa_max[1]
            t_totprimo=mossa_max[2]
            t_totsecondo=mossa_max[3]
            totprimo[padre]=t_totprimo
            totsecondo[padre]=t_totsecondo
            if tab[padre][figlio]==0:
                if tab[figlio][padre]==1:
                    print "C"
                    print nodi[padre]
                    print nodi[figlio]
                    tab[padre][figlio]=1
                    tab[figlio][padre]=0
                    g.delete_edge(nodi[figlio],nodi[padre])
                    g.add_edge(nodi[padre],nodi[figlio])
                else:
                    print nodi[padre]
                    print nodi[figlio]
                    tab[padre][figlio]=1
                    g.add_edge(nodi[padre],nodi[figlio])
            else:
                print "D"
                print nodi[padre]
                print nodi[figlio]
                tab[padre][figlio]=0
                g.delete_edge(nodi[padre],nodi[figlio])
        if max==massimo:
            return True,max,tab
        else:
            print max
            print tab
            g.stampa()
            return False,max,tab


    def alg(self, tab, nodo):#algoritmo per trovare la migliore struttura del grafo da generare
        sum_padre=[]
        for i in range(nodi.__len__()):#inserimento dei nodi padre di ogni nodo nell'array chiamato sum_padre
            padre=[]
            for j in range(nodi.__len__()):
                if i!=j and tab[j][i]==1:
                    padre.append(nodi[j])
            sum_padre.append(padre)

        confnodo=[]
        for i in range(nodi.__len__()):
            confno=[]
            grouped = dati.groupby(nodi[i]) #uso groupby per raggruppare i dati in base a cosa mi serve
            for name,group in grouped: #va usata per trovare le possibili configurazioni di ogni nodo
                confno.append(name)
            confnodo.append(confno)
        if nodo==None:
            global nij
            global totsecondo
            global totprimo
            for i in range(nodi.__len__()): #per ogni nodo svolgo il for per calcolare la funzione da massimizzare
                it=[] #inizializzo l'array in cui ci metto tutte le varie combinazioni possibili del nodo con i propri genitori
                count=1
                alfa=0
                nf=int(nodi_dict[nodi[i]])
                for j in range(confnodo[nf].__len__()):#aggiungo le configurazioni del nodo selezionato
                    figlio='1'
                    n=nodi_dict[nodi[i]]
                    nodo=str(n)
                    c=confnodo[i][j]
                    conf=str(c)
                    fusion=figlio+nodo+conf
                    it.append(fusion)
                    alfa=alfa+1
                for k in range(sum_padre[i].__len__()):#seleziono i nodi genitori tramite l'array sum_padre
                    padre='0'
                    count=count+1
                    p=sum_padre[i][k]
                    np=int(nodi_dict[p])
                    for l in range(confnodo[np].__len__()):#aggiungo le configurazioni dei nodi genitori
                        n=nodi_dict[p]
                        nodo=str(n)
                        c=confnodo[np][l]
                        conf=str(c)
                        fusion=padre+nodo+conf
                        it.append(fusion)
                it.sort()#ordino l'array in modo che il nodo selezionato sia in fondo a ogni record dell'array
                pp=self.configurator(it, count)#richiamo la funzione configurator per generarmi le possibili configurazioni passandogli l'array i
                temp_nij, temp_totsecondo=self.calc(pp, confnodo, nf)#richiamo la funzione calc per calcolarmi gli nijk
                nij.append(temp_nij)
                secondo=1
                for j in range(temp_totsecondo.__len__()):#trovo i secondi fattori della funzione
                    secondo=secondo*temp_totsecondo[j]
                totsecondo.append(secondo)
                primo=1
                for j in range(temp_nij.__len__()):#trovo i primi fattori della funzione
                    dividendo=alfa
                    divisore=alfa+temp_nij[j]
                    totale=self.fattori(dividendo, divisore)
                    primo=primo*totale
                totprimo.append(primo)
            blocco_1=1
            blocco_2=1
            tot=1
            for i in range(nodi.__len__()):#trovo il valore moltiplicato o sommato del primo e secondo membro della funzione
                blocco_1=blocco_1*totprimo[i]
                blocco_2=blocco_2*totsecondo[i]
            tot=blocco_1*blocco_2 #totale della funzione da massimizzare che restituisco
            return tot
        else:
            it=[] #inizializzo l'array in cui ci metto tutte le varie combinazioni possibili del nodo con i propri genitori
            count=1
            alfa=0
            for j in range(confnodo[nodo].__len__()):#aggiungo le configurazioni del nodo selezionato
                figlio='1'
                n=nodi_dict[nodi[nodo]]
                nodod=str(n)
                c=confnodo[nodo][j]
                conf=str(c)
                fusion=figlio+nodod+conf
                it.append(fusion)
                alfa=alfa+1
            for k in range(sum_padre[nodo].__len__()):#seleziono i nodi genitori tramite l'array sum_padre
                padre='0'
                count=count+1
                p=sum_padre[nodo][k]
                np=int(nodi_dict[p])
                for l in range(confnodo[np].__len__()):#aggiungo le configurazioni dei nodi genitori
                    n=nodi_dict[p]
                    nodod=str(n)
                    c=confnodo[np][l]
                    conf=str(c)
                    fusion=padre+nodod+conf
                    it.append(fusion)
            it.sort()#ordino l'array in modo che il nodo selezionato sia in fondo a ogni record dell'array
            pp=self.configurator(it, count)#richiamo la funzione configurator per generarmi le possibili configurazioni passandogli l'array i
            temp_nij, temp_totsecondo=self.calc(pp, confnodo, nodo)#richiamo la funzione calc per calcolarmi gli nijk
            nij[nodo]=temp_nij
            secondo=1
            for j in range(temp_totsecondo.__len__()):#trovo i secondi fattori della funzione
                secondo=secondo*temp_totsecondo[j]
            temporaneo_totsecondo=secondo
            primo=1
            for j in range(temp_nij.__len__()):#trovo i primi fattori della funzione
                dividendo=alfa
                divisore=alfa+temp_nij[j]
                totale=self.fattori(dividendo, divisore)
                primo=primo*totale
            temporaneo_totprimo=primo
            blocco_1=1
            blocco_2=1
            tot=1
            for i in range(nodi.__len__()):#trovo il valore moltiplicato o sommato del primo e secondo membro della funzione
                if i==nodo:
                    blocco_1=blocco_1*temporaneo_totprimo
                    blocco_2=blocco_2*temporaneo_totsecondo
                else:
                    blocco_1=blocco_1*totprimo[i]
                    blocco_2=blocco_2*totsecondo[i]
            tot=blocco_1*blocco_2 #totale della funzione da massimizzare che restituisco
            return tot, temporaneo_totprimo, temporaneo_totsecondo



    def calc(self, pp, confnodo, nf):#calcola gli nij
        totsecondo=[]
        nij=[]
        sec=[]
        for l in range(confnodo[nf].__len__()):#inizializzo l'array totsecondo per poi inserirci i vari totali relativi al secondo membro della funzione
            zero=1
            totsecondo.append(zero)
        for i in range(pp.__len__()):#svolgo il for per ogni possibile configurazione
            first=dati
            sicurezza=""
            for j in range(pp[i].__len__()):#per ogni configurazione controllo ogni singolo nodo della configurazione
                parola=pp[i][j]
                par=str(parola)
                prefisso=par[1]
                pre=int(prefisso)
                configure=par[2:]
                if len(first)==0:
                    tempgroup=[]
                else:
                    temp = first.groupby(nodi[pre])
                    trovato="no"
                    for name,group in temp:
                        if name==configure:
                            trovato="si"
                    if trovato=="si":
                        tempgroup=temp.get_group(configure)
                    else:
                        tempgroup=[]
                first=tempgroup
                if (pre==nf):
                    controllo="no"
                    if nij:
                        for k in range(nij.__len__()):
                            if sec[k]==sicurezza:
                                controllo="ok"
                                nij[k]=nij[k]+len(first)
                        if controllo=="no":
                            sec.append(sicurezza)
                            nij.append(len(first))
                    else:
                        sec.append(sicurezza)
                        nij.append(len(first))
                    for k in range(confnodo[nf].__len__()):
                        if (confnodo[nf][k]==configure):
                            nprov=len(first)
                            dividendo=1+nprov
                            totale=self.fattori(dividendo, 1)
                            totsecondo[k]=totsecondo[k]*totale

                else:
                    sicurezza=sicurezza+par
        return nij, totsecondo

    def fattori(self, dividendo, divisore):#calcola la divisione e le funzioni gamma dell'espressione
        if (dividendo==1):
            x=1
        else:
            x=math.factorial(dividendo-1)
        if (divisore==1):
            y=1
        else:
            y=math.factorial(divisore-1)
        xd=decimal.Decimal(x)
        yd=decimal.Decimal(y)
        zd=xd/yd
        return zd


    def configurator(self,comb, num):#funzione per trovare tutte le possibili combinazioni dei vari nodi passati in ingresso
        tot=[]
        lst = list(itertools.combinations(comb, num))#crea la lista di possibili configurazione di tutti i record passati come ingresso

        for i in range(0,len(lst)): #ciclo for per ricavare il prefisso relativo al nodo a cui appartiene il record
            prova=[]
            for j in range(0,len(lst[i])):
                parola=lst[i][j]
                par=str(parola)
                prefisso=par[1]
                prova.append(prefisso)
            pre=[]
            stampa='si'
            for l in range(0,len(lst[i])): #ciclo per confrontare i prefissi relativi a ogni record della lista evitando ripetizioni
                if (len(pre)==0):
                    pre.append(prova[l])
                else:
                    for k in range(len(pre)):
                        if (pre[k]==prova[l]):
                            l=len(lst[i])
                            k=len(pre)
                            stampa='no'
                    if(stampa!='no'):
                        pre.append(prova[l])
            if (stampa!='no'):
                prova=[]
                for j in range(0,len(lst[i])):
                    parola=lst[i][j]
                    par=str(parola)
                    #prefisso=par[1:]
                    prova.append(par)
                #print prova
                tot.append(prova)
        return tot


frode = learn("FR.dat")
