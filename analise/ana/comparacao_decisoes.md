# Comparação de decisões: notebooks da Ana × grupo

Os notebooks da Ana (`analise/ana/01` a `05`) são uma proposta completa, do escopo ao modelo. Os notebooks do grupo (`analise/01` a `03`, sem o modelo), o `CLAUDE.md`, o `TODO.md` e o dicionário de dados (`dados/dicionario_hotel_bookings.md`) são a outra. Este arquivo lista cada ponto em que as duas propostas se encontram ou se separam, para o grupo escolher o modelo final. Os números saem das saídas dos notebooks citados.

**Situação:**
- *igual*: o mesmo tratamento;
- *igual no resultado*: a mesma decisão, por motivos diferentes;
- *diferente*: tratamentos diferentes;
- *só no grupo* ou *só na Ana*: só uma das propostas trata o ponto;
- *a decidir*: nenhuma das propostas fecha o ponto.

## Método e organização

| Ponto | Ana | Grupo | Situação |
| --- | --- | --- | --- |
| Notebooks | 01 exploratória, 02 variáveis uma a uma, 03 multicolinearidade, 04 qualidade do teste, 05 modelo e avaliação | 01 avaliação das variáveis, 02 exploração, 03 relações entre as variáveis. O `TODO.md` prevê 04 preparação, 05 modelo e 06 avaliação | diferente (só organização) |
| Divisão treino e teste | Treino com as chegadas de 2015 e 2016, teste com as de 2017 | A mesma (`CLAUDE.md`, regra 3) | igual |
| Uso do teste (2017) | Nenhuma escolha usa o teste. A estabilidade é conferida entre 2015 e 2016, dentro do treino. Antes do modelo, só a taxa de 2017 aparece (01, seção 5: 31,8%, contra 26,2% em 2016 nos mesmos meses). O 04 olha só as variáveis de 2017, sem o cancelamento. A régua e a decomposição da alta vêm depois do modelo fechado (05, seções 8 e 9) | Antes do modelo, aparecem a taxa de 2017 e a régua das regras simples, medida em 2017 (02, seções 6 e 7), e a decomposição da alta (03, seção 7). Nenhuma escolha de variável parece depender disso | diferente: as duas mostram a taxa de 2017, mas só o grupo mede a régua e decompõe a alta antes do modelo |
| Estabilidade no tempo | Cada corte, cada agrupamento e cada sinal do modelo precisam valer em 2015 e em 2016 | Não há essa conferência | diferente |
| Forma das variáveis | Todas categóricas. Os cortes saem de uma árvore de decisão (ganho de informação), conferida em 2015 e em 2016, e são comparados pelo BIC | Faixas de negócio (semana, mês, trimestre) e agrupamentos pela taxa. A diária entra como número | diferente |
| Critério de comparação | BIC; se a diferença for de até 2 pontos, decide o AIC | AIC (`TODO.md` e 03, seção 4) | diferente |
| Seleção das variáveis | Triagem nos notebooks 01 a 03. No 05, stepwise pelo BIC, repetido até nenhum sinal inverter entre 2015 e 2016. Saem também as variáveis cujo efeito no modelo tem o sentido contrário ao da comparação direta | Rodar o modelo com e sem cada variável em teste, pelo AIC (`TODO.md`) | diferente |
| Multicolinearidade | VIF generalizado (GVIF), uma linha por variável, com limite de 2,5. Só o canal passa do limite junto com tem agência e sai (03) | VIF por dummy, com a categoria mais frequente como referência: todos abaixo de 2,1 (03, seção 8). O canal já tinha saído por repetir o segmento (01, seção 10) | igual no resultado: nenhum problema forte, e o canal sai nos dois |
| Referência das categóricas | O nível maior | A categoria mais frequente (`CLAUDE.md`, regra 5) | igual |
| Dicionário de dados | Versões dentro dos notebooks: 01 (seções 2 e 6), 02 (seção 4) e a final no 05 (seção 12) | `dados/dicionario_hotel_bookings.md` (`CLAUDE.md`, regra 7) | diferente: o dicionário do grupo não tem as decisões da Ana |

## Escopo e limpeza

