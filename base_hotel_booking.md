# Hotel Booking Demand (regressão logística)

## Base
- Kaggle: https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand
  - O Kaggle exige login. O mesmo CSV está no repositório do TidyTuesday (rfordatascience, 11/02/2020).
- Fonte original (citar no anexo): Antonio, Almeida & Nunes (2019), *Hotel booking demand datasets*, Data in Brief.
- 119.390 reservas, 32 variáveis, dois hotéis em Portugal (City Hotel e Resort Hotel), chegadas de julho de 2015 a agosto de 2017.
- Variável alvo: `is_canceled` (37,0% de cancelamento na base toda; 28,4% entre as reservas sem depósito).
- Detalhes de cada variável: [dados/dicionario_hotel_bookings.md](dados/dicionario_hotel_bookings.md).

## Por que esta base
Escolhida no kickoff (26/11) entre Hotel Booking (regressão logística) e Bike Sharing (regressão linear). Wholesale Customers (clusterização) foi descartada antes: só 8 variáveis, e os clusters tendem a repetir a variável `Channel`.

- **Decisão clara e com dinheiro envolvido:** cancelamentos geram quartos vazios e receita perdida.
- **Alvo naturalmente sim/não:** a reserva foi cancelada ou não, o que encaixa na logística sem adaptar o problema.
- **Resultado fácil de comunicar:** "esta reserva tem 70% de chance de cancelar" funciona para o público não técnico; razões de chances, AUC e limiar interessam ao técnico.
- **Modelo mais fácil de defender:** cada reserva é independente, sem os problemas de série temporal da Bike Sharing (resíduos autocorrelacionados, alvo de contagem, crescimento entre os anos).
- **Com só 4 slides:** a decisão cabe numa frase e a evidência leva direto à ação.

## Problema, público e decisão
- **Problema:** muitas reservas são canceladas, e o quarto fica vazio.
- **Público:** Diretoria de Receita (não técnica) e analista de BI (técnico).
- **Decisão:** em quais reservas pedir depósito, ligar para confirmar ou aceitar overbooking?

## Roteiro dos slides

| Slide | Conteúdo |
|---|---|
| 1. Contexto e decisão | Taxa de cancelamento e impacto em receita. Decisão em discussão: onde agir para reduzir o prejuízo. |
| 2. Como funciona | O modelo estima a probabilidade de cancelamento com informações disponíveis **no momento da reserva**. Exemplo: "reserva feita mais de 180 dias antes, via agência online, sem pedidos especiais → __% de risco". |
| 3. Evidências | Título com a conclusão (por exemplo: "Reservas feitas com meses de antecedência concentram os cancelamentos"). Até três resultados: (1) principais fatores, (2) curva de ganho ("os 20% de maior risco concentram __% dos cancelamentos"), (3) comparação do modelo com uma regra simples que o hotel poderia usar hoje. Limitações. |
| 4. Recomendação | Score de risco no momento da reserva; para as reservas de alto risco, pedir depósito ou ligar para confirmar. Próximo passo: piloto A/B de 3 meses em um dos hotéis, medindo cancelamentos e receita. |
| Anexo técnico | Escopo, variáveis excluídas por vazamento, divisão temporal, AUC, matriz de confusão, justificativa do limiar, tabela de razões de chances. |

Os `__%` são preenchidos com saídas reais dos notebooks.

## Escolhas técnicas
As regras da análise estão no [CLAUDE.md](CLAUDE.md) e o uso de cada variável no [dicionário de dados](dados/dicionario_hotel_bookings.md). Em resumo:

- **Modelo:** regressão logística binária (`statsmodels`, `GLM` binomial). A saída usada no negócio é a probabilidade de cancelamento de cada reserva.
- **Escopo proposto:** só as reservas sem depósito (`deposit_type = No Deposit`), a validar pelo grupo.
- **Sem vazamento:** só entram variáveis conhecidas quando a reserva entra (coluna "Quando se sabe" do dicionário).
- **Validação temporal:** treino com as chegadas de 2015 e 2016, teste com as de 2017.
- **Limiar:** justificado pelo custo de cada erro (ligar para uma reserva que não cancelaria × deixar passar um cancelamento).
- **Métricas:** AUC, matriz de confusão, precisão e recall no limiar escolhido, curva de ganho.

## Limitações para mencionar
- Dois hotéis em Portugal, de 2015 a 2017, antes da pandemia: a generalização é limitada.
- O modelo mostra associação, não causa.
- 27% das linhas são cópias idênticas de outras, concentradas em grupos e operadoras; a base não tem número de reserva para distinguir quartos do mesmo grupo de erros.
- O escopo exclui as reservas Non Refund (99,4% de cancelamento, concentradas em blocos de grupos e operadoras): o modelo vale só para reservas sem depósito.
