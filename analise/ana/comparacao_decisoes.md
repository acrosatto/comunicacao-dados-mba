# Comparação de decisões: notebooks da Ana × grupo

Pontos em que os notebooks da Ana (`analise/ana/01` a `05`) chegam a uma decisão diferente dos notebooks do grupo (`analise/01` a `03`), do `CLAUDE.md` ou do `TODO.md`, ou em que a decisão ainda está em aberto. Serve para o grupo fechar cada ponto. Os números saem das saídas dos notebooks citados.

**Situação:** *igual* (mesmo tratamento), *diferente* (tratamentos diferentes) ou *a decidir* (sem decisão do grupo).

## Método e organização

| Ponto | Ana | Grupo (`CLAUDE.md`, `TODO.md` ou notebooks) | Situação |
| --- | --- | --- | --- |
| Notebooks | 01 exploratória, 02 variáveis uma a uma, 03 multicolinearidade, 04 qualidade do teste, 05 modelo e avaliação | `TODO.md`: 04 preparação, 05 modelo, 06 avaliação | diferente (só organização) |
| Uso do teste (2017) | Nenhuma escolha usa o teste; a estabilidade é conferida entre 2015 e 2016, dentro do treino. O 04 olha só as variáveis de 2017, sem o cancelamento | Notebook 03 do grupo: decomposição da alta de 2017 antes do modelo, com o cancelamento do teste | diferente: o grupo usa o teste antes do modelo |
| Estabilidade no tempo | Cada corte e cada sinal do modelo precisam valer em 2015 e em 2016 | Não há essa conferência | diferente |
| Critério de comparação | BIC; se a diferença for de até 2 pontos, decide o AIC | `TODO.md`: comparar pelo AIC | diferente |
| Seleção das variáveis | Triagem nos notebooks 01 a 03; no 05, stepwise pelo BIC, repetido até nenhum sinal inverter entre 2015 e 2016 | `TODO.md`: testar com e sem cada variável em teste, pelo AIC | diferente |
| Multicolinearidade | VIF generalizado (GVIF), limite de 2,5: só o canal sai (03) | Notebook 03: VIF com a categoria mais frequente como referência, todos abaixo de 2,1 | igual na conclusão (nenhum problema forte); o canal só sai na Ana |
| Dicionário de dados | Versões dentro dos notebooks: 01 (seções 2 e 6), 02 (seção 4) e a final no 05 | `CLAUDE.md`, regra 7: atualizar `dados/dicionario_hotel_bookings.md` | diferente: o dicionário do grupo não foi alterado |

## Escopo e limpeza

| Ponto | Reservas | Ana | Grupo | Situação |
| --- | --- | --- | --- | --- |
| Escopo | 104.641 | Só reservas sem depósito (01, seção 5.2) | Mesma proposta | igual |
| Linhas idênticas | 31.994 cópias | Manter; rodar o modelo sem elas para conferir | Mesma proposta | igual |
| `children` vazio | 4 | Remover: cadastros incompletos (as 4 têm `distribution_channel = Undefined`) | Preencher com 0 | diferente |
| Sem hóspede | 180 | Remover | `TODO.md`: tirar; ainda não aplicado no código | igual na proposta |
| Diária negativa (−6,38) | 1 | Remover | Não removida | diferente |
| Zero noites | 715 | Remover: o zero pode ter sido gravado na chegada (vazamento) ou ser outro produto, sem pernoite (01, seção 4.4) | Dicionário: juntar com 1 noite. Notebook 03: faixa própria | diferente |
| `meal = Undefined` | 1.169 | Fica separado, mas não importa: `meal` sai (02, seção 3.14) | Juntar com SC | diferente, sem efeito no modelo da Ana |
| `agent` / `company` vazios | 16.340 / 112.593 | Vazio quer dizer "sem agência" e "não é paga por empresa" | As duas colunas saem | diferente em `company` (ver Variáveis) |

## Variáveis