| Ponto | Reservas | Ana | Grupo | Situação |
| --- | --- | --- | --- | --- |
| Escopo | 104.641 | Só reservas sem depósito; Non Refund e Refundable ficam fora (01, seção 5.2) | A mesma proposta | igual |
| Linhas idênticas | 31.994 cópias | Manter; rodar o modelo sem elas para conferir (05, seção 11) | A mesma proposta | igual |
| `children` vazio | 4 | Remover: cadastros incompletos (as 4 têm `distribution_channel = Undefined`) | Preencher com 0 | diferente |
| Sem hóspede | 180 | Remover | `TODO.md` e 01, seção 12: tirar. Ainda não aplicado no código | igual na proposta |
| Diária negativa (−6,38) | 1 | Remover | Não removida | diferente |
| Zero noites | 715 | Remover: o zero pode ter sido gravado na chegada (vazamento) ou ser outro produto, sem pernoite (01, seção 4.4) | Juntar com 1 noite (dicionário e 03, seção 8). O 03 mostra as zero noites numa faixa própria (4,9% de cancelamento), mas propõe juntar | diferente |
| `meal = Undefined` | 1.169 | Fica separado, mas não importa: `meal` sai (02, seção 3.14) | Juntar com SC | diferente, sem efeito no modelo da Ana |
| `agent` e `company` vazios | 16.340 e 112.593 | Vazio quer dizer "sem agência" e "não é paga por empresa" | As duas colunas saem | diferente em `company` (ver Variáveis) |
| Tamanho do treino e do teste | | Depois da limpeza: treino com 67.455 reservas (26,8% de cancelamento), teste com 36.356 (31,9%) (02, seção 1; 05, seção 9) | Sem limpeza: treino com 68.107 (26,6%), teste com 36.534 (31,8%) (02, seção 6) | diferente: os números das duas propostas não batem exatamente |

## Variáveis

