#pragma once

#include <QDialog>

class QLineEdit;

class InputDialog : public QDialog
{
    Q_OBJECT

public:
    explicit InputDialog(QWidget *parent = nullptr);

    void setValues(double amountByn, double euroRate, bool hasData);

signals:
    void valuesSubmitted(const QString &amountText, const QString &rateText);

private:
    void submit();

    QLineEdit *m_amountEdit = nullptr;
    QLineEdit *m_rateEdit = nullptr;
};