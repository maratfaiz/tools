# Higgsfield — генерация картинок/видео в Claude Code

Higgsfield — сервис генерации изображений, видео, 3D и аудио. В Claude Code есть два независимых способа им пользоваться, можно комбинировать.

## Способ 1 — MCP-инструменты (работают сразу, без установки)

Если в Claude Code подключён Higgsfield MCP-сервер (обычно так и есть по умолчанию), можно просто попросить словами: *«сделай картинку заката над городом»*, *«сделай видео как эта фотка оживает»* — Claude сам вызовет нужный инструмент. Ключевые MCP-инструменты:

| Инструмент | Что делает |
|---|---|
| `generate_image` / `generate_image_batch` | генерация картинок (одна или пачкой) |
| `generate_video` / `generate_video_batch` | генерация видео |
| `generate_audio` / `generate_audio_batch` | генерация звука/музыки |
| `generate_3d` | картинка → 3D модель (GLB) |
| `upscale_image` / `upscale_video` | апскейл до 2K/4K |
| `outpaint_image` | расширение картинки за края (uncrop) |
| `reframe` | смена соотношения сторон видео |
| `remove_background` | вырезка фона |
| `motion_control` | перенос движения на другой референс |
| `virality_predictor` | оценка виральности готового видео (хук, удержание внимания) |
| `show_generations` / `job_display` | посмотреть историю генераций |
| `balance` / `show_plans_and_credits` | баланс и тарифы |

Не нужен ни CLI, ни авторизация вручную — если MCP подключён, он уже авторизован под моим аккаунтом.

## Способ 2 — CLI + skills (для терминала / автономных агентов)

В этом репозитории (`.agents/skills/`, `.claude/skills/`) уже установлены skills-пакеты от `higgsfield-ai/skills`, которые учат Claude Code пользоваться CLI `higgsfield` (алиасы `higgs`, `hf`):

- **higgsfield-generate** — универсальная генерация: картинки, видео, 3D, аудио, Marketing Studio (рекламные ролики/креативы), Virality Predictor
- **higgsfield-brandkit** — полноценный брендбук: логотип, палитра, типографика, упаковка, вывески, презентация
- **higgsfield-product-photoshoot** — предметная/рекламная фотосъёмка товара (studio shot, lifestyle, hero-banner и т.д.)
- **higgsfield-marketplace-cards** — карточки товара под маркетплейсы (главное фото, доп. фото, A+ контент)
- **higgsfield-youtube-thumbnail** — превью для YouTube/Shorts
- **higgsfield-soul-id** — обучение «Soul» — персональной модели лица для генераций с сохранением внешности
- **higgsfield-video-explainer** — сборка озвученного объясняющего видео из блоков
- **higgsfield-websites** — сборка и деплой сайтов/приложений/игр через `higgsfield website …`

Как активировать эти skills в новой сессии Claude Code — они уже лежат в `.claude/skills/*`, Claude подхватывает их автоматически внутри этого репозитория.

Установка/настройка (уже сделана в этом окружении, но для справки на будущее — например, на своём ноутбуке):

```bash
npm i -g @higgsfield/cli       # ставим CLI
higgsfield auth login          # логин через браузер (нужен локальный браузер!)
npx skills add higgsfield-ai/skills   # ставим skills в текущий репозиторий
```

**Важно про `auth login`:** это OAuth-логин через браузер с обратным вызовом на `localhost` — он работает только там, где у тебя одновременно есть браузер и терминал (свой компьютер). Из облачной/удалённой сессии Claude Code (где нет своего браузера) залогинить CLI не получится — но это и не обязательно, для этого есть способ 1 (MCP), который уже авторизован.

Базовые команды CLI после логина:

```bash
higgsfield model list --video          # список видео-моделей
higgsfield model list --image          # список картиночных моделей
higgsfield workflow list               # список готовых воркфлоу
higgsfield generate create <model> --prompt "..." --wait   # генерация, дождаться результата
higgsfield generate list --json        # история генераций
higgsfield account status              # проверить, авторизован ли
```
