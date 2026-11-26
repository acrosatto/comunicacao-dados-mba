# Projeto de comunicação com dados

> MBA em Ciência de Dados · 3 integrantes: Ana - Caio - Paulo · Entrega: **terça, 08/12**

---

## 1. Enunciado

### Objetivo
- Apresentar os resultados de uma análise de **regressão, logística ou clusterização**, explicando o problema abordado e como os resultados podem apoiar uma decisão ou ação.
- Considerar um **público misto**: um stakeholder técnico e uma pessoa sem conhecimento técnico na metodologia utilizada.

### Storyline base
**Contexto e decisão → técnica aplicada → evidências e interpretação → recomendação e próximos passos**

Os detalhes metodológicos complementares devem ficar no anexo técnico.

### Tema
Livre.

### Formato da apresentação
- Até **4 slides principais**, mais **1 ou 2 slides de anexo técnico**.
- A estrutura sugerida é um roteiro: as perguntas orientam a construção e não precisam aparecer literalmente na apresentação.

### Estrutura sugerida

#### Slide 1 – Contexto e decisão
- Qual é o problema ou oportunidade?
- Quem é o público da apresentação?
- Que decisão ou ação está em discussão?

#### Slide 2 – Como a análise funciona
- O que o método procura identificar?
- Que dados e variáveis foram utilizados?
- Como o resultado deve ser interpretado?
- Um exemplo simples de interpretação.

#### Slide 3 – Evidências e interpretação
- Uma mensagem principal no título.
- Até 3 resultados essenciais.
- Elementos visuais que sustentem a mensagem.
- O que os resultados sugerem para o problema analisado?
- Incertezas, limitações ou implicações alternativas relevantes.

#### Slide 4 – Decisão e próximos passos
- Qual é a recomendação ou ação proposta?
- Como a evidência apresentada sustenta essa recomendação?
- Qual é o próximo passo concreto para avançar ou validar essa recomendação?

#### Anexo técnico
- Ficha técnica da análise: dados utilizados, metodologia, principais escolhas e pressupostos, métricas de avaliação (quando aplicáveis) e resultados técnicos complementares.

---

## 2. Base de dados

**Hotel Booking Demand, com regressão logística**, escolhida no kickoff (26/11). Roteiro dos slides, motivos da escolha e limitações em [base_hotel_booking.md](base_hotel_booking.md); variáveis no [dicionário de dados](dados/dicionario_hotel_bookings.md).

---

## 3. Equipe

Projeto criado e apresentado por Ana, Caio e Paulo

### Modelo de trabalho: os três em todas as etapas
- Ana, Caio e Paulo trabalham juntos em todas as etapas: análise, slides, fala e ensaio.
- Cada mudança entra por um *pull request*, revisado pelos outros dois antes do merge.
- Todos conhecem tudo (notebooks, slides, roteiro), para que qualquer um consiga responder perguntas na apresentação.

| Etapa | O que os revisores validam |
|---|---|
| 1. Análise e Anexo técnico | Regras da análise do [CLAUDE.md](CLAUDE.md) (vazamento, escopo, validação temporal), uso das variáveis no dicionário e se os resultados fazem sentido para o negócio |
| 2. Slides e fala | Os números batem com as saídas dos notebooks, inclusive o que é dito na fala? A história flui e cada slide tem uma única mensagem? Quem não é técnico entende em 10 segundos? |
| 3. Ensaio | Clareza para o público não técnico, tempo (até 8 minutos), transições e respostas para perguntas prováveis |

### Cuidados
- Revisão é sobre decisões, não só sobre "achei bom": cada revisor registra no *pull request* o que aprovou ou o que precisa mudar.
- Decisões em aberto (por exemplo, o escopo só com reservas sem depósito) viram *issues* e são fechadas pelo grupo.
- Quem fala em cada slide fica registrado no `data-who` das notas. Confirmar com o professor se todos precisam falar.

---

## 4. Cronograma

Todas as etapas são feitas pelos três.

