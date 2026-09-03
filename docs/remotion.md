# Remotion — видео из кода (React)

[remotion.dev](https://www.remotion.dev) — библиотека и CLI, которые позволяют делать видео на React: пишешь обычные компоненты, а Remotion покадрово рендерит их в MP4. Это принципиально другой подход, чем у Higgsfield (`docs/higgsfield.md`) — там видео генерирует AI по промпту, здесь ты контролируешь каждый пиксель и каждый кадр кодом. Хорошо подходит для: субтитров/капшенов, шаблонных видео с динамическими данными (например, персонализированные ролики из CSV), дата-визуализаций в движении, программных анимаций.

**Никакого API-ключа не нужно** — это чистая JS/React-библиотека, рендерит локально на твоей машине (или в облаке, см. ниже — опционально). Никак не завязана на Claude/Anthropic/другие AI-провайдеры.

**Лицензия:** бесплатно для команд до 3 человек и для личного использования; если у тебя компания больше — нужна отдельная лицензия ([подробности](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md)).

## Что установлено сейчас

Готовый стартовый проект (`--blank` шаблон) лежит в папке [`remotion/`](../remotion) этого репозитория:

```bash
cd remotion
npm i          # уже сделано при установке
```

Проверено реальным рендером — `npx remotion render` собрал рабочий `out/MyComp.mp4` (88.6 kB, 60 кадров @ 30fps). `node_modules` и `out/` в `.gitignore`, в git попадает только сам проект (исходники, конфиг).

## Структура проекта

```
remotion/
├── src/
│   ├── Root.tsx          — реестр композиций (какие видео вообще есть)
│   ├── Composition.tsx   — сама композиция + React-компонент, который рендерится
│   └── index.ts          — точка входа
├── public/                — статика (картинки, шрифты, музыка)
└── remotion.config.ts     — конфиг рендера
```

Одна композиция — это `<Composition id="..." component={...} durationInFrames={...} fps={...} width={...} height={...} />` в `Root.tsx`. Можно завести сколько угодно композиций — разные видео в одном проекте.

## Как этим пользоваться

**1. Визуальный превью-редактор (Remotion Studio) — открывается в браузере:**

```bash
cd remotion
npm run dev
```

Живой предпросмотр с таймлайном — правишь `src/Composition.tsx`, видишь изменения сразу.

**2. Рендер готового видео:**

```bash
npx remotion render                    # рендерит первую композицию
npx remotion render MyComp out/final.mp4   # конкретная композиция → конкретный файл
```

**3. Рендер одного кадра (картинка вместо видео):**

```bash
npx remotion still MyComp out/frame.png
```

**4. Посмотреть, какие композиции есть в проекте:**

```bash
npx remotion compositions
```

**5. Обновить Remotion до последней версии:**

```bash
npx remotion upgrade
```

## Как писать сам ролик

Правишь `src/Composition.tsx` — это обычный React-компонент. Главное отличие от веб-React: время. Хук `useCurrentFrame()` даёт номер текущего кадра, из него считаешь анимацию:

```tsx
import { useCurrentFrame, interpolate } from "remotion";

export const MyComponent: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1]); // фейд-ин за первые 30 кадров

  return <div style={{ opacity }}>Привет из Remotion</div>;
};
```

Дальше — обычный React: пропсы, стейт (для статичных значений, не для анимации кадра), любые библиотеки. Данные (CSV/JSON) можно подключать через `calculateMetadata` в `Composition.tsx`, чтобы генерировать разное число кадров/разный контент под разные данные — это основа для «пачки персонализированных видео».

## Если понадобится рендер в облаке (Google Cloud Run)

Изначально вопрос был про это — если решишь рендерить не локально, а в GCP (для больших объёмов/масштабирования), ставится отдельным пакетом внутрь этого же проекта:

```bash
cd remotion
npx remotion add @remotion/cloudrun
```

Дальше нужен отдельный **GCP-проект с включённым биллингом**:

```bash
gcloud auth application-default login
npx remotion cloudrun services deploy   # разворачивает Cloud Run сервис
npx remotion cloudrun sites create      # выкладывает проект в Cloud Storage
npx remotion cloudrun render <serve-url> <composition-id>
```

⚠️ Это отдельная инфраструктура с отдельным биллингом на стороне Google — не делается по умолчанию, статус этой фичи у Remotion сейчас **Alpha**. Локальный рендер (`npx remotion render`) для большинства задач достаточен и ничего этого не требует.

## Документация

- [remotion.dev/docs/the-fundamentals](https://www.remotion.dev/docs/the-fundamentals) — с чего начать
- [remotion.dev/docs/cli](https://www.remotion.dev/docs/cli) — все команды CLI
- [Discord](https://discord.gg/6VzzNDwUwV) — помощь от сообщества
