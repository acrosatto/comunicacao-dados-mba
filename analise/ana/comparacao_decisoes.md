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
| `previous_cancellations` | Sai, por suspeita de vazamento (notebook 02, seção 3.9). Nos blocos (com linha idêntica), 100% das reservas com cancelamento anterior cancelaram, em 2015 (1.361) e em 2016 (210): a contagem parece gravada junto com o cancelamento do próprio bloco. Fora dos blocos, 92,1% em 2015 e 38,1% em 2016. Pelo método, seria a variável mais forte (ganho de 0,0474) | Testar: já cancelou × nunca cancelou | diferente |
| `children` | Até 1 criança × 2 ou mais (notebook 02, seção 3.5): corte da árvore, conferido em 2015 e 2016 (até 1: 24,6% e 27,1%; 2 ou mais: 27,3% e 40,9%). Os três níveis (0, 1 e 2 ou mais) não valem nos dois anos: 1 criança cancela menos que nenhuma em 2015 e mais em 2016. "Com criança × sem" fica 35,7 pontos de BIC atrás | `com_crianca` (notebook 03): com × sem, somando crianças e bebês | diferente |
| `babies` | Entra como "com bebê" (sim ou não), ao lado de "sozinho" e "2 ou mais crianças" (notebook 02, seção 3.7). Sozinho, o bebê não separa o cancelamento (a árvore não faz corte); com adultos e crianças no modelo, melhora o BIC em 9,0 pontos, e a ordem se mantém em 2015 e 2016 (19,4% e 21,4% com bebê, contra 24,7% e 27,6% sem). Não é somado às crianças: vai no sentido oposto | Sai: quase sempre zero. A derivada `com_crianca` (notebook 03) soma crianças e bebês | diferente |
| `lead_time` | Faixas pela árvore de decisão (ganho de informação), conferidas em 2015 e 2016: 0, 1–8, 9–25 e mais de 25 dias. Os cortes em 257 e 315 dias invertem a ordem entre os anos (acima de 315 dias: 82,6% em 2015, 18,8% em 2016) e saem. A proposta do `TODO.md` fica 62,0 pontos de BIC atrás | `TODO.md` e dicionário: até 7, 8–30, 31–90, 91–180 e mais de 180 dias | diferente |
| `noites` | Faixas pela árvore de decisão: 1, 2–3 e 4 ou mais (as zero noites saem da base). Separar 4–7 de mais de 7 não se sustenta pelo BIC | Dicionário: até 1 (zero noites junto), 2–3, 4–7 e mais de 7. Notebook 03: zero noites numa faixa própria | quase igual ao dicionário |
| `meal` | Sai (notebook 02, seção 3.14): nenhum agrupamento vale nos dois anos do treino. SC cancela 8,6% em 2015 e 37,6% em 2016 | Testar: sem refeição (SC e Undefined) × com refeição | diferente |
| `arrival_date_month` | Três temporadas pela árvore (notebook 02, seção 3.16): baixa (jan, mar, nov), média (fev, abr–jun, set, out, dez) e alta (jul–ago), com a ordem mantida em 2015 e 2016. As três temporadas fixas do grupo ficam 75,0 pontos de BIC atrás, e abril a junho não existe em 2015 | Três temporadas: jul–ago, abr–jun e set–mar | diferente |
| `customer_type` | Sai (notebook 02, seção 3.13): o único corte da árvore (avulso × avulso ligado a outra reserva) inverte entre 2015 e 2016 | Entra | diferente |
| `company` | Entra como "paga por empresa" × não (notebook 02, seção 3.17): 11,4% contra 27,8%, ordem mantida em 2015 e 2016. O código sai | Sai: quase toda vazia | diferente |
| `adr` | Candidata como até 59 € × mais de 59 € (notebook 02, seção 3.3; diária arredondada para o euro). Da árvore saem os cortes que criam faixas de menos de 10 € (tarifas de grupos, operadoras e empresas, como 62 € em blocos de grupos) e o de 115 €, que inverte entre 2015 e 2016. O preço sobe em 2017: faixas em euros envelhecem. O notebook 02, seção 4, decide se entra | Entra como número (155,6 pontos de BIC atrás das 2 faixas) | diferente |
| `agent` | Sai: 275 códigos anônimos, embora separem reservas do mesmo segmento (agência online: de 13,9% a 38,7%) | Sai por ora | igual |
| `market_segment` | Dois grupos pela árvore (notebook 02, seção 3.11): agência online e grupos × demais. Todos os segmentos separados não valem nos dois anos: grupos cancelam mais que a agência online em 2015 (37,8% × 26,8%) e menos em 2016 (25,9% × 35,7%) | Todos os segmentos, com cortesia, aviação e Undefined em "Outros" | diferente |

## Leituras

| Ponto | Ana | Notebooks do grupo | Situação |
| --- | --- | --- | --- |
| Alta de 2017 | Sai do notebook 02: a decomposição usava o cancelamento do teste. Fica para o `03_modelo`, depois da avaliação | Notebook 03: "a alta é sobretudo comportamento, concentrada na agência online com antecedência longa", analisada antes do modelo | diferente: o grupo usa o teste antes do modelo |

## Para fechar com o grupo

1. **`children` vazio:** remover ou preencher com 0? São só 4 reservas: a escolha não muda o modelo, mas o `04_preparacao` precisa de uma regra só.
2. **Sem hóspede, diária negativa e zero noites:** aplicar a remoção no `04_preparacao`. Nas duas primeiras, as propostas apontam para o mesmo lado; a remoção das zero noites é nova (o dicionário junta com 1 noite, e o notebook 03 deixa numa faixa própria).
3. **Faixas de antecedência e de noites:** adotar os cortes da árvore de decisão (notebook 02, seções 3.1 e 3.2) no lugar dos do `TODO.md` e do dicionário.
4. **`meal`:** sai no notebook 02 (nenhum agrupamento vale em 2015 e 2016) ou entra como sem refeição × com refeição?
5. **`previous_cancellations`:** sair por suspeita de vazamento (notebook 02, seção 3.9) ou manter em teste? A evidência vem só do treino: 100% de cancelamento nos blocos com cancelamento anterior, nos dois anos.
6. **Criança e bebê:** três variáveis sim ou não (sozinho, 2 ou mais crianças, com bebê) ou `com_crianca` somando crianças e bebês. Uma variável única de composição fica 3,9 pontos de BIC atrás das três separadas.
7. **Temporadas:** três pela árvore (baixa, média, alta) ou as três fixas do grupo (jul–ago, abr–jun, set–mar).
8. **`company`:** testar "paga por empresa" ou deixar fora.
9. **`customer_type`:** sai no notebook 02 (o único corte inverte entre 2015 e 2016) ou entra?
10. **Uso do teste:** nenhuma escolha de cortes ou de variáveis usa o teste (2017); a estabilidade é conferida entre 2015 e 2016, dentro do treino. Os notebooks do grupo usam o teste antes do modelo (notebook 03, decomposição da alta de 2017).
