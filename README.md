# Projeto de comunicação com dados

Apresentação dos resultados de uma análise estatística para apoiar uma decisão de negócio, pensada para um público misto (técnico e não técnico).

MBA em Ciência de Dados · **Ana, Caio e Paulo** · Entrega: **terça, 08/12**

## Status

- **Base:** [Hotel Booking Demand](escolha_base/base_hotel_booking.md), com regressão logística (escolhida no kickoff, 26/11).
- **Papéis:** a definir (A – Análise, B – Slides, C – Apresentador).
- **Próximo marco:** kickoff na quinta, 26/11.

## Onde está cada coisa

| Arquivo ou pasta | Conteúdo |
|---|---|
| [projeto.md](projeto.md) | Enunciado, divisão de tarefas, fluxo de revisão, cronograma e pendências |
| [CLAUDE.md](CLAUDE.md) | Contexto e regras do projeto para agentes de IA que trabalham no repositório |
| [escolha_base/](escolha_base/) | Opções de base avaliadas: [Hotel Booking](escolha_base/base_hotel_booking.md) e [Bike Sharing](escolha_base/base_bike_sharing.md), cada uma com decisão, roteiro dos slides, escolhas técnicas e limitações |
| `dados/` | Base escolhida (CSV) e [dicionário de dados do Hotel Booking](dados/dicionario_hotel_bookings.md) |
| `analise/` | Notebooks da análise e gráficos. [01_avaliacao_variaveis_hotel.ipynb](analise/01_avaliacao_variaveis_hotel.ipynb): avaliação das variáveis, vazamento e escopo |
| `apresentacao/` | Apresentação em um único arquivo HTML, com a fala nas notas do apresentador |

## Como colaboramos

Cada etapa tem **1 responsável e 2 revisores** (detalhes em [projeto.md](projeto.md#3-equipe)).

1. O responsável trabalha numa *branch* própria e abre um *pull request* quando a etapa estiver pronta.
2. Os dois revisores comentam no *pull request* o que aprovam e o que precisa mudar. Quem não usa git pode revisar direto pelo site do GitHub.
3. Com as duas aprovações, o *pull request* é incorporado e a próxima etapa começa.

Dúvidas e decisões em aberto ficam registradas em *issues*.

## Datas principais

| Data | Marco |
|---|---|
| Qui 26/11 | Kickoff |
| Ter 01/12 | 🔒 Resultados da análise congelados |
| Qui 03/12 | Apresentação v1 (slides e fala) |
| Dom 06/12 | Ensaio geral |
| **Ter 08/12** | **Apresentação** |

## Como rodar a análise

Abra os notebooks de `analise/` no Jupyter (o Anaconda já traz tudo). Eles leem a base de `../dados/hotel_bookings.csv` e usam pandas, numpy, scipy e matplotlib.
