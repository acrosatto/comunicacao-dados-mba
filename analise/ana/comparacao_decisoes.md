# Comparação de decisões: notebook da Ana × notebooks do grupo

Decisões de escopo e limpeza em que o `01_exploratoria.ipynb` (Ana) e os notebooks `01` a `03` da pasta `analise/` chegam a tratamentos diferentes, ou em que a proposta ainda não foi aplicada no código. Serve para o grupo fechar cada ponto antes do `04_preparacao.ipynb`.

**Situação:** *igual* (mesmo tratamento), *diferente* (tratamentos diferentes) ou *a decidir* (proposta sem decisão do grupo).

## Escopo

| Ponto | Ana | Notebooks do grupo | Situação |
| --- | --- | --- | --- |
| Reservas usadas no modelo | Base inteira até a seção 4; o escopo é avaliado na seção 5 | Só `No Deposit` (104.641 reservas, 28,4% de cancelamento), aplicado desde o notebook 01 | a decidir (TODO, item 1) |

## Limpeza

| Ponto | Reservas | Ana | Notebooks do grupo | Situação |
| --- | --- | --- | --- | --- |
| `children` vazio | 4 | Remover: cadastros incompletos (as 4 têm `distribution_channel = Undefined`, 2 têm `market_segment = Undefined`) | Preencher com 0 (sem criança) | diferente |
| Sem hóspede | 180 | Remover | Proposta de remover (notebook 01, seção 12), ainda não aplicada no código | a decidir |
| Diária negativa (−6,38) | 1 | Remover | Não removida; continua no escopo | diferente |
| Diária de 5.400 | 1 | Remover | Fica fora só por causa do escopo (é `Non Refund`) | igual no escopo |
| Zero noites | 715 | Manter; juntar com 1 noite no total de noites | Dicionário: juntar com 1 noite. Notebook 03: faixa própria (`0`) em `faixa_noites` | diferente entre o dicionário e o notebook 03 |
| `meal = Undefined` | 1.169 (644 no treino do escopo) | Manter separado. Undefined só existe no resort e SC quase só no urbano; no urbano, SC cancela mais que BB (35,6% × 28,6%); no resort, Undefined cancela menos (13,2% × 22,5%) | Juntar com SC em `sem_refeicao` | diferente |
| Linhas idênticas | 31.994 cópias | Manter; rodar o modelo sem elas para conferir | Manter; rodar o modelo sem elas para conferir | igual |
| `agent` / `company` vazios | 16.340 / 112.593 | Os códigos saem. `company` vira a binária "paga por empresa" (vazio = não), em teste | As duas saem do modelo (`agent`: código sem significado de negócio; `company`: 94% vazia) | diferente em `company` (ver Variáveis) |
| `Undefined` no segmento e no canal | 2 e 5 | Segmento em "Outros"; o canal tende a sair | Segmento em "Outros" (com Complementary e Aviation); o canal sai | igual |

## Variáveis

| Variável | Ana | Notebooks do grupo | Situação |
| --- | --- | --- | --- |
| `previous_cancellations` | Sai: 1 cancelamento anterior cancela 92,4% no treino (79,8% dessas reservas são de 2015) e 17,5% no teste, contra 31,9% sem cancelamento anterior. A relação muda de sentido em 2017 | Testar: já cancelou × nunca cancelou | diferente |
| `babies` | Sai: com bebê cancela 20,6%, contra 26,6% sem; sentido oposto ao de `children`, então não junta com ela | Sai: quase sempre zero. A derivada `com_crianca` (notebook 03) soma crianças e bebês | igual para `babies`; diferente na derivada |
| `noites` | Faixas: até 1 (zero noites junto), 2–3, 4–7 e mais de 7 | Dicionário: as mesmas faixas. Notebook 03: zero noites numa faixa própria | igual ao dicionário |
| `meal` | Testar com quatro níveis: BB (referência), com pensão (HB e FB), SC e Undefined | Testar: sem refeição (SC e Undefined) × com refeição | diferente |
| `arrival_date_month` | Duas temporadas: jul–ago × resto do ano. Só jul–ago fica acima nos dois anos (35,0% e 30,7%); em 2016, abr–jun (25,9%) e set–mar (26,9%) não se separam | Três temporadas: jul–ago, abr–jun e set–mar | diferente |
| `customer_type` | Testar; Group (348 reservas, 12,6%) junta com Contract em "contrato ou grupo". A seção 8 confere se acrescenta algo ao segmento | Entra | diferente no nível Group |
| `company` | Testar "paga por empresa": nos grupos, 4,8% de cancelamento com empresa (625 reservas), contra 34,0% sem | Sai: quase toda vazia | diferente |
| `agent` | Sai: 275 códigos anônimos, embora separem reservas do mesmo segmento (agência online: de 13,8% a 38,6%) | Sai por ora | igual |

## Para fechar com o grupo

1. **`children` vazio:** remover ou preencher com 0? São só 4 reservas: a escolha não muda o modelo, mas o `04_preparacao` precisa de uma regra só.
2. **Sem hóspede e diária negativa:** aplicar a remoção no `04_preparacao`, já que as duas propostas apontam para o mesmo lado.
3. **Zero noites:** alinhar o notebook 03 com o dicionário (juntar com 1 noite) ou manter a faixa própria. Com faixa própria, a referência das dummies não pode ser a de zero noites (VIF alto).
4. **`meal`:** quatro níveis (Undefined separado) ou sem refeição × com refeição. Com a junção, efeitos opostos dos dois hotéis se misturam.
5. **`previous_cancellations`:** tirar do modelo ou manter em teste? Se ficar em teste, conferir o sinal do coeficiente também no teste (2017).
6. **Criança e bebê:** `com_crianca` com ou sem os bebês.
7. **Temporadas:** duas (jul–ago × resto) ou três.
8. **`company`:** testar "paga por empresa" ou deixar fora.