| Variável | Ana | Grupo | Situação |
| --- | --- | --- | --- |
| Colunas vazadas (`reservation_status`, `reservation_status_date`, `assigned_room_type`, `booking_changes`, `required_car_parking_spaces`) | Saem | Saem | igual |
| `country` | Sai: provável preenchimento no check-in | Sai, pelo mesmo motivo | igual |
| `arrival_date_week_number` e `arrival_date_day_of_month` | Saem: o mês representa a época do ano | Saem: a semana repete o mês, e o dia do mês é plano | igual |
| `hotel` | **Entra** (razão de chances do resort: 0,83) | Entra | igual |
| `lead_time` | Faixas pela árvore, conferidas em 2015 e 2016: 0, 1–8, 9–25 e mais de 25 dias. A proposta do grupo fica 62,0 pontos de BIC atrás (02, seção 3.1) | Até 7, 8–30, 31–90, 91–180 e mais de 180 dias (dicionário e `TODO.md`) | diferente |
| Noites | Faixas 1, 2–3 e 4 ou mais (02, seção 3.2); **sai** no 05: não reduz o BIC no stepwise final | Até 1 (com as zero noites), 2–3, 4–7 e mais de 7; em teste | diferente: sai na Ana, em teste no grupo |
| `adr` | Faixas até 59 € × mais de 59 €; como número, fica 155,6 pontos de BIC atrás (02, seção 3.3). **Sai** no 05: inverte o sinal entre 2015 e 2016 (+0,27 e −0,27) | Entra como número | diferente |
| `adults` | "Sozinho" (1 adulto) × outros; **entra** | Sozinho × acompanhado; em teste | igual na forma |
| `children` | 2 ou mais crianças × nenhuma ou 1; **entra**. "Com criança" (1 ou mais) inverte entre os anos (02, seção 3.5) | `com_crianca` (com × sem), somando crianças e bebês; em teste | diferente |
| `babies` | "Com bebê" como candidata; **o stepwise deixa de fora**: 84,7% das reservas com bebê fizeram pedido especial, e com o pedido no modelo o bebê não acrescenta | Sai sozinha (quase sempre zero), mas entra somada em `com_crianca` | diferente na forma; nenhuma das duas usa o bebê sozinho |
| Pedido especial | Fez pedido × nenhum; **entra**, com o score calculado alguns dias depois da reserva. Sem ele, o BIC do modelo final piora 4.367,7 pontos (05, seção 6) | Em teste. O 03 (seção 5) não encontra sinal de que os pedidos se acumulem até a chegada, mas encontra sinal nos dois primeiros dias; se entrar, o score é calculado alguns dias depois | igual na proposta; a decidir (ver Para fechar, item 3) |
| `previous_cancellations` | Sai, por suspeita de vazamento: nos blocos, 100% das reservas com cancelamento anterior cancelaram, em 2015 (1.361) e em 2016 (210) (02, seção 3.9) | Já cancelou × nunca cancelou; em teste, com desconfiança se a AUC subir muito por causa dela (01, seção 12) | diferente |
| `previous_bookings_not_canceled` | "Já veio" × nunca veio; **entra** | "Já veio" × nunca veio; entra | igual |
| `is_repeated_guest` | Sai: inverte entre os anos (02, seção 3.18) | Sai: repete "já veio" (V de Cramér de 0,76) | igual no resultado |
| `days_in_waiting_list` | Sai: a árvore não faz corte, e o efeito inverte entre os anos (02, seção 3.9) | Sai: fraca no escopo (V de 0,02) | igual no resultado |
| `meal` | Sai: nenhum agrupamento vale nos dois anos (02, seção 3.14) | Sem refeição (SC e Undefined) × com refeição; em teste | diferente |
| `customer_type` | Sai: o único corte inverte entre 2015 e 2016 (02, seção 3.13) | Entra, como está ou avulso × outros | diferente |
| `reserved_room_type` | Sai: o único corte inverte entre os anos (02, seção 3.15) | Sai: fraca e com código anônimo | igual no resultado |
| `market_segment` | **Entra em 3 níveis:** agência online, grupos e demais (05, seção 4). Olhando só o segmento, grupos e agência online trocam de lugar entre os anos (02, seção 3.11); com as outras variáveis no modelo, os sinais se mantêm, e o BIC melhora 960,5 pontos | Todos os segmentos, com cortesia, aviação e Undefined em "Outros" | diferente |
| `distribution_channel` | Sai no 03 por repetir tem agência (V de Cramér de 0,71). Volta como candidata no 05 e sai pela regra do sentido: no modelo, "demais" cancelaria mais, mas na comparação direta cancela 15,4% contra 29,6% (05, seção 5) | Sai: repete o segmento (V de 0,70) | igual no resultado |
| `agent` | Os códigos saem. "Tem agência" **sai** no 05 pela regra do sentido: no modelo, sem agência cancelaria mais, mas na comparação direta cancela 14,5% contra 28,8%, e também menos em 5 das 6 combinações de segmento e ano e em 7 das 8 de antecedência e ano. Custo: 45,9 pontos de BIC (05, seção 5) | Sai, por ora: códigos sem significado de negócio | igual no resultado |
| `company` | "Paga por empresa" × não; **entra** (11,4% contra 27,8%, com a ordem mantida nos dois anos) | Sai: quase toda vazia | diferente |
| `arrival_date_month` | Três temporadas pela árvore: baixa (janeiro, março e novembro), média e alta (julho e agosto); as do grupo ficam 75,0 pontos de BIC atrás (02, seção 3.16). **Sai** no 05: a temporada alta inverte o sinal entre 2015 e 2016 com o segmento em 3 níveis e a interação no modelo (+0,68 e −0,04) | Três temporadas fixas: jul–ago, abr–jun e set–mar; entra | diferente |
| Variáveis derivadas (dia da semana da chegada e da reserva, só fim de semana, preço relativo) | Não avaliadas | Avaliadas e fora: fracas ou difíceis de explicar (03, seção 2) | só no grupo |
| Interação agência online × antecedência | **Entra** como "agência online com até 8 dias" (razão de chances de 0,28; 05, seção 4). A versão com as três faixas curtas fica 17,8 pontos de BIC atrás | Testar (03, seção 4, e `TODO.md`) | igual na ideia |
| Interação hotel × pedido especial | Próximo passo: melhora o ajuste no treino, mas foi encontrada depois da avaliação em 2017 (05, seções 6 e 13) | Não avaliada | só na Ana |

