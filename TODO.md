# TODO

Tarefas do projeto até a apresentação (terça, 08/12). Marque `[x]` ao concluir, no mesmo pull request da tarefa. Decisões em aberto viram *issues*; quando forem fechadas, atualize esta lista, o dicionário de dados e o `CLAUDE.md`.

## 1. Decisões do grupo (antes do modelo)

- [ ] **Escopo:** modelar só as reservas sem depósito (`No Deposit`, 104.641 reservas)? Proposta: sim. Ver a seção "Escopo proposto" do dicionário de dados.
- [ ] **Duplicadas:** manter ou remover as linhas idênticas? Proposta: manter e rodar uma versão sem elas para conferir.
- [ ] **Variáveis em teste:** decidir pelo teste com e sem (notebook 04): fez pedido especial, já cancelou antes, sozinho × acompanhado, com criança, total de noites e regime de refeição.
- [ ] **Faixas de antecedência:** até 7, 8–30, 31–90, 91–180 e mais de 180 dias?
- [ ] **Limpeza:** tirar as reservas sem hóspede e decidir sobre as reservas com zero noites.
- [ ] **Ação principal do slide 4:** lista de ligação (ordenar), depósito acima de um ponto de corte (decidir) ou overbooking (estimar). Proposta: lista de ligação, com depósito para a faixa de maior risco; overbooking como próximo passo.
- [ ] **Premissa de custo:** quanto custa contatar uma reserva e quanto da receita de um cancelamento evitado se recupera. Sem isso, o ponto de corte não tem justificativa.
- [ ] **Quem fala em cada slide** (`data-who` nas notas).

## 2. Análise (até terça, 01/12, quando os resultados congelam)

- [x] `01_avaliacao_variaveis_hotel.ipynb`: vazamento, escopo, linearidade no logito, V de Cramér e dicionário de dados.
- [ ] `02_exploracao_hotel.ipynb`: tamanho do problema, quando os cancelamentos acontecem, onde se concentram, mudança em 2017 e regras simples. Primeira versão pronta; falta a revisão do grupo.
- [ ] `03_preparacao.ipynb`: aplicar escopo e limpeza; criar as variáveis no formato do dicionário (faixas, binárias, agrupamentos); separar treino (2015 e 2016) e teste (2017).
- [ ] `04_modelo.ipynb`: regressão logística no treino; testar com e sem as variáveis em teste; conferir se os sinais das razões de chances fazem sentido para o negócio; escolher o modelo.
- [ ] `05_avaliacao.ipynb`, no ano de teste (2017):
  - [ ] curva de ganho comparada às regras simples do notebook 02: o modelo precisa encontrar mais de 66% dos cancelamentos contatando 44% das reservas;
  - [ ] AUC e calibração (probabilidade prevista × taxa real), com atenção à alta de 2017;
  - [ ] precisão e recall no ponto de corte, justificado pela premissa de custo;
  - [ ] sensibilidade: o mesmo modelo sem as linhas duplicadas.
- [ ] Exportar os números da apresentação para um JSON, que alimenta o bloco de dados do HTML.
- [ ] 🔒 **Terça, 01/12:** modelo decidido e resultados congelados.

## 3. Apresentação (quarta, 02/12, a segunda, 07/12)

- [ ] Estrutura do HTML em `apresentacao/`, no modelo de `apresentacao_html/para_quem_vale_ligar.html`.
- [ ] **Slide 1, contexto e decisão:** quantas reservas e quanta receita são canceladas, e a decisão em discussão.
- [ ] **Slide 2, como funciona:** o modelo explicado com o exemplo de uma reserva e a probabilidade dela.
- [ ] **Slide 3, evidências:** principais fatores, curva de ganho contra as regras simples e limitações.
- [ ] **Slide 4, recomendação:** a ação principal, quando agir e o próximo passo (piloto A/B).
- [ ] **Anexo técnico:** escopo, variáveis excluídas e por quê, divisão temporal, métricas, ponto de corte, razões de chances e limitações (2017 cancela mais; receita em risco não é perda; reservas de um mesmo grupo não são independentes).
- [ ] Notas com `data-who` e `data-time` em todos os slides.
- [ ] Link pelo GitHub Pages (precisa de um *workflow* ou da pasta `docs/`).
- [ ] Quinta, 03/12: apresentação v1 · sexta, 04/12: revisão · sábado, 05/12: v2 · domingo, 06/12: ensaio geral com cronômetro (até 8 minutos) · segunda, 07/12: folga e ensaio final.

## 4. Repositório

- [x] Base, dicionário de dados, `CLAUDE.md` e modelo de referência da apresentação.
- [ ] Manter o `CLAUDE.md`, o dicionário e esta lista atualizados a cada decisão.
