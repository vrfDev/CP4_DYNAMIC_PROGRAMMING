# CHECKPOINT - Pre-processador de Transcricoes TOTVS
# Dynamic Programming - Engenharia de Software - FIAP / Challenge TOTVS
# =============================================================================

# -----------------------------------------------------------------------------
# DADOS DE PARTIDA
# -----------------------------------------------------------------------------

# Base minima comum
registros = [
    ["1247082", "LOCUTOR 54", "  Perguntar se era o novo uniforme da Totos.  "],
    ["1247082", "LOCUTOR 49", "A sua e da TOTVS, nao e?"],
    ["1247082", "LOCUTOR 72", "O time usa Protheu no processo."],
    ["1247082", "LOCUTOR 49", "Podemos revisar a proposta do Protheus."],
    ["1247082", "LOCUTOR 83", "O modulo Datasul esta funcionando."],
    ["1247082", "LOCUTOR 72", "A migracao para totvss ainda esta em analise."],
]

# Falas adicionadas pelo grupo
registros_do_grupo = [
    ["1309455", "LOCUTOR 12", "   O cliente pediu integracao do Fluig com o RM.   "],
    ["1309455", "LOCUTOR 31", "Hoje o financeiro roda no Protheuss, versao antiga."],
    ["1309455", "LOCUTOR 12", " Vale avaliar o Senior tambem antes de fechar a proposta. "],
]

for fala in registros_do_grupo:
    registros.append(fala)

# Catalogo oficial de produtos (referencia de escrita correta)
catalogo = ["totvs", "protheus", "datasul", "rm", "fluig", "senior"]

# Termos observados na transcricao (base minima + termos das falas do grupo)
termos_observados = ["Totos", "TOTVS", "Protheu", "Protheus", "Datasul", "totvss"]

termos_do_grupo = ["Fluig", "RM", "Protheuss", "Senior"]

for termo in termos_do_grupo:
    termos_observados.append(termo)


# -----------------------------------------------------------------------------
# FUNCOES DE APOIO (impressao)
# -----------------------------------------------------------------------------

def titulo(texto):
    """Imprime um cabecalho de secao para facilitar a leitura da saida."""
    print("")
    print("=" * 70)
    print(texto)
    print("=" * 70)


def primeira_linha(matriz):
    """Devolve a primeira linha da matriz DP (casos-base do eixo horizontal)."""
    return matriz[0]


def primeira_coluna(matriz):
    """Devolve a primeira coluna da matriz DP (casos-base do eixo vertical)."""
    coluna = []
    for i in range(len(matriz)):
        coluna.append(matriz[i][0])
    return coluna


def imprimir_matriz(matriz):
    """Imprime a matriz DP linha a linha."""
    for i in range(len(matriz)):
        print("   ", matriz[i])


# -----------------------------------------------------------------------------
# ETAPA 1 - REPRESENTAR E VALIDAR AS FALAS
# -----------------------------------------------------------------------------

def exibir_registros(lista_de_registros):
    """Percorre os registros e imprime meeting, locutor e texto separadamente.

    Retorna a quantidade total de registros processados.
    """
    total = 0
    for registro in lista_de_registros:
        meeting = registro[0]
        locutor = registro[1]
        texto = registro[2]
        total = total + 1
        print("Registro", total)
        print("   meeting :", meeting)
        print("   locutor :", locutor)
        print("   texto   :", texto)
    return total


# -----------------------------------------------------------------------------
# ETAPA 2 - LIMPEZA BASICA
# -----------------------------------------------------------------------------

def limpar_texto(texto):
    """Aplica a limpeza basica: caixa baixa e remocao de espacos nas pontas.

    O texto entra por parametro e sai pelo return: nada fica fixo na funcao.
    """
    return texto.lower().strip()


def limpar_registros(lista_de_registros):
    """Gera uma nova estrutura limpa preservando meeting e locutor."""
    limpos = []
    for registro in lista_de_registros:
        meeting = registro[0]
        locutor = registro[1]
        texto_limpo = limpar_texto(registro[2])
        limpos.append([meeting, locutor, texto_limpo])
    return limpos


# -----------------------------------------------------------------------------
# ETAPA 3 - TRIAGEM POR IGUALDADE EXATA
# -----------------------------------------------------------------------------

def comparar_exato(a, b):
    """Compara duas strings apos a limpeza basica. Retorna True ou False."""
    return limpar_texto(a) == limpar_texto(b)


def esta_na_lista(item, lista):
    """Verifica presenca de um item em uma lista sem usar estruturas prontas."""
    for elemento in lista:
        if elemento == item:
            return True
    return False


