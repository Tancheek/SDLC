#pragma once

#include <QMainWindow>

#include "model/CurrencyModel.h"

class QLabel;
class QPushButton;

class MainWindow : public QMainWindow, public CurrencyModel::Listener
{
    Q_OBJECT

public:
    explicit MainWindow(CurrencyModel *model, QWidget *parent = nullptr);
    ~MainWindow() override;

    QPushButton *inputButton() const { return m_inputButton; }

    void onModelChanged() override;

private:
    void buildUi();
    void refreshLabels();

    CurrencyModel *m_model = nullptr;

    QLabel *m_amountLabel = nullptr;
    QLabel *m_rateLabel = nullptr;
    QLabel *m_resultLabel = nullptr;
    QPushButton *m_inputButton = nullptr;
};