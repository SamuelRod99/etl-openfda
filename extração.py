import requests
import logging
import time


logger = logging.getLogger(__name__)


def extrair_dados(url, limit=3, max_paginas=1):

    skip = 0
    todos_dados = []

    logger.info("Extração iniciada")

    for pagina in range(max_paginas):

        params = {
            "limit": limit,
            "skip": skip
        }

        tentativa= 1
        max_tentativa = 3
        sucesso_pagina = False

        while tentativa <= max_tentativa:


            logger.info(
                "Extraindo página %d (Tentativa %d/%d) | skip=%d | limit=%d",
                pagina + 1,
                skip,
                limit,
                tentativa,
            )

            try:#tentativa de request
                resposta = requests.get(
                    url,
                    params=params,
                    timeout=10
                )

                resposta.raise_for_status()

                dados_da_pagina = resposta.json()

                resultados = dados_da_pagina.get("results", [])

                todos_dados.extend(resultados)

                max_tentativa = True
                break#quebra do loop de tentativas, para passar para a proxima extração

            except requests.exceptions.HTTPError as erro:
                logger.error("Erro HTTP: %s", erro)
                tentativa += 1
                time.sleep(2)

            except requests.exceptions.ConnectionError:
                logger.error("Erro de conexão")
                tentativa += 1
                time.sleep(2)

            except requests.exceptions.Timeout:
                logger.error("A API demorou muito para responder")
                tentativa += 1
                time.sleep(2)

            except requests.exceptions.RequestException as erro:
                logger.error("Erro inesperado: %s", erro)
                tentativa += 1
                time.sleep(2)

        if sucesso_pagina == False:
            logger.error("Falha definitiva na página %d após %d tentativas. Interrompendo script.", pagina + 1, max_tentativa)
            break

        # Incrementa o offset para a próxima requisição
        skip += limit


    # Validação dos dados extraídos
    if not isinstance(todos_dados, list):
        logger.error(
            "Erro: dados retornaram em formato diferente de uma lista"
        )

    if len(todos_dados) == 0:
        logger.error("Erro: nenhum registro foi extraído")

    return todos_dados