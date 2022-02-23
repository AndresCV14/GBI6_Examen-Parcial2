def download_pubmed(keyword):
    """ Función que extrae listado de artículos desde pubmed a traves de un keyword que ingresa el usuario entre comillas"""
    import Bio
    from Bio import Entrez
    from Bio import SeqIO
    Entrez.email = "andres.calderon@est.ikiam.edu.ec"
   
    record=Entrez.read(Entrez.esearch(db="pubmed",
                        term= "Ecuador genomics",
                        usehistory="y"))
    
    webenv=record["WebEnv"]
    query_key=record["QueryKey"]
    
    handlexd=Entrez.efetch(db="pubmed",
                      rettype='medline',
                      retmode="text",
                      retstart=0,
                      retmax=543, webenv=webenv, query_key=query_key)
    out_handlexd = open(keyword+".txt", "w")
    m=handlexd.read()
    out_handlexd.write(m)
    out_handlexd.close()
    handlexd.close()
    return m

def mining_pubs(tipo, archivo):
    """
    Función que pide como primera entrada tres tipos de opciones "DP", "AU" y "AD". Si coloca "DP" el resultado es un data con el PMID y el DP_year, si es "AU" recupera el número de autores (num_auth) por PMID, y si el tipo es "AD" el retorno es un dataframe con el country y el num_auth. Se pide un segundo argumento que corresponde al keyword usado para la descarga de archivos con la funcion download pubmed
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
        pmid_y = pd.DataFrame()
        pmid_y["PMID"] = PMID
        pmid_y["Año de publicación"] = año
        return (pmid_y)
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
        AD = texto.split("AD  - ")
        num_paises = []
        for i in range(len(AD)): 
            pais = re.findall("\S, ([A-Za-z]*)\.", AD[i])
            if not pais == []: 
                if not len(pais) >= 2:  
                    if re.findall("^[A-Z]", pais[0]): 
                        num_paises.append(pais[0])
        conteo=Counter(num_paises)
        resultado = {}
        for clave in conteo:
            valor = conteo[clave]
            if valor != 1: 
                resultado[clave] = valor 
        rep_pais = pd.DataFrame()
        rep_pais["pais"] = resultado.keys()
        rep_pais["numero de autores"] = resultado.values()
        return (veces_pais)