def triar_termos(lista_de_termos, lista_catalogo):
    """Separa os termos em EXATO e PENDENTE_DP.

    Retorna [relatorio, pendentes_dp], onde cada linha do relatorio e
    [termo_original, termo_limpo, status, correspondencia_no_catalogo].
    Nenhuma correcao automatica e feita aqui.
    """
    relatorio = []
    pendentes_dp = []

    for termo in lista_de_termos:
        termo_limpo = limpar_texto(termo)
        status = "PENDENTE_DP"
        correspondencia = "-"

        for item_catalogo in lista_catalogo:
            if comparar_exato(termo, item_catalogo):
                status = "EXATO"
                correspondencia = item_catalogo
                break

        if status == "PENDENTE_DP":
            if esta_na_lista(termo_limpo, pendentes_dp) == False:
                pendentes_dp.append(termo_limpo)

        relatorio.append([termo, termo_limpo, status, correspondencia])

    return [relatorio, pendentes_dp]


# -----------------------------------------------------------------------------
# ETAPA 4 - PREPARAR A MATRIZ DE PROGRAMACAO DINAMICA
# -----------------------------------------------------------------------------

def preparar_dp(a, b):
    """Cria a matriz DP com dimensao (len(a)+1) x (len(b)+1).

    Preenche apenas os casos-base:
      - primeira coluna: 0, 1, 2, ... (custo de apagar caracteres de 'a')
      - primeira linha : 0, 1, 2, ... (custo de inserir caracteres de 'b')
    As celulas internas continuam zeradas de proposito: nesta etapa elas ainda
    NAO representam distancia de edicao.
    """
    linhas = len(a) + 1
    colunas = len(b) + 1

    matriz = []
    for i in range(linhas):
        linha = []
        for j in range(colunas):
            linha.append(0)
        matriz.append(linha)

    for i in range(linhas):
        matriz[i][0] = i

    for j in range(colunas):
        matriz[0][j] = j

    return matriz


# -----------------------------------------------------------------------------
# ETAPA 5 - CONECTAR A PREPARACAO DE DP AO PIPELINE
# -----------------------------------------------------------------------------

def montar_pares_pendentes(pendentes_dp, lista_catalogo):
    """Monta os pares [pendente, candidato] que irao para a DP na proxima etapa.

    Cada termo pendente e cruzado com todos os itens do catalogo, pois ainda nao
    existe criterio de similaridade para escolher um unico candidato.
    """
    pares = []
    for pendente in pendentes_dp:
        for candidato in lista_catalogo:
            pares.append([pendente, candidato])
    return pares


def detalhar_par(a, b):
    """Prepara a DP de um par e imprime as evidencias exigidas na Etapa 5."""
    matriz = preparar_dp(a, b)
    print("Par:", a, "x", b)
    print("   linhas          :", len(matriz))
    print("   colunas         :", len(matriz[0]))
    print("   primeira linha  :", primeira_linha(matriz))
    print("   primeira coluna :", primeira_coluna(matriz))
    print("   matriz preparada:")
    imprimir_matriz(matriz)
    return matriz


# -----------------------------------------------------------------------------
# TESTES MINIMOS DE ACEITACAO
# -----------------------------------------------------------------------------

def verificar(descricao, obtido, esperado):
    """Compara o valor obtido com o esperado e imprime o resultado do teste."""
    if obtido == esperado:
        resultado = "OK"
    else:
        resultado = "FALHA"
    print("[" + resultado + "]", descricao)
    print("        esperado:", esperado)
    print("        obtido  :", obtido)
    if obtido == esperado:
        return 1
    return 0


def executar_testes():
    """Roda os casos minimos de aceitacao do enunciado."""
    aprovados = 0
    total = 0

    total = total + 1
    aprovados = aprovados + verificar(
        'limpar_texto("  TOTOS  ")', limpar_texto("  TOTOS  "), "totos"
    )

    total = total + 1
    aprovados = aprovados + verificar(
        'comparar_exato("TOTVS", " totvs ")', comparar_exato("TOTVS", " totvs "), True
    )

    total = total + 1
    aprovados = aprovados + verificar(
        'comparar_exato("Totos", "totvs")', comparar_exato("Totos", "totvs"), False
    )

    dp_totos = preparar_dp("totos", "totvs")

    total = total + 1
    aprovados = aprovados + verificar(
        'preparar_dp("totos", "totvs") -> dimensao',
        [len(dp_totos), len(dp_totos[0])],
        [6, 6],
    )

    total = total + 1
    aprovados = aprovados + verificar(
        "primeira linha de totos x totvs",
        primeira_linha(dp_totos),
        [0, 1, 2, 3, 4, 5],
    )

    total = total + 1
    aprovados = aprovados + verificar(
        "primeira coluna de totos x totvs",
        primeira_coluna(dp_totos),
        [0, 1, 2, 3, 4, 5],
    )

    dp_protheu = preparar_dp("protheu", "protheus")

    total = total + 1
    aprovados = aprovados + verificar(
        'preparar_dp("protheu", "protheus") -> dimensao',
        [len(dp_protheu), len(dp_protheu[0])],
        [8, 9],
    )

    # A lista pendentes_dp precisa conter todos os termos ruidosos da triagem.
    # O teste procura cada termo esperado e acumula em 'faltando' o que nao
    # apareceu: se a lista final ficar vazia, nenhum pendente foi perdido.
    resultado_triagem = triar_termos(termos_observados, catalogo)
    pendentes_obtidos = resultado_triagem[1]

    termos_ruidosos = ["totos", "protheu", "totvss", "protheuss"]
    faltando = []
    for termo in termos_ruidosos:
        if esta_na_lista(termo, pendentes_obtidos) == False:
            faltando.append(termo)

    total = total + 1
    aprovados = aprovados + verificar(
        "pendentes_dp contem os termos ruidosos",
        faltando,
        [],
    )

    return [aprovados, total]


