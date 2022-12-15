# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 14:52:33 2020

@author: jaime
"""

from difflib import SequenceMatcher
from lxml import etree
import spacy
import nltk 
import pandas as pd
from pathlib import Path
import zipfile
import numpy as np
from operator import itemgetter
#from extrafuns import fun_result

"""
1. lista os livos do pesquisador.
2. Não diferencia se o livro foi organizado ou não pelo pesquisador
Entrada: currículo lattes em XML.
Saída: lista com  
"""  
def lista_livros(xml):
 
    lista_livros = []
    tipo = ""
    isbn = ""
    ano = 0

    for livros in xml.xpath('//LIVROS-PUBLICADOS-OU-ORGANIZADOS'):
        for livro in livros:
            print("buscando dados de livro...")
            for dados in livro:
                if dados.tag=='DADOS-BASICOS-DO-LIVRO':
                    tipo = dados.attrib.get('TIPO')
                    ano = dados.attrib.get('ANO')
                if dados.tag=='DETALHAMENTO-DO-LIVRO':
                    isbn = dados.attrib.get('ISBN')
            print("dados do livro...{}, {}, {}".format(ano, isbn, tipo))
            lista_livros.append([ano, isbn, tipo])
            
    lista_livros = sorted(lista_livros, key=itemgetter(0), reverse=True)
    return lista_livros

def lista_capitulos(xml):
    
    lista_capitulos = []
    tipo = ""
    isbn = ""
    ano = 0
    
    for capitulos in xml.xpath('//CAPITULOS-DE-LIVROS-PUBLICADOS'):
        for capitulo in capitulos:
            print("buscando dados de capítulo de livro...")
            for dados in capitulo:
                if dados.tag=='DADOS-BASICOS-DO-CAPITULO':
                    tipo = dados.attrib.get('TIPO')
                    ano = dados.attrib.get('ANO')
                if dados.tag=='DETALHAMENTO-DO-CAPITULO':
                    isbn = dados.attrib.get('ISBN')
            print("dados do capítulo de livro...{}, {}, {}".format(ano, isbn, tipo))
            lista_capitulos.append([ano, isbn, tipo])
    lista_capitulos = sorted(lista_capitulos, key=itemgetter(0), reverse=True)
    return lista_capitulos

def lista_artigos(xml, lista_qualis):
    lista_artigos = []
    ano = 0
    issn = ""
    qualis = ""
    
    for artigos in xml.xpath('//ARTIGOS-PUBLICADOS'):
        for artigo in artigos:
            print("buscando dados de artigo...")
            for dados in artigo:
                if dados.tag=='DADOS-BASICOS-DO-ARTIGO':
                   ano = dados.attrib.get('ANO-DO-ARTIGO')
                if dados.tag=='DETALHAMENTO-DO-ARTIGO':
                   issn = dados.attrib.get('ISSN')
                   issn = issn[0:4] +"-" + issn[4:9]
            qualis = list(lista_qualis[lista_qualis['ISSN']==issn]['Estrato'])
            
            #busca maior qualis
            qualis = np.sort(qualis)
            qualis = qualis[0:1]
                                
            #for index, row in lista_qualis.iterrows():
            #    if row["ISSN"]==issn:
            #        qualis = row['Estrato']
            print("dados de qualis do artigo...{}, {}, {}".format(ano, issn, qualis))
            lista_artigos.append([ano, issn, qualis])
    lista_artigos = sorted(lista_artigos, key=itemgetter(0), reverse=True)
    return lista_artigos

def lista_eventos(xml):
    
    lista_eventos = []
    natureza = "" #completo ou resumo
    classificacao = "" #nacional ou internacional
    pais = ""
    ano = 0
    
    for eventos in xml.xpath('//TRABALHOS-EM-EVENTOS'):
        for evento in eventos:
            print("buscando dados de evento...")
            for dados in evento:
                if dados.tag=='DADOS-BASICOS-DO-TRABALHO':
                    natureza = dados.attrib.get('NATUREZA')
                    ano = dados.attrib.get('ANO-DO-TRABALHO')
                    pais = dados.attrib.get('PAIS-DO-EVENTO')
                if dados.tag=='DETALHAMENTO-DO-TRABALHO':
                    classificacao = dados.attrib.get('CLASSIFICACAO-DO-EVENTO')
            print("dados do evento...{}, {}, {}, {}".format(natureza, ano, pais, classificacao))
            lista_eventos.append([natureza, ano, pais, classificacao])
    lista_eventos = sorted(lista_eventos, key=itemgetter(1), reverse=True)
    return lista_eventos

def lista_orientacoes_doutorado(xml):
    
    lista_orientacoes_doutorado = []
    tipo_orientacao = "" #orientador: sim ou não
    natureza = "" #Dissertação de mestrado, tese de doutorado, iniciação científica
    ano = 0
    
    for orientacoes in xml.xpath('//ORIENTACOES-CONCLUIDAS'):
        print("buscando dados de orientação...")
        for orientacao in orientacoes:
            if orientacao.tag=="ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO":
                for dados in orientacao:              
                    if dados.tag=='DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO':
                        natureza = dados.attrib.get('NATUREZA')
                        ano = dados.attrib.get('ANO')
                    if dados.tag=='DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO':
                        tipo_orientacao = dados.attrib.get('TIPO-DE-ORIENTACAO')

                print("dados da orientação...{}, {}, {}".format(natureza, ano, tipo_orientacao))
                lista_orientacoes_doutorado.append([natureza, ano, tipo_orientacao])
    lista_orientacoes_doutorado = sorted(lista_orientacoes_doutorado, key=itemgetter(1), reverse=True)
    return lista_orientacoes_doutorado


def lista_orientacoes_mestrado(xml):
    
    lista_orientacoes_mestrado = []
    tipo_orientacao = "" #orientador: sim ou não
    natureza = "" #Dissertação de mestrado, tese de doutorado, iniciação científica
    ano = 0
    
    for orientacoes in xml.xpath('//ORIENTACOES-CONCLUIDAS'):
        print("buscando dados de orientação...")
        for orientacao in orientacoes:
            if orientacao.tag=="ORIENTACOES-CONCLUIDAS-PARA-MESTRADO":
                for dados in orientacao:              
                    if dados.tag=='DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO':
                        natureza = dados.attrib.get('NATUREZA')
                        ano = dados.attrib.get('ANO')
                    if dados.tag=='DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO':
                        tipo_orientacao = dados.attrib.get('TIPO-DE-ORIENTACAO')

                print("dados da orientação...{}, {}, {}".format(natureza, ano, tipo_orientacao))
                lista_orientacoes_mestrado.append([natureza, ano, tipo_orientacao])
    lista_orientacoes_mestrado = sorted(lista_orientacoes_mestrado, key=itemgetter(1), reverse=True)
    return lista_orientacoes_mestrado

def lista_orientacoes_outras(xml):
    
    lista_orientacoes_outras = []
    tipo_orientacao = "" #orientador: sim ou não
    natureza = "" #Dissertação de mestrado, tese de doutorado, iniciação científica
    ano = 0
    
    for orientacoes in xml.xpath('//ORIENTACOES-CONCLUIDAS'):
        print("buscando dados de orientação...")
        for orientacao in orientacoes:
            if orientacao.tag=="OUTRAS-ORIENTACOES-CONCLUIDAS":
                for dados in orientacao:              
                    if dados.tag=='DADOS-BASICOS-DE-OUTRAS-ORIENTACOES-CONCLUIDAS':
                        natureza = dados.attrib.get('NATUREZA')
                        ano = dados.attrib.get('ANO')
                        tipo_orientacao = dados.attrib.get('TIPO')

                print("dados da orientação...{}, {}, {}".format(natureza, ano, tipo_orientacao))
                lista_orientacoes_outras.append([natureza, ano, tipo_orientacao])
    lista_orientacoes_outras = sorted(lista_orientacoes_outras, key=itemgetter(1), reverse=True)
    return lista_orientacoes_outras

def lista_patente_cultivar(xml):
  
    lista_producao = []
    natureza = ""
    tipo = ""
    patente = ""
    ano = 0
        
    for producoesTecnicas in xml.xpath('//PRODUCAO-TECNICA'):
        for producao in producoesTecnicas:
            if producao.tag=="CULTIVAR-REGISTRADA":
                tipo = "CULTIVAR"
                for dados in producao:
                    if dados.tag=="DADOS-BASICOS-DA-CULTIVAR":
                        ano = dados.attrib.get('ANO-SOLICITACAO')
                    if dados.tag=="DETALHAMENTO-DA-CULTIVAR":
                        for registro in dados:
                            if registro.tag=="REGISTRO-OU-PATENTE":
                                patente = registro.attrib.get("CODIGO-DO-REGISTRO-OU-PATENTE")
                            else:
                                patente=""
                
            elif producao.tag=="SOFTWARE":
                tipo = "SOFTWARE"
                for dados in producao:
                    if dados.tag=="DADOS-BASICOS-DO-SOFTWARE":
                        ano = dados.attrib.get('ANO')
                    if dados.tag=="DETALHAMENTO-DO-SOFTWARE":
                        for registro in dados:
                            if registro.tag=="REGISTRO-OU-PATENTE":
                                patente = registro.attrib.get("CODIGO-DO-REGISTRO-OU-PATENTE")
                            else:
                                patente = ""
            
            elif producao.tag=="MARCA":
                tipo = "MARCA"
                for dados in producao:
                    if dados.tag=="DADOS-BASICOS-DA-MARCA":
                        ano = dados.attrib.get('ANO-DESENVOLVIMENTO')
                    if dados.tag=="DETALHAMENTO-DA-MARCA":
                        for registro in dados:
                            if registro.tag=="REGISTRO-OU-PATENTE":
                                patente = registro.attrib.get("CODIGO-DO-REGISTRO-OU-PATENTE")
                            else:
                                patente = ""
            else:
                tipo = "OUTRO"
                patente = "SEM INFORMAÇÃO"
                ano = 0
            
            lista_producao.append([tipo, int(ano), patente])
    lista_producao = sorted(lista_producao, key=itemgetter(1), reverse=True)       
    return lista_producao



def ano_doutorado(xml):
    ano_doutorado = 0
    for formacoes in xml.xpath('//FORMACAO-ACADEMICA-TITULACAO'):
        print("buscando dados de formação acadêmica...")
        for formacao in formacoes:
            if formacao.tag=="DOUTORADO":
                ano_doutorado = formacao.attrib.get('ANO-DE-CONCLUSAO')
    print("ano doutorado: {}".format(ano_doutorado))
    return ano_doutorado

def nome_completo(xml):
    nome_completo = ""
    for dados in xml.xpath('//CURRICULO-VITAE'):
        for item in dados:
            print("buscando dados de formação acadêmica...")
            if item.tag=="DADOS-GERAIS":
                nome_completo = item.attrib.get('NOME-COMPLETO')
    print("nome_completo: {}".format(nome_completo))
    return nome_completo

def adiciona_indices(df_pontuacao, df_indices):
    """
    recebe os dataframes com a pontuação e com os índice e concatena com base no idlattes
   
    """
    df_pontuacao = df_pontuacao.set_index("nome")
    df_indices = df_indices.set_index("nome")
    
    novo = pd.merge(df_pontuacao, df_indices)
    
    return novo
    
    
def main():
    
    lista_qualis = pd.read_csv('dados/qualis_todas_areas.csv', delimiter="\t", encoding='ISO-8859-1')
    dados_docentes = pd.read_csv('dados/lista_lattes.csv', encoding='ISO-8859-1', delimiter=";")
    lista_lattes = dados_docentes["lattes"]
    
    lim_livros = 500
    lim_artigos = 500
    lim_eventos = 500
    lim_org_livros = 500
    lim_patentes = 500
    lim_orient_dout = 500
    lim_orient_mest = 500
    lim_coorient_dout = 500
    lim_coorient_mest = 500
    lim_orient_espec = 500
    lim_orient_tcc = 500
    lim_orient_ic = 500
    
    ano_inicial = 2015
    
    pontuacao = []
    
    for lattes in lista_lattes:
        zipname = lattes.split("/")
        zipname = zipname[3]
        zipfilepath = './lattes' + '/' + str(zipname) + '.zip'
        archive = zipfile.ZipFile(zipfilepath, 'r')
        caminho_xml = archive.open("curriculo.xml")
        #caminho_xml = "lattes/7985936674676993/curriculo.xml" 
        #caminho_xml = "lattes/5657051115739955/curriculo.xml"
        xml = etree.parse(caminho_xml)
        
        
        pnts_capitulos = 0
        pnts_livros_pub = 0
        pnts_livros_org = 0
        pnts_artigos_a1_a2 = 0
        pnts_artigos_b1 = 0
        pnts_artigos_b2_b3 = 0
        pnts_artigos_b4_b5_c = 0
        pnts_eventos_completos_inter = 0
        pnts_eventos_completos_nac = 0
        pnts_eventos_resumo_inter = 0
        pnts_eventos_resumo_nac = 0
        pnts_patentes = 0
        pnts_orientacoes_dout = 0
        pnts_coorientacoes_dout = 0
        pnts_orientacoes_mest= 0
        pnts_coorientacoes_mest= 0
        pnts_orientacoes_espec= 0
        pnts_orientacoes_ic= 0
        pnts_orientacoes_tcc= 0
        
        total_livros = 0
        total_artigos = 0
        total_eventos = 0
        total_org_livros = 0
        total_patentes = 0
        total_orient_dout = 0
        total_orient_mest = 0
        total_coorient_dout = 0
        total_coorient_mest = 0
        total_orient_espec = 0
        total_orient_tcc = 0
        total_orient_ic = 0
               
    
        livros = lista_livros(xml)
        
        for livro_pub in livros:
            if total_livros >= lim_livros:
                break
            elif int(livro_pub[0]) >= ano_inicial and livro_pub[1]!=[] and livro_pub[2]=='LIVRO_PUBLICADO':
                pnts_livros_pub += 1
                total_livros += 1
    
        
        capitulos = lista_capitulos(xml)
        #calcula pontuação para capitulos
        for capitulo in capitulos:
            if total_livros >= lim_livros:
                break
            elif int(capitulo[0]) >= ano_inicial and capitulo[1]!=[]:
                pnts_capitulos += 1
                total_livros += 1
    
                
        #calcula pontuação para capitulos
        for livro_org in livros:
            if total_org_livros >= lim_org_livros:
                break
            elif int(livro_org[0]) >= ano_inicial and livro_org[1]!=[] and livro_org[2]=='LIVRO_ORGANIZADO_OU_EDICAO':
                pnts_livros_org += 1
                total_org_livros += 1
             
    
        
        
        artigos = lista_artigos(xml, lista_qualis)
        for artigo in artigos:
            if total_artigos >= lim_artigos:
                break
            if int(artigo[0]) >= ano_inicial:
                if str(artigo[2])=="['A1']" or str(artigo[2])=="['A2']":
                    pnts_artigos_a1_a2 += 1
                    total_artigos += 1
                if str(artigo[2])=="['B1']":
                    pnts_artigos_b1 += 1
                    total_artigos += 1
                if str(artigo[2])=="['B2']" or str(artigo[2])=="['B3']":
                    pnts_artigos_b2_b3 += 1
                    total_artigos += 1
                if str(artigo[2])=="['B4']" or str(artigo[2])=="['B5']" or str(artigo[2])=="['C']":
                    pnts_artigos_b4_b5_c += 1
                    total_artigos += 1
        
        eventos = lista_eventos(xml)
        for evento in eventos:
            if total_eventos >= lim_eventos:
                break
            elif evento[0]=='COMPLETO' and int(evento[1]) >= ano_inicial and evento[3]=='INTERNACIONAL':
                pnts_eventos_completos_inter += 1
                total_eventos += 1
                
            elif evento[0]=='COMPLETO' and int(evento[1]) >= ano_inicial and evento[3]!='INTERNACIONAL':
                pnts_eventos_completos_nac += 1
                total_eventos += 1
                
            elif evento[0]=='RESUMO' and int(evento[1]) >= ano_inicial and evento[3]=='INTERNACIONAL':
                pnts_eventos_resumo_inter += 1
                total_eventos += 1
                
            elif evento[0]=='RESUMO' and int(evento[1]) >= ano_inicial and evento[3]!='INTERNACIONAL':
                pnts_eventos_resumo_nac += 1
                total_eventos += 1
        
    
        orientacoes_dout = lista_orientacoes_doutorado(xml)
        for orientacao in orientacoes_dout:
            if total_orient_dout >= lim_orient_dout:
                break
            if int(orientacao[1]) >= ano_inicial and orientacao[2]=='ORIENTADOR_PRINCIPAL':
                pnts_orientacoes_dout += 1
                total_orient_dout += 1
                
        for coorientacao in orientacoes_dout:
            if total_coorient_dout >= lim_coorient_dout:
                break
            if int(coorientacao[1]) >= ano_inicial and coorientacao[2]=='CO_ORIENTADOR':
                pnts_coorientacoes_dout += 1
                total_coorient_dout += 1
        
        orientacoes_mest = lista_orientacoes_mestrado(xml)
        for orientacao in orientacoes_mest:
            if total_orient_mest >= lim_orient_mest:
                break
            if int(orientacao[1]) >= ano_inicial and orientacao[2]=='ORIENTADOR_PRINCIPAL':
                pnts_orientacoes_mest += 1
                total_orient_mest += 1
                
        for coorientacao in orientacoes_mest:
            if total_coorient_mest >= lim_coorient_mest:
                break
            if int(coorientacao[1]) >= ano_inicial and coorientacao[2]=='CO_ORIENTADOR':
                pnts_coorientacoes_mest += 1
                total_coorient_mest += 1
        
        orientacoes_outras = lista_orientacoes_outras(xml)   
        for orientacao in orientacoes_outras:
            if total_orient_tcc >= lim_orient_tcc:
                break
            if int(orientacao[1]) >= ano_inicial and orientacao[0]=='TRABALHO_DE_CONCLUSAO_DE_CURSO_GRADUACAO':
                pnts_orientacoes_tcc += 1
                total_orient_tcc += 1
                
        for orientacao in orientacoes_outras:
            if total_orient_ic >= lim_orient_ic:
                break
            if int(orientacao[1]) >= ano_inicial and orientacao[0]=='INICIACAO_CIENTIFICA':
                pnts_orientacoes_ic += 1
                total_orient_ic += 1
                
        for orientacao in orientacoes_outras:  
            if total_orient_espec >= lim_orient_espec:
                break
            if int(orientacao[1]) >= ano_inicial and orientacao[0]=='MONOGRAFIA_DE_CONCLUSAO_DE_CURSO_APERFEICOAMENTO_E_ESPECIALIZACAO':
                pnts_orientacoes_espec += 1
                total_orient_espec +=1
                
        patentes_cultivar = lista_patente_cultivar(xml) 
        for patente in patentes_cultivar:
            if total_patentes >= lim_patentes:
                break
            if int(patente[1]) >= ano_inicial  and patente[2]!="SEM INFORMAÇÃO":
                pnts_patentes +=1
                total_patentes +=1
        ano_dout = ano_doutorado(xml)
        nome = nome_completo(xml)
       
        pontuacao.append([nome,
                          zipname,
                         pnts_livros_pub, 
                         pnts_capitulos, 
                         pnts_artigos_a1_a2, 
                         pnts_artigos_b1,
                         pnts_artigos_b2_b3, 
                         pnts_artigos_b4_b5_c, 
                         pnts_eventos_completos_inter, 
                         pnts_eventos_completos_nac, 
                         pnts_eventos_resumo_inter, 
                         pnts_eventos_resumo_nac,
                         pnts_livros_org,
                         pnts_patentes,
                         pnts_orientacoes_dout,
                         pnts_orientacoes_mest,
                         pnts_coorientacoes_dout, 
                         pnts_coorientacoes_mest,
                         pnts_orientacoes_espec,
                         pnts_orientacoes_tcc,
                         pnts_orientacoes_ic,
                         ano_dout])
    
    pontuacao = np.array(pontuacao)
    
    df = pd.DataFrame(pontuacao, columns=['nome',
                                          'lattes',
                                          'pnts_livros_pub', 
                                          'pnts_capitulos', 
                                          'pnts_artigos_a1_a2', 
                                          'pnts_artigos_b1', 
                                          'pnts_artigos_b2_b3', 
                                          'pnts_artigos_b4_b5_c', 
                                          'pnts_eventos_completos_inter', 
                                          'pnts_eventos_completos_nac', 
                                          'pnts_eventos_resumo_inter', 
                                          'pnts_eventos_resumo_nac',
                                          'pnts_livros_org',
                                          'pnts_patentes',
                                          'pnts_orientacoes_dout',
                                          'pnts_orientacoes_mest',
                                          'pnts_coorientacoes_dout', 
                                          'pnts_coorientacoes_mest',
                                          'pnts_orientacoes_espec',
                                          'pnts_orientacoes_tcc',
                                          'pnts_orientacoes_ic',
                                          'ano_doutorado'])
        
    
    df.to_csv("dados/dados_pontuacao.csv")
    

if __name__ == "__main__":
    main()