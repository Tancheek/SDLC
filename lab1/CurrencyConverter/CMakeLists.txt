cmake_minimum_required(VERSION 3.21)

project(CurrencyConverter
        VERSION 1.0.0
        DESCRIPTION "Конвертер белорусских рублей в евро (MVC, активная модель)"
        LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Подключаем Qt 6 (компонент Widgets отвечает за графический интерфейс)
find_package(Qt6 REQUIRED COMPONENTS Widgets)

qt_standard_project_setup()

# WIN32 = приложение с графическим интерфейсом (без окна консоли)
qt_add_executable(CurrencyConverter WIN32
    src/main.cpp
    src/util/Format.h
    src/model/CurrencyModel.h
    src/model/CurrencyModel.cpp
    src/view/MainWindow.h
    src/view/MainWindow.cpp
    src/view/InputDialog.h
    src/view/InputDialog.cpp
    src/controller/ConverterController.h
    src/controller/ConverterController.cpp
)

target_include_directories(CurrencyConverter PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)

target_link_libraries(CurrencyConverter PRIVATE Qt6::Widgets)

if (MSVC)
    target_compile_options(CurrencyConverter PRIVATE /utf-8 /W4)
else()
    # Кириллица в строковых литералах компилируется в UTF-8
    target_compile_options(CurrencyConverter PRIVATE -Wall -Wextra
                           -finput-charset=UTF-8 -fexec-charset=UTF-8)
endif()