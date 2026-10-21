// Лабораторная работа №1, вариант 1.
// Структурное описание приложения «Конвертер белорусских рублей в евро»
// в текстовой нотации SysML v2 (расширение Syside Editor для VS Code).

package CurrencyConverter {
    private import ScalarValues::*;

    doc /* Приложение конвертирует сумму в белорусских рублях в евро
           и построено по архитектурному паттерну MVC с активной моделью. */

    port def UserInputPort {
        doc /* Действие пользователя: нажатие кнопки или «ОК» в окне ввода. */
    }

    port def ModelChangedPort {
        doc /* Уведомление представления об изменении состояния модели. */
    }

    part def CurrencyModel {
        doc /* Модель: хранит введённые числа и результат, проверяет
               корректность данных и уведомляет подписчиков. */
        attribute amountByn : Real;
        attribute euroRate : Real;
        attribute resultEur : Real;
        attribute hasData : Boolean;
        port changed : ModelChangedPort;
    }

    part def MainWindow {
        doc /* Главная форма: метки с введёнными числами и результатом. */
        port input : UserInputPort;
        port modelChanged : ModelChangedPort;
    }

    part def InputDialog {
        doc /* Дополнительное окно ввода суммы и курса евро. */
        port submit : UserInputPort;
    }

    part def ConverterController {
        doc /* Контроллер: обрабатывает нажатие кнопки «Ввод чисел»,
               разбирает текст в числа и передаёт данные модели. */
        port ui : UserInputPort;
        port model : ModelChangedPort;
    }

    part def Application {
        doc /* Каркас MVC: контроллер управляет представлением,
               активная модель уведомляет представление. */
        part model : CurrencyModel;
        part mainView : MainWindow;
        part dialog : InputDialog;
        part controller : ConverterController;

        connect mainView.input to controller.ui;
        connect dialog.submit to controller.ui;
        connect controller.model to model.changed;
        connect model.changed to mainView.modelChanged;
    }
}