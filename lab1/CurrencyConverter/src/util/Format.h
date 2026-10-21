#pragma once

#include <QLocale>
#include <QString>


namespace format {


inline QString money(double value)
{
    return QLocale(QLocale::Russian, QLocale::Belarus).toString(value, 'f', 2);
}


inline QString rate(double value)
{
    QString text = QLocale(QLocale::Russian, QLocale::Belarus).toString(value, 'f', 4);
    return text;
}

} 