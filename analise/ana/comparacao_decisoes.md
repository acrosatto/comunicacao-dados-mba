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
| `previous_cancellations` | A refazer (notebook 02, seção 3.9). A proposta anterior (sair, porque a relação se invertia em 2017) usava o teste e foi retirada. No treino, a ordem se mantém: 1 cancelamento anterior cancela 98,4% em 2015 e 69,4% em 2016, contra 16,1% e 27,1% sem; 79,9% dessas reservas são de 2015 | Testar: já cancelou × nunca cancelou | a decidir |
| `children` | Até 1 criança × 2 ou mais (notebook 02, seção 3.5): corte da árvore, conferido em 2015 e 2016 (até 1: 24,6% e 27,1%; 2 ou mais: 27,3% e 40,9%). Os três níveis (0, 1 e 2 ou mais) não valem nos dois anos: 1 criança cancela menos que nenhuma em 2015 e mais em 2016. "Com criança × sem" fica 35,7 pontos de BIC atrás | `com_crianca` (notebook 03): com × sem, somando crianças e bebês | diferente |
| `babies` | Entra como "com bebê" (sim ou não), ao lado de "sozinho" e "2 ou mais crianças" (notebook 02, seção 3.7). Sozinho, o bebê não separa o cancelamento (a árvore não faz corte); com adultos e crianças no modelo, melhora o BIC em 9,0 pontos, e a ordem se mantém em 2015 e 2016 (19,4% e 21,4% com bebê, contra 24,7% e 27,6% sem). Não é somado às crianças: vai no sentido oposto | Sai: quase sempre zero. A derivada `com_crianca` (notebook 03) soma crianças e bebês | diferente |
| `lead_time` | Faixas pela árvore de decisão (ganho de informação), conferidas em 2015 e 2016: 0, 1–8, 9–25 e mais de 25 dias. Os cortes em 257 e 315 dias invertem a ordem entre os anos (acima de 315 dias: 82,6% em 2015, 18,8% em 2016) e saem. A proposta do `TODO.md` fica 62,0 pontos de BIC atrás | `TODO.md` e dicionário: até 7, 8–30, 31–90, 91–180 e mais de 180 dias | diferente |
| `noites` | Faixas pela árvore de decisão: 1, 2–3 e 4 ou mais (as zero noites saem da base). Separar 4–7 de mais de 7 não se sustenta pelo BIC | Dicionário: até 1 (zero noites junto), 2–3, 4–7 e mais de 7. Notebook 03: zero noites numa faixa própria | quase igual ao dicionário |
| `meal` | Testar com quatro níveis: BB (referência), com pensão (HB e FB), SC e Undefined | Testar: sem refeição (SC e Undefined) × com refeição | diferente |
| `arrival_date_month` | Duas temporadas: jul–ago × resto do ano. Só jul–ago fica acima nos dois anos (35,2% e 30,9%); em 2016, abr–jun (26,1%) e set–mar (27,1%) não se separam | Três temporadas: jul–ago, abr–jun e set–mar | diferente |
| `customer_type` | A decidir no notebook 02, seção 4. Group (344 reservas, 12,8%) não se parece com nenhum nível. Possibilidades: juntar com Contract (taxa mais próxima, 22,5%), juntar com Transient-Party (conceito mais próximo, 24,2%), deixar separado ou tirar a variável (V de 0,049; repete parte do segmento) | Entra | a decidir |
| `company` | Testar "paga por empresa": nos grupos, 4,7% de cancelamento com empresa (614 reservas), contra 34,1% sem | Sai: quase toda vazia | diferente |
| `adr` | Candidata em 6 faixas da árvore de decisão, conferidas em 2015 e 2016: até 59, 60–64, 65–67, 68–114, 115 e mais de 115 € (diária arredondada para o euro). Os cortes em 61 e 63 € invertem a ordem entre os anos e saem. As faixas estreitas seguem tarifas de grupos, operadoras e empresas (por exemplo, 62 € em blocos de grupos). O preço sobe em 2017 (mediana do urbano de 96,2 para 114,4): faixas em euros envelhecem. O notebook 02, seção 4, decide se entra | Entra como número (858,0 pontos de BIC atrás das 6 faixas) | diferente |
| `agent` | Sai: 275 códigos anônimos, embora separem reservas do mesmo segmento (agência online: de 13,9% a 38,7%) | Sai por ora | igual |

## Leituras

| Ponto | Ana | Notebooks do grupo | Situação |
| --- | --- | --- | --- |
| Alta de 2017 | Sai do notebook 02: a decomposição usava o cancelamento do teste. Fica para o `03_modelo`, depois da avaliação | Notebook 03: "a alta é sobretudo comportamento, concentrada na agência online com antecedência longa", analisada antes do modelo | diferente: o grupo usa o teste antes do modelo |

## Para fechar com o grupo

1. **`children` vazio:** remover ou preencher com 0? São só 4 reservas: a escolha não muda o modelo, mas o `04_preparacao` precisa de uma regra só.
2. **Sem hóspede, diária negativa e zero noites:** aplicar a remoção no `04_preparacao`. Nas duas primeiras, as propostas apontam para o mesmo lado; a remoção das zero noites é nova (o dicionário junta com 1 noite, e o notebook 03 deixa numa faixa própria).
3. **Faixas de antecedência e de noites:** adotar os cortes da árvore de decisão (notebook 02, seções 3.1 e 3.2) no lugar dos do `TODO.md` e do dicionário.
4. **`meal`:** quatro níveis (Undefined separado) ou sem refeição × com refeição. Com a junção, efeitos opostos dos dois hotéis se misturam.
5. **`previous_cancellations`:** tirar do modelo ou manter? A decisão é refeita no notebook 02, seção 3.9, sem o teste.
6. **Criança e bebê:** três variáveis sim ou não (sozinho, 2 ou mais crianças, com bebê) ou `com_crianca` somando crianças e bebês. Uma variável única de composição fica 3,9 pontos de BIC atrás das três separadas.
7. **Temporadas:** duas (jul–ago × resto) ou três.
8. **`company`:** testar "paga por empresa" ou deixar fora.
9. **`customer_type`:** entra ou sai (notebook 02, seção 4); se entrar, o destino do nível Group.
10. **Uso do teste:** nenhuma escolha de cortes ou de variáveis usa o teste (2017); a estabilidade é conferida entre 2015 e 2016, dentro do treino. Os notebooks do grupo usam o teste antes do modelo (notebook 03, decomposição da alta de 2017).
