# Contrato de temas

Um tema é a composição de `base.json` com um modo, como `light.json` ou
`dark.json`. A validação ocorre depois do merge: cada arquivo pode conter
somente a parte que possui.

## Seções obrigatórias após o merge

- `meta.name` e `meta.schema_version` (o default é `1`);
- `layout`, `typography`, `spacing`, `borders`, `icons`, `colors` e `effects`;
- `chart`, incluindo `severity`, `echarts` e `colorscale_extended`.

As chaves obrigatórias correspondem aos tokens que os componentes atuais já
consomem. A falha aponta a chave e o tipo esperado.

## Seções extensíveis

`components` é opcional: o núcleo completa seus valores neutros antes da
validação. Portanto, um tema novo pode começar apenas com os tokens primitivos
e sobrescrever componentes aos poucos. Chaves desconhecidas são permitidas
para tornar o contrato compatível com evolução futura.

O tema-base do Bankai ilustra os blocos atualmente consumidos: `button`,
`input`, `navigation`, `metric` e `card`. Para cards, as variantes
`surface`, `elevated`, `outline` e `minimal` definem `background`, `border`,
`radius`, `shadow`, `hover_shadow` e `hover_transform`.

Na aplicação, a intenção é declarada sem CSS:

```python
CardConfig(card_id="summary", context=context, variant="elevated")
```

Uma aplicação pode acrescentar outras variantes no seu tema. O nome deve ser
um identificador simples, pois também integra a chave CSS do componente.

As quatro variantes base (`surface`, `elevated`, `outline` e `minimal`) são
sempre disponibilizadas pelo núcleo. Uma aplicação pode sobrescrever seus
tokens, mas não precisa duplicar a estrutura para iniciar um tema novo.

Cards não recebem espaço interno implícito. Declare `padding="compact"` ou
`padding="normal"` em `CardConfig` quando o componente realmente precisar
desse respiro; o padrão `padding="none"` evita acúmulo em cards aninhados.

## Variáveis CSS compiladas

Todo valor primitivo do tema vira automaticamente uma variável `--ui-*`, usando
o caminho JSON em kebab-case. Por exemplo,
`components.card.variants.elevated.radius` resulta em
`--ui-components-card-variants-elevated-radius`.

O sistema expõe somente tokens `--ui-*`; não há aliases com o nome de uma
aplicação. Isso permite que qualquer aplicação use os mesmos componentes sem
herdar identidade visual de outra.
