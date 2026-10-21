#include "view/InputDialog.h"

#include <QDialogButtonBox>
#include <QFormLayout>
#include <QLabel>
#include <QLineEdit>
#include <QLocale>
#include <QPushButton>
#include <QVBoxLayout>

#include "util/Format.h"

InputDialog::InputDialog(QWidget *parent)
    : QDialog(parent)
{
    setWindowTitle(QStringLiteral("Ввод чисел"));
    setModal(true);
    setMinimumWidth(420);

    auto *layout = new QVBoxLayout(this);

    auto *hint = new QLabel(
        QStringLiteral("Введите сумму в белорусских рублях и курс евро.\n"
                       "Дробную часть можно отделять запятой или точкой."),
        this);
    hint->setWordWrap(true);
    layout->addWidget(hint);

    auto *form = new QFormLayout();
    m_amountEdit = new QLineEdit(this);
    m_amountEdit->setPlaceholderText(QStringLiteral("например, 1500,50"));
    m_rateEdit = new QLineEdit(this);
    m_rateEdit->setPlaceholderText(QStringLiteral("например, 3,2750"));

    form->addRow(QStringLiteral("Сумма в белорусских рублях (BYN):"), m_amountEdit);
    form->addRow(QStringLiteral("Курс евро (BYN за 1 EUR):"), m_rateEdit);
    layout->addLayout(form);

    auto *buttons = new QDialogButtonBox(QDialogButtonBox::Ok | QDialogButtonBox::Cancel, this);
    buttons->button(QDialogButtonBox::Ok)->setText(QStringLiteral("ОК"));
    buttons->button(QDialogButtonBox::Cancel)->setText(QStringLiteral("Отмена"));
    layout->addWidget(buttons);

    
    connect(buttons, &QDialogButtonBox::accepted, this, &InputDialog::submit);
    connect(buttons, &QDialogButtonBox::rejected, this, &QDialog::reject);
    connect(m_amountEdit, &QLineEdit::returnPressed, this, &InputDialog::submit);
    connect(m_rateEdit, &QLineEdit::returnPressed, this, &InputDialog::submit);

    m_amountEdit->setFocus(); 
}

void InputDialog::setValues(double amountByn, double euroRate, bool hasData)
{
    if (!hasData) {
        return; 
    }

    const QLocale locale(QLocale::Russian, QLocale::Belarus);
    m_amountEdit->setText(locale.toString(amountByn, 'f', 2));
    m_rateEdit->setText(locale.toString(euroRate, 'f', 4));
    m_amountEdit->selectAll();
}

void InputDialog::submit()
{
    emit valuesSubmitted(m_amountEdit->text(), m_rateEdit->text());
}