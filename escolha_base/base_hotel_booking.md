# Opção 1 – Hotel Booking Demand (regressão logística) — RECOMENDADA

## Base
- Kaggle: https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand
  - O Kaggle exige login. O mesmo CSV está no repositório do TidyTuesday (rfordatascience, 11/02/2020).
- Fonte original (citar no anexo): Antonio, Almeida & Nunes (2019), *Hotel booking demand datasets*, Data in Brief.
- 119.390 reservas, 32 variáveis, dois hotéis em Portugal (Resort Hotel e City Hotel), chegadas entre 2015 e 2017.
- Variável alvo: `is_canceled` (cerca de 37% das reservas foram canceladas).

## Por que esta base
- **Decisão clara e com dinheiro envolvido:** cancelamentos geram quartos vazios e receita perdida.
- **Resultado fácil de comunicar:** "esta reserva tem 70% de chance de cancelar" funciona para o público não técnico; odds ratios, AUC e limiar interessam ao técnico.
- **Bom material para o anexo:** vazamento de dados, validação temporal e escolha do limiar mostram rigor.
- **Com só 4 slides:** a decisão cabe numa frase e a evidência leva direto à ação.

## Problema, público e decisão
- **Problema:** cerca de 37% das reservas são canceladas.
- **Público:** Diretor(a) de Receita (não técnico) e Analista de BI (técnico).
- **Decisão:** em quais reservas aplicar depósito, contato de confirmação ou overbooking?

## Roteiro dos slides

| Slide | Conteúdo |
|---|---|
| 1. Contexto e decisão | Cerca de 37% das reservas canceladas e o impacto em receita. Decisão em discussão: onde agir para reduzir o prejuízo. |
| 2. Como funciona | O modelo estima a probabilidade de cancelamento com informações disponíveis **no momento da reserva**. Exemplo: "reserva feita 200 dias antes, via agência online, sem pedidos especiais → __% de risco". |
| 3. Evidências | Título com a mensagem (por exemplo: "Reservas antecipadas via agências online concentram o risco de cancelamento"). Três resultados: (1) principais fatores (barras horizontais com odds ratios), (2) curva de ganho ("os 20% de maior risco concentram __% dos cancelamentos"), (3) risco por faixa de antecedência. Limitações. |
| 4. Recomendação | Score de risco no momento da reserva; para reservas de alto risco, depósito ou contato de confirmação. Próximo passo: piloto A/B de 3 meses em um dos hotéis, medindo cancelamentos e receita. |
| Anexo técnico | Tratamento dos dados, variáveis removidas por vazamento, divisão temporal, VIF, AUC, matriz de confusão, justificativa do limiar, tabela completa de coeficientes. |

Os `__%` são preenchidos depois que a análise rodar.

## Escolhas técnicas (para A, revisadas por B e C)
- **Modelo:** regressão logística binária.
  - Alvo: `is_canceled` (1 = cancelada, 0 = não cancelada).
  - Saída: probabilidade de cancelamento de cada reserva, sempre entre 0% e 100%.
  - Por que não linear: uma regressão linear sobre um alvo 0/1 pode prever valores abaixo de 0% ou acima de 100%; a logística mantém o resultado entre 0 e 1.
  - Como comunicar: nos slides, falar em **probabilidade** ("esta reserva tem 70% de chance de cancelar"; "com 1 pedido especial, o risco cai de __% para __%"). Os odds ratios (exponencial dos coeficientes) ficam no anexo.
- **Remover por vazamento:** `reservation_status` e `reservation_status_date` (revelam o resultado). Avaliar também `assigned_room_type` e `booking_changes`, que podem mudar depois da reserva.
- **Variáveis candidatas:** `lead_time`, `deposit_type`, `market_segment`, `distribution_channel`, `previous_cancellations`, `previous_bookings_not_canceled`, `total_of_special_requests`, `required_car_parking_spaces`, `customer_type`, `adr`, `hotel`, `is_repeated_guest`, número de noites e hóspedes.
- **Validação temporal:** treinar com 2015–2016 e testar com 2017.
- **Métricas:** AUC, matriz de confusão, precisão e recall no limiar escolhido, curva de ganho.
- **Limiar:** justificar pelo custo de cada erro (contatar uma reserva que não cancelaria × perder um cancelamento).
- **Multicolinearidade:** checar VIF; agrupar categorias raras (por exemplo, `country` e `agent`).

## Limitações para mencionar
- Dois hotéis em Portugal, entre 2015 e 2017, antes da pandemia: a generalização é limitada.
- O modelo mostra associação, não causa.
- Reservas "Non Refund" cancelam mais que as reembolsáveis, ao contrário do esperado. Provável artefato da origem dos dados; vale citar.
