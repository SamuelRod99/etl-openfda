import requests
import logging


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

        logger.info(
            "Extraindo página %d | skip=%d | limit=%d",
            pagina + 1,
            skip,
            limit
        )

        try:
            resposta = requests.get(
                url,
                params=params,
                timeout=10
            )

            resposta.raise_for_status()

            dados_da_pagina = resposta.json()

            resultados = dados_da_pagina.get("results", [])

            todos_dados.extend(resultados)

            # Incrementa o offset para a próxima requisição
            skip += limit

        except requests.exceptions.HTTPError as erro:
            logger.error("Erro HTTP: %s", erro)
            break

        except requests.exceptions.ConnectionError:
            logger.error("Erro de conexão")
            break

        except requests.exceptions.Timeout:
            logger.error("A API demorou muito para responder")
            break

        except requests.exceptions.RequestException as erro:
            logger.error("Erro inesperado: %s", erro)
            break


    # Validação dos dados extraídos
    if not isinstance(todos_dados, list):
        logger.error(
            "Erro: dados retornaram em formato diferente de uma lista"
        )

    if len(todos_dados) == 0:
        logger.error("Erro: nenhum registro foi extraído")

    return todos_dados