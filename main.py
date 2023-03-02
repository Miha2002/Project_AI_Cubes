import copy
import time
import sys

class NodParcurgere:
    def __init__(self, info, parinte, cost=0, h=0, priority=0):
        self.info=info
        self.parinte=parinte #parintele din arborele de parcurgere
        self.g=cost #consider cost=1 pentru o mutare
        self.h=h
        self.f=self.g+self.h
        self.priority=priority

    def obtineDrum(self):
        l=[self]
        nod=self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod=nod.parinte
        return l
        
    def afisDrum(self, afisCost=False, afisLung=False): #returneaza si lungimea drumului
        l=self.obtineDrum()
        #am modificat functia afisDrum pentru a respecta formatul cerut
        for iNod, nod in enumerate(l):
            inaltimeMax=0
            for stiva in nod.info:
                if (len(stiva))>inaltimeMax:
                    inaltimeMax=len(stiva)
            print(iNod,")",sep='',file=fo)
            for i in reversed(range(inaltimeMax)):
                for stiva in nod.info:
                    if len(stiva)>i:
                        if int(stiva[i][:-1])<10:
                            print(stiva[i][:-1],"[",stiva[i][-1],"] ",sep='',end = '  ',file=fo)
                        else:
                            print(stiva[i][:-1],"[",stiva[i][-1],"] ",sep='',end = ' ',file=fo)
                    else:
                        print("      ",sep='',end = ' ',file=fo)
                print('',file=fo)
            print('---------------------------------\n',file=fo)
                        
        if afisCost:
            print("Cost: ", self.g, file=fo)
        if afisCost:
            print("Lungime: ", len(l), file=fo)       
        return len(l)


    def contineInDrum(self, infoNodNou):
        nodDrum=self
        while nodDrum is not None:
            if(infoNodNou==nodDrum.info):
                return True
            nodDrum=nodDrum.parinte
        
        return False
    
    def getPriority(self):
        return self.priority
        
    def __repr__(self):
        sir=""        
        sir+=str(self.info)
        return(sir)

    #euristica banală: daca nu e stare scop, returnez 1, altfel 0

    def __str__(self):
        sir=""
        maxInalt=max([len(stiva) for stiva in self.info])
        for inalt in range(maxInalt, 0, -1):
            for stiva in self.info:
                if len(stiva)< inalt:
                    sir+="  "
                else:
                    sir+=stiva[inalt-1]+" "
            sir+="\n"
        sir+="-"*(2*len(self.info)-1)
        return sir