| Data | Etapa | Entrega |
|---|---|---|
| Qui 26/11 | Kickoff | ✅ Base escolhida: Hotel Booking |
| 26/11 → Ter 01/12 | Análise, escolha do modelo e revisão | 🔒 Modelo decidido e resultados congelados na ter 01/12 |
| *em paralelo* | Contexto de negócio e perguntas prováveis | Insumos para os slides 1 e 4 e para a sessão de perguntas |
| Qua 02/12 → Qui 03/12 | Slides e fala juntos + Anexo técnico | Apresentação v1 com notas do apresentador |
| Sex 04/12 | Revisão de slides e fala | Lista de ajustes |
| Sáb 05/12 | Ajustes | Apresentação v2 |
| Dom 06/12 | Ensaio geral com cronômetro | Ajustes de fala e tempo |
| Seg 07/12 | Folga para imprevistos e ensaio final | Versão final |
| **Ter 08/12** | **Apresentação** | — |

### Regras
- Depois de 01/12 o modelo não muda mais.
- A folga de 07/12 fica protegida. Se o grupo não puder trabalhar no fim de semana, adiantar a revisão dos slides para quinta e ensaiar na segunda.

---

## 5. Repositório e apresentação

### Repositório no GitHub (público)
- Um repositório **público**, com os 3 integrantes como colaboradores, com script, arquivos .md e apresentação num lugar só.
- Público porque cada turma escolhe a própria base (sem risco de cópia), o GitHub Pages fica grátis e o projeto serve de portfólio.
- A base é pública e pode ser redistribuída com citação da fonte.
- O histórico registra quem mudou o quê e permite voltar atrás.
- As revisões são registradas no próprio GitHub (*issues* ou *pull requests*), o que atende à regra de "cada revisor registra o que aprovou ou o que precisa mudar".
- Cada integrante precisa de uma conta no GitHub. Quem não usa git pode revisar e comentar direto pelo site.

Estrutura de pastas:

```
comunicacao/
├── README.md                # resumo do projeto e do fluxo de revisão
├── CLAUDE.md                # contexto e regras para agentes de IA
├── projeto.md               # este arquivo
├── base_hotel_booking.md    # roteiro dos slides, escolhas técnicas e limitações
├── dados/                   # base original (CSV) e dicionário de dados
├── analise/                 # notebooks da análise, numerados (01_, 02_...)
├── apresentacao/            # apresentação em um único arquivo HTML
└── apresentacao_html/       # modelo de referência da apresentação (só consulta)
```

### Apresentação em HTML (arquivo único, sem framework)
Modelo de referência: a apresentação do Hackathon Terra Signal ([apresentacao_pitch.html](https://github.com/acrosatto/Hackathon_Terra_Signal/blob/main/reports/apresentacao_pitch.html)).

| Parte | Como fazer |
|---|---|
| **Estrutura** | Um único arquivo HTML; cada slide é um `<section class="slide">`. |
| **Dados** | Os números da análise ficam num bloco JSON embutido (`<script type="application/json" id="dados">`). Os gráficos leem desse bloco: se um número mudar, troca-se num lugar só. |
| **Gráficos** | Desenhados em SVG pelo JavaScript, com as cores definidas em variáveis CSS (por exemplo, `--loss`, `--gain`, `--calm`) para manter a identidade visual. |
| **Animações por clique** | Cada slide declara quantos passos tem (`data-steps="2"`); cada clique revela o próximo elemento. |
| **Notas do apresentador** | `<aside class="notes" data-who="..." data-time="0:50">` em cada slide: fala, quem apresenta e duração. A tecla `N` abre o painel de notas. |
| **Navegação** | Setas, espaço, `Home`/`End`, `F` para tela cheia e `#s3` no endereço para ir direto a um slide. |
| **PDF** | Estilo de impressão (`@media print`) para salvar em PDF pelo navegador, caso o professor peça um arquivo. |

Adaptações para este trabalho:
- **Poucas animações:** com 4 slides, usar animação por clique só onde ela conta a história (por exemplo, revelar a comparação "modelo × regra atual" no Slide 3).
- **Notas com `data-who` e `data-time`** em todos os slides, para o fluxo "slides e fala juntos" e para cronometrar o ensaio.
- **Números só no bloco JSON:** depois do congelamento dos resultados (01/12), qualquer ajuste é feito ali.

### Link da apresentação
- **GitHub Pages** (grátis em repositório público): gera um link que qualquer pessoa abre, no formato `https://<usuário>.github.io/<repositório>/`.
- Atenção: pelo modo simples, o Pages só publica a raiz do repositório ou uma pasta chamada `docs/`. Para publicar `apresentacao/`, é preciso um pequeno *workflow* do GitHub Actions (o Claude pode criar) ou renomear a pasta para `docs/`.

