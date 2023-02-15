#%%
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import logging

# %%
url = 'https://portalcafebrasil.com.br/todos/podcasts/page/5/?ajax=true'

# %%
#puxar o retorno da url
retorno = requests.get(url)
retorno
# %%
retorno.text
soup = bs(retorno.text)
lista_podcast = soup.find_all('h5')

# %%
lista_podcast
# %%
#link do site
url = 'https://portalcafebrasil.com.br/todos/podcasts/page/{}/?ajax=true'

# %%
# .format puxa a formatação onde tem o {}
url.format(5)
# %%
# função pra pegar a url
def pegar_podcast(url):
    ret = requests.get(url)
    soup = bs(ret.text)
    return soup.find_all('h5')

# %%
pegar_podcast(url.format(5))


# %%
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)

# %%

n = 1
lista_podcast = []
lista_get = pegar_podcast(url.format(n))
log.debug(f"Coletado {len(lista_podcast)} episódios do link: {url.format(n)}")

while len(lista_get) > 0:
    lista_podcast += lista_get
    n += 1
    lista_get = pegar_podcast(url.format(n))
    log.debug(f"Coletado {len(lista_podcast)} episódios do link: {url.format(n)}")

# %%
len(lista_podcast)
# %%
lista_podcast
# %%

df = pd.DataFrame(columns=['nome', 'link'])

# %%
for item in lista_podcast:
    df.loc[df.shape[0]] = [item.text, item.a['href']]

# %%
df.shape
# %%
df
# %%
df.to_csv('banco_podcast', sep=';', index=False)