class Graph: #graful problemei
    def __init__(self):

        def obtineStiva(sir):
            listaStive=[]
            stiveSiruri=sir.strip().split("\n")
            culoare=stiveSiruri[0] #culoarea pe care o vrem la final
            if not culoare in ['g','r','a']:
                print("ERROR: Scop",culoare,"incorect!")
                sys.exit()
            stiveSiruri.pop(0)
            listaStive = [sirStiva.replace('[','').replace(']','').split("/") if sirStiva!='-' else [] for sirStiva in stiveSiruri]
            
            # in C++:  x = cond ? val_true : val_false
            # in Python: x = val_true if cond else val_false
            
            return culoare, listaStive
        
        
        while True:            
            try:
                pathCond=0
                while pathCond==0:
                    path_fisier=input("Path pentru fisier .txt: ")
                    path_fisier=path_fisier.strip()
                    if path_fisier[-4:]=='.txt':
                        pathCond=1
                    else:
                        print("\nEroare: Fisierul nu este .txt!")

                f = open(path_fisier, 'r')
            except:
                print("\nEroare: Fisierul nu exista sau path-ul este gresit!")
            else:
                break
        

        continutFisier=f.read() #citesc tot continutul fisierului
       
        self.scop,self.start=obtineStiva(continutFisier)
        print("Stare Initiala:", self.start)
        print("Culoare scop:",self.scop)
        
        #verificam daca avem macar 2 elemente de culoare scop, altfel nu putem sa ajungem la un rezultat
        nr_elem_scop=0
        for stiva in self.start:
            for elem in stiva:
                if not elem[:-1].isnumeric():
                    print("ERROR: Elemete", elem ,"introdus gresit! Numar gresit!")
                    sys.exit()
                    
                if not elem[-1] in ['g','r','a']:
                    print("ERROR: Elemete", elem ,"introdus gresit! Caracter gresit!")
                    sys.exit()
                    
                if elem[-1]==self.scop:
                    nr_elem_scop+=1
        if nr_elem_scop<2:
            print("ERROR: Starea initiala nu poate ajunge in configuratie scop.")
            sys.exit()
        #input()

    def testeaza_scop(self, nodCurent):
        k=1
        for list in nodCurent.info:
            if list:
                if list[-1][-1]!=self.scop:
                    k=0
            else:
                k=0
        
        return k

    #va genera succesorii sub forma de noduri in arborele de parcurgere    

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        listaSuccesori=[]
        stive_c=nodCurent.info # stivele din nodul curent
        nr_stive=len(stive_c)
        for idx in range(nr_stive):#idx= indicele stivei de pe care iau bloc
            
            if len(stive_c[idx])==0 :
                continue
            copie_interm=copy.deepcopy(stive_c)
            bloc=copie_interm[idx].pop() #iau varful stivei
            #if not bloc:
                #continue

            for j in range(nr_stive): #j = indicele stivei pe care pun blocul
                if idx == j: # nu punem blocul de unde l-am luat
                        continue
                        
                # aflam inltimea stivei curente
                inaltimeNoua=len(copie_interm[j])
                
                if copie_interm[j]: # daca stiva nu e goala
                    if bloc[-1]==copie_interm[j][-1][-1]: # daca blocurile sunt aceeasi culoare
                        continue
                        
                    if inaltimeNoua>1:
                        if copie_interm[j][-1][-1]==self.scop and bloc[-1]!=self.scop and copie_interm[j][-2][-1]==bloc[-1]:
                            continue
                    ''' 
                    daca blocul pe care il mutam nu este culoarea pe care o vrem !=[g], iar blocul peste care il punem este [g],
                    si in acelasi timp blocul de sub este aceeasi culoare ca blocul mutat, asta inseamna ca pierdem un bloc de
                    culoarea pe care o vrem
                    '''
                    
                # verificam daca numarul blocului ales este par sau impar
                paritate=int(bloc[:-1])%2

                # verificam conditia de paritate
                paritateBuna=0

                
                if j!=0 and j!=nr_stive-1:
                    
                    if len(copie_interm[j-1])<=inaltimeNoua and len(copie_interm[j+1])<=inaltimeNoua:
                        paritateBuna=1
                    
                    if len(copie_interm[j-1])>inaltimeNoua:
                        if int(copie_interm[j-1][inaltimeNoua][:-1])%2 == paritate:
                            paritateBuna=1
                            
                    if len(copie_interm[j+1])>inaltimeNoua:
                        if int(copie_interm[j+1][inaltimeNoua][:-1])%2 == paritate:
                            paritateBuna=1
                    
                        
                elif j==0:
                    if len(copie_interm[j+1])>inaltimeNoua:
                        if int(copie_interm[j+1][inaltimeNoua][:-1])%2 == paritate:
                            paritateBuna=1
                    else:
                        paritateBuna=1
                        
                elif j==nr_stive-1:
                    if len(copie_interm[j-1])>inaltimeNoua:  
                        if int(copie_interm[j-1][inaltimeNoua][:-1])%2 == paritate:
                            paritateBuna=1
                    else:
                        paritateBuna=1
                            
                if paritateBuna==0:
                    continue

                
                stive_n=copy.deepcopy(copie_interm)#lista noua de stive
                stive_n[j].append(bloc) # pun blocul in stiva aleasa
                
                #verificam daca blocul peste care am mutat blocul nostru se afla intre 2 blocuri de aceeasi culoarea
                #daca da, ii schimbam culoarea
                if len(stive_n[j])>2:
                    if stive_n[j][len(stive_n[j])-3][-1] == bloc[-1]:
                        stive_n[j][len(stive_n[j])-2] = stive_n[j][len(stive_n[j])-2][:-1]+bloc[-1]
                
                costMutareBloc=int(bloc[:-1])
                if not nodCurent.contineInDrum(stive_n):
                    nod_nou=NodParcurgere(stive_n,nodCurent, cost=nodCurent.g+costMutareBloc,h= self.calculeaza_h(stive_n, tip_euristica),priority=self.calculeaza_priority(stive_n))
                    
                    listaSuccesori.append(nod_nou)
        
        listaSuccesori.sort(key=lambda x: x.priority, reverse=True)

        return listaSuccesori
    
    # functia returneaza prioritatea unui nod
    # cu cat e mai mare nr, cu atat este mai buna mutarea
    def calculeaza_priority(self,infoNod):
        p=0
        for iStiva, stiva in enumerate(infoNod):
            if stiva!=[]:
                for iElem, elem in enumerate(stiva):
                    if elem[-1]==self.scop:
                        if iElem==len(stiva)-1:
                            p+=7
                        elif iElem==len(stiva)-2 or iElem==len(stiva)-3:
                            p+=4
                        else:
                            p+=1
                    elif iElem==len(stiva)-1 and stiva[iElem-1][-1]==self.scop:
                        p+=3       
        return p


    # euristica banala
    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if tip_euristica=="euristica banala":
            k=1
            for list in infoNod:
                if list:
                    if list[-1][-1]!=self.scop:
                        k=0
                else:
                    k=0
                    
            if k==0:
                return 1 #se pune costul minim pe o mutare
            return 0
        
        elif tip_euristica=="euristica admisibila 1":
            # pentru fiecare bloc din varf care nu este culoarea scop avem +1 h
            
            h=0
            k1=0
            for iStiva, stiva in enumerate(infoNod):
                if stiva!=[]:
                    for iElem, elem in enumerate(stiva):
                        if elem[-1]==self.scop:
                            if iElem==len(stiva)-1:
                                k1+=1
            h=len(infoNod)-k1
            return h
        
        elif tip_euristica=="euristica admisibila 2":
            # daca avem mai mult de 2 blocuri de culoare scop de varf ramane pe principiul de la admisibila1
            # altfel, avem k2 elementele pe locul 2 in stiva pentru care asumam ca facem cel putin 2 mutari pentru a ajunge
            # la o configurare scop
            
            h=0
            k1=0 #stiva are un singur bloc de culoarea scop in varf
            k2=0 #stiva are cel putin 2 blocuri de culoarea scop in varf
            k3=0 #stiva are un singur bloc de culoarea scop sub un bloc de alta culoare care e in varf
            vid=0
            
            for iStiva, stiva in enumerate(infoNod):
                if stiva!=[]:
                    for iElem, elem in enumerate(stiva):
                        if elem[-1]==self.scop and iElem==len(stiva)-1:
                            if len(stiva)>1:
                                if stiva[iElem-1][-1]!=self.scop:
                                    k1+=1
                                else:
                                    k2+=1
                            else:
                                k1+=1
                                
                        elif iElem==len(stiva)-2 and stiva[iElem+1][-1]!=self.scop:
                            k3+=1
                else:
                    vid+=1
                    
            k4=len(infoNod)-(k1+k2+k3+vid) #stiva care nu respecta celelalte config
            
            if k2!=0:        
                h = vid + k3 + k3-k2 + k4
                
            elif k1!=0:
                h = vid + k3 + k1 - abs(k1-k3) + k4
                
            else:
                h = vid + k3 + k4
            
            return h  
        
        else: #tip_euristica=="euristica neadmisibila"
            h=0
            k1=0
            for iStiva, stiva in enumerate(infoNod):
                if stiva!=[]:
                    for iElem, elem in enumerate(stiva):
                        if elem[-1]==self.scop:
                            if iElem==len(stiva)-1:
                                k1+=1
                                
            h=abs(len(infoNod) - k1*3)
            return h
        
        

    def __repr__(self):
        sir=""
        for (k,v) in self.__dict__.items() :
            sir+="{} = {}\n".format(k,v)
        return(sir)


