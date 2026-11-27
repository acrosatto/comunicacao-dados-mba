# Comparação de decisões: notebook da Ana × notebooks do grupo

Decisões de escopo e limpeza em que os notebooks da Ana (`01_exploratoria.ipynb` e `02_variaveis.ipynb`) e os notebooks `01` a `03` da pasta `analise/` chegam a tratamentos diferentes, ou em que a proposta ainda não foi aplicada no código. Serve para o grupo fechar cada ponto antes do `04_preparacao.ipynb`.

**Situação:** *igual* (mesmo tratamento), *diferente* (tratamentos diferentes) ou *a decidir* (proposta sem decisão do grupo).

## Escopo

| Ponto | Ana | Notebooks do grupo | Situação |
| --- | --- | --- | --- |
| Reservas usadas no modelo | Base inteira até a seção 4; o escopo é avaliado na seção 5 | Só `No Deposit` (104.641 reservas, 28,4% de cancelamento), aplicado desde o notebook 01 | a decidir (TODO, item 1) |

## Limpeza

| Ponto | Reservas | Ana | Notebooks do grupo | Situação |
| --- | --- | --- | --- | --- |
| `children` vazio | 4 | Remover: cadastros incompletos (as 4 têm `distribution_channel = Undefined`, 2 têm `market_segment = Undefined`) | Preencher com 0 (sem criança) | diferente |
| Sem hóspede | 180 | Remover | Proposta de remover (notebook 01, seção 12), ainda não aplicada no código | a decidir |
| Diária negativa (−6,38) | 1 | Remover | Não removida; continua no escopo | diferente |
| Diária de 5.400 | 1 | Remover | Fica fora só por causa do escopo (é `Non Refund`) | igual no escopo |
| Zero noites | 715 | Remover (notebook 01, seção 4.4). Todas têm diária zero e 95,1% terminaram em check-out. Pode ser uso do quarto durante o dia (outro produto) ou um valor gravado depois da chegada (vazamento); sem como garantir, saem | Dicionário: juntar com 1 noite. Notebook 03: faixa própria (`0`) em `faixa_noites` | diferente |
| `meal = Undefined` | 1.169 (642 no treino do escopo) | Manter separado. Undefined só existe no resort e SC quase só no urbano; no urbano, SC cancela mais que BB (35,7% × 28,7%); no resort, Undefined cancela menos (13,2% × 22,7%) | Juntar com SC em `sem_refeicao` | diferente |
| Linhas idênticas | 31.994 cópias | Manter; rodar o modelo sem elas para conferir | Manter; rodar o modelo sem elas para conferir | igual |
| `agent` / `company` vazios | 16.340 / 112.593 | Os códigos saem. `company` vira a binária "paga por empresa" (vazio = não), em teste | As duas saem do modelo (`agent`: código sem significado de negócio; `company`: 94% vazia) | diferente em `company` (ver Variáveis) |
| `Undefined` no segmento e no canal | 2 e 5 | Segmento em "Outros"; o canal tende a sair | Segmento em "Outros" (com Complementary e Aviation); o canal sai | igual |

## Variáveis

