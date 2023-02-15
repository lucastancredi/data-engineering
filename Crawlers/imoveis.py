#%%
from itertools import repeat
import requests, pandas as pd
from bs4 import BeautifulSoup as bs
import logging
import schedule
# %%
logging.basicConfig(format='%(filename)s: %(message)s',
                    level=logging.DEBUG)
# logging.basicConfig(format='%(filename)s: %(message)s', level=logging.info)


# %%
def extrair_valor(element, tag, tipo_classe, var_pre_texto=None):
    try:
        if var_pre_texto:
            return element.find(tag, {'class' : tipo_classe}).find(var_pre_texto).text.strip()
        else:
            return element.find(tag, {'class' : tipo_classe}).text.strip()
    except Exception:
        return None


# %%

DICIO_PARAMETROS = {
    'descricao': ['span', 'property-card__title'],
    'endereco': ['span', 'property-card__address'],
    'area': ['li', 'property-card__detail-area', 'span'],
    'quartos': ['li', 'property-card__detail-room', 'span'],
    'banheiro': ['li', 'property-card__detail-bathroom', 'span'],
    'vagas': ['li', 'property-card__detail-garage', 'span'],
    'valor': ['div', 'property-card__price'],
    'condominio': ['strong', 'js-condo-price']
}

df_final = pd.DataFrame(columns=list(DICIO_PARAMETROS.keys())+['site'])

URL = 'https://www.vivareal.com.br/venda/distrito-federal/brasilia/?pagina={}'

n_da_pagina = 1

#%%
CAMINHO_PG1 = '//*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[2]'

for i in range(2):
    soup_test = bs(requests.get(URL.format(1)).text)

    soup_test = soup_test.find('div', 'results-main__panel js-list')\
    .find('ul',{'class': 'pagination__wrapper'})\
    .find('button', {'class': 'js-change-page', '})

    print(soup_test)


#%%

while True:
    retorno = requests.get(URL.format(n_da_pagina))

    logging.info(f'PAGINA {n_da_pagina} ENCONTRADA')

    # MEMORIZA PAGINA 1
    if n_da_pagina == 1: soup_pg1 = bs(retorno.text)
        
    # PAGINA ATUAL
    soup = bs(retorno.text)

    if n_da_pagina > 1 and soup == soup_pg1:
        break


    aps = soup.find_all('a', {'class' : 'property-card__content-link js-card-title'})
    qts_aps = soup.find('strong', {'class' : 'results-summary__count'}).text.replace('.', '')
    qts_aps = float(qts_aps)
    ap = aps[0]




    lista_info_extraida = []
    for ap in aps:
        temp_list = []
        for nome_variavel, parametros in DICIO_PARAMETROS.items():
            temp_list.append(extrair_valor(ap, *parametros))
        site = 'https://www.vivareal.com.br' + ap['href']
        temp_list.append(site)

        pd.concat([df_final, pd.Series(temp_list)], axis=1)
        #df_final.append(temp_list.copy())


   

    n_da_pagina = n_da_pagina+1

# %%

print(df_final)