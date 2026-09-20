# Phoenix Security Skills — AppSec-ревью, SAST-правила, threat intel

## Что это простыми словами

Без этого набора, если попросить Claude «проверь код на безопасность», он делает это по наитию — смотрит на глаз, может пропустить что-то специфичное для языка, не даёт структурированного вердикта. Это набор из 27 skills от [Security-Phoenix-demo/security-skills-claude-code](https://github.com/Security-Phoenix-demo/security-skills-claude-code) (компания Phoenix Security), которые превращают Claude в security-инженера с чёткими чек-листами под 7+ языков, готовыми SAST-правилами, поиском по 595 источникам threat intelligence и двумя «шлюзами» — «готов ли план» и «готов ли код к продакшену».

**Конкретный пример разницы.** Просишь «проверь этот PR на безопасность перед мержем»:
- **Без skill'а:** Claude читает диф, называет пару очевидных вещей (может быть SQL-инъекция, вроде норм), без структуры и без гарантии, что прошёлся по всем классам уязвимостей.
- **Со skill'ом `security-reviewer`:** Claude грузит чек-лист именно под язык твоего кода (отдельные référence-файлы под Python/JS-TS/Go/Java/Rust/Ruby/.NET), проходит по 8-пунктовому чеку OWASP/ASVS, и по каждой находке даёт: severity, файл:строка, категория, доказательство, конкретный фикс.

**Работает с обычной подпиской на Claude.** Большинство skills не требуют ключей — используют веб-поиск и рассуждения самого Claude. Исключение — расширенные интеграции (например пуш в NotebookLM, поиск через отдельный Brave API вместо встроенного поиска Claude) — они опциональны, базовая функциональность работает без них.

## Что установлено сейчас

Скопированы все 27 skills из всех 6 плагинов репозитория напрямую в `.claude/skills/` — это официально задокументированный в самом репозитории способ ручной установки («Copying a single skill instead»), не через `/plugin marketplace`. Коммитится в git, работает сразу при открытии `maratfaiz/tools` в Claude Code.

**Что сознательно НЕ скопировано и почему:**
- **Слэш-команды и сабагент** (`/security-review`, `/threatmodel`, `security-reviewer` agent) — они написаны под настоящую plugin-установку (ссылаются на переменную `${CLAUDE_PLUGIN_ROOT}`, которая существует только внутри реального `/plugin install`) и полезны просто как явные ярлыки. Skills при этом работают полностью сами по себе — Claude активирует их по описанию, без слэш-команды.
- **Агент `security-reviewer`** отдельно — под этим именем уже есть агент от ECC (`docs/ecc.md`), переустановка затёрла бы его. Skill `security-reviewer` (не агент) установлен и работает.
- **Node CLI + MCP-сервер** для `cti-domain-research` (нужен для отдельной команды `/cti-search` вне диалога) — сам skill внутри диалога Claude Code использует обычный веб-поиск Claude по встроенному списку из 595 доменов, CLI для этого не нужен.
- **Активные хуки** (блокировка опасных Bash-команд, авто-скан после правок) — opt-in даже в официальной установке, требуют отдельного шага на своей машине.

## Что внутри — по категориям

### Ревью кода (реагируют на «проверь код», «есть уязвимости?», «security review»)

| Skill | Когда использовать |
|---|---|
| `security-reviewer` | Стандартное пре-мерж ревью — новый эндпоинт, изменения в auth, работа с внешним HTTP. 7 языковых référence-паков (Python, JS/TS, Go, Java/Kotlin, Rust, Ruby, .NET) |
| `security-assessment` | Полный прогон по всему репозиторию — OWASP Top 10 2025 + ASVS Level 1 |
| `0day-scanner` | Точечный анализ одного коммита/PR/файла/ветки на новые уязвимости |
| `threat-modeling` | STRIDE + DREAD модель угроз из архитектуры кода |
| `tm-quick-security-assessment` | Быстрый пре-мерж проход — только то, что изменилось в ветке |
| `tm-security-review` | Максимально глубокий — полная модель угроз + тройной проход (найти → проверить → подтвердить эксплойт) с рабочим PoC |

### Готовность к продакшену (два «шлюза»)

| Skill | Вопрос, на который отвечает | Вердикт |
|---|---|---|
| `plan-readiness-review` | Сможет ли другой senior-инженер реализовать этот план/PRD, ничего не выдумывая? | READY / NOT READY |
| `production-readiness-review` | Код реально написан, подключён, протестирован и безопасен для деплоя? | SHIP / NO-SHIP |

Оба честно помечают: `VERIFIED` (проверено), `GAP` (пробел), `UNVERIFIABLE` (нельзя проверить) — никогда не выдумывают процент готовности из воздуха.

### Генерация SAST-правил

| Skill | Когда использовать |
|---|---|
| `opengrep-rule-generator` | Написать opengrep/semgrep правило (pattern или taint-режим) под 30+ языков |
| `opengrep-rule-generator-research` | То же самое, но сначала исследует конкретную CVE/CWE через веб-поиск, потом пишет правило под неё |

### Threat intelligence и research

| Skill | Когда использовать |
|---|---|
| `cti-domain-research` | Поиск по 595 источникам threat intel (BleepingComputer, Krebs, CISA, Unit42, Mandiant...) под конкретную CVE/актора/малварь |
| `notebooklm` | Задать вопрос своим Google NotebookLM ноутбукам — ответы строго по источникам, без галлюцинаций |
| `phoenix-research-pipeline` | Автоматический поиск по YouTube/вебу/Reddit под тему, с пушем в NotebookLM |

### Security-first PRD (11-ролевый пайплайн)

Одна связанная цепочка ролей — от сырых заметок до готового к разработке спека с threat-моделью:

```
phoenix-context-curator → phoenix-scope-cutter → phoenix-constraint-distiller
→ phoenix-requirements-engineer ⇄ phoenix-ambiguity-hunter → phoenix-security-engineer
→ phoenix-contract-architect → phoenix-verification-matrix → phoenix-batch-planner
→ phoenix-final-gate
```

- **`phoenix-orchestrator`** — запускает всю цепочку сразу от сырых заметок до готового PRD
- **`phoenix-pipeline-navigator`** — если не знаешь, с какой роли начать, спрашивает и направляет
- **`prd-generator`** — быстрый одношаговый вариант: сразу полный security-focused PRD из одного описания фичи, без прохода по всем 11 ролям

### Документация проекта

| Skill | Когда использовать |
|---|---|
| `project-documenter` | Сгенерировать пакет документации проекта — от README до архитектурных карт, 5 режимов (от экспресс до полного пакета) |

## Как этим пользоваться

Просто формулируй задачу словами — skills активируются сами:

```
Проверь этот код перед мержем на безопасность
Прогони полный security-аудит по всему репозиторию
Проверь, нет ли новых уязвимостей в последнем коммите
Построй модель угроз для этого сервиса
Готов ли этот PR к продакшену?
Готов ли этот план к реализации, или в нём дыры?
Напиши semgrep-правило для обнаружения этой уязвимости
Найди, что говорят вендоры про CVE-2025-XXXXX
Сделай PRD для фичи X с учётом безопасности
```

## Полная версия на своей машине (командные ярлыки, хуки, CTI CLI)

Установленного здесь достаточно для использования skills в диалоге. Если хочется ещё и `/security-review`, `/threatmodel`, автоматические хуки (блокировка опасных команд, авто-скан после правок) и отдельный `/cti-search` из терминала — на своей машине ставится полноценно через официальный plugin-путь:

```
/plugin marketplace add Security-Phoenix-demo/security-skills-claude-code
/plugin install phoenix-security-review@phoenix-security
/plugin install phoenix-readiness-reviews@phoenix-security
/plugin install phoenix-sast-rules@phoenix-security
/plugin install phoenix-cti-search@phoenix-security
/plugin install phoenix-prd-pipeline@phoenix-security
/plugin install phoenix-docs-research@phoenix-security
```

Ставить только то, что реально нужно — каждый плагин независим. Требования: Node.js 18+ для плагинов; поисковый API-ключ (Brave, есть бесплатный тариф) нужен только для расширенных сценариев вроде `/cti-search` из терминала — сами skills внутри Claude Code используют встроенный веб-поиск и ключа не требуют.

## Важно по безопасности

Ставить только из официального источника — `Security-Phoenix-demo/security-skills-claude-code` (репозиторий с открытым исходным кодом от Phoenix Security, MIT-лицензия).
