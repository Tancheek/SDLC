#include "view/MainWindow.h"

#include <QFont>
#include <QGroupBox>
#include <QLabel>
#include <QPushButton>
#include <QStatusBar>
#include <QVBoxLayout>

#include "util/Format.h"

MainWindow::MainWindow(CurrencyModel *model, QWidget *parent)
    : QMainWindow(parent)
    , m_model(model)
{

    m_model->addListener(this);

    buildUi();
    refreshLabels();
}

MainWindow::~MainWindow()
{
    m_model->removeListener(this);
}

void MainWindow::buildUi()
{
    setWindowTitle(QStringLiteral("Конвертер белорусских рублей в евро (MVC, активная модель)"));
    setMinimumSize(560, 320);

    auto *central = new QWidget(this);
    auto *layout = new QVBoxLayout(central);
    layout->setContentsMargins(24, 24, 24, 24);
    layout->setSpacing(16);

    auto *inputGroup = new QGroupBox(QStringLiteral("Введённые числа"), central);
    auto *inputLayout = new QVBoxLayout(inputGroup);
    inputLayout->setSpacing(8);

    m_amountLabel = new QLabel(inputGroup);
    m_rateLabel = new QLabel(inputGroup);
    inputLayout->addWidget(m_amountLabel);
    inputLayout->addWidget(m_rateLabel);

    auto *resultGroup = new QGroupBox(QStringLiteral("Результат конвертации"), central);
    auto *resultLayout = new QVBoxLayout(resultGroup);

    m_resultLabel = new QLabel(resultGroup);
    QFont resultFont = m_resultLabel->font();
    resultFont.setPointSize(resultFont.pointSize() + 6);
    resultFont.setBold(true);
    m_resultLabel->setFont(resultFont);
    m_resultLabel->setStyleSheet(QStringLiteral("color: #0b5394;"));
    resultLayout->addWidget(m_resultLabel);

    m_inputButton = new QPushButton(QStringLiteral("Ввод чисел"), central);
    m_inputButton->setMinimumHeight(40);
    QFont buttonFont = m_inputButton->font();
    buttonFont.setPointSize(buttonFont.pointSize() + 1);
    m_inputButton->setFont(buttonFont);
    m_inputButton->setToolTip(QStringLiteral("Открыть окно ввода суммы и курса евро"));
    m_inputButton->setCursor(Qt::PointingHandCursor);
    m_inputButton->setDefault(true);
    m_inputButton->setFocus(); 

    layout->addWidget(inputGroup);
    layout->addWidget(resultGroup);
    layout->addStretch();
    layout->addWidget(m_inputButton);

    setCentralWidget(central);

    statusBar()->showMessage(
        QStringLiteral("Нажмите «Ввод чисел», укажите сумму в BYN и курс евро."));

    setStyleSheet(QStringLiteral(
        "QGroupBox { font-size: 11pt; border: 1px solid #b8c4d0; border-radius: 6px;"
        "            margin-top: 12px; padding: 12px 12px 8px 12px; }"
        "QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 4px; }"
        "QLabel { font-size: 12pt; }"
        "QPushButton { background-color: #0b5394; color: white; border: none;"
        "              border-radius: 6px; font-size: 12pt; padding: 8px 16px; }"
        "QPushButton:hover { background-color: #12659f; }"
        "QPushButton:pressed { background-color: #093f70; }"));
}

void MainWindow::refreshLabels()
{
    if (!m_model->hasData()) {
        m_amountLabel->setText(QStringLiteral("Сумма в белорусских рублях: —"));
        m_rateLabel->setText(QStringLiteral("Курс евро: —"));
        m_resultLabel->setText(QStringLiteral("— EUR"));
        return;
    }

    m_amountLabel->setText(
        QStringLiteral("Сумма в белорусских рублях: %1 BYN").arg(format::money(m_model->amountByn())));
    m_rateLabel->setText(
        QStringLiteral("Курс евро: %1 BYN за 1 EUR").arg(format::rate(m_model->euroRate())));
    m_resultLabel->setText(
        QStringLiteral("%1 EUR").arg(format::money(m_model->resultEur())));
}

void MainWindow::onModelChanged()
{
    refreshLabels();
}