## Avaliação (05, seções 7 a 10)

| Ponto | Ana | Grupo | Situação |
| --- | --- | --- | --- |
| Régua do modelo | A regra "agência online com mais de 30 dias" do grupo, também ordenada pela antecedência, e a de mais de 90 dias. Em 2017, o modelo encontra mais cancelamentos que a regra de 30 dias com 10% a 30% das ligações (38,6% contra 33,1% com 20%) e empata a partir de 40% (65,6% contra 66,2% nos 44,3% que a regra marca). No treino, ganha em todos os pontos | A regra encontra 66% dos cancelamentos contatando 44% das reservas de 2017 (02, seção 7) | igual: mesma régua |
| AUC | 0,738 no treino e 0,727 em 2017 | A medir (`TODO.md`) | só na Ana |
| Calibração em 2017 | Prevê 29,2% contra 31,9% reais. A diferença se concentra na agência online (+4,4 pontos) e em quem fez pedido especial (+6,0) | A conferir, com atenção à alta de 2017 (`TODO.md`) | igual na preocupação |
| Sensibilidade sem as linhas idênticas | Todas as razões de chances mantêm o lado do 1; grupos, paga por empresa e sozinho mudam de tamanho (05, seção 11) | A fazer (`TODO.md`) | só na Ana |
| Alta de 2017 | Depois do modelo fechado: dos 5,5 pontos, 1,3 são explicados pelas variáveis do modelo e 4,2 não (05, seção 9) | Antes do modelo, só com o segmento: dos 5,6 pontos, 1,4 vêm da mistura de segmentos (03, seção 7) | igual na conclusão: a maior parte da alta não vem do perfil das reservas. Diferente no momento (ver Uso do teste) |
| Ponto de corte | Sem custo: ligar para as reservas com probabilidade acima de 30,2%. É o primeiro grupo da fila com taxa abaixo da média do treino, e são as 23,1% mais arriscadas do treino. Em 2017, 25,8% das reservas e 44,6% dos cancelamentos (05, seção 10). A premissa de custo fica como próximo passo | Depende da premissa de custo (`TODO.md`) | diferente |
| Ação recomendada | Ligar para confirmar as reservas acima do corte. O overbooking fica para depois de ajustar as probabilidades ao ano e ao mês (05, seção 13) | Lista de ligação, com depósito para a faixa de maior risco; overbooking como próximo passo (`TODO.md`) | quase igual: o depósito só aparece no grupo |

## Para fechar com o grupo

1. **Uso do teste:** antes do modelo, só a taxa de 2017 (Ana), ou também a régua e a decomposição da alta (grupo). Em nenhuma das duas o teste decide uma variável.
2. **Forma e seleção:** cortes pela árvore conferidos por ano e stepwise pelo BIC com as regras dos sinais e do sentido (Ana), ou faixas de negócio e testes com e sem pelo AIC (grupo).
3. **Momento do score:** as duas propostas aceitam calcular o score alguns dias depois da reserva, com o pedido especial no modelo. Falta o grupo confirmar.
4. **Segmento e interação:** segmento em 3 níveis e "agência online com até 8 dias" (Ana), ou todos os segmentos com a interação a testar (grupo).
5. **Faixas e agrupamentos:** antecedência, crianças e temporadas pela árvore (Ana), ou pelas propostas do dicionário (grupo).
6. **Variáveis que saem na Ana e entram ou ficam em teste no grupo:** temporada e diária (invertem o sinal no modelo), noites (não reduzem o BIC), `customer_type` e `meal` (instáveis entre os anos) e `previous_cancellations` (suspeita de vazamento).
7. **`company`:** "paga por empresa" entra no modelo da Ana e sai no grupo.
8. **Limpeza:** `children` vazio, diária negativa e zero noites.
9. **Ponto de corte e ação:** sem premissa de custo, ligar para as reservas com mais de 30,2% de chance de cancelar (1 em cada 4 reservas), ou definir a premissa de custo. Decidir também se o depósito entra na recomendação.
