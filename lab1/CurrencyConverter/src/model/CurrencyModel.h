#pragma once

#include <vector>

class CurrencyModel
{
public:
    
    class Listener
    {
    public:
        virtual ~Listener() = default;

        
        virtual void onModelChanged() = 0;
    };

    // Границы допустимых значений 
    static constexpr double kMinAmount = 0.01;      // 1 копейка
    static constexpr double kMaxAmount = 1.0e9;     // 1 млрд BYN
    static constexpr double kMinRate = 1.0e-4;      // 0,0001 BYN за 1 EUR
    static constexpr double kMaxRate = 1.0e5;       // 100 000 BYN за 1 EUR

    CurrencyModel() = default;
    CurrencyModel(const CurrencyModel &) = delete;
    CurrencyModel &operator=(const CurrencyModel &) = delete;

    void addListener(Listener *listener);
    
    void removeListener(Listener *listener);

    void convert(double amountByn, double euroRate);

    bool hasData() const { return m_hasData; }
    double amountByn() const { return m_amountByn; }
    double euroRate() const { return m_euroRate; }
    double resultEur() const { return m_resultEur; }

private:
    void validate(double amountByn, double euroRate) const;
    void notifyListeners();

    std::vector<Listener *> m_listeners;

    bool m_hasData = false;
    double m_amountByn = 0.0;  
    double m_euroRate = 0.0;    
    double m_resultEur = 0.0;  
};