# Graphify — превращает кодовую базу в граф знаний вместо grep

[github.com/Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) — CLI + skill, который сканирует проект (код, доки, PDF, картинки, видео) и строит из него граф знаний: концепции-узлы и связи между ними (`calls`, `imports`, `inherits`, `references`...). Дальше вместо того, чтобы гонять Claude по файлам через grep/чтение, ему задают вопрос по графу — быстрее и в разы меньше токенов.

**Код разбирается полностью локально** — через tree-sitter (AST), без LLM, ничего никуда не уходит. Доки/PDF/картинки/видео проходят «семантический проход» моделью — но **работает прямо на модели текущей сессии Claude Code, отдельный API-ключ не нужен**. Headless-режим (`graphify extract` из терминала без открытого Claude Code) тоже поддерживает бэкенд `claude` через обычный `claude` CLI — то есть через твою подписку, без `ANTHROPIC_API_KEY`.

## Что установлено сейчас

- CLI `graphify` (пакет `graphifyy` на PyPI, команда — `graphify`) стоит в этом окружении: `uv tool install graphifyy`.
- Skill зарегистрирован **project-local** прямо в этот репозиторий: `graphify install --project`. Это значит — коммитится в git и работает у всех, кто откроет `maratfaiz/tools` в Claude Code, без переустановки.

Что реально приехало:
- `.claude/skills/graphify/SKILL.md` + `references/` — сам skill (реагирует на `/graphify`)
- `.claude/settings.json` — добавлен `PreToolUse`-хук (`graphify hook-guard`), который до поиска по Bash/Grep и до чтения файлов через Read/Glob подсказывает Claude сначала свериться с графом, если он уже построен
- `CLAUDE.md` (корень) и `.claude/CLAUDE.md` — инструкция для Claude: если есть `graphify-out/graph.json`, сначала `graphify query`, а не грепать сырые файлы

**Граф пока не построен** — это отдельный шаг, сознательно не сделан молча (создаёт новую папку `graphify-out/` с файлами, которые имеет смысл коммитить только осознанно). Строится командой ниже, когда решишь, что нужно.

## Как построить граф

В любой сессии Claude Code внутри репозитория, который хочешь разобрать:

```
/graphify .
```

Получаешь три файла в `graphify-out/`:

```
graphify-out/
├── graph.html       открывается в браузере — кликабельные узлы, фильтры, поиск
├── GRAPH_REPORT.md  главное: ключевые концепции, неожиданные связи, вопросы-подсказки
└── graph.json        сам граф — по нему потом идут все запросы
```

Полезные варианты:

```
/graphify ./docs --update          # переразобрать только изменённые файлы
/graphify . --cluster-only         # пересчитать кластеры без переразбора
/graphify . --no-viz               # без HTML, только отчёт + json
/graphify . --wiki                 # собрать markdown-wiki из графа
```

## Как этим пользоваться после того, как граф есть

Вместо «прочитай эти 20 файлов» — спрашиваешь граф:

```
/graphify query "что связывает авторизацию с базой данных?"
/graphify path "UserService" "DatabasePool"
/graphify explain "RateLimiter"
```

- `query "<вопрос>"` — возвращает нужный кусок графа под вопрос
- `path "A" "B"` — кратчайший путь между двумя концепциями, по шагам
- `explain "X"` — все связи одного узла, откуда взят, с чем соединён

Каждая связь помечена `EXTRACTED` (буквально видно в исходнике) или `INFERRED` (вывел graphify) — понятно, что найдено напрямую, а что — предположение.

Добавить внешний материал в граф:

```
/graphify add https://arxiv.org/abs/1706.03762   # статья
/graphify add <youtube-ссылка>                    # видео (транскрибируется локально)
```

## Поддержание графа в актуальном состоянии

Одна команда один раз после клонирования репозитория — дальше три обычные git-команды сами держат граф свежим:

```bash
graphify hook install   # один раз: ставит git-хуки + merge-driver для graph.json
```

| Делаешь | Что происходит |
|---|---|
| `git commit` | граф пересобирается сам (только AST, без API-затрат) |
| `git checkout` / `git switch` | граф пересобирается сам |
| `git pull` / `git merge` | нужно руками: `graphify update .` |
| `git push` | ничего делать не нужно |

Совет из их README — алиас, чтобы не забывать про пункт с `pull`:
```bash
git config --global alias.gpull '!git pull && graphify update .'
```

## Файлы графа и git

`graphify-out/` создатели советуют коммитить в репозиторий — тогда у всех, кто клонирует, граф уже готов, не нужно ждать пересборки. Кроме `graphify-out/cost.json` (чисто локальный, в `.gitignore`).

## Игнор-файлы

`.gitignore` учитывается автоматически. Если нужно исключить что-то ещё — `.graphifyignore` в корне, синтаксис как у `.gitignore`:

```
node_modules/
dist/
*.generated.py
```

## MCP-сервер (если нужен доступ к графу из другого инструмента)

```bash
python -m graphify.serve graphify-out/graph.json                    # локально, по одному на разработчика
python -m graphify.serve graphify-out/graph.json --transport http --port 8080   # общий на всю команду
```

Даёт инструменты `query_graph`, `get_node`, `get_neighbors`, `shortest_path`, `list_prs`, `get_pr_impact`, `triage_prs`.

## На других платформах / другой машине

```bash
uv tool install graphifyy      # или: pipx install graphifyy
graphify install               # регистрирует skill в свой профиль (~/.claude вместо project-local)
```

Работает также в Cursor, Codex, Gemini CLI, GitHub Copilot и 15+ других — команда `graphify install --platform <имя>`, полный список в README репозитория.

## Приватность

- Код — только локально (tree-sitter), без сети вообще.
- Видео/аудио — локальная транскрипция (faster-whisper), без сети.
- Доки/PDF/картинки — уходят в модель текущей сессии Claude Code (или в указанный API-ключ при headless-запуске). Телеметрии и трекинга нет.
