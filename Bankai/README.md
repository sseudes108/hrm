# Bankai / Zanpakutou Framework

Framework para hospedar múltiplas aplicações Streamlit independentes no mesmo
repositório. O núcleo em `system/` contém infraestrutura, layout, tema e
componentes reutilizáveis. Cada aplicação (`bankai/`, `athena/` ou outra) é dona
das suas rotas, estado, tema e regra de negócio.

## Requisitos

- Python 3.12 ou superior
- `pip`
- Opcionalmente, um PostgreSQL configurado quando a aplicação usar o manager de
  banco de dados

## Instalação

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No Linux/macOS, use `source .venv/bin/activate`.

Instale o projeto e suas dependências:

```powershell
python -m pip install --upgrade pip
pip install -e .
```

Se necessário, crie um arquivo `.env` na raiz. Ele é carregado pelo bootstrap
são:

```env
DB_USER=usuario
DB_PASS=senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=base
```

Não versione segredos no `.env`.

### Autenticação opcional

Uma aplicação pode habilitar o guard local do framework na sua
`ApplicationDefinition`:

```python
from system.core.auth import AuthConfig

auth=AuthConfig(enabled=True, allow_local_auth=True, local_users={...})
```

O Bankai vem habilitado apenas para demonstração com `admin / bankai123`.
Troque ou remova essa credencial antes de qualquer implantação. Para ambiente
persistente, defina um segredo forte no `.env`:

```env
AUTH_COOKIE_SECRET=uma-chave-aleatoria-longa-e-exclusiva-do-ambiente
```

Quando o PostgreSQL estiver configurado, o guard consulta a tabela `app_users`
por `username`, `password_hash` e `is_active`. A senha deve estar no formato
PBKDF2 gerado por `system.core.auth.hash_password()`. Consultas e inserts usam
parâmetros e identificadores SQL validados; não concatene valores fornecidos por
usuários em consultas.

Exemplo mínimo da tabela:

```sql
CREATE TABLE app_users (
    id BIGSERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);
```

O cookie contém somente um token assinado e com expiração, nunca a senha. Como
cookies escritos pelo navegador não podem ser `HttpOnly`, use HTTPS, configure
`AUTH_COOKIE_SECRET` e mantenha a expiração curta em produção.

## Execução

O ponto de entrada é [app.py](D:\Dev\Python\Bankai\app.py). Execute sempre a
partir da raiz:

```powershell
streamlit run app.py
```

Sem parâmetro, o bootstrap abre `bankai`. Para selecionar uma aplicação, passe
o parâmetro de URL `app`:

```text
http://localhost:8501/?app=bankai
http://localhost:8501/?app=athena
```

Também há compatibilidade com argumento de linha de comando:

```powershell
streamlit run app.py -- --athena
```

### Docker

Construa a imagem na raiz do projeto:

```powershell
docker build -t zanpakutou-framework .
```

Execute expondo a porta do Streamlit. O app padrão é Bankai; para selecionar
Athena, acesse a URL com `?app=athena`.

```powershell
docker run --rm -p 8501:8501 --env-file .env zanpakutou-framework
```

O `.dockerignore` impede o envio de segredos, ambientes virtuais e caches ao
contexto de build. Não inclua `.env` dentro da imagem.

## Dependências

| Pacote | Uso no projeto |
| --- | --- |
| `streamlit` | Runtime e widgets da interface. |
| `streamlit-echarts` | Renderização dos gráficos ECharts. |
| `streamlit-js-eval` | Leitura da largura do navegador para comportamento responsivo. |
| `pandas` e `numpy` | Manipulação e agregação de dados. |
| `ortools` | Recursos de otimização usados pelas aplicações que precisam deles. |
| `pandas-ta` | Indicadores técnicos, quando usados por uma aplicação. |
| `psycopg2-binary` | Conexão opcional com PostgreSQL. |
| `python-dotenv` | Carregamento do `.env`. |