| Variável | Ana | Grupo | Situação |
| --- | --- | --- | --- |
| `lead_time` | Faixas pela árvore, conferidas em 2015 e 2016: 0, 1–8, 9–25 e mais de 25 dias. A proposta do grupo fica 62,0 pontos de BIC atrás (02, seção 3.1) | `TODO.md` e dicionário: até 7, 8–30, 31–90, 91–180 e mais de 180 | diferente |
| Noites | 1, 2–3 e 4 ou mais (02, seção 3.2); **sai** no 05: não reduz o BIC no stepwise final | Dicionário: até 1 (com as zero noites), 2–3, 4–7 e mais de 7 | quase igual |
| `adr` | Faixas até 59 € × mais de 59 € (02, seção 3.3); **sai** no 05: inverte o sinal entre 2015 e 2016 (+0,27 e −0,27) | Entra como número | diferente |
| `adults` | "Sozinho" (1 adulto) × outros; **entra no modelo** | `TODO.md`: sozinho × acompanhado, em teste | igual na forma |
| `children` | 2 ou mais crianças × nenhuma ou 1; **entra no modelo**. "Com criança" (1 ou mais) inverte entre os anos (02, seção 3.5) | `com_crianca` (com × sem), somando crianças e bebês | diferente |
| `babies` | "Com bebê" como candidata; **o stepwise deixa de fora**: 84,7% das reservas com bebê fizeram pedido especial, e com o pedido no modelo o bebê não acrescenta | Sai | igual no resultado |
| Pedido especial | Fez pedido × nenhum; **entra**: o score é calculado alguns dias depois da reserva. Sem ele, o BIC do modelo final piora 4.367,7 pontos (05, seção 6) | Notebook 03: em teste; se entrar, o score é calculado alguns dias depois | igual na proposta; a decidir pelo grupo |
| `previous_cancellations` | Sai, por suspeita de vazamento: nos blocos, 100% das reservas com cancelamento anterior cancelaram, em 2015 (1.361) e em 2016 (210) (02, seção 3.9) | `TODO.md`: já cancelou × nunca cancelou, em teste | diferente |
| `previous_bookings_not_canceled` | "Já veio" × nunca veio; **entra no modelo** | — | só na Ana |
| `is_repeated_guest` | Sai: inverte entre os anos (02, seção 3.18) | — | só na Ana |
| `days_in_waiting_list` | Sai: a árvore não faz corte, e o efeito inverte entre os anos (02, seção 3.9) | — | só na Ana |
| `meal` | Sai: nenhum agrupamento vale nos dois anos (02, seção 3.14) | `TODO.md`: em teste, sem refeição × com refeição | diferente |
| `customer_type` | Sai: o único corte inverte entre 2015 e 2016 (02, seção 3.13) | Entra | diferente |
| `reserved_room_type` | Sai: o único corte inverte entre os anos (02, seção 3.15) | — | só na Ana |
| `market_segment` | **Entra em 3 níveis:** agência online, grupos e demais (05, seção 4). Olhando só o segmento, grupos e agência online trocam de lugar entre os anos (02, seção 3.11); com as outras variáveis no modelo, os sinais se mantêm, e o BIC melhora 960,5 pontos | Todos os segmentos, com os pequenos em "Outros" | diferente |
| `distribution_channel` | Sai por multicolinearidade: repete tem agência (V de Cramér de 0,71; 03, seção 3) | Sai: repete o segmento | igual no resultado |
| `agent` | Os códigos saem; "tem agência" **sai** no 05: o sinal no modelo contradiz as comparações diretas, dentro de cada segmento e de cada faixa de antecedência | Sai | igual no resultado |
| `company` | "Paga por empresa" × não; **entra no modelo** (11,4% contra 27,8%) | Sai: quase toda vazia | diferente |
| `arrival_date_month` | **Sai** no 05: a temporada alta inverte o sinal entre 2015 e 2016 com o segmento em 3 níveis e a interação no modelo (+0,68 e −0,04) | Três temporadas fixas: jul–ago, abr–jun e set–mar | diferente |
| Interação agência online × antecedência | **Entra** como "agência online com até 8 dias" (razão de chances de 0,28; 05, seção 4). A versão com as três faixas curtas fica 17,8 pontos de BIC atrás | Notebook 03 e `TODO.md`: testar | igual na ideia |

## Avaliação (05, seção 8)

| Ponto | Ana | Grupo | Situação |
| --- | --- | --- | --- |
| Régua do modelo | Em 2017, o modelo encontra mais cancelamentos que a regra "agência online com mais de 30 dias" com 10% a 30% das ligações (38,6% contra 33,1% com 20%) e empata a partir de 40% (65,6% contra 66,2% nos 44,3% que a regra marca). No treino, ganha em todos os pontos | Notebook 02: a regra encontra 66% dos cancelamentos contatando 44% das reservas | mesma régua |
| AUC | 0,738 no treino e 0,727 em 2017 | `TODO.md`: a medir | — |
| Calibração em 2017 | Prevê 29,2% contra 31,9% reais; a diferença se concentra na agência online (+4,4 pontos) e em quem fez pedido especial (+6,0) | `TODO.md`: conferir, com atenção à alta de 2017 | igual na preocupação |
| Sensibilidade sem as linhas idênticas | Todas as razões de chances mantêm o lado do 1; grupos, paga por empresa e sozinho mudam de tamanho | `TODO.md`: a fazer | — |
| Alta de 2017 | Decomposta depois do modelo fechado: dos 5,5 pontos, 1,3 são composição e 4,2 comportamento (05, seção 9) | Notebook 03: decomposição antes do modelo, com o cancelamento do teste | diferente (ver Uso do teste) |
| Ponto de corte | Sem custo: ligar para as reservas com probabilidade acima de 30,2%, o primeiro bloco de ligações com taxa abaixo da média do treino. Em 2017, 25,8% das reservas e 44,6% dos cancelamentos (05, seção 10). A premissa de custo fica como próximo passo | `TODO.md`: o ponto de corte depende da premissa de custo | diferente |

## Para fechar com o grupo

1. **Uso do teste:** nenhuma escolha usa 2017 (Ana) ou a decomposição da alta vem antes do modelo (grupo).
2. **Seleção:** stepwise pelo BIC com a conferência dos sinais em 2015 e 2016 (Ana), ou testes com e sem pelo AIC (`TODO.md`).
3. **Momento do score:** a Ana propõe alguns dias depois da reserva, com o pedido especial no modelo; o grupo precisa confirmar.
4. **Segmento e interação:** segmento em 3 níveis e "agência online com até 8 dias" (Ana) ou todos os segmentos (grupo).
5. **Faixas e agrupamentos:** antecedência e crianças pela árvore conferida por ano (Ana) ou pelas propostas do dicionário.
6. **Variáveis que saem na Ana e ficam no grupo:** temporada e diária (invertem o sinal no modelo), `customer_type` e `meal` (instáveis entre os anos), `previous_cancellations` (suspeita de vazamento).
7. **`company`:** "paga por empresa" entra no modelo da Ana.
8. **Limpeza:** `children` vazio, diária negativa e zero noites.
9. **Ponto de corte:** sem premissa de custo, ligar para as reservas com mais de 30,2% de chance de cancelar (1 em cada 4 reservas), na faixa em que o modelo ganha da régua; ou definir a premissa de custo.
