# tools

Личный репозиторий с инструментами, которыми я пользуюсь в работе. Подробная инструкция по каждому — отдельным файлом в [`docs/`](docs/).

| Инструмент | Что делает | Инструкция |
|---|---|---|
| **Higgsfield** | генерация картинок, видео, 3D, аудио прямо из Claude Code (MCP + CLI) | [docs/higgsfield.md](docs/higgsfield.md) |
| **ECC** | «операционная система» для Claude Code — 68 агентов, 286 skills, команды, rules, TDD-процесс | [docs/ecc.md](docs/ecc.md) |
| **Headroom** | сжимает контекст перед отправкой в LLM — меньше токенов, те же ответы | [docs/headroom.md](docs/headroom.md) |
| **Graphify** | превращает кодовую базу в граф знаний — запросы вместо grep | [docs/graphify.md](docs/graphify.md) |
| **styles.refero.design** | каталог из 2000+ дизайн-систем как референс для UI-работы | [docs/refero-design.md](docs/refero-design.md) |

Higgsfield, ECC и Graphify установлены прямо в этот репозиторий (`.claude/`, `.agents/`) и подхватываются автоматически при открытии его в Claude Code — подробности в соответствующем файле. Headroom — CLI-инструмент уровня машины (прокси/MCP), его нужно ставить и настраивать на своей машине отдельно, см. `docs/headroom.md`.
