def download_pubmed(keyword):
    """ Función que extrae listado de artículos desde pubmed a traves de un keyword"""
    from Bio import Entrez
    Entrez.email = "andres.calderon@est.ikiam.edu.ec"
    Ingresar=Entrez.read(Entrez.esearch(db="pubmed",
                        term= keyword,
                        usehistory="y"))
    
    webenv=Ingresar["WebEnv"]
    querykey=Ingresar["QueryKey"]
    hand1=Entrez.efetch(db="pubmed",
                      rettype='medline',
                      retmode="text",
                      retstart=0,
                      retmax=543, webenv=webenv, querykey=querykey)
    out_hand1 = open(keyword+".txt", "w")
    a=hand1.read()
    out_hand1.write(a)
    out_hand1.close()
    hand1.close()
    return a

def mining_pubs(tipo, archivo):
    """
    Función que registra tres tipos de opciones "DP", "AU", "AD". Si se encuentra DP se regresa una data con el PMID y el año_DP, pero si es un AU se regresa una recuperación del número de autores (num_autores) por PMID, finalmente, si es un AD se retorna un dataframe con el país y el num_autores. Para esto se usara un keyword que descargara un archivo de pubmed con la función download_pubmed
    """
    import csv
    import re
    import pandas as pd
    from collections import Counter
    with open(archivo+".txt", errors="ignore") as f: 
        mitexto = f.read() 
    if tipo == "DP":
        PMID = re.findall("PMID-\s\d{8}", mitexto)
        PMID = "".join(PMID)
        PMID = PMID.split("PMID- ")
        año = re.findall("DP\s{2}-\s(\d{4})", mitexto)
        pmid = pd.DataFrame()
        pmid["PMID"] = PMID
        pmid["Año de publicación"] = año
        return (pmid)
    elif tipo == "AU": 
        PMID = re.findall("PMID- (\d*)", mitexto) 
        autores = mitexto.split("PMID- ")
        autores.pop(0)
        num_autores = []
        for i in range(len(autores)):
            numero = re.findall("AU -", autores[i])
            n = (len(numero))
            num_autores.append(n)
        pmid_a = pd.DataFrame()
        pmid_a["PMID"] = PMID 
        pmid_a["Numero de autores"] = num_autores
        return (pmid_a)
    elif tipo == "AD": 
        mitexto = re.sub(r" [A-Z]{1}\.","", mitexto)
        mitexto = re.sub(r"Av\.","", mitexto)
        mitexto = re.sub(r"Vic\.","", mitexto)
        mitexto = re.sub(r"Tas\.","", mitexto)
        AD = mitexto.split("AD  - ")
        num_paises = []
        for i in range(len(AD)): 
            pais = re.findall("\S, ([A-Za-z]*)\.", AD[i])
            if not pais == []: 
                if not len(pais) >= 2:  
                    if re.findall("^[A-Z]", pais[0]): 
                        num_paises.append(pais[0])
        conteo = Counter(num_paises)
        resultado = {}
        for clave in conteo:
            valor = conteo[clave]
            if valor != 1: 
                resultado[clave] = valor 
        rep_pais = pd.DataFrame()
        rep_pais["país"] = resultado.keys()
        rep_pais["número de autores"] = resultado.values()
        return (rep_pais)
