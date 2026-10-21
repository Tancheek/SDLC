# Конвертер белорусских рублей в евро

Лабораторная работа №1 по дисциплине «Жизненный цикл разработки программного
обеспечения». Вариант 1. Язык — C++ (Qt 6 Widgets), среда разработки — Visual
Studio Code. Архитектура — MVC с **активной** моделью.

## Важно: путь к проекту не должен содержать кириллицу

Компилятор метаобъектов Qt (`moc.exe`) не умеет создавать файлы в каталогах,
в пути которых есть символы вне ASCII. Если проект расположен, например, в
`D:\0000000жрцпо\lab1\CurrencyConverter`, сборка завершится ошибкой
`moc: Cannot create ... Error: No such file or directory`.

Решение — работать с проектом по ASCII-пути. Ссылку (junction) достаточно
создать один раз:

```cmd
mklink /J D:\lab1 "D:\0000000жрцпо\lab1"
```

После этого открывайте в VS Code каталог `D:\lab1\CurrencyConverter` —
сборка, запуск и отладка будут работать.

## Возможности

- главная форма с метками введённых чисел и результата конвертации;
- кнопка «Ввод чисел» открывает отдельное окно для ввода суммы и курса евро;
- последние успешно введённые данные восстанавливаются при повторном вводе;
- некорректные данные (не число, отрицательная сумма, нулевой курс) приводят
  к появлению сообщения об ошибке, окно ввода при этом не закрывается;
- активная модель самостоятельно уведомляет представление через паттерн
  «Наблюдатель», контроллер не обновляет форму вручную.

## Состав проекта

```
CurrencyConverter/
├── CMakeLists.txt
├── .vscode/                     настройки сборки, запуска и отладки VS Code
├── docs/
│   ├── class-diagram.puml       диаграмма классов (PlantUML, UML)
│   └── architecture.sysml       структурная модель (SysML v2)
└── src/
    ├── main.cpp                 точка входа, сборка каркаса MVC
    ├── model/CurrencyModel.*    модель (активная) и интерфейс Listener
    ├── view/MainWindow.*        главная форма (подписана на модель)
    ├── view/InputDialog.*       окно ввода суммы и курса
    ├── controller/ConverterController.*  обработка действий пользователя
    └── util/Format.h            форматирование чисел для представления
```

## Сборка и запуск

```powershell
cmake -S D:\lab1\CurrencyConverter -B D:\lab1\CurrencyConverter\build -G Ninja `
      -DCMAKE_PREFIX_PATH=C:/Qt/6.11.1/mingw_64 `
      -DCMAKE_MAKE_PROGRAM=C:/Qt/Tools/Ninja/ninja.exe `
      -DCMAKE_CXX_COMPILER=C:/Qt/Tools/mingw1310_64/bin/g++.exe `
      -DCMAKE_BUILD_TYPE=Debug
cmake --build D:\lab1\CurrencyConverter\build
$env:PATH = "C:\Qt\6.11.1\mingw_64\bin;$env:PATH"
D:\lab1\CurrencyConverter\build\CurrencyConverter.exe
```

В VS Code: `Ctrl+Shift+B` — сборка, `F5` — запуск под отладчиком
(точка останова ставится в `CurrencyModel::convert`, строка 35).

Рядом с исполняемым файлом уже разложены библиотеки Qt и MinGW
(`Qt6Core.dll`, `Qt6Gui.dll`, `Qt6Widgets.dll`, `platforms/qwindows.dll` и др.),
поэтому `CurrencyConverter.exe` запускается двойным щелчком.

## Расширения VS Code

- **PlantUML** (`jebbs.plantuml`) — UML-диаграммы; предпросмотр `Alt+D`
  для файла `docs/class-diagram.puml`;
- **Syside Editor** (`sensmetry.syside-editor`) — поддержка SysML v2 для
  файла `docs/architecture.sysml`.

## Установка расширений с нуля

```powershell
code --install-extension ms-vscode.cpptools-extension-pack
code --install-extension ms-vscode.cmake-tools
code --install-extension jebbs.plantuml
code --install-extension sensmetry.syside-editor
```