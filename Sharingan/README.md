# Sharingan

Dashboard de monitoramento antifraude com visualização 3D e uma API local de dados de propostas.

## Estrutura

- `frontend/`: aplicação React que renderiza o dashboard.
- `backend/`: API FastAPI que expõe os dados em `backend/data/dados_fraude.csv`.

As coordenadas de `dados_fraude.csv` são vinculadas a municípios de `backend/data/brasil.csv`.
Elas servem à visualização e não representam o endereço real dos clientes.

## Pré-requisitos

- Node.js 20 ou superior
- Python 3.12 ou superior

## Frontend

```bash
cd frontend
npm ci
npm run dev
```

O dashboard fica disponível em `http://localhost:5173`.

Comandos de validação:

```bash
npm run lint
npm run build
```

O comando de build executa a verificação de TypeScript antes de gerar os arquivos de produção em `frontend/dist`.

## Backend

```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

A API fica disponível em `http://localhost:8000`. A documentação interativa está em `http://localhost:8000/docs`.

Endpoints atuais:

- `GET /stats` ou `GET /dashboard/summary`
- `GET /propostas?limit=100`
- `GET /analytics`
- `GET /investigations?limit=30`

O frontend consome `/analytics` para os cards, gráficos e rankings. A leitura do
CSV está encapsulada em `backend/app/main.py::load_dataframe`; para migrar para
PostgreSQL, substitua essa função por consultas ao banco mantendo os contratos
dos endpoints.

Para mudar o endereço da API sem alterar código, crie `frontend/.env` a partir de
`frontend/.env.example` e defina `VITE_API_URL`.

## Coordenadas do mapa

Para vincular novamente as fraudes a municípios reais, execute no diretório `backend`:

```bash
python data/vincular_coordenadas_brasil.py
python data/vincular_coordenadas_brasil.py --check
python data/adicionar_datas_fraude.py
```

O processo é determinístico (seed padrão `20260726`) e adiciona `ibge`, `municipio`,
`uf` e `estado` a cada registro, além de substituir `lat` e `lng` pelas coordenadas
do município vinculado.

`adicionar_datas_fraude.py` cria a coluna `occurred_at`, distribuída entre
`01/01/2026` e a data de execução, para alimentar as análises temporais.

## Tema e cores

`frontend/src/constants/colors.ts` concentra as cores fixas e os temas disponíveis. O estado do tema e a troca de modo ficam em `frontend/src/context/ThemeContext.tsx`; os componentes usam o hook `frontend/src/context/useTheme.ts` diretamente, sem receber o tema por propriedades.

O Tailwind continua responsável por utilitários de layout e estilos estáticos. As cores que mudam ao trocar de tema são aplicadas em estilos dinâmicos para preservar a troca em tempo de execução.
