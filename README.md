# Checkpoint — Pré-processador de Transcrições TOTVS

Etapa 1 do pipeline de pré-processamento das transcrições do Challenge TOTVS:
**dados brutos → estruturas → limpeza → triagem → DP preparada**.

Disciplina: Dynamic Programming — Engenharia de Software (FIAP)
Entrega: 13/09/2026

## Integrantes

- Vitor Ramos de Farias RM: 561958
- Leonardo Eiji Kina RM: 562784
- Nicholas Braga de Souza RM: 561733
- Tomé Rossi Giani RM: 562422

## Objetivo

Construir a parte inicial de uma ferramenta determinística de pré-processamento
de transcrições. O programa organiza as falas, aplica limpeza básica, separa os
termos que já batem exatamente com o catálogo de produtos daqueles que exigirão
comparação aproximada, e prepara as matrizes de Programação Dinâmica com seus
casos-base.

## Como executar

```bash
python checkpoint_preprocessamento_totvs.py
```

Não há dependências externas: apenas Python 3 padrão. Também funciona colando o
conteúdo em uma célula do Google Colab ou abrindo o arquivo no PyCharm e
executando com Shift+F10.

## Restrição respeitada

O código usa somente: strings, listas e listas de listas, funções, `if`, `for`,
`len`, `range`, `lower()`, `strip()`, `append()`, comparação exata e matriz DP
com casos-base. Não há uso de `difflib`, `pandas`, bibliotecas de NLP, de
similaridade, de distância de Levenshtein nem de IA generativa.

## Organização das funções

| Função | Etapa | O que faz |
|---|---|---|
| `exibir_registros(lista)` | 1 | Percorre os registros e imprime `meeting`, `locutor` e `texto` separadamente; retorna o total processado |
| `limpar_texto(texto)` | 2 | Limpeza básica com `lower()` + `strip()`; recebe por parâmetro e devolve por `return` |
| `limpar_registros(lista)` | 2 | Gera `registros_limpos` preservando `meeting` e `locutor` |
| `comparar_exato(a, b)` | 3 | Reutiliza `limpar_texto()` e devolve `True`/`False` na igualdade exata |
| `esta_na_lista(item, lista)` | 3 | Evita duplicar termos em `pendentes_dp` |
| `triar_termos(termos, catalogo)` | 3 | Classifica cada termo como `EXATO` ou `PENDENTE_DP` e monta a lista de pendentes com `append()` |
| `preparar_dp(a, b)` | 4 | Cria a matriz `(len(a)+1) x (len(b)+1)` e preenche apenas as bordas |
| `montar_pares_pendentes(pendentes, catalogo)` | 5 | Cruza cada pendente com o catálogo, gerando os pares que irão para a DP |
| `detalhar_par(a, b)` | 5 | Prepara a DP de um par e imprime dimensões, primeira linha e primeira coluna |
| `verificar(...)` / `executar_testes()` | Testes | Roda os casos mínimos de aceitação e imprime OK/FALHA |
| `main()` | — | Encadeia as cinco etapas; cada uma consome a saída da anterior |

Nenhum dado fica preso dentro de função: `registros`, `catalogo` e
`termos_observados` estão no escopo do módulo e circulam por parâmetro e
`return`.

## Dados usados

Além da base mínima comum do enunciado, o grupo adicionou 3 falas adaptadas do
material do próprio Challenge (reunião `1309455`), sem nomes de clientes ou
qualquer dado pessoal. Essas falas trouxeram os termos `Fluig`, `RM`,
`Protheuss` e `Senior`, que também entram na triagem.

## O significado de `dp[i][j]` e do `+1`

A matriz DP guarda a solução dos subproblemas da distância de edição entre duas
strings `a` e `b`.

**`dp[i][j]` = o menor número de operações (inserir, remover ou substituir um
caractere) necessário para transformar os `i` primeiros caracteres de `a` nos
`j` primeiros caracteres de `b`.**

O `+1` em `linhas = len(a) + 1` e `colunas = len(b) + 1` existe porque os
índices não representam apenas os caracteres, mas os **prefixos** das strings —
e o primeiro prefixo é a string vazia. A linha 0 e a coluna 0 representam esse
prefixo vazio, e por isso a matriz precisa de uma linha e uma coluna a mais do
que o tamanho das strings.

Os casos-base saem direto dessa definição:

- `dp[i][0] = i` → transformar os `i` primeiros caracteres de `a` em uma string
  vazia custa `i` remoções;
- `dp[0][j] = j` → transformar uma string vazia nos `j` primeiros caracteres de
  `b` custa `j` inserções.

Exemplo com `preparar_dp("totos", "totvs")`, matriz 6 × 6:

```
    [0, 1, 2, 3, 4, 5]
    [1, 0, 0, 0, 0, 0]
    [2, 0, 0, 0, 0, 0]
    [3, 0, 0, 0, 0, 0]
    [4, 0, 0, 0, 0, 0]
    [5, 0, 0, 0, 0, 0]
```

**Atenção:** os zeros das células internas ainda **não** são distâncias de
edição — são apenas valores iniciais. Eles serão substituídos na próxima etapa
da disciplina, quando a relação de recorrência for aplicada.

## Armadilha tratada

`lower()` e `strip()` normalizam caixa e espaços, mas não corrigem erro de
transcrição: depois da limpeza, `"Totos"` vira `"totos"` e continua diferente de
`"totvs"`. Por isso a triagem da Etapa 3 não tenta corrigir nada — apenas separa
o que é resolvível por igualdade exata do que precisará de comparação
aproximada.

## Saída do programa (resumo da execução)

```
Registros brutos          : 9
Registros limpos          : 9
Termos observados         : 10
Termos EXATO              : 6
Termos PENDENTE_DP        : 4
Pendentes                 : ['totos', 'protheu', 'totvss', 'protheuss']
Matrizes DP preparadas    : 24
Testes minimos aprovados  : 8 de 8
```

## Testes mínimos de aceitação

| Teste | Esperado | Status |
|---|---|---|
| `limpar_texto("  TOTOS  ")` | `"totos"` | OK |
| `comparar_exato("TOTVS", " totvs ")` | `True` | OK |
| `comparar_exato("Totos", "totvs")` | `False` | OK |
| `preparar_dp("totos", "totvs")` | matriz 6 × 6 | OK |
| primeira linha do caso acima | `[0, 1, 2, 3, 4, 5]` | OK |
| primeira coluna do caso acima | `[0, 1, 2, 3, 4, 5]` | OK |
| `preparar_dp("protheu", "protheus")` | matriz 8 × 9 | OK |
| `pendentes_dp` | contém `totos`, `protheu`, `totvss` e `protheuss` | OK |

Os testes ficam na função `executar_testes()` e rodam automaticamente ao final
da execução do programa.

## Por que isso importa em produção

Rodar uma etapa determinística antes de mandar a transcrição para uma IA
generativa reduz ruído, organiza os registros e separa o que é trivial do que
realmente exige comparação aproximada. O resultado é menos token gasto, um
pipeline testável e controle sobre o que é decidido por regra e o que é
delegado ao modelo.
