from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json


def formata_html(html: bytes) -> str:
    # transforma o html em string, remove os caracteres especiais e transforma o decode em UTF-8
    html: str = html.decode('UTF-8')
    return " ".join(html.split()).replace("> <", "><")


def gera_dict(lista_tags: list) -> dict:
    # Gera um dict com os atributos name e content da tag
    lista_metas: list = []
    for item in lista_tags:
        if 'name' and 'content' in item.attrs:
            lista_metas.append({'name': item.__dict__['name'],
                                'content': item.__dict__['attrs']['content']})

    # retorna um dicionário com Metas_site como chave e a lista de dicts criada
    return {'Metas_site': lista_metas}


def get_metas(url: str):
    # Realiza o acesso a página
    try:
        headers: dict = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/103.0.5060.114 Safari/537.36 OPR/89.0.4447.48'}
        # Requisição
        req = Request(url, headers=headers)
        # Acessa o html da página
        response = urlopen(req)
        html: bytes = response.read()
        # Cria o obj soup e já chama a função para formatar o hmtl
        soup = BeautifulSoup(formata_html(html), 'html.parser')

        # Retorna o Json contendo as tags metas e seus atributos
        return json.dumps(obj=gera_dict(soup.findAll('meta')))

    except HTTPError as e:
        print(e.status)

    except URLError as e:
        print(e.reason)


if __name__ == '__main__':
    get_metas("https://www.youtube.com/watch?v=DvE7O3bLQgE&list=LL&index=23")
