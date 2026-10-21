#include "model/CurrencyModel.h"

#include <algorithm>
#include <cmath>
#include <limits>
#include <stdexcept>

void CurrencyModel::addListener(Listener *listener)
{
    if (listener == nullptr) {
        return;
    }
    if (std::find(m_listeners.begin(), m_listeners.end(), listener) == m_listeners.end()) {
        m_listeners.push_back(listener);
    }
}

void CurrencyModel::removeListener(Listener *listener)
{
    m_listeners.erase(std::remove(m_listeners.begin(), m_listeners.end(), listener),
                      m_listeners.end());
}

void CurrencyModel::convert(double amountByn, double euroRate)
{
    validate(amountByn, euroRate);

    const double euroAmountRaw = amountByn / euroRate;
    const double euroAmountRounded = std::round(euroAmountRaw * 100.0) / 100.0;

    m_amountByn = amountByn;
    m_euroRate = euroRate;
    m_resultEur = euroAmountRounded;
    m_hasData = true;

    notifyListeners();
}

void CurrencyModel::validate(double amountByn, double euroRate) const
{
    if (!std::isfinite(amountByn) || !std::isfinite(euroRate)) {
        throw std::invalid_argument("Введённые значения должны быть числами.");
    }
    if (amountByn < kMinAmount) {
        throw std::invalid_argument("Сумма должна быть положительным числом "
                                    "(не меньше 0,01 BYN).");
    }
    if (amountByn > kMaxAmount) {
        throw std::invalid_argument("Сумма слишком велика: не более 1 000 000 000 BYN.");
    }
    if (euroRate < kMinRate) {
        throw std::invalid_argument("Курс евро должен быть положительным числом "
                                    "(не меньше 0,0001 BYN за 1 EUR).");
    }
    if (euroRate > kMaxRate) {
        throw std::invalid_argument("Курс евро слишком велик: не более 100 000 BYN за 1 EUR.");
    }
}

void CurrencyModel::notifyListeners()
{
    for (Listener *listener : m_listeners) {
        if (listener != nullptr) {
            listener->onModelChanged();
        }
    }
}