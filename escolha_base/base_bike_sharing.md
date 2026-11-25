# Opção 2 – Bike Sharing (regressão linear)

## Base
- UCI: https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset
- Capital Bikeshare, Washington DC, 2011–2012.
- Dois arquivos: `day.csv` (731 dias) e `hour.csv` (17.379 horas).
- Variável alvo: `cnt` (número de aluguéis).

## Pontos de atenção em relação à Hotel
- **A decisão é menos óbvia:** "mais calor gera mais aluguéis" é intuitivo demais. É preciso enquadrar bem a decisão (abaixo) para os slides 1 e 4 terem força.
- **Mais armadilhas estatísticas:** série temporal (resíduos autocorrelacionados), alvo de contagem, efeito não linear da temperatura, crescimento entre 2011 e 2012.
- **Vantagem:** o Slide 2 é fácil de explicar ("chuva reduz os aluguéis em __%").

## Problema, público e decisão
- **Problema:** a demanda varia muito por hora e clima; faltam bicicletas nos picos e há bicicletas paradas em outros horários.
- **Público:** Gerente de Operações (não técnico) e Analista de dados (técnico).
- **Decisão:** quando concentrar manutenção e rebalanceamento, e quanto reforçar a frota por turno e previsão do tempo.

## Roteiro dos slides

| Slide | Conteúdo |
|---|---|
| 1. Contexto e decisão | A demanda oscila muito ao longo do dia e com o clima. Decisão: planejar manutenção, rebalanceamento e frota de acordo com a demanda esperada. |
| 2. Como funciona | O modelo estima quantos aluguéis esperar a partir de hora, dia útil, estação e clima. Exemplo: "dia útil, 8h, tempo bom, 20 °C → cerca de __ aluguéis; com chuva → __% a menos". |
| 3. Evidências | Título com a mensagem (por exemplo: "Hora e clima explicam a maior parte da variação da demanda"). Três resultados: (1) perfil por hora em dias úteis × fins de semana (picos às 8h e às 17–18h), (2) efeito da chuva em %, (3) efeito da temperatura (curva). Limitações. |
| 4. Recomendação | Concentrar manutenção na madrugada e em dias de chuva prevista; reforçar o rebalanceamento antes dos picos. Próximo passo: piloto usando a previsão do tempo para planejar a escala por algumas semanas e medir falta de bicicletas. |
| Anexo técnico | Escolha do modelo, variáveis, validação temporal, métricas, diagnóstico de resíduos, tabela de coeficientes. |

Os `__` são preenchidos depois que a análise rodar.

## Escolhas técnicas (para A, revisadas por B e C)
- **Base:** usar `hour.csv`, porque a decisão (manutenção, rebalanceamento) é por horário.
- **Remover por vazamento:** `casual` e `registered` (somam exatamente `cnt`). Remover também `instant` e `dteday` como preditores.
- **Variáveis:** `hr` (categórica), `workingday`, interação `hr × workingday`, `season`, `yr`, `weathersit`, `temp` (com termo quadrático ou faixas), `hum`, `windspeed`. Usar só uma entre `temp` e `atemp` (são quase idênticas).
- **Modelo:** regressão linear com alvo `log(cnt + 1)`. O projeto permite apenas regressão linear, logística ou clusterização, e o log resolve os principais problemas da linear com contagens:
  - não prevê aluguéis negativos;
  - estabiliza a variância (o erro no pico é muito maior que de madrugada);
  - transforma os efeitos em %: "chuva reduz os aluguéis em cerca de __%", o que vale tanto no pico quanto na madrugada.
  - No anexo, explicar a transformação e que, para voltar à escala de aluguéis, aplica-se a exponencial.
- **Validação temporal:** treinar com os dados até setembro de 2012 e testar com outubro a dezembro de 2012.
- **Métricas:** MAE e RMSE no teste, comparação com uma linha de base simples (média por hora e dia útil).
- **Diagnóstico:** resíduos (normalidade e variância constante após o log) e autocorrelação temporal; citar no anexo.

## Limitações para mencionar
- Uma cidade, em 2011–2012: o padrão de uso pode ter mudado.
- Autocorrelação temporal: os erros-padrão podem estar subestimados.
- O modelo explica a demanda total; não indica em quais estações faltam bicicletas.
