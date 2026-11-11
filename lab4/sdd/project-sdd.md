# Описание дизайна программного обеспечения

Для проекта «SVS-RVC — синтез поющего голоса»

Версия 0.1

Подготовила Ананьева Т.М., группа 450501

БГУИР, кафедра ЭВМ

11.11.2026

## Оглавление

* [1. Введение](#1-введение)
  * [1.1 Назначение документа](#11-назначение-документа)
  * [1.2 Область применения](#12-область-применения)
  * [1.3 Определения, акронимы и сокращения](#13-определения-акронимы-и-сокращения)
  * [1.4 Ссылки](#14-ссылки)
  * [1.5 Обзор документа](#15-обзор-документа)
* [2. Обзор дизайна](#2-обзор-дизайна)
  * [2.1 Задачи стейкхолдеров](#21-задачи-стейкхолдеров)
  * [2.2 Выбранные точки зрения](#22-выбранные-точки-зрения)
* [3. Проектные представления](#3-проектные-представления)
  * [3.1 Приоритеты функционала](#31-приоритеты-функционала)
  * [3.2 DV-001 Контекст](#32-dv-001-контекст)
  * [3.3 DV-002 Композиция](#33-dv-002-композиция)
  * [3.4 DV-003 Интерфейс](#34-dv-003-интерфейс)
  * [3.5 DV-004 Взаимодействие](#35-dv-004-взаимодействие)
  * [3.6 DV-005 Динамика состояний](#36-dv-005-динамика-состояний)
  * [3.7 DV-006 Зависимости](#37-dv-006-зависимости)
* [4. Решения](#4-решения)
* [5. Приложения](#5-приложения)

## История изменений

| Name | Date | Reason For Changes | Version |
|------|------|--------------------|---------|
| Ананьева Т.М. | 11.11.2026 | Первоначальная редакция SDD на основе SRS v0.2 | 0.1 |

## 1. Введение

### 1.1 Назначение документа

Документ описывает **как** устроена система SVS-RVC: её границы, компонентный состав, интерфейсы, сценарии взаимодействия, состояния и зависимости. SDD предназначен для разработчиков, архитектора, тестировщиков и сопровождающего персонала. Он служит руководством при реализации MVP, основой для оценки трудозатрат и плана итераций, а также источником трассировки от требований SRS к элементам дизайна.

### 1.2 Область применения

SVS-RVC — Windows-приложение для синтеза вокальной партии по MIDI-партитуре и тексту с переносом тембра RVC. В область проектирования входят:

* импорт MIDI и лирики, привязка слогов к нотам;
* выбор и проверка локальных RVC-моделей;
* офлайн-синтез и перенос тембра;
* прослушивание, экспорт WAV/FLAC и сохранение файла;
* real-time-мониторинг с задержкой не более 250 мс;
* локальное хранение проектов, моделей и настроек.

Вне области проектирования остаются: обучение SVS- и RVC-моделей, облачные сервисы, интеграция с DAW через плагин, система лицензирования голосовых моделей, установщик и инфраструктура выпуска. Они описаны в документах уровня приложения либо запланированы на следующие релизы.

Проект реализует требования SRS v0.2 [`lab3/srs/srs-svs-rvc.md`](../../lab3/srs/srs-svs-rvc.md) и реестра [`lab3/srs/req-svs-rvc.md`](../../lab3/srs/req-svs-rvc.md).

### 1.3 Определения, акронимы и сокращения

| Term | Definition |
|------|------------|
| SVS | Singing Voice Synthesis — синтез поющего голоса |
| RVC | Retrieval-based Voice Conversion — перенос тембра голоса |
| F0 | Основная частота голоса (мелодия), Гц |
| MIDI | Musical Instrument Digital Interface; файл SMF 0/1 с нотами и длительностями |
| ONNX | Open Neural Network Exchange — формат переносимых нейросетевых моделей |
| ONNX Runtime | Кроссплатформенный движок вывода ONNX-моделей |
| HuBERT / ContentVec | Модели извлечения лингвистических признаков для RVC |
| DAW | Digital Audio Workstation — цифровая звуковая станция |
| WAV / FLAC | Форматы аудиофайлов без потерь |
| MVP | Minimum Viable Product — минимально жизнеспособный продукт |
| SRS | Software Requirements Specification — спецификация требований |
| SDD | Software Design Description — описание дизайна ПО |
| ADR | Architectural Decision Record — протокол архитектурного решения |
| REQ | Requirement — идентификатор требования |
| BR | Business Requirement — бизнес-требование |

### 1.4 Ссылки

| # | Ссылка | Тип |
|---|--------|-----|
| 1 | SRS v0.2 — [`lab3/srs/srs-svs-rvc.md`](../../lab3/srs/srs-svs-rvc.md) | Нормативная |
| 2 | Реестр требований — [`lab3/srs/req-svs-rvc.md`](../../lab3/srs/req-svs-rvc.md) | Нормативная |
| 3 | ADR-001 — [`lab4/adr/project-adr.md`](../adr/project-adr.md) | Нормативная |
| 4 | ISO/IEC/IEEE 42010:2022 — архитектурное описание | Справочная |
| 5 | ISO/IEC/IEEE 29148:2018 — инженерия требований | Справочная |
| 6 | MIDI 1.0 Specification | Справочная |
| 7 | Документация Qt 6 Widgets | Справочная |
| 8 | Документация ONNX Runtime | Справочная |
| 9 | Мокапы интерфейса — [`lab3/mockups/`](../../lab3/mockups/) | Информационная |

### 1.5 Обзор документа

Раздел 2 описывает задачи стейкхолдеров и выбранные точки зрения. Раздел 3 содержит шесть проектных представлений DV-001…DV-006 с трассировкой на требования SRS и приоритетами функционала от 10 до 50. Раздел 4 фиксирует архитектурное решение ADR-001. Раздел 5 содержит матрицу трассировки, план итераций и описание форматов данных. История изменений ведётся в таблице выше.

## 2. Обзор дизайна

### 2.1 Задачи стейкхолдеров

| Стейкхолдер | Основной интерес | Чем адресуется |
|-------------|------------------|----------------|
| Композитор / продюсер | Быстро получить черновик вокальной партии и выгрузить его в DAW | DV-002, DV-003, DV-004, DV-005 |
| Заказчик / слушатель | Естественный тембр, разборчивость текста, отсутствие артефактов | DV-001, DV-004, DV-005 |
| Владелец голоса | Контроль использования модели, локальная обработка без облака | ADR-001, DV-001, DV-006 |
| Разработчики | Понятная декомпозиция, заменяемость моделей и компонентов, тестируемость | DV-002, DV-003, DV-006 |
| QA | Воспроизводимые проверки, граничные случаи, измеримая задержка | DV-003, DV-004, DV-005 |
| Сопровождение | Стабильная сборка под Windows, минимум внешних зависимостей | DV-002, DV-006 |

### 2.2 Выбранные точки зрения

| Точка зрения | Что адресует | Представление |
|--------------|--------------|---------------|
| **Context** | Границы системы, внешние акторы, предоставляемые сервисы | DV-001 |
| **Composition** | Крупные компоненты и их организация | DV-002 |
| **Interface** | Контракты между компонентами и форматы данных | DV-003 |
| **Interaction** | Сценарии выполнения, включая пути отказа | DV-004 |
| **State Dynamics** | Состояния приложения, рендера, модели и real-time-режима | DV-005 |
| **Dependency** | Направленные связи «использует / требует» | DV-006 |

Точки зрения Physical, Logical, Information, Algorithm, Concurrency, Patterns, Deployment, Resources и Structure в данном SDD не детализируются: для MVP-приложения они либо покрываются перечисленными представлениями, либо не влияют на архитектурные решения. Например, алгоритм синтеза раскрывается в ADR-001 и DV-004, а вопросы развёртывания сводятся к переносимой Windows-сборке.

## 3. Проектные представления

### 3.1 Приоритеты функционала

Приоритеты определены совместно с заказчиком по шкале от 10 (наивысший) до 50 (минимальный). Идентификаторы требований сохранены, формулировки приведены на русском языке.

| Приоритет | Требование | Функциональность |
|-----------|------------|------------------|
| 10 | REQ-FUNC-001 | Импорт MIDI-партитуры и лирики; автоматическая привязка слогов к нотам |
| 10 | REQ-FUNC-003 | Синтез вокальной партии и перенос выбранного тембра RVC |
| 20 | REQ-FUNC-004, REQ-FUNC-005, REQ-SEC-001 | Экспорт WAV/FLAC, сохранение в выбранный каталог, локальная обработка |
| 30 | REQ-FUNC-002 | Выбор, проверка и управление локальными RVC-моделями |
| 40 | REQ-REL-001 | Надёжный аудиовыход и корректная обработка граничных случаев |
| 50 | REQ-PERF-001 | Real-time-мониторинг с задержкой не более 250 мс |

Приоритеты 10 и 10 означают, что импорт и синтез образуют минимальный сквозной сценарий: без любого из них продукт не создаёт ценности. Экспорт (20) необходим для передачи результата в DAW. Управление моделями (30) важно, но может быть реализовано на готовой библиотеке. Надёжность (40) и real-time (50) повышают качество, но не блокируют первый рабочий инкремент.

При сроке 10 рабочих дней и одном исполнителе приоритет 50 не помещается в MVP. По согласованию с заказчиком real-time перенесён в версию 1.1 и зафиксирован как следующий приоритет; архитектура функции при этом описана в DV-004 и DV-005.

### 3.2 DV-001 Контекст

* **ID:** DV-001-Context
* **Title:** Границы системы SVS-RVC
* **Viewpoint:** Context
* **Representation:**

  SVS-RVC — настольное приложение, работающее локально на компьютере пользователя. Внешние акторы: **композитор / продюсер** (импортирует партитуру и текст, выбирает модель, запускает рендер и экспорт), **заказчик / слушатель** (оценивает тембр и разборчивость), **владелец голоса** (предоставляет RVC-модель и контролирует условия её использования). Внешние элементы: файловая система, аудиоустройство, локальная библиотека моделей. Сеть не является обязательной: все вычисления и данные остаются на машине пользователя.

  ```mermaid
  flowchart LR
      Composer[Композитор / продюсер]
      Listener[Заказчик / слушатель]
      Owner[Владелец голоса]
      System[SVS-RVC Desktop App]
      FS[(Файловая система)]
      Audio[Аудиоустройство]
      Models[(Локальная библиотека RVC-моделей)]

      Composer -->|MIDI, лирика, настройки| System
      System -->|WAV/FLAC, проект| FS
      System -->|real-time audio| Audio
      Models -->|ONNX-модели| System
      Owner -->|лицензия и согласие| Models
      System -->|аудио для оценки| Listener
  ```

  Сервисы системы: импорт партитуры и лирики; привязка слогов к нотам; выбор и проверка модели; офлайн-рендер; real-time-мониторинг; экспорт и сохранение; загрузка/сохранение проекта.

* **SRS Requirements:** REQ-FUNC-001, REQ-FUNC-003, REQ-FUNC-004, REQ-SEC-001
* **Decision:** ADR-001
* **More Information:** Границы не включают обучение моделей и облачные вычисления. Библиотека моделей принадлежит пользователю; приложение отвечает только за чтение, проверку целостности и использование.

### 3.3 DV-002 Композиция

* **ID:** DV-002-Composition
* **Title:** Компонентная декомпозиция
* **Viewpoint:** Composition
* **Representation:**

  Система разделена на четыре слоя: представление (Qt 6 Widgets), приложение (контроллеры), домен (алгоритмы и сущности), инфраструктура (файлы, ONNX Runtime, аудио, настройки). Такое разделение позволяет тестировать доменную логику без GUI и заменять инфраструктурные библиотеки.

  ```mermaid
  flowchart TB
      subgraph UI[Presentation: Qt 6 Widgets]
          MW[MainWindow]
          SV[ScoreView]
          LE[LyricsEditor]
          TB[TransportBar]
          RD[RenderDialog]
          MM[ModelManagerDialog]
          LM[LiveMonitorWindow]
      end
      subgraph APP[Application]
          PC[ProjectController]
          RC[RenderController]
          MC[ModelController]
          RTC[RealtimeController]
      end
      subgraph DOM[Domain / Core]
          MI[MidiImporter]
          LA[LyricsAligner]
          PH[PhonemeConverter]
          F0[F0Builder]
          SVS[SvsEngine]
          RVC[RvcConverter]
          PP[AudioPostProcessor]
          EX[AudioExporter]
          PS[ProjectSerializer]
      end
      subgraph INF[Infrastructure]
          ORT[OnnxModelLoader]
          MR[ModelRepository]
          AD[AudioDevice]
          FS[FileSystem]
          SS[SettingsStore]
          LG[Logger]
      end

      UI --> APP
      APP --> DOM
      DOM --> INF
      INF --> EXT[ONNX Runtime / Qt / libsndfile / MIDI parser]
  ```

  | Компонент | Ответственность | Требования |
  |-----------|-----------------|------------|
  | `MainWindow` | Главное окно: партитура, лирика, инспектор голоса, транспорт, меню | REQ-FUNC-001, REQ-FUNC-004 |
  | `ProjectController` | Координация проекта, импорт, сохранение, состояние | REQ-FUNC-001, REQ-FUNC-005 |
  | `MidiImporter` | Разбор SMF 0/1, извлечение нот, длительностей, темпа | REQ-FUNC-001 |
  | `LyricsAligner` | Привязка слогов к нотам, предупреждение при несовпадении | REQ-FUNC-001 |
  | `PhonemeConverter` | Преобразование текста в фонемы (RU/EN) | REQ-FUNC-003 |
  | `F0Builder` | Построение F0-контура, вибрато, портаменто, глиссандо | REQ-FUNC-003 |
  | `SvsEngine` | Акустический синтез вокального сигнала по партитуре и фонемам | REQ-FUNC-003 |
  | `RvcConverter` | Перенос тембра: ContentVec/HuBERT, индексный поиск, генератор | REQ-FUNC-002, REQ-FUNC-003 |
  | `AudioPostProcessor` | Нормализация, ограничение клиппинга, сглаживание | REQ-REL-001 |
  | `AudioExporter` | Запись WAV/FLAC с заданными параметрами, атомарное сохранение | REQ-FUNC-004, REQ-FUNC-005 |
  | `ModelRepository` | Сканирование библиотеки, чтение манифестов, проверка хешей | REQ-FUNC-002 |
  | `OnnxModelLoader` | Загрузка ONNX-сессий, выбор execution provider | ADR-001 |
  | `AudioDevice` | Вывод real-time-аудио, буферизация, обработка underrun | REQ-PERF-001 |
  | `SettingsStore` | Параметры экспорта, аудио, последние проекты | REQ-FUNC-005 |
  | `ProjectSerializer` | Формат `.svsproj` (JSON), версионирование | REQ-FUNC-001, REQ-FUNC-005 |

* **SRS Requirements:** REQ-FUNC-001, REQ-FUNC-002, REQ-FUNC-003, REQ-FUNC-004, REQ-FUNC-005
* **Decision:** ADR-001
* **More Information:** Домен не зависит от Qt Widgets. `SvsEngine` и `RvcConverter` скрыты за интерфейсами, что позволяет заменить модель или движок без изменения UI.

### 3.4 DV-003 Интерфейс

* **ID:** DV-003-Interface
* **Title:** Контракты компонентов и форматы данных
* **Viewpoint:** Interface
* **Representation:**

  Поскольку SVS-RVC — настольное приложение, внешние контракты — это C++-интерфейсы, форматы файлов и события UI. Все интерфейсы возвращают результат через `Result<T, Error>` и не бросают исключения через границы слоёв.

  ```cpp
  struct Score;              // ноты, длительности, темп, размер
  struct Lyrics;             // текст и язык
  struct AlignedScore;       // слоги, привязанные к нотам
  struct AudioBuffer;        // сэмплы, частота, каналы, разрядность
  struct ModelInfo;          // id, name, version, sample_rate, files, hash
  struct RenderSettings;     // модель, параметры F0, качество, формат
  struct ExportSettings;     // путь, WAV/FLAC, частота, разрядность, каналы

  class IMidiImporter {
  public:
      virtual Result<Score, ImportError> import(const std::filesystem::path& path) = 0;
  };

  class ILyricsAligner {
  public:
      virtual Result<AlignedScore, AlignmentError> align(
          const Lyrics& lyrics, const Score& score) = 0;
  };

  class IModelRepository {
  public:
      virtual std::vector<ModelInfo> scan() = 0;
      virtual Result<ModelInfo, ModelError> validate(const std::string& modelId) = 0;
  };

  class ISynthesisPipeline {
  public:
      virtual Result<AudioBuffer, RenderError> render(
          const AlignedScore& score,
          const ModelInfo& model,
          const RenderSettings& settings,
          IProgress& progress) = 0;
  };

  class IAudioExporter {
  public:
      virtual Result<void, ExportError> exportAudio(
          const AudioBuffer& audio,
          const std::filesystem::path& path,
          const ExportSettings& settings) = 0;
  };

  class IRealtimeMonitor {
  public:
      virtual Result<void, AudioError> start(
          const AlignedScore& score,
          const ModelInfo& model,
          const RenderSettings& settings) = 0;
      virtual void stop() = 0;
  };
  ```

  | Контракт | Вход | Выход | Ошибки | Требования |
  |----------|------|-------|--------|------------|
  | `IMidiImporter::import` | путь к `.mid` | `Score` | `E_MIDI_FORMAT`, `E_MIDI_EMPTY`, `E_MIDI_IO` | REQ-FUNC-001 |
  | `ILyricsAligner::align` | `Lyrics`, `Score` | `AlignedScore` | `E_ALIGN_COUNT`, `E_ALIGN_LANG` | REQ-FUNC-001 |
  | `IModelRepository::validate` | `modelId` | `ModelInfo` | `E_MODEL_NOT_FOUND`, `E_MODEL_CORRUPT`, `E_MODEL_INCOMPATIBLE` | REQ-FUNC-002 |
  | `ISynthesisPipeline::render` | `AlignedScore`, `ModelInfo`, `RenderSettings` | `AudioBuffer` | `E_RENDER_CANCELLED`, `E_RENDER_OOM`, `E_RENDER_MODEL` | REQ-FUNC-003 |
  | `IAudioExporter::exportAudio` | `AudioBuffer`, путь, `ExportSettings` | `void` | `E_EXPORT_IO`, `E_EXPORT_FORMAT`, `E_EXPORT_CANCELLED` | REQ-FUNC-004, REQ-FUNC-005 |
  | `IRealtimeMonitor::start` | `AlignedScore`, `ModelInfo`, `RenderSettings` | `void` | `E_AUDIO_DEVICE`, `E_AUDIO_UNDERRUN` | REQ-PERF-001 |

  **Форматы данных.**

  | Формат | Назначение | Обязательные поля / параметры |
  |--------|------------|-------------------------------|
  | `.svsproj` | Проект | `version`, `midiPath`, `lyrics`, `language`, `modelId`, `renderSettings`, `exportSettings` |
  | `model.json` | Манифест RVC-модели | `id`, `name`, `version`, `sampleRate`, `f0`, `onnxFiles`, `indexFile`, `license`, `sha256` |
  | WAV | Экспорт | PCM 16/24 bit, 44.1/48 kHz, mono/stereo |
  | FLAC | Экспорт | 16/24 bit, 44.1/48 kHz, mono/stereo |
  | MIDI | Импорт | SMF 0/1, ноты, длительности, темп |

  **Инварианты:**

  * приложение не выполняет сетевых запросов для синтеза, хранения и экспорта (REQ-SEC-001);
  * рендер запрещён, если модель не прошла `validate` (REQ-FUNC-002);
  * частота дискретизации модели, F0-контура и выходного буфера согласованы;
  * экспорт выполняется в временный файл с последующим переименованием, чтобы не повредить существующий файл;
  * пути и имена файлов обрабатываются в UTF-8, включая кириллицу (REQ-FUNC-005);
  * real-time-буфер — 128–256 сэмплов, целевая задержка — не более 250 мс (REQ-PERF-001).

* **SRS Requirements:** REQ-FUNC-001, REQ-FUNC-002, REQ-FUNC-003, REQ-FUNC-004, REQ-FUNC-005, REQ-PERF-001, REQ-SEC-001
* **Decision:** ADR-001
* **More Information:** Формат `.svsproj` версионируется; неизвестные поля сохраняются для обратной совместимости. Манифест модели содержит хеш, чтобы обнаруживать повреждение до загрузки в ONNX Runtime.

### 3.5 DV-004 Взаимодействие

* **ID:** DV-004-Interaction
* **Title:** Сценарии выполнения
* **Viewpoint:** Interaction
* **Representation:**

  **Счастливый путь: импорт → рендер → прослушивание → экспорт.**

  ```mermaid
  sequenceDiagram
      actor C as Композитор
      participant UI as MainWindow
      participant PC as ProjectController
      participant MI as MidiImporter
      participant LA as LyricsAligner
      participant MC as ModelController
      participant MR as ModelRepository
      participant RC as RenderController
      participant SP as SynthesisPipeline
      participant EX as AudioExporter

      C->>UI: Выбрать MIDI и файл лирики
      UI->>PC: importFiles(midi, lyrics)
      PC->>MI: import(midi)
      MI-->>PC: Score
      PC->>LA: align(lyrics, score)
      LA-->>PC: AlignedScore
      PC-->>UI: Партитура и слоги отображены
      C->>UI: Выбрать RVC-модель
      UI->>MC: selectModel(modelId)
      MC->>MR: validate(modelId)
      MR-->>MC: ModelInfo
      MC-->>UI: Модель валидна
      C->>UI: Нажать «Рендер»
      UI->>RC: render(project, model, settings)
      RC->>SP: render(alignedScore, model, settings)
      SP-->>RC: AudioBuffer: SVS, RVC, postprocess
      RC-->>UI: Готово, доступно прослушивание
      C->>UI: Нажать «Экспорт»
      UI->>EX: exportAudio(audio, path, settings)
      EX-->>UI: Файл сохранён
  ```

  1. Композитор открывает проект или импортирует MIDI и лирику.
  2. `MidiImporter` разбирает партитуру, `LyricsAligner` привязывает слоги к нотам.
  3. Композитор выбирает RVC-модель; `ModelRepository` проверяет манифест, хеш и совместимость.
  4. `RenderController` запускает `SynthesisPipeline`: SVS-этап формирует вокальный сигнал, RVC-этап переносит тембр, постобработка убирает артефакты.
  5. Результат прослушивается в приложении.
  6. `AudioExporter` сохраняет WAV/FLAC в выбранный каталог.

  **Пути отказа.**

  | Сценарий | Триггер | Поведение системы | Требования |
  |----------|---------|-------------------|------------|
  | Несовпадение слогов и нот | Количество слогов ≠ количество нот | Предупреждение с предложением автоматически распределить слоги или отредактировать вручную; рендер не блокируется | REQ-FUNC-001 |
  | Повреждённая модель | Ошибка хеша или ONNX-файла | Рендер запрещён, показывается сообщение и список валидных моделей | REQ-FUNC-002 |
  | Несовместимая модель | Неподдерживаемая частота или набор входов | Модель помечается `Incompatible`, выбор блокируется | REQ-FUNC-002 |
  | Отмена экспорта | Пользователь закрыл диалог | Файл не создаётся; временный файл удаляется | REQ-FUNC-005 |
  | Совпадение имени | Файл уже существует | Запрос на перезапись; при отказе — возврат к выбору имени | REQ-FUNC-005 |
  | Нет аудиоустройства | Real-time-режим недоступен | Сообщение и предложение перейти в офлайн-рендер | REQ-PERF-001 |
  | Underrun в real-time | Не хватает времени на буфер | Увеличение буфера до 256 сэмплов, снижение качества preview, запись в лог | REQ-PERF-001 |
  | Ошибка записи | Нет прав или места на диске | Понятное сообщение, существующий файл не повреждается | REQ-FUNC-005 |

* **SRS Requirements:** REQ-FUNC-001 … REQ-FUNC-005, REQ-PERF-001, REQ-REL-001
* **Decision:** ADR-001
* **More Information:** Все длительные операции выполняются в фоновом потоке с прогрессом и возможностью отмены. UI-поток не блокируется.

### 3.6 DV-005 Динамика состояний

* **ID:** DV-005-StateDynamics
* **Title:** Состояния приложения, рендера, модели и real-time
* **Viewpoint:** State Dynamics
* **Representation:**

  ```mermaid
  stateDiagram-v2
      [*] --> NoProject
      NoProject --> ProjectLoaded: открыть / импортировать
      ProjectLoaded --> ProjectLoaded: редактировать партитуру или лирику
      ProjectLoaded --> ModelSelected: выбрать валидную модель
      ModelSelected --> Rendering: «Рендер»
      Rendering --> Rendered: успех
      Rendering --> Error: ошибка / отмена
      Rendered --> Rendering: повторный рендер
      Rendered --> Exporting: «Экспорт»
      Exporting --> Exported: файл сохранён
      Exporting --> Error: ошибка ввода-вывода
      Error --> ProjectLoaded: исправить и продолжить
      Exported --> Rendered: продолжить работу
  ```

  **Состояния приложения и проекта.**

  | Состояние | Триггер | Следующее состояние / действие |
  |-----------|---------|--------------------------------|
  | `NoProject` | запуск приложения | `ProjectLoaded` после открытия или импорта |
  | `ProjectLoaded` | загружены MIDI и лирика | редактирование, выбор модели |
  | `ModelSelected` | модель прошла проверку | `Rendering` по кнопке «Рендер» |
  | `Rendering` | запущен синтез | `Rendered` или `Error` |
  | `Rendered` | синтез завершён | прослушивание, `Exporting` |
  | `Exporting` | выбран путь и формат | `Exported` или `Error` |
  | `Exported` | файл записан | `Rendered` (продолжить) |
  | `Error` | сбой или отмена | `ProjectLoaded` после исправления |

  **Состояния модели.**

  | Состояние | Триггер | Следующее состояние / действие |
  |-----------|---------|--------------------------------|
  | `Available` | модель найдена в библиотеке | `Validating` при выборе |
  | `Validating` | чтение манифеста и хеша | `Valid` / `Corrupt` / `Incompatible` |
  | `Valid` | проверка пройдена | разрешён выбор и рендер |
  | `Corrupt` | хеш или файл повреждён | выбор заблокирован, сообщение |
  | `Incompatible` | другая частота или входы | выбор заблокирован, сообщение |

  **Состояния real-time-мониторинга.**

  | Состояние | Триггер | Следующее состояние / действие |
  |-----------|---------|--------------------------------|
  | `Stopped` | приложение запущено | `Starting` по кнопке «Live» |
  | `Starting` | открытие аудиоустройства | `Running` или `Failed` |
  | `Running` | аудио выводится | `Underrun` / `Stopping` |
  | `Underrun` | пропущен дедлайн буфера | увеличить буфер, снизить качество, вернуться в `Running` |
  | `Stopping` | пользователь остановил режим | `Stopped` |
  | `Failed` | нет устройства или ошибка | `Stopped` после сообщения |

* **SRS Requirements:** REQ-FUNC-001, REQ-FUNC-002, REQ-FUNC-003, REQ-FUNC-004, REQ-FUNC-005, REQ-PERF-001, REQ-REL-001
* **Decision:** ADR-001
* **More Information:** Состояние `Rendering` не блокирует закрытие приложения: при выходе пользователь получает запрос на отмену рендера. Отмена освобождает ресурсы ONNX Runtime и удаляет временные файлы.

### 3.7 DV-006 Зависимости

* **ID:** DV-006-Dependency
* **Title:** Направленные зависимости компонентов
* **Viewpoint:** Dependency
* **Representation:**

  ```mermaid
  flowchart LR
      UI[Presentation: Qt 6 Widgets] --> APP[Application controllers]
      APP --> DOM[Domain / Core]
      DOM --> INF[Infrastructure adapters]
      INF --> ORT[ONNX Runtime]
      INF --> QT[Qt 6 Core]
      INF --> CODEC[libsndfile / FLAC]
      INF --> MIDI[MIDI parser]
      DOM -.->|интерфейсы| INF
  ```

  Правила зависимостей:

  * UI зависит только от контроллеров приложения, не от ONNX Runtime и файловой системы напрямую;
  * домен не зависит от Qt Widgets; допустимы только Qt Core и стандартная библиотека C++;
  * инфраструктура реализует интерфейсы, объявленные в домене/приложении;
  * `ModelRepository` — единственный владелец метаданных моделей;
  * `SettingsStore` — единственный владелец пользовательских настроек;
  * внешние библиотеки изолированы в инфраструктурном слое.

  | Зависимость | Направление | Влияние изменения |
  |-------------|-------------|-------------------|
  | UI → Application | `MainWindow` → `ProjectController`, `RenderController` | изменение API контроллера затрагивает только UI |
  | Application → Domain | `RenderController` → `SynthesisPipeline` | замена pipeline не меняет UI |
  | Domain → Infrastructure | `SvsEngine`, `RvcConverter` → `OnnxModelLoader` | замена ONNX Runtime локализована в загрузчике |
  | Infrastructure → External | `AudioExporter` → libsndfile | добавление формата затрагивает экспортёр и диалог |
  | ModelRepository → FileSystem | чтение манифестов и хешей | повреждённая модель не попадает в рендер |

  Циклических зависимостей нет. Общей базы данных в приложении нет: состояние проекта хранится в `.svsproj`, модели — в локальной библиотеке, настройки — в `SettingsStore`.

* **SRS Requirements:** REQ-FUNC-002, REQ-FUNC-003, REQ-SEC-001, REQ-PERF-001
* **Decision:** ADR-001
* **More Information:** Добавление нового формата экспорта затрагивает `AudioExporter`, `ExportSettings` и диалог экспорта. Добавление новой RVC-модели не требует изменения кода, если она соответствует манифесту.

## 4. Решения

| ID | Title | Status | Outcome / Reference |
|----|-------|--------|---------------------|
| ADR-001 | Локальный двухстадийный конвейер SVS → RVC на ONNX Runtime | accepted | Локальный конвейер с ONNX Runtime и CPU execution provider; см. [`lab4/adr/project-adr.md`](../adr/project-adr.md) |

ADR-001 обосновывает выбор локального двухстадийного конвейера вместо облачного API, единой end-to-end модели и встроенного PyTorch runtime. Решение обеспечивает выполнение REQ-SEC-001 (локальность), REQ-PERF-001 (задержка ≤ 250 мс) и REQ-FUNC-003 (качество тембра) на целевом оборудовании без GPU.

## 5. Приложения

### Приложение A. Матрица трассировки BR → REQ → DV

| BR | REQ | Проектные представления |
|----|-----|-------------------------|
| BR-01 | REQ-FUNC-003, REQ-FUNC-004 | DV-001, DV-002, DV-004, DV-005 |
| BR-02 | REQ-FUNC-003 | DV-002, DV-004 |
| BR-03 | REQ-FUNC-001, REQ-FUNC-004, REQ-FUNC-005 | DV-001, DV-002, DV-003, DV-004 |
| BR-04 | REQ-FUNC-002, REQ-FUNC-003 | DV-002, DV-003, DV-004, DV-005 |
| BR-05 | REQ-SEC-001 | DV-001, DV-002, DV-006, ADR-001 |
| BR-06 | REQ-FUNC-001, REQ-FUNC-004, REQ-FUNC-005 | DV-002, DV-003, DV-004, DV-005 |

### Приложение B. Оценка трудозатрат и план итераций

| Функционал | REQ | Оценка, чел.-дн. |
|------------|-----|------------------|
| UI: главное окно, партитура, лирика, транспорт, проект | REQ-FUNC-001, REQ-FUNC-004 | 2 |
| Импорт MIDI и привязка слогов | REQ-FUNC-001 | 2 |
| Менеджер моделей и проверка целостности | REQ-FUNC-002 | 1 |
| Конвейер SVS + RVC | REQ-FUNC-003 | 3 |
| Экспорт и сохранение WAV/FLAC | REQ-FUNC-004, REQ-FUNC-005 | 1 |
| Надёжность и граничные случаи | REQ-REL-001 | 1 |
| **Итого MVP** | | **10** |

Real-time-мониторинг (REQ-PERF-001) имеет приоритет 50 и вынесен в версию 1.1: при сроке 10 рабочих дней резерв отсутствует. Оценка версии 1.1: real-time — 1 человеко-день, пресеты настроек — 0,5 человеко-дня.

| Итерация | Рабочие дни | Содержание | Демонстрация |
|----------|-------------|------------|--------------|
| 1 | 1–5 | UI, проект, импорт MIDI/лирики, менеджер моделей, SVS-preview | Импорт → выбор модели → preview |
| 2 | 6–10 | RVC-тембр, A/B-переключение, экспорт, надёжность | Сквозной сценарий, A/B, экспорт |

Подробный план с пересчётом после второго раунда обсуждения приведён в [`lab4/plan/iteration-plan.md`](../plan/iteration-plan.md).

### Приложение C. Формат проекта `.svsproj`

```json
{
  "version": 1,
  "midiPath": "song.mid",
  "lyrics": "Текст песни",
  "language": "ru",
  "modelId": "voice-alice-v2",
  "renderSettings": {
    "f0Method": "rmvpe",
    "pitchShift": 0,
    "quality": "high"
  },
  "exportSettings": {
    "format": "wav",
    "sampleRate": 48000,
    "bitDepth": 24,
    "channels": 2
  }
}
```

Формат расширяемый: при загрузке неизвестные поля сохраняются, а отсутствующие заполняются значениями по умолчанию. Это упрощает миграцию проектов между версиями.
