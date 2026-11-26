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

As opções estão detalhadas em arquivos separados. A base foi escolhida no kickoff (26/11): Hotel Booking Demand.

| Base | Técnica | Status |
|---|---|---|
| [Hotel Booking Demand](escolha_base/base_hotel_booking.md) | Regressão logística | ✅ Escolhida |
| [Bike Sharing](escolha_base/base_bike_sharing.md) | Regressão linear | Não escolhida |
| [Wholesale Customers](https://archive.ics.uci.edu/dataset/292/wholesale+customers) | Clusterização | ❌ Descartada: só 8 variáveis, e os clusters tendem a repetir a variável `Channel` |

---

## 3. Equipe

Projeto criado e apresentado por Ana, Caio e Paulo

### Divisão de tarefas (proposta)

| Pessoa | Papel | Responsabilidades |
|---|---|---|
| **A – Análise** | Responsável pelos números | Limpeza, modelo, validação e principais escolhas técnicas. Entrega os resultados prontos e escreve o Anexo técnico. Responde às perguntas técnicas na apresentação. |
| **B – Slides** | Responsável pelos slides | Gera os slides a partir dos resultados de A. Garante identidade visual única, gráficos limpos e uma mensagem por slide. |
| **C – Apresentador** | Responsável pela história | Define o público e a decisão no início, escreve o roteiro de fala, revisa os slides como público não técnico ("entendi isso em 10 segundos?") e apresenta. |

### Modelo de trabalho: 1 responsável por etapa + 2 revisores
- Cada etapa tem um responsável que produz e os outros dois revisam e validam as decisões antes de seguir para a próxima.
- Todos têm acesso a tudo (script, slides, roteiro), para que qualquer um consiga responder perguntas na apresentação.

| Etapa | Responsável | Revisores | O que os revisores validam |
|---|---|---|---|
| 0. Kickoff (juntos) | Todos | — | Pergunta de negócio, público, decisão em discussão e mensagem principal |
| 1. Análise e Anexo técnico | A | B e C | Escolhas técnicas listadas no arquivo da base (vazamento, validação, métricas) e se os resultados fazem sentido para o negócio |
| 2. Slides e fala (juntos) | B (slides) e C (fala, nas notas do apresentador) | A | Os números e interpretações estão corretos, inclusive o que é dito na fala? B e C revisam um ao outro enquanto trabalham juntos. |
| 3. Ensaio | C | A e B | Clareza para o público não técnico, tempo, transições, respostas para perguntas prováveis |

### Cuidados
- Revisão é sobre decisões, não só sobre "achei bom": cada revisor registra o que aprovou ou o que precisa mudar.
- C participa desde o kickoff, ajudando a definir a mensagem principal.
- A e B também ficam no palco: A responde às perguntas técnicas e B pode conduzir os slides.
- Confirmar com o professor se todos precisam falar. Se sim: C apresenta os slides 1 a 4 e A apresenta o anexo técnico.

---

## 4. Cronograma

| Data | Etapa | Quem | Entrega |
|---|---|---|---|
| Qui 26/11 | Kickoff (1h) | Todos | Escolha da base, decisão, público e mensagem principal |
| 26/11 → Dom 29/11 | Análise | A | Script e resultados v1 |
| *em paralelo* | Contexto de negócio e perguntas prováveis | C | Insumos para os slides 1 e 4 e para a sessão de perguntas |
| Seg 30/11 → Ter 01/12 | Revisão da análise | B e C revisam | 🔒 Resultados congelados na ter 01/12 |
| Qua 02/12 → Qui 03/12 | Slides e fala juntos + Anexo técnico | B e C juntos, A no anexo | Apresentação v1 com notas do apresentador |
| Sex 04/12 | Revisão de slides e fala | A revisa | Lista de ajustes |
| Sáb 05/12 | Ajustes | B e C | Apresentação v2 |
| Dom 06/12 | Ensaio geral com cronômetro | Todos | Ajustes de fala e tempo |
| Seg 07/12 | Folga para imprevistos e ensaio final | Todos | Versão final |
| **Ter 08/12** | **Apresentação** | — | — |

### Regras
- Depois de 01/12 o modelo não muda mais.
- A folga de 07/12 fica protegida. Se o grupo não puder trabalhar no fim de semana, adiantar a revisão dos slides para quinta e ensaiar na segunda.

---

## 5. Repositório e apresentação

### Repositório no GitHub (público)
- Um repositório **público**, com os 3 integrantes como colaboradores, com script, arquivos .md e apresentação num lugar só.
- Público porque cada turma escolhe a própria base (sem risco de cópia), o GitHub Pages fica grátis e o projeto serve de portfólio.
- As bases são públicas e podem ser redistribuídas com citação da fonte.
- O histórico registra quem mudou o quê e permite voltar atrás.
- As revisões são registradas no próprio GitHub (*issues* ou *pull requests*), o que atende à regra de "cada revisor registra o que aprovou ou o que precisa mudar".
- Cada integrante precisa de uma conta no GitHub. Quem não usa git pode revisar e comentar direto pelo site.

Estrutura de pastas proposta:

```
comunicacao/
├── README.md                # resumo do projeto e do fluxo de revisão
├── projeto.md               # este arquivo
├── escolha_base/            # opções de base avaliadas
│   ├── base_hotel_booking.md
│   └── base_bike_sharing.md
├── dados/                   # base escolhida (CSV)
├── analise/                 # script ou notebook da análise e gráficos
└── apresentacao/            # apresentação em um único arquivo HTML
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

