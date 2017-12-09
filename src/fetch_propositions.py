import datetime
import os

import requests

URL_FORMAT = (
    'http://www.camara.leg.br'
    '/SitCamaraWS/Proposicoes.asmx/ListarProposicoes'
    '?sigla=PL&numero=&ano={}&datApresentacaoIni=&datApresentacaoFim='
    '&parteNomeAutor=&idTipoAutor=&siglaPartidoAutor=&siglaUFAutor='
    '&generoAutor=&codEstado=&codOrgaoEstado=&emTramitacao='
)
FILENAME_FORMAT = 'data/sources/propositions/{}.xml'

folder = '/'.join(FILENAME_FORMAT.split('/')[:-1])
os.makedirs(folder)

for year in range(1945, datetime.datetime.now().year + 1):
    url = URL_FORMAT.format(year)
    request = requests.get(url, stream=True)
    filename = FILENAME_FORMAT.format(year)
    with open(filename, 'wb') as file:
        for chunk in request.iter_content(chunk_size=128):
            file.write(chunk)
