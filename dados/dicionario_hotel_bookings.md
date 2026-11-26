# Dicionário de dados: Hotel Booking Demand

- **Arquivo:** `hotel_bookings.csv`, com 119.390 linhas e 32 colunas. Cada linha é uma reserva.
- **Hotéis:** dois hotéis em Portugal, o City Hotel (Lisboa) e o Resort Hotel (Algarve).
- **Período:** chegadas de julho de 2015 a agosto de 2017.
- **Fonte:** Antonio, Almeida e Nunes (2019), *Hotel booking demand datasets*, Data in Brief. Versão em CSV distribuída pelo TidyTuesday (11/02/2020) e pelo Kaggle.

As evidências de cada decisão estão no notebook [01_avaliacao_variaveis_hotel.ipynb](../analise/01_avaliacao_variaveis_hotel.ipynb).

## Como ler

- **Tipo:** o tipo da variável para a análise, que nem sempre é o tipo da coluna no arquivo. Por exemplo, `agent` vem como número, mas é um código.
- **Quando se sabe:** o modelo será usado no momento em que a reserva entra, então só pode usar o que o hotel sabe nessa hora.
  - *na reserva*: o hotel tem a informação quando a reserva entra;
  - *pode mudar até a chegada*: existe na reserva, mas a base guarda o valor final;
  - *só no fim*: só existe depois do check-in ou do cancelamento (vazamento);
  - *suspeita*: os dados indicam que a informação foi registrada depois.
- **Uso proposto:** *entra*, *testar* (rodar o modelo com e sem) ou *sai*. É uma proposta, a validar pelo grupo.

## Escopo proposto

O modelo usa só as reservas **sem depósito** (`deposit_type = No Deposit`): 104.641 reservas, com 28,4% de cancelamento. A ação em discussão (pedir depósito ou ligar para confirmar) só se aplica a quem ainda não deu garantia de pagamento. As reservas Non Refund cancelam 99,4% e se concentram em blocos de grupos e operadoras, o que distorceria o modelo.

## Variável resposta

| Variável | Descrição | Tipo | Valores |
| --- | --- | --- | --- |
| `is_canceled` | 1 = reserva cancelada (inclui no-show); 0 = o hóspede veio | binária | 37,0% de cancelamento na base toda; 28,4% entre as reservas sem depósito |

## Variáveis explicativas

