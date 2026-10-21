#pragma once

#include <QObject>

class CurrencyModel;
class InputDialog;
class MainWindow;


class ConverterController : public QObject
{
    Q_OBJECT

public:
    ConverterController(CurrencyModel *model, MainWindow *view, QObject *parent = nullptr);

public slots:
    void openInputDialog();

    void handleInput(const QString &amountText, const QString &rateText);

private:

    static double parseNumber(const QString &text, bool *ok);

    void showError(const QString &message);

    CurrencyModel *m_model = nullptr;
    MainWindow *m_view = nullptr;
    InputDialog *m_inputDialog = nullptr;
};