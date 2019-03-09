#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Criado por: Sandro M. Silva
# Data: 25/02/2018
# 
# Software realiza a procura de arquivos e diretorio em um endereço de host. 
#
# Site: http://crowsec.wordpress.com
#


import requests
import sys
import argparse
import os
import time
import re

vermelho = '\033[31m'
verde = '\033[32m'
azul = '\033[34m'
amarelo = '\033[33m'
original = '\033[0;0m'

os.system('cls' if os.name =='nt' else 'clear')
print(50*'{}*' .format(verde))
print("BBS - BlackBird Search 1.0 - Alpha ")
print("\nRealiza procura de arquivos e diretórios em um host ")
print(50*'{}-{}' .format(verde,original))



# Utilizando a lib argparse para usar o programa com argumentos.

parser = argparse.ArgumentParser(description='Ajuda help')
parser.add_argument('-u', "--url",required=True,
        help= "Precisa informar a url com http://")
parser.add_argument('-w', "--wordlist", required=True,
        help= "Uma wordlist para brute force é necessária")

# action="store_true" permite setar apenas -r e nao exige argumentos como '-r texto'
parser.add_argument('-r', "--recursive",
        help="Realiza a busca de forma recursiva.", action="store_true")

# Modo verbose salva todas as tentivas no arquivo out.log e exibe também os erros 404,200.
parser.add_argument('-v', "--verbose",
        help="Ativa o modo verbose mostrando mais detalhes e salva a saida em out.log", action="store_true")



args = parser.parse_args()
salvou = open('out.log','w')
achado = []
logs = []


# Realiza a checagem se foi inserido http no endereço do host alvo.
if 'http' in args.url:
    print("{}Informações do Host{} \n" .format(verde,original)) 
    r = requests.get(args.url)
    info_host = r.headers  # Pega o headers da requisição no host e as exibe.
    for chave in info_host:
        print('{}{}:{}{}' .format(verde,chave,original,info_host[chave]))
    print(50*'*')
    print("\n{}[-]{} {}Procurando....{}\n" .format(azul,original,amarelo,original))


    if not os.path.exists(args.wordlist): # Checa se a wordlist informada  existe.
        print(vermelho,"Arquivo {} não existe\n" .format(args.wordlist))
        sys.exit()
    arq = open(args.wordlist,'r') # Abre arquivo de wordlist somente leitura.
    salvou = open('out.log','w') # Abre/cria arquivo out.log como escrita para salvar a saida do modo verbose.
    texto = arq.readlines()

    for linha in texto:
        if len(linha) == 1:
           # print("LINHA EM BRANCO\n")
            pass
        else:
            saida = linha.split() # Transforma a string em uma lista
            r = requests.get(args.url+'/'+saida[0]) # Faz request da url, concatenada com a palavra da wordlist.
                
        if args.verbose:
            if r.status_code == 200:
                print("{}[v]{}{}\t{}{}" .format(azul,original,r.url,verde,r.status_code))
                achado.append(r.url) # Adiciona a url que foi encontrada com codigo 200 a lista de achado.
                logs.append(r.url+'\t'+str(r.status_code)+'\n') # Adiciona a url encontrada no logs para salvar no out.log
                salvou.writelines(logs) # Escreve no arquivo out.log
            else:
                print("{}[v]{}{}\t{}{}" .format(azul,original,r.url,vermelho,r.status_code))
                logs.append(r.url+'\t'+str(r.status_code)+'\n')
                salvou.writelines(logs)
        else:
            
            if r.status_code == 200:
                achado.append(r.url)
                print("{}[>]{} {}" .format(verde,original,r.url))
    arq.close()

    if args.recursive:
        arq = open(args.wordlist,'r')
        texto = arq.readlines()
        print("\n{}{}[-]{} Realizando pesquisa recursiva...{}\n" .format(original,azul,amarelo,original))
        
        time.sleep(2) 
        
        for url in achado:
            for linha in texto:
                if len(linha) == 1:
                    pass
                else:
                    saida = linha.split()
                    filtro = re.sub('//$','/',url) # Realiza expressão regular para tirar duplicidade de // no final da url.
                    r = requests.get(filtro+saida[0])
                if args.verbose:
                    if r.status_code == 200:
                        achado.append(r.url+'/')
                        logs.append(r.url+'\t'+str(r.status_code)+'\n')
                        salvou.writelines(logs)
                        
                        print("{}[v]{}{}\t{}{}" .format(azul,original,r.url,verde,r.status_code))
                            
                    else:
                        logs.append(r.url+'\t'+str(r.status_code)+'\n')
                        salvou.writelines(logs)
                        print("{}[v]{}{}\t{}{}" .format(azul,original,r.url,vermelho,r.status_code))
                else:
                    if r.status_code == 200:
                        achado.append(r.url+'/')
                        print("{}[>]{} {}" .format(verde,original,r.url))
else:
    print("Endereço precisa conter http://")
    sys.exit(0)
print("\n")
arq.close()
salvou.close()
