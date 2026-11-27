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
| `meal = Undefined` | 1.169 | Manter separado ("não informado"): cancela 24,5%, contra 37,2% do SC | Juntar com SC em `sem_refeicao` | diferente; testar na bivariada |
| Linhas idênticas | 31.994 cópias | Manter; rodar o modelo sem elas para conferir | Manter; rodar o modelo sem elas para conferir | igual |
| `agent` / `company` vazios | 16.340 / 112.593 | Ainda não decidido se as variáveis entram. Se entrarem, o vazio vira categoria ("sem agência" / "sem empresa") | As duas saem do modelo (`agent`: código sem significado de negócio; `company`: 94% vazia), então o vazio não precisa de tratamento | a decidir: primeiro se entram (bivariada), depois o vazio |
| `Undefined` no segmento e no canal | 2 e 5 | Segmento em "Outros"; o canal tende a sair | Segmento em "Outros" (com Complementary e Aviation); o canal sai | igual |

## Para fechar com o grupo

1. **`children` vazio:** remover ou preencher com 0? São só 4 reservas: a escolha não muda o modelo, mas o `04_preparacao` precisa de uma regra só.
2. **Sem hóspede e diária negativa:** aplicar a remoção no `04_preparacao`, já que as duas propostas apontam para o mesmo lado.
3. **Zero noites:** alinhar o notebook 03 com o dicionário (juntar com 1 noite) ou manter a faixa própria. Com faixa própria, a referência das dummies não pode ser a de zero noites (VIF alto).
4. **`meal = Undefined`:** decidir pela bivariada no treino (2015 e 2016) e no escopo escolhido.