def breadth_first(gr, nrSolutiiCautate):

    #in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c=[NodParcurgere(gr.start, None)]
    maxNod=0
    nrNodCalc=0
    
    while len(c)>0:
        ti=time.time()
        
        if(ti-t1>300):
            print("TIMEOUT ERROR: BF a depasit timpul alocat de 5min.",file=fo)
            return
        
        #print("Coada actuala: " + str(c))
        #input()
        nodCurent=c.pop(0)
        
        if len(nodCurent.obtineDrum())>maxNod:
            maxNod=len(nodCurent.obtineDrum())

        if gr.testeaza_scop(nodCurent):    
            t2=time.time()
            print("Solutie: \nTimp pana la solutie: ",t2-t1,"s\n",file=fo)
            
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("Numarul max de noduri existente:", maxNod, file=fo)
            maxNod=0
            print("Numar de noduri calculate pana la solutie:", nrNodCalc, file=fo)
            print("\n----------------\n",file=fo)
            
            nrSolutiiCautate-=1
            if nrSolutiiCautate==0:
                return
        
        lSuccesori=gr.genereazaSuccesori(nodCurent)
        nrNodCalc+=len(lSuccesori)
        #print('\n\n=================================')
        #nodCurent.afisDrum()
        c.extend(lSuccesori)