| Variável | Ana | Notebooks do grupo | Situação |
| --- | --- | --- | --- |
| `previous_cancellations` | Sai: 1 cancelamento anterior cancela 92,5% no treino (79,9% dessas reservas são de 2015) e 17,6% no teste, contra 32,0% sem cancelamento anterior. A relação muda de sentido em 2017 | Testar: já cancelou × nunca cancelou | diferente |
| `babies` | Sai: com bebê cancela 20,8%, contra 26,8% sem; sentido oposto ao de `children`, então não junta com ela | Sai: quase sempre zero. A derivada `com_crianca` (notebook 03) soma crianças e bebês | igual para `babies`; diferente na derivada |
| `lead_time` | Faixas pela árvore de decisão (ganho de informação): 0, 1–8, 9–25, 26–257, 258–315 e mais de 315 dias. A proposta do `TODO.md` fica 261,5 pontos de BIC atrás. Acima de 315 dias a taxa cai (blocos de grupos e operadoras); o notebook 02, seção 4, confere se o corte continua com o segmento no modelo | `TODO.md` e dicionário: até 7, 8–30, 31–90, 91–180 e mais de 180 dias | diferente |
| `noites` | Faixas pela árvore de decisão: 1, 2–3 e 4 ou mais (as zero noites saem da base). Separar 4–7 de mais de 7 não se sustenta pelo BIC | Dicionário: até 1 (zero noites junto), 2–3, 4–7 e mais de 7. Notebook 03: zero noites numa faixa própria | quase igual ao dicionário |
| `meal` | Testar com quatro níveis: BB (referência), com pensão (HB e FB), SC e Undefined | Testar: sem refeição (SC e Undefined) × com refeição | diferente |
| `arrival_date_month` | Duas temporadas: jul–ago × resto do ano. Só jul–ago fica acima nos dois anos (35,2% e 30,9%); em 2016, abr–jun (26,1%) e set–mar (27,1%) não se separam | Três temporadas: jul–ago, abr–jun e set–mar | diferente |
| `customer_type` | A decidir no notebook 02, seção 4. Group (344 reservas, 12,8%) não se parece com nenhum nível. Possibilidades: juntar com Contract (taxa mais próxima, 22,5%), juntar com Transient-Party (conceito mais próximo, 24,2%), deixar separado ou tirar a variável (V de 0,049; repete parte do segmento) | Entra | a decidir |
| `company` | Testar "paga por empresa": nos grupos, 4,7% de cancelamento com empresa (614 reservas), contra 34,1% sem | Sai: quase toda vazia | diferente |
| `adr` | Em euros, não serve: a relação muda em 2017 (acima de 130, de cerca de 31% no treino para 38% a 40% no teste) e o preço sobe (mediana do urbano de 96,2 para 114,4). O notebook 02, seção 4, decide se entra | Entra como número | diferente |
| `agent` | Sai: 275 códigos anônimos, embora separem reservas do mesmo segmento (agência online: de 13,9% a 38,7%) | Sai por ora | igual |

## Leituras

| Ponto | Ana | Notebooks do grupo | Situação |
| --- | --- | --- | --- |
| Alta de 2017 | Cerca de 70% vem do perfil das reservas: com as taxas do treino em cada grupo (hotel × segmento × antecedência × temporada) e o perfil de 2017, a taxa esperada é 30,3%, contra 26,8% no treino e 31,9% real | Notebook 03: "a alta é sobretudo comportamento, concentrada na agência online com antecedência longa" | diferente; conferir se a diferença vem dos grupos usados em cada decomposição |

## Para fechar com o grupo

1. **`children` vazio:** remover ou preencher com 0? São só 4 reservas: a escolha não muda o modelo, mas o `04_preparacao` precisa de uma regra só.
2. **Sem hóspede, diária negativa e zero noites:** aplicar a remoção no `04_preparacao`. Nas duas primeiras, as propostas apontam para o mesmo lado; a remoção das zero noites é nova (o dicionário junta com 1 noite, e o notebook 03 deixa numa faixa própria).
3. **Faixas de antecedência e de noites:** adotar os cortes da árvore de decisão (notebook 02, seções 3.1 e 3.2) no lugar dos do `TODO.md` e do dicionário.
4. **`meal`:** quatro níveis (Undefined separado) ou sem refeição × com refeição. Com a junção, efeitos opostos dos dois hotéis se misturam.
5. **`previous_cancellations`:** tirar do modelo ou manter em teste? Se ficar em teste, conferir o sinal do coeficiente também no teste (2017).
6. **Criança e bebê:** `com_crianca` com ou sem os bebês.
7. **Temporadas:** duas (jul–ago × resto) ou três.
8. **`company`:** testar "paga por empresa" ou deixar fora.
9. **`customer_type`:** entra ou sai (notebook 02, seção 4); se entrar, o destino do nível Group.