As versões declaradas estão em [pyproject.toml](D:\Dev\Python\Bankai\pyproject.toml).

## Estrutura do projeto

```text
.
├── app.py                    # Bootstrap Streamlit e resolução de ?app=
├── pyproject.toml            # Metadados e dependências Python
├── system/                   # Framework, sem regras de negócio dos apps
│   ├── core/
│   │   ├── applications/     # ApplicationDefinition e registry
│   │   ├── contexts/         # AppContext e contratos de estado
│   │   ├── infrastructure/   # Ambiente e infraestrutura compartilhada
│   │   ├── managers/         # Tema, estado, gráficos, banco e handlers
│   │   └── log/              # Alertas e logging
│   └── view/
│       ├── components/       # Cards, filtros, inputs, charts e layout
│       ├── styles/           # CSS genérico dirigido por tokens de tema
│       └── pages/            # Telas genéricas, como app inexistente
├── bankai/                   # Aplicação demonstrativa de análise de dados
│   ├── app.py                # Definição ApplicationDefinition
│   ├── layout.py             # Shell visual da aplicação
│   ├── routes.py             # Mapa declarativo de rotas e slots
│   ├── state.py              # Estado pertencente ao Bankai
│   ├── pages/                # Páginas e componentes específicos
│   ├── theme/                # base.json, light.json e dark.json
│   └── data/                 # Dados pertencentes ao app
├── athena/                   # Aplicação de planejamento de capacidade
│   ├── app.py
│   ├── layout.py
│   ├── routes.py
│   ├── state.py
│   ├── pages/
│   └── theme/
└── tests/                    # Testes de contrato do framework
```

O diretório histórico `apps/` não faz parte do padrão para novas aplicações.
O padrão atual é uma pasta de primeiro nível para cada app, como `bankai/` ou
`athena/`.

## Fluxo da aplicação

```text
Navegador (?app=athena)
          │
          ▼
app.py
  ├─ carrega .env
  ├─ importa athena.app
  ├─ obtém ApplicationDefinition
  ├─ cria/recupera AppContext e estado da sessão
  └─ injeta tokens/CSS do tema
          │
          ▼
athena.app.render(context)
          │
          ▼
athena.layout.render(context)
  ├─ resolve a rota atual
  ├─ renderiza o header compartilhado
  └─ chama renderer da página
          │
          ▼
athena.pages.<pagina>.render(context)
```

O bootstrap importa dinamicamente `<nome-do-app>.app`. Esse módulo deve expor
`get_application()`, retornando uma `ApplicationDefinition`. O registry valida
o contrato e evita registros duplicados.

### Estado

`AppContext` é técnico e compartilhado: contém nome do app, tema, modo,
largura da tela e uma referência ao estado do app. O estado de domínio não fica
no framework; cada aplicação fornece `state_factory`.

Para filtros e cliques em gráficos, o estado deve implementar o contrato de
filtro: `active_filters`, `update_filter()` e `remove_filter()`. Para eventos
de gráfico, também deve implementar `get_last_event_ts()` e
`set_last_event_ts()`.

### Tema e componentes

Cada app possui `theme/base.json` e ao menos um modo, como `theme/dark.json`.
O manager de tema combina os arquivos, aplica defaults do framework e valida o
contrato. Tokens são convertidos em variáveis CSS `--ui-*`; assim, cards,
inputs, navegação e gráficos mudam de aparência sem o framework conhecer a
identidade visual do app.

## Criando uma nova aplicação

O exemplo abaixo cria um app chamado `orion`, sem alterar o `system/` nem os
outros apps.

### 1. Crie a estrutura

```text
orion/
├── __init__.py
├── app.py
├── layout.py
├── routes.py
├── state.py
├── pages/
│   ├── __init__.py
│   └── home.py
└── theme/
    ├── base.json
    └── dark.json
```

### 2. Defina o estado do app

Em `orion/state.py`:

