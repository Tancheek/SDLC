#include "controller/ConverterController.h"

#include <QMessageBox>
#include <QPushButton>
#include <QString>

#include <cmath>
#include <stdexcept>

#include "model/CurrencyModel.h"
#include "view/InputDialog.h"
#include "view/MainWindow.h"

ConverterController::ConverterController(CurrencyModel *model, MainWindow *view, QObject *parent)
    : QObject(parent)
    , m_model(model)
    , m_view(view)
{
    connect(m_view->inputButton(), &QPushButton::clicked,
            this, &ConverterController::openInputDialog);
}

void ConverterController::openInputDialog()
{
    if (m_inputDialog == nullptr) {
        m_inputDialog = new InputDialog(m_view);
        connect(m_inputDialog, &InputDialog::valuesSubmitted,
                this, &ConverterController::handleInput);
    }

    m_inputDialog->setValues(m_model->amountByn(), m_model->euroRate(), m_model->hasData());
    m_inputDialog->show();
    m_inputDialog->raise();
    m_inputDialog->activateWindow();
}

void ConverterController::handleInput(const QString &amountText, const QString &rateText)
{

    bool amountOk = false;
    bool rateOk = false;
    const double amount = parseNumber(amountText, &amountOk);
    const double rate = parseNumber(rateText, &rateOk);

    if (!amountOk) {
        showError(QStringLiteral("Сумма «%1» не является числом.").arg(amountText.trimmed()));
        return;
    }
    if (!rateOk) {
        showError(QStringLiteral("Курс «%1» не является числом.").arg(rateText.trimmed()));
        return;
    }

    try {
        m_model->convert(amount, rate);
    } catch (const std::invalid_argument &error) {
        showError(QString::fromUtf8(error.what()));
        return; 
    }

 
    m_inputDialog->hide();
}

double ConverterController::parseNumber(const QString &text, bool *ok)
{
    QString normalized = text.trimmed();
    normalized.remove(QChar(0x00A0)); 
    normalized.remove(QChar(0x2009)); 
    normalized.remove(QLatin1Char(' '));
    normalized.replace(QLatin1Char(','), QLatin1Char('.'));

    if (normalized.isEmpty()) {
        *ok = false;
        return 0.0;
    }

    const double value = normalized.toDouble(ok);
    if (!std::isfinite(value)) {
        *ok = false;
        return 0.0;
    }
    return value;
}

void ConverterController::showError(const QString &message)
{
    QMessageBox::warning(m_inputDialog != nullptr ? static_cast<QWidget *>(m_inputDialog)
                                                  : static_cast<QWidget *>(m_view),
                         QStringLiteral("Ошибка ввода"), message, QMessageBox::Ok);
}