def depth_first(gr, nrSolutiiCautate=1):    
    #vom simula o stiva prin relatia de parinte a nodului curent
    maxNod=0
    nrNodCalc=0
    df(NodParcurgere(gr.start, None), nrSolutiiCautate, maxNod, nrNodCalc)

                
def df(nodCurent, nrSolutiiCautate, maxNod, nrNodCalc):
    ti=time.time()
        
    if(ti-t1>60):
        print("TIMEOUT ERROR: DF a depasit timpul alocat de 1min.",file=fo)
        return
    
    if nrSolutiiCautate<=0: #testul acesta s-ar valida doar daca in apelul initial avem df(start,if nrSolutiiCautate=0)
        return nrSolutiiCautate
    
    if len(nodCurent.obtineDrum())>maxNod:
        maxNod=len(nodCurent.obtineDrum())
    
    if gr.testeaza_scop(nodCurent):
        t2=time.time()
        print("Solutie: \nTimp pana la solutie: ",t2-t1,"s\n",file=fo)
        
        nodCurent.afisDrum(afisCost=True, afisLung=True)
        print("Numarul max de noduri existente:", maxNod, file=fo)
        maxNod=0
        print("Numar de noduri calculate pana la solutie:", nrNodCalc, file=fo)
        print("\n----------------\n",file=fo)
        
        nrSolutiiCautate-=1
        if nrSolutiiCautate==0:
            return nrSolutiiCautate
        
    lSuccesori=gr.genereazaSuccesori(nodCurent)
    nrNodCalc+=len(lSuccesori)
    
    for sc in lSuccesori:
        if nrSolutiiCautate!=0:
            
            nrSolutiiCautate=df(sc, nrSolutiiCautate, maxNod, nrNodCalc)
    
    return nrSolutiiCautate


def a_star(gr, nrSolutiiCautate, tip_euristica):
    #in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c=[NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    maxNod=0
    nrNodCalc=0
    while len(c)>0:
        ti=time.time()
        
        if(ti-t1>300):
            print("TIMEOUT ERROR: A* a depasit timpul alocat de 5min.",file=fo)
            return
        
        nodCurent=c.pop(0)
        #print("\nNOD CURENT:\n",nodCurent.afisDrum())
        
        if len(nodCurent.obtineDrum())>maxNod:
            maxNod=len(nodCurent.obtineDrum())
        
        if gr.testeaza_scop(nodCurent):
            t2=time.time()
            print("Solutie: \nTimp pana la solutie: ",t2-t1,"s\n",file=fo)
            
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("Numarul max de noduri existente:", maxNod, file=fo)
            maxNod=0
            print("Numar de noduri calculate pana la solutie:", nrNodCalc, file=fo)
            print("\n----------------\n",file=fo)
            
            nrSolutiiCautate-=1
            if nrSolutiiCautate==0:
                return
        lSuccesori=gr.genereazaSuccesori(nodCurent,tip_euristica=tip_euristica)
        nrNodCalc+=len(lSuccesori)
        for s in lSuccesori:
            i=0
            gasit_loc=False
            for i in range(len(c)):
                #diferenta fata de UCS e ca ordonez dupa f
                if c[i].f>=s.f :
                    gasit_loc=True
                    break;
            if gasit_loc:
                c.insert(i,s)
            else:
                c.append(s)


def a_star_opt(gr,tip_euristica):
    #in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    l_open=[NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    #l_open contine nodurile candidate pentru expandare (este echivalentul lui c din A* varianta neoptimizata)
    #l_closed contine nodurile expandate
    l_closed=[]
    
    maxNod=0
    nrNodCalc=0
    while len(l_open)>0:
        ti=time.time()
        
        if(ti-t1>300):
            print("TIMEOUT ERROR: A* optimizat a depasit timpul alocat de 5min.",file=fo)
            return
        
        nodCurent=l_open.pop(0)
        #print("\nNOD CURENT:\n",nodCurent.afisDrum())
        l_closed.append(nodCurent)
        
        if len(nodCurent.obtineDrum())>maxNod:
            maxNod=len(nodCurent.obtineDrum())
        
        if gr.testeaza_scop(nodCurent):
            t2=time.time()
            print("Solutie: \nTimp pana la solutie: ",t2-t1,"s\n",file=fo)
            
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("Numarul max de noduri existente:", maxNod, file=fo)
            maxNod=0
            print("Numar de noduri calculate pana la solutie:", nrNodCalc, file=fo)
            print("\n----------------\n",file=fo)
            return
        lSuccesori=gr.genereazaSuccesori(nodCurent,tip_euristica=tip_euristica)
        nrNodCalc+=len(lSuccesori)
        for s in lSuccesori:
            gasitC=False
            for nodC in l_open:
                if s.info==nodC.info:
                    gasitC=True
                    if s.f>=nodC.f:
                        lSuccesori.remove(s)
                    else:#s.f<nodC.f
                        l_open.remove(nodC)
                    break
            if not gasitC:
                for nodC in l_closed:
                    if s.info==nodC.info:
                        if s.f>=nodC.f:
                            lSuccesori.remove(s)
                        else:#s.f<nodC.f
                            l_closed.remove(nodC)
                        break
        for s in lSuccesori:
            i=0
            gasit_loc=False
            for i in range(len(l_open)):
                #diferenta fata de UCS e ca ordonez crescator dupa f
                #daca f-urile sunt egale ordonez descrescator dupa g
                if l_open[i].f>s.f or (l_open[i].f==s.f and l_open[i].g<=s.g) :
                    gasit_loc=True
                    break
            if gasit_loc:
                l_open.insert(i,s)
            else:
                l_open.append(s)


def ida_star(gr, nrSolutiiCautate):
    
    nodStart=NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))
    limita=nodStart.f
    
    maxNod=0
    nrNodCalc=0
    while True:
        ti=time.time()
        
        if(ti-t1>300):
            print("TIMEOUT ERROR: IDA* a depasit timpul alocat de 5min.",file=fo)
            return

        #print("Limita de pornire: ", limita)
        nrSolutiiCautate, rez= construieste_drum(gr, nodStart, limita,nrSolutiiCautate, maxNod,nrNodCalc)
        if rez=="gata":
            break
        if rez==float('inf'):
            print("Nu mai exista solutii!")
            break
        limita=rez
        #print(">>> Limita noua: ", limita)
        #input()


def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate, maxNod,nrNodCalc):
    #print("A ajuns la: ", nodCurent)
    if nodCurent.f>limita:
        return nrSolutiiCautate, nodCurent.f
    
    if len(nodCurent.obtineDrum())>maxNod:
            maxNod=len(nodCurent.obtineDrum())
    
    if gr.testeaza_scop(nodCurent) and nodCurent.f==limita :
        t2=time.time()
        
        print("Solutie: \nTimp pana la solutie: ",t2-t1,"s\n",file=fo)
        
        nodCurent.afisDrum(afisCost=True, afisLung=True)
        #print(limita)
        print("Numarul max de noduri existente:", maxNod, file=fo)
        maxNod=0
        print("Numar de noduri calculate pana la solutie:", nrNodCalc, file=fo)
        print("\n----------------\n",file=fo)
        
        nrSolutiiCautate-=1
        if nrSolutiiCautate==0:
            return 0,"gata"
    lSuccesori=gr.genereazaSuccesori(nodCurent)
    nrNodCalc+=len(lSuccesori)
    minim=float('inf')
    for s in lSuccesori:
        nrSolutiiCautate, rez=construieste_drum(gr, s, limita, nrSolutiiCautate,maxNod,nrNodCalc)
        if rez=="gata":
            return 0,"gata"
        #print("Compara ", rez, " cu ", minim)
        if rez<minim:
            minim=rez
            #print("Noul minim: ", minim)
    return nrSolutiiCautate, minim


def uniform_cost(gr, nrSolutiiCautate=1):

    #in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c=[NodParcurgere(gr.start, None, 0)]
    
    maxNod=0
    nrNodCalc=0
    while len(c)>0:
        ti=time.time()
        
        if(ti-t1>300):
            print("TIMEOUT ERROR: USC* a depasit timpul alocat de 5min.",file=fo)
            return
        
        #print("Coada actuala: " + str(c))
        #input()
        nodCurent=c.pop(0)
        
        if len(nodCurent.obtineDrum())>maxNod:
            maxNod=len(nodCurent.obtineDrum())
        
        if gr.testeaza_scop(nodCurent):
            t2=time.time()
            print("Solutie: \nTimp pana la solutie: ",t2-t1,"s\n",file=fo)
            
            nodCurent.afisDrum(afisCost=True, afisLung=True)
            print("Numarul max de noduri existente:", maxNod, file=fo)
            maxNod=0
            print("Numar de noduri calculate pana la solutie:", nrNodCalc, file=fo)
            print("\n----------------\n",file=fo)
            nrSolutiiCautate-=1
            if nrSolutiiCautate==0:
                return
        lSuccesori=gr.genereazaSuccesori(nodCurent)
        nrNodCalc+=len(lSuccesori)
        for s in lSuccesori:
            i=0
            gasit_loc=False
            for i in range(len(c)):
                #ordonez dupa cost(notat cu g aici și în desenele de pe site)
                if c[i].g>s.g :
                    gasit_loc=True
                    break
            if gasit_loc:
                c.insert(i,s)
            else:
                c.append(s)


gr=Graph()                

# path pt fisierul de output

while True:
    try:
        pathCond=0
        while pathCond==0:
            output_path=input("Path pentru fisier de output .txt: ")
            output_path=output_path.strip()
            if output_path[-4:]=='.txt':
                pathCond=1
            else:
                print("\nEroare: Fisierul nu este .txt!")

        fo = open(output_path, 'w')
    except:
        print("\nEroare: Fisierul nu exista sau path-ul este gresit!")
    else:
        break

#fo=open(r'C:\Users\Asus tuf\Desktop\University\ANUL3_S1\Inteligenta Artificiala\Proiect2\input&output\output.txt','w')

#Rezolvat cu breadth first

print("Solutii obtinute cu breadth first:",file=fo)
t1=time.time()
breadth_first(gr, nrSolutiiCautate=2)

print("\n\nURMATOAREA METODA:\n\n",file=fo)

print("Solutii obtinute cu depth first:",file=fo)
t1=time.time()
depth_first(gr, nrSolutiiCautate=2)

print("\n\nURMATOAREA METODA:\n\n",file=fo)

print("Solutii obtinute cu A*:",file=fo)
t1=time.time()
a_star(gr, nrSolutiiCautate=1, tip_euristica="euristica neadmisibila")


print("\n\nURMATOAREA METODA:\n\n",file=fo)

print("Solutii obtinute cu A* optimizat:",file=fo)
t1=time.time()
a_star_opt(gr,tip_euristica="euristica neadmisibila")

print("\n\nURMATOAREA METODA:\n\n",file=fo)

print("Solutii obtinute cu IDA*:",file=fo)
t1=time.time()
ida_star(gr, nrSolutiiCautate=2)

print("\n\nURMATOAREA METODA:\n\n",file=fo)

print("Solutii obtinute cu USC*:",file=fo)
t1=time.time()
uniform_cost(gr, nrSolutiiCautate=1)

fo.close()

# C:\Users\Asus tuf\Desktop\University\ANUL3_S1\Inteligenta Artificiala\Proiect2\input&output\input.txt
# C:\Users\Asus tuf\Desktop\University\ANUL3_S1\Inteligenta Artificiala\Proiect2\input&output\output.txt
