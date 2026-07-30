# Contexto técnico do sistema

Este arquivo registra o entendimento da arquitetura em 29/07/2026. Ele deve ser
atualizado quando os contratos de bootstrap, aplicação, tema, estado ou layout
mudarem de forma relevante.

## Visão geral

O repositório hospeda aplicações Streamlit independentes sobre um framework
compartilhado. A divisão central é:

- system: infraestrutura e UI reutilizáveis, sem regra de negócio de uma
  aplicação concreta;
- bankai: aplicação demonstrativa, dona de rotas, estado, páginas, dados e
  identidade visual;
- app.py: bootstrap que escolhe e inicia uma aplicação;
- tests: testes de contrato e de preparação de dados.

Uma aplicação nova deve ser irmã de bankai e expor get_application() em seu
módulo app.py. Não há uma lista central de aplicações.

## Fluxo de inicialização

1. O app.py raiz carrega o ambiente e resolve o app pelo query param app, com
   fallback para argumento de linha de comando e depois para bankai.
2. O ApplicationRegistry importa o módulo nome.app e obtém uma
   ApplicationDefinition.
3. O Streamlit recebe os metadados de página e a largura do navegador é
   detectada uma vez por sessão.
4. system.core.managers.config.state cria ou recupera o estado da aplicação e o
   AppContext.
5. Na primeira criação do contexto, o modo visual é lido de
   .streamlit/runtime_preferences.json. Um modo ausente ou inválido usa o
   default_mode da aplicação.
6. O tema é carregado pela própria aplicação, validado pelo System e compilado
   em variáveis CSS.
7. A autenticação opcional é executada.
8. O renderer da aplicação resolve a rota e compõe os slots de layout.

Fluxo resumido:

    navegador -> app.py -> ApplicationDefinition -> AppContext
              -> tema/CSS -> autenticação -> layout da aplicação -> página

## Contratos e responsabilidades

### ApplicationDefinition

É o contrato mínimo entre o bootstrap e uma aplicação. Declara app_id, título,
rota inicial, modo padrão, renderer, carregador de tema, fábrica de estado e
configuração de autenticação.

O System não deve importar bankai. A direção correta da dependência é a
aplicação importar componentes e contratos do System.

### AppContext

É um contexto técnico compartilhado. Contém:

- app_name;
- mode e o mapa theme já normalizado;
- screen_width e as propriedades responsivas derivadas;
- referência ao estado que pertence à aplicação;
- callbacks injetados para carregar e persistir o modo do tema.

Filtros, rota atual e outros dados de domínio não devem migrar para o
AppContext.

### Estado da aplicação

O Bankai mantém BankaiState em st.session_state com a chave bankai. Ele é a
fonte de verdade para current_route, active_filters, detalhes e deduplicação de
eventos de gráfico.

O contexto técnico usa uma chave separada, app_context_bankai. Assim, trocar o
tema não recria os filtros nem a navegação.

### Tema

Cada aplicação fornece theme/base.json e arquivos de modo, atualmente
light.json e dark.json no Bankai. O carregamento:

1. combina base e modo;
2. aplica defaults neutros do framework;
3. valida os tokens obrigatórios;
4. converte valores primitivos para variáveis CSS com prefixo --ui.

O CSS do System só deve consumir tokens genéricos --ui e nunca nomes ou cores
fixas de uma aplicação.

O modo selecionado é persistido por aplicação em
.streamlit/runtime_preferences.json. A escrita usa arquivo temporário e troca
atômica para evitar JSON parcialmente gravado. O arquivo representa uma
preferência do servidor, não uma preferência individual por navegador ou
usuário. Em execução distribuída ele deve ficar em volume compartilhado, ou ser
substituído futuramente por uma persistência por usuário.

## Componentes visuais

Os componentes reutilizáveis ficam em system/view/components. O padrão atual é
expor uma função draw(), receber context e um identificador estável, gerar
chaves isoladas por aplicação e deixar a aparência no CSS/token de tema.

O componente system.view.components.button envolve st.button e possui três
variações:

- primary: ação de maior ênfase;
- secondary: ação neutra;
- ghost: barras de ferramentas e ações discretas.

Exemplo:

    from system.view.components import button

    clicked = button.draw(
        context=context,
        label="Salvar",
        button_id="save_report",
        variant="primary",
        icon=":material/save:",
        width="stretch",
    )

O button_id forma a identidade estável do widget. A variant altera apenas o
contêiner semântico usado pelo CSS. Cores, bordas, sombras e estados hover vêm
de components.button.variants no tema normalizado.

O seletor de tema e o logout do cabeçalho já usam a variante ghost.

## Rotas e layout atual

bankai/routes.py mapeia cada rota somente para seu renderer. O shell em
bankai/layout.py desenha o header compartilhado e chama a página atual.

Cada página compõe diretamente suas colunas, filtros, sidebar e áreas roláveis
com primitivas do Streamlit. Não existe mais PageLayout nem posicionamento
sticky no framework. A Home demonstra duas colunas na proporção 1:3, com
sidebar independente e conteúdo dentro de st.container com altura de 800 px.
Análise e Relatórios posicionam os filtros acima de seus próprios containers.

Essa composição manual é intencional: páginas podem usar qualquer quantidade
ou proporção de colunas e decidir individualmente onde ocorre a rolagem.

## Dados, filtros e gráficos

bankai/application contém casos de uso e transformação de dados.
bankai/infrastructure contém a origem concreta dos dados. bankai/domain contém
conceitos de domínio.

Os filtros são guardados no estado da aplicação e aplicados por managers puros
de dataframe. Gráficos podem atualizar filtros por eventos, desde que o estado
implemente active_filters, update_filter(), remove_filter(),
get_last_event_ts() e set_last_event_ts().

Managers em system/core/managers/charts preparam payloads e interações; os
componentes em system/view/components/charts cuidam da renderização.

## Convenções para mudanças futuras

- Regra de negócio pertence à aplicação, não ao System.
- Um componente compartilhado recebe context e usa chaves com escopo por app.
- Novos estilos entram na árvore system/view/styles e usam tokens --ui.
- Novos tokens opcionais devem ter defaults no framework antes de serem
  exigidos pela validação.
- O shell da aplicação deve conter apenas elementos realmente compartilhados;
  a topologia do conteúdo pertence ao renderer da página.
- Mudanças de contratos devem ganhar testes em tests.
- A preferência persistida não deve sobrescrever o contexto a cada rerun; ela
  só inicializa uma sessão nova e é atualizada quando o modo realmente muda.

## Verificação

A suíte principal é executada com:

    python -m unittest discover -s tests -p "test_theme_contract.py" -v

Para alterações visuais, a validação complementar é iniciar o Streamlit,
alternar light/dark e conferir primary, secondary e ghost, incluindo hover,
focus, disabled e largura stretch.
