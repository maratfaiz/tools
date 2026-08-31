# ECC (Engineering Control Center) — «операционная система» для Claude Code

[github.com/affaan-m/ECC](https://github.com/affaan-m/ECC) — большой open-source плагин-набор для Claude Code (и ещё 10+ других агентских харнессов, но заточен в первую очередь под Claude Code). Даёт готовый инженерный процесс `план → тесты → реализация → ревью → верификация → память → улучшение` вместо того, чтобы каждый раз объяснять это Claude заново.

**Работает с обычной подпиской на Claude** — это не отдельный API-сервис, а надстройка над самим `claude` CLI. Ключей/биллинга сверх того, что уже нужно Claude Code, не требует. Раздел "Self-Hosted Models" в их README про кастомные шлюзы — опционален, для тебя не актуален.

**Что внутри:** 68 сабагентов (planner, code-reviewer, security-reviewer, build-error-resolver и т.д.), 286 skills (TDD, security, frontend, data, ML, и т.д.), 94 команды-шорткаты, хуки (например блокирует опасные `rm`/`git checkout --force` до выполнения — GateGuard), и rules (всегда-загруженные стандарты по языку).

## Установлено прямо в этот репозиторий

ECC уже стоит здесь, project-local, под `.claude/` (профиль `developer`, таргет `claude-project` — официальный установщик ECC, не плагин-путь). Это значит: как только Claude Code открывает этот репозиторий, все агенты/skills/команды/rules из ECC подхватываются автоматически, ничего доустанавливать не нужно.

Что реально приехало (807 файлов): агенты (`.claude/agents/`), skills (`.claude/skills/`), команды (`.claude/commands/`), rules по всем языкам/фреймворкам (`.claude/rules/ecc/*` — common, typescript, python, golang, react, vue и т.д.), конфиг хуков (`.claude/hooks/`) и MCP-шаблоны (`.claude/mcp-configs/`).

**Важный нюанс про хуки:** файл `.claude/hooks/hooks.json` физически лежит в репозитории, но сам по себе Claude Code его не подхватывает — project-local `claude-project`-установка не регистрирует хуки как активный runtime (это отличие от установки через `/plugin`, где Claude Code 2.1+ грузит `hooks.json` автоматически по конвенции). То есть агенты/skills/команды/rules работают сразу, а автоматические проверки (блокировка опасных команд, автоформат после правок и т.д.) — нет. Если понадобятся именно они, это отдельный шаг с официальным установщиком на своей машине (`./install.sh --target claude --modules hooks-runtime`) — см. `.claude/hooks/README.md`.

## Установка на своей машине (если Claude Code у тебя работает не только здесь)

Этот репозиторий — временная облачная сессия, она удаляется. Чтобы ECC был у тебя постоянно (на ноутбуке), там нужно поставить его отдельно — либо рекомендуемым plugin-путём (2 команды прямо в Claude Code):

```
/plugin marketplace add https://github.com/affaan-m/ECC
/plugin install ecc@ecc
```

либо так же, как здесь — вручную скачать репозиторий и прогнать установщик:

```bash
git clone https://github.com/affaan-m/ECC.git
cd ECC
npm install
node scripts/install-apply.js --target claude --profile developer   # глобально в ~/.claude
# или --target claude-project, если хочешь project-local как здесь
```

Проверить версию Claude Code перед установкой (нужно 2.1.0+): `claude --version`.

## Как этим пользоваться каждый день

| Что делаю | Команда |
|---|---|
| Начать новую фичу | `/ecc:plan "описание фичи"`, затем skill `tdd-workflow` |
| Чиню баг | сначала пишу тест, который его воспроизводит, дальше `tdd-workflow` |
| Прошу проверить код | `/code-review` (ревью со «свежим» контекстом) |
| Чиню упавшую сборку | `/build-fix` |
| Чищу мёртвый код | `/refactor-clean` |
| Проверяю, не забит ли контекст | `/context-budget` |
| Заканчиваю долгую сессию | `/save-session` или `/learn-eval` |
| Продолжаю позже | `/resume-session` |
| Проверяю безопасность своих агент-конфигов | `/security-scan` или `npx -y ecc-agentshield scan --path .` |

Типичная цепочка на фичу:
```
/ecc:plan "Add user authentication with OAuth"   -> planner делает план реализации
tdd-workflow (skill)                              -> tdd-guide заставляет писать тесты сначала
/code-review                                      -> code-reviewer проверяет результат
```

## Важно по безопасности

Ставить ТОЛЬКО из официальных источников — сам GitHub-репозиторий `affaan-m/ECC`, npm-пакеты `ecc-universal`/`ecc-agentshield`, или их официальный GitHub App. Авторы прямо предупреждают: сторонние зеркала/копии могут содержать вредоносный код.

## Если что-то пошло не так

```bash
node scripts/ecc.js doctor      # диагностика
node scripts/ecc.js repair      # почини
node scripts/uninstall.js --dry-run   # что удалится
node scripts/uninstall.js       # удалить
```
