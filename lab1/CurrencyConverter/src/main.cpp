#include <QApplication>
#include <QStyleFactory>

#include "controller/ConverterController.h"
#include "model/CurrencyModel.h"
#include "view/MainWindow.h"


int main(int argc, char *argv[])
{
    QApplication application(argc, argv);
    QApplication::setApplicationName(QStringLiteral("CurrencyConverter"));
    QApplication::setApplicationVersion(QStringLiteral("1.0"));
    QApplication::setStyle(QStyleFactory::create(QStringLiteral("Fusion")));

    CurrencyModel model;
    MainWindow view(&model);
    ConverterController controller(&model, &view);

    view.show();

    return application.exec();
}