# CLAUDE.md

Contexto para agentes que trabalham neste repositório.

## O projeto

Apresentação dos resultados de uma regressão logística que apoia uma decisão de negócio, para um público misto: uma pessoa técnica e uma sem conhecimento da técnica. Grupo: Ana, Caio e Paulo. Apresentação na terça, 08/12/2026.

- **Base:** Hotel Booking Demand, escolhida no kickoff (26/11). Cada linha é uma reserva de um de dois hotéis em Portugal, com chegadas de julho de 2015 a agosto de 2017.
- **Y:** `is_canceled` (1 = cancelada, incluindo no-show). 37% na base toda.
- **Decisão em discussão:** em quais reservas pedir depósito, ligar para confirmar ou aceitar overbooking.
- **Público:** Diretoria de Receita (não técnica) e analista de BI (técnico).
- **Formato:** até 8 minutos; até 4 slides principais e 1 ou 2 de anexo técnico. Roteiro: contexto e decisão → como a análise funciona → evidências e interpretação → recomendação e próximos passos. A recomendação precisa ser clara.

O `projeto.md` é a referência para enunciado, papéis, fluxo de revisão, cronograma e formato da apresentação. Se uma tarefa contradisser o `projeto.md`, avise quem pediu antes de seguir.

## Onde está cada coisa

| Caminho | Conteúdo |
| --- | --- |
| `projeto.md` | Enunciado, papéis, fluxo de revisão, cronograma e modelo da apresentação |
| `escolha_base/base_hotel_booking.md` | Roteiro dos slides, escolhas técnicas e limitações da base escolhida |
| `dados/hotel_bookings.csv` | Base original. Não editar: toda transformação fica nos notebooks |
| `dados/dicionario_hotel_bookings.md` | Dicionário de dados: tipo, quando se sabe e uso proposto de cada variável |
| `analise/01_avaliacao_variaveis_hotel.ipynb` | Avaliação das variáveis: vazamento, escopo, linearidade no logito e V de Cramér |
| `apresentacao/` | A apresentação, num único arquivo HTML |
| `apresentacao_html/para_quem_vale_ligar.html` | Modelo de referência da apresentação (estrutura, bloco JSON, gráficos em SVG e notas). Só consulta: não editar |

## Regras da análise

1. **Sem vazamento.** O modelo é usado quando a reserva entra, então só pode usar o que o hotel sabe nessa hora. Estão fora: `reservation_status`, `reservation_status_date`, `assigned_room_type`, `booking_changes`, `required_car_parking_spaces` e `country`. Antes de usar qualquer variável, confira a coluna "Quando se sabe" do dicionário.
2. **Escopo proposto:** só as reservas com `deposit_type = No Deposit` (104.641 reservas, 28,4% de cancelamento). Ainda precisa ser validado pelo grupo: confirme antes de assumir. O motivo está no dicionário, na seção "Escopo proposto".
3. **Validação temporal:** treino com as chegadas de 2015 e 2016, teste com as de 2017 (janeiro a agosto). Não use divisão aleatória. `arrival_date_year` não entra como variável.
4. **Numéricas:** só entram como número se forem lineares no logito (gráfico do logito por decis). Se não forem, viram faixas. `lead_time` entra em faixas.
5. **Modelo:** regressão logística (`statsmodels`, `GLM` com família binomial). A saída usada no negócio é a probabilidade de cancelamento de cada reserva. Razões de chances ($e^b$) e métricas ficam no anexo técnico.
6. **Dicionário atualizado:** ao incluir, tirar ou transformar uma variável, atualize a coluna "Uso proposto" do dicionário no mesmo pull request.
7. **Congelamento:** os resultados ficam congelados em 01/12. Depois disso, o modelo não muda; só texto e visual.
8. **Números verificáveis:** todo número de slide, fala ou texto sai de uma saída real de um notebook. Não invente nem estime de cabeça. Enquanto a análise não tiver rodado, use `__`.

## Como rodar

Jupyter, pelo Anaconda. Os notebooks ficam em `analise/`, numerados na ordem de leitura (`01_`, `02_`...), e leem a base de `../dados/hotel_bookings.csv`. Usam pandas, numpy, scipy e matplotlib; o modelo usa statsmodels. Antes de commitar um notebook, rode-o do começo ao fim, para que as saídas salvas batam com o código.

## Como colaborar

- Cada etapa tem 1 responsável e 2 revisores (`projeto.md`, seção 3).
- Trabalhe numa branch própria e abra um pull request. Não faça commit direto na `main` nem merge sem as duas aprovações.
- Commits e pull requests em português, dizendo o que mudou.
- Dúvidas e decisões em aberto viram *issues*.

## Como escrever

- Português do Brasil, frases curtas e voz ativa.
- Escreva só o que o projeto precisa. Não registre de onde veio uma ideia, uma regra ou um texto; justifique pelo negócio ou pelos dados.
- **Slides para público misto:** fale em probabilidade ("esta reserva tem 70% de chance de cancelar"), não em log-odds ou coeficientes. Métricas como AUC, precisão e recall ficam no anexo técnico.
- **Um slide, uma mensagem:** o título diz a conclusão ("Reservas feitas com meses de antecedência concentram os cancelamentos"), não o assunto ("Antecedência").
- **Limitações à vista:** dois hotéis em Portugal, de 2015 a 2017, antes da pandemia; o modelo mostra associação, não causa.

## Apresentação

- Um único arquivo HTML em `apresentacao/`, sem framework, no modelo descrito na seção 5 do `projeto.md` e exemplificado em `apresentacao_html/para_quem_vale_ligar.html`: cada slide num `<section class="slide">`, números num bloco JSON embutido, gráficos em SVG lendo desse bloco e notas com `data-who` e `data-time` em todos os slides.
- Depois de 01/12, qualquer ajuste de número é feito só no bloco JSON.