# -----------------------------------------------------------------------------
# PIPELINE PRINCIPAL
# -----------------------------------------------------------------------------

def main():
    # ---------------------------- ETAPA 1 ------------------------------------
    titulo("ETAPA 1 - REGISTROS BRUTOS")
    total_registros = exibir_registros(registros)
    print("")
    print("Total de registros processados:", total_registros)

    # ---------------------------- ETAPA 2 ------------------------------------
    titulo("ETAPA 2 - LIMPEZA BASICA (antes -> depois)")
    registros_limpos = limpar_registros(registros)

    quantidade_amostras = 4
    for i in range(quantidade_amostras):
        print("Registro", i + 1, "-", registros[i][0], "|", registros[i][1])
        print("   antes : [" + registros[i][2] + "]")
        print("   depois: [" + registros_limpos[i][2] + "]")

    print("")
    print("Total de registros limpos:", len(registros_limpos))
    print("Estrutura preservada (exemplo):", registros_limpos[0])

    # ---------------------------- ETAPA 3 ------------------------------------
    titulo("ETAPA 3 - TRIAGEM POR IGUALDADE EXATA")
    resultado_triagem = triar_termos(termos_observados, catalogo)
    relatorio = resultado_triagem[0]
    pendentes_dp = resultado_triagem[1]

    total_exatos = 0
    for linha in relatorio:
        termo_original = linha[0]
        termo_limpo = linha[1]
        status = linha[2]
        correspondencia = linha[3]
        if status == "EXATO":
            total_exatos = total_exatos + 1
        print(
            "termo:", termo_original,
            "| limpo:", termo_limpo,
            "| status:", status,
            "| catalogo:", correspondencia,
        )

    print("")
    print("Termos EXATO      :", total_exatos)
    print("Termos PENDENTE_DP:", len(pendentes_dp))
    print("Lista pendentes_dp:", pendentes_dp)
    print("")
    print("Observacao: lower() e strip() nao corrigem erro de transcricao.")
    print("'totos' continua diferente de 'totvs' depois da limpeza.")

    # ---------------------------- ETAPA 4 ------------------------------------
    titulo("ETAPA 4 - MATRIZ DP PREPARADA (pares de teste)")
    pares_de_teste = [
        ["totos", "totvs"],
        ["protheu", "protheus"],
        ["totvss", "totvs"],
    ]

    for par in pares_de_teste:
        detalhar_par(par[0], par[1])
        print("")

    # ---------------------------- ETAPA 5 ------------------------------------
    titulo("ETAPA 5 - PENDENTES CONECTADOS A DP")
    pares_pendentes = montar_pares_pendentes(pendentes_dp, catalogo)

    print("Pares preparados a partir de pendentes_dp x catalogo:")
    print("")
    total_matrizes = 0
    for par in pares_pendentes:
        a = par[0]
        b = par[1]
        matriz = preparar_dp(a, b)
        total_matrizes = total_matrizes + 1
        print(
            a, "x", b,
            "| linhas:", len(matriz),
            "| colunas:", len(matriz[0]),
            "| 1a linha:", primeira_linha(matriz),
            "| 1a coluna:", primeira_coluna(matriz),
        )

    print("")
    print("Total de matrizes preparadas:", total_matrizes)
    print("Celulas internas nao foram preenchidas: transicao fica para a Etapa 2 da disciplina.")

    # ------------------------------ TESTES -----------------------------------
    titulo("TESTES MINIMOS DE ACEITACAO")
    resultado_testes = executar_testes()
    aprovados = resultado_testes[0]
    total_testes = resultado_testes[1]
    print("")
    print("Testes aprovados:", aprovados, "de", total_testes)

    # ------------------------------ RESUMO -----------------------------------
    titulo("RESUMO DE EXECUCAO")
    print("Registros brutos          :", total_registros)
    print("Registros limpos          :", len(registros_limpos))
    print("Termos observados         :", len(termos_observados))
    print("Termos EXATO              :", total_exatos)
    print("Termos PENDENTE_DP        :", len(pendentes_dp))
    print("Pendentes                 :", pendentes_dp)
    print("Matrizes DP preparadas    :", total_matrizes)
    print("Testes minimos aprovados  :", aprovados, "de", total_testes)


main()