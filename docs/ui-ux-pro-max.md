# UI UX Pro Max — дизайн-интеллект для интерфейсов

## Что это простыми словами

Без этого skill'а, если попросить Claude «сделай лендинг», он обычно выдаёт узнаваемый «AI-шаблон»: центрированный хиро-блок, фиолетово-розовый градиент, карточки с одинаковыми отступами — то, что сразу видно как «сгенерировано нейросетью», не зависимо от того, для банка это лендинг или для спа-салона.

**Конкретный пример разницы.** Просишь «сделай лендинг для спа-салона»:
- **Без skill'а:** типовой SaaS-стиль — синие кнопки, градиенты, бодрый шрифт — как будто это лендинг для стартапа, а не для спа.
- **С skill'ом:** Claude сначала смотрит в базу под тип продукта «spa/wellness» и получает готовую рекомендацию — например мягкую розово-салатовую палитру, элегантный serif-шрифт (Cormorant Garamond), паттерн «Hero → Услуги → Отзывы → Запись», плюс список того, чего для этой индустрии делать НЕ надо (никаких резких неоновых цветов и агрессивных анимаций) — и уже по этой рекомендации пишет код.

То есть это не генератор дизайна с нуля, а «насмотренность» — база данных реальных дизайн-паттернов и правил, которую Claude использует вместо того, чтобы придумывать стиль наугад.

[github.com/nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) — skill для Claude Code, который добавляет «дизайнерский мозг» при вёрстке интерфейсов: вместо дефолтного шаблонного UI Claude подбирает стиль, палитру, типографику и паттерн лендинга под конкретный тип продукта, опираясь на локальную базу данных (без обращений в сеть).

**Работает полностью локально и бесплатно.** Никаких API-ключей и обращений в интернет — вся база (стили, палитры, шрифты, UX-гайдлайны) лежит в CSV/JSON внутри skill'а, поиск по ней делает Python (только стандартная библиотека). Подходит под обычную подписку на Claude — это просто справочные данные + инструкция, ничего не генерирует само по себе.

## Что внутри

- **79 UI-стилей** (50 активных) — Glassmorphism, Claymorphism, Neumorphism, Brutalism, Bento Grid, AI-Native UI и т.д.
- **192 индустриальных reasoning-правила** — под конкретный тип продукта (SaaS, фудтех, фитнес-трекер, банкинг...) сразу даёт: паттерн лендинга, приоритет стиля, палитру, типографику, эффекты и anti-patterns («чего не делать для этой индустрии»)
- **192 цветовые палитры**, **74 пары шрифтов**, **119 UX-гайдлайнов** (доступность, устойчивая вёрстка текста), **25 типов графиков**, **22 стека** (React, Vue, Next.js, SwiftUI, Flutter, Jetpack Compose, HTML+Tailwind и др.)

Есть платная Premium-версия (брендинг, логотипы, презентации, генерация реальных визуалов) — но то, что установлено здесь, это полностью открытая базовая версия, ничего доплачивать не нужно.

## Что установлено сейчас

CLI `uipro` (npm-пакет `ui-ux-pro-max-cli`) поставлен глобально, skill зарегистрирован **project-local** прямо в этот репозиторий:

```bash
npm install -g ui-ux-pro-max-cli
uipro init --ai claude   # выполнено в /home/user/tools
```

Что реально приехало в `.claude/skills/`:

- **ui-ux-pro-max** — основной skill с базой данных и reasoning-движком
- **ui-styling** — вёрстка на shadcn/ui + Tailwind, доступные компоненты, тёмная тема
- **brand** — брендовый голос, визуальная идентичность, гайдлайны консистентности
- **banner-design** — баннеры для соцсетей/рекламы/хиро-секций
- **slides** — HTML-презентации с Chart.js и дизайн-токенами
- **design** — общий дизайн-скилл

Всё это коммитится в git и подхватывается автоматически, как только Claude Code открывает `maratfaiz/tools`.

## Как этим пользоваться

**Просто попроси словами** — skill активируется сам на запросы по UI/UX:

```
Сделай лендинг для SaaS-продукта
Собери дашборд для медицинской аналитики
Спроектируй портфолио-сайт с тёмной темой
Сделай мобильный UI для e-commerce
```

Дальше Claude сам: подбирает паттерн страницы + стиль + палитру + типографику под тип продукта → пишет код под нужный стек → проверяет по чек-листу анти-паттернов (никаких emoji вместо иконок, контраст текста 4.5:1, `prefers-reduced-motion`, отзывчивая вёрстка на 375/768/1024/1440px и т.д.)

## Прямой доступ к поисковому движку (продвинутое использование)

Если нужно руками, без обращения через диалог:

```bash
# Сгенерировать целую дизайн-систему под продукт
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness" --design-system -p "Serenity Spa"
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "fintech banking" --design-system -f markdown

# Точечный поиск по одной области
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "glassmorphism" --domain style
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "elegant serif" --domain typography
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "dashboard" --domain chart
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "error summary validation" --domain ux

# Гайдлайны под конкретный стек
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "form validation" --stack react
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "responsive layout" --stack html-tailwind
```

## Сохранение дизайн-системы между сессиями (Master + Overrides)

Чтобы не пересчитывать дизайн-систему заново на каждой странице проекта:

```bash
# Сгенерировать и сохранить как источник правды для проекта
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "SaaS dashboard" --design-system --persist -p "MyApp"

# Плюс override под конкретную страницу
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "SaaS dashboard" --design-system --persist -p "MyApp" --page "dashboard"
```

Создаёт:
```
design-system/myapp/
├── MASTER.md           — общий источник правды (цвета, типографика, компоненты)
└── pages/dashboard.md  — только отличия для конкретной страницы
```

При работе над страницей Claude сначала проверяет `pages/<страница>.md` (если есть — эти правила побеждают), иначе берёт `MASTER.md` целиком.

## На своей машине / другом проекте

```bash
npm install -g ui-ux-pro-max-cli
cd /путь/к/проекту
uipro init --ai claude          # Claude Code, project-local
uipro init --ai claude --global # либо глобально в ~/.claude/skills/ — сразу для всех проектов
uipro init --ai cursor          # тот же skill для Cursor, Windsurf, Codex CLI и ещё 15+ инструментов — см. README репозитория
```

Обновить / удалить:
```bash
uipro update             # обновить установленный skill до последней версии
uipro uninstall          # удалить (автоопределение платформы)
uipro uninstall --global # удалить глобальную установку
```

Требование — Python 3.x (только стандартная библиотека, ничего не ставит и никуда не стучится по сети), проверить: `python3 --version`.