```python
from dataclasses import dataclass, field


@dataclass
class OrionState:
    current_route: str = "home"
    active_filters: dict[str, object] = field(default_factory=dict)
    _last_events: dict[str, int] = field(default_factory=dict)

    def navigate(self, route: str) -> None:
        self.current_route = route

    def update_filter(self, column: str, value: object, rerun: bool = True) -> bool:
        if self.active_filters.get(column) == value:
            return False
        self.active_filters[column] = value
        return True

    def remove_filter(self, column: str, rerun: bool = True) -> bool:
        return self.active_filters.pop(column, None) is not None

    def get_last_event_ts(self, column: str) -> int | None:
        return self._last_events.get(column)

    def set_last_event_ts(self, column: str, timestamp: int) -> None:
        self._last_events[column] = timestamp


def create_state(initial_route: str) -> OrionState:
    return OrionState(current_route=initial_route)
```

### 3. Declare uma página e as rotas

Em `orion/pages/home.py`:

```python
import streamlit as st


def render(context) -> None:
    sidebar, content = st.columns([1, 3])

    with sidebar:
        st.write("Filtros e controles laterais")

    with content:
        with st.container(height=800, border=False):
            st.title("Orion")
            st.write("Página inicial da aplicação.")
```

Em `orion/routes.py`:

```python
from dataclasses import dataclass
from collections.abc import Callable

from .pages import home


@dataclass(frozen=True)
class RouteDefinition:
    renderer: Callable


ROUTES = {
    "home": RouteDefinition(renderer=home.render),
}


def get_current_route(context):
    try:
        return ROUTES[context.state.current_route]
    except KeyError as exc:
        raise ValueError(f"Rota Orion não registrada: {context.state.current_route}") from exc
```

A rota conhece somente o renderer. Colunas, filtros, sidebar, altura e rolagem
são decisões explícitas da página, usando diretamente as primitivas do
Streamlit.

### 4. Componha o layout

Em `orion/layout.py`, renderize apenas o shell realmente compartilhado e
delegue toda a composição do conteúdo à página.

```python
from system.view.components.layout import header
from .routes import get_current_route


def render(context) -> None:
    route = get_current_route(context)
    header.draw(context=context, title="Orion", subtitle="Meu app")
    route.renderer(context)
```

Esse modelo evita CSS de posicionamento e permite que cada página escolha
livremente a quantidade e a proporção das colunas. Um
`st.container(height=800)` cria uma área rolável quando o conteúdo excede a
altura definida.

### 5. Exponha `ApplicationDefinition`

Em `orion/app.py`:

```python
from pathlib import Path

from system.core.applications import ApplicationDefinition
from system.core.managers.view import theme as theme_man
from .layout import render
from .state import create_state


APP_ROOT = Path(__file__).resolve().parent
THEME_DIRECTORY = APP_ROOT / "theme"


def load_theme(mode: str) -> dict:
    normalized_mode = mode.strip().lower()
    return theme_man.load(
        THEME_DIRECTORY / "base.json",
        THEME_DIRECTORY / f"{normalized_mode}.json",
    )


def get_application() -> ApplicationDefinition:
    return ApplicationDefinition(
        app_id="orion",
        title="Orion",
        initial_route="home",
        default_mode="dark",
        render=render,
        load_theme=load_theme,
        state_factory=create_state,
    )
```

### 6. Crie os temas e execute

Copie `bankai/theme/base.json` como ponto de partida. Preserve as chaves
exigidas pelo contrato de tema e altere cores, tipografia, assets, variantes de
card e demais tokens no JSON. Em seguida, execute:

```text
http://localhost:8501/?app=orion
```

Não é preciso registrar `orion` manualmente em uma lista central: o bootstrap
encontra `orion.app` pela convenção de diretórios.

## Testes

Os testes atuais verificam contratos de tema, layout, estado e preparação pura
de dados de gráficos:

```powershell
python -m unittest discover -s tests -p "test_theme_contract.py" -v
```

Para validação visual e de componentes ECharts, inicie o Streamlit no navegador
com a aplicação desejada.