| Variável | Descrição | Tipo | Valores | Quando se sabe | Uso proposto |
| --- | --- | --- | --- | --- | --- |
| `hotel` | Hotel da reserva | categórica | City Hotel (66%), Resort Hotel (34%) | na reserva | entra |
| `lead_time` | Dias entre a data da reserva e a chegada | numérica | 0 a 737; mediana de 69 | na reserva | entra, em faixas: até 7, 8–30, 31–90, 91–180 e mais de 180 dias |
| `arrival_date_year` | Ano da chegada | tempo | 2015, 2016, 2017 | na reserva | não entra: separa treino (2015 e 2016) e teste (2017) |
| `arrival_date_month` | Mês da chegada | categórica | January a December | na reserva | entra, em três temporadas: jul–ago, abr–jun e set–mar |
| `arrival_date_week_number` | Semana do ano da chegada | numérica | 1 a 53 | na reserva | sai: repete o mês |
| `arrival_date_day_of_month` | Dia do mês da chegada | numérica | 1 a 31 | na reserva | sai: sem relação com o cancelamento |
| `stays_in_weekend_nights` | Noites de sábado ou domingo | contagem | 0 a 19 | pode mudar até a chegada | testar, somada às noites de semana |
| `stays_in_week_nights` | Noites de segunda a sexta | contagem | 0 a 50 | pode mudar até a chegada | testar, somada às noites de fim de semana |
| `adults` | Adultos | contagem | 0 a 55 (403 reservas com 0) | na reserva | testar: sozinho × acompanhado |
| `children` | Crianças | contagem | 0 a 10 (4 vazios) | na reserva | testar: com × sem criança |
| `babies` | Bebês | contagem | 0 a 10 (99% zero) | na reserva | sai: quase sempre zero |
| `meal` | Regime de refeição | categórica | BB (café da manhã), HB (meia pensão), FB (pensão completa), SC (sem refeição), Undefined | na reserva | testar: sem refeição × com refeição |
| `country` | País de origem do hóspede, em código de três letras | categórica | 177 países; PRT em 41%; 488 vazios | suspeita | sai: o efeito de Portugal aparece só em grupos e operadoras |
| `market_segment` | Segmento de mercado | categórica | Online TA (agência online), Offline TA/TO (agência ou operadora tradicional), Groups, Direct, Corporate, Complementary (cortesia), Aviation, Undefined | na reserva | entra; Complementary, Aviation e Undefined juntas em "Outros" |
| `distribution_channel` | Canal de distribuição | categórica | TA/TO, Direct, Corporate, GDS, Undefined | na reserva | sai: repete o segmento |
| `is_repeated_guest` | Hóspede que já se hospedou antes | binária | 0, 1 (3% de 1) | na reserva | sai: repete `previous_bookings_not_canceled` |
| `previous_cancellations` | Reservas anteriores canceladas pelo cliente | contagem | 0 a 26 (95% zero) | na reserva, mas com contagem suspeita | testar: já cancelou × nunca cancelou |
| `previous_bookings_not_canceled` | Reservas anteriores que o cliente manteve | contagem | 0 a 72 (97% zero) | na reserva | entra: já veio × nunca veio |
| `reserved_room_type` | Tipo de quarto reservado, em código anônimo | categórica | A, B, C, D, E, F, G, H, L, P | na reserva | sai: fraca e sem significado de negócio |
| `assigned_room_type` | Tipo de quarto entregue | categórica | A, B, C, D, E, F, G, H, I, K, L, P | só no fim | sai: definido no check-in |
| `booking_changes` | Alterações feitas na reserva até o check-in ou o cancelamento | contagem | 0 a 21 | só no fim | sai: na hora da reserva, é sempre zero |
| `deposit_type` | Tipo de depósito | categórica | No Deposit (88%), Non Refund (12%), Refundable (0,1%) | na reserva | define o escopo: o modelo usa só No Deposit |
| `agent` | Código da agência que fez a reserva | código | 333 códigos; 14% vazio | na reserva | sai por ora: código sem significado de negócio |
| `company` | Código da empresa que paga a reserva | código | 352 códigos; 94% vazio | na reserva | sai: quase toda vazia |
| `days_in_waiting_list` | Dias em lista de espera até a confirmação | numérica | 0 a 391 (97% zero) | na reserva | sai: fraca entre as reservas sem depósito |
| `customer_type` | Tipo de cliente | categórica | Transient (avulso), Transient-Party (avulso ligado a outra reserva), Contract (contrato), Group | na reserva | entra |
| `adr` | Diária média: soma das diárias dividida pelo número de noites | numérica | −6,38 a 5.400; mediana de 94,58 | na reserva | entra como número |
| `required_car_parking_spaces` | Vagas de garagem pedidas | contagem | 0 a 8 | suspeita | sai: nenhuma das 7.416 reservas com vaga foi cancelada |
| `total_of_special_requests` | Pedidos especiais (cama de casal, andar alto etc.) | contagem | 0 a 5 | pode mudar até a chegada | testar: fez pedido × não fez |
| `reservation_status` | Último status da reserva | categórica | Check-Out, Canceled, No-Show | só no fim | sai: é a própria resposta |
| `reservation_status_date` | Data do último status | data | 17/10/2014 a 14/09/2017 | só no fim | sai: para quem cancelou, é a data do cancelamento |

**Resumo:** das 31 variáveis explicativas, 7 entram, 7 vão para teste (as duas de noites viram uma só), 6 saem por vazamento ou suspeita, 1 define o escopo e 10 saem por serem fracas, redundantes ou sem uso.

## Qualidade dos dados

- **Linhas duplicadas:** 31.994 linhas são cópia idêntica de outra (27% da base), concentradas em grupos e operadoras. A base não tem número de reserva, então não dá para saber se são quartos diferentes do mesmo grupo ou erro.
- **Reservas sem hóspede:** 180.
- **Reservas com zero noites:** 715.
- **Diárias fora do padrão:** uma negativa (−6,38) e uma de 5.400 (o percentil 99 é 252).
- **`meal`:** a documentação da base trata Undefined e SC como a mesma coisa, mas as duas categorias têm taxas de cancelamento diferentes.
- **Vazios:** `company` (94%), `agent` (14%), `country` (488 linhas) e `children` (4 linhas, tratadas como zero).
