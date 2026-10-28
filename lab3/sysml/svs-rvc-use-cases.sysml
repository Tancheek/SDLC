package 'SVS-RVC Business' {
    private import ScalarValues::*;

    /* Система, для которой формулируются бизнес-требования. */
    part def 'SVS-RVC Application' {
        attribute renderMinutes : Real;
        attribute demoCostRatio : Real;
        attribute timbreSimilarity : Real;
        attribute wordAccuracy : Real;
        attribute offline : Boolean;
        attribute consentConfirmed : Boolean;
        attribute latencyMilliseconds : Real;
        attribute exportFormat : String;
    }

    part def 'Composer';
    part def 'SoundEngineer';
    part def 'VoiceOwner';
    part def 'LegalReviewer';
    part def 'ModelOperator';
    part def 'Customer';

    use case def 'Create vocal demo' {
        subject app : 'SVS-RVC Application';
        actor composer : 'Composer';
        objective {
            doc /* Получить вокальную демо-партию за один рабочий сеанс без сессии вокалиста. */
        }
    }

    use case def 'Transfer target timbre' {
        subject app : 'SVS-RVC Application';
        actor composer : 'Composer';
        actor voiceOwner : 'VoiceOwner';
        objective {
            doc /* Перенести тембр целевого певца на партитуру с сохранением мелодии и слов. */
        }
    }

    use case def 'Monitor performance in real time' {
        subject app : 'SVS-RVC Application';
        actor composer : 'Composer';
        objective {
            doc /* Озвучить партию в реальном времени для быстрой оценки до финального рендера. */
        }
    }

    use case def 'Export to DAW' {
        subject app : 'SVS-RVC Application';
        actor soundEngineer : 'SoundEngineer';
        objective {
            doc /* Передать WAV/FLAC в DAW без дополнительной конвертации. */
        }
    }

    use case def 'Manage voice models' {
        subject app : 'SVS-RVC Application';
        actor modelOperator : 'ModelOperator';
        actor legalReviewer : 'LegalReviewer';
        objective {
            doc /* Импортировать, проверить и версионировать RVC-модели с согласиями владельцев. */
        }
    }

    use case def 'Accept demo' {
        subject app : 'SVS-RVC Application';
        actor customer : 'Customer';
        objective {
            doc /* Принять демо по естественности тембра и разборчивости лирики. */
        }
    }

    requirement def 'BG-1 Reduce demo time' {
        subject app : 'SVS-RVC Application';
        doc /* Сократить время создания вокального демо до одного рабочего сеанса. */
        require constraint { app.renderMinutes <= 30.0 }
    }

    requirement def 'BG-2 Reduce demo cost' {
        subject app : 'SVS-RVC Application';
        doc /* Снизить стоимость демо за счёт отказа от сессии вокалиста. */
        require constraint { app.demoCostRatio <= 0.3 }
    }

    requirement def 'BG-3 Access multiple timbres' {
        subject app : 'SVS-RVC Application';
        doc /* Дать доступ к разным тембрам без найма исполнителя. */
        require constraint { app.timbreSimilarity >= 0.75 }
    }

    requirement def 'BG-4 Legal cleanliness' {
        subject app : 'SVS-RVC Application';
        doc /* Обеспечить согласие владельца голоса и маркировку синтезированного аудио. */
        require constraint { app.consentConfirmed == true }
    }

    requirement def 'BR-01 Demo in one session' {
        subject app : 'SVS-RVC Application';
        doc /* BR-01: демо-партия на 3 минуты создаётся за один рабочий сеанс не дольше 30 минут. */
        require constraint { app.renderMinutes <= 30.0 }
    }

    requirement def 'BR-02 Lower recording cost' {
        subject app : 'SVS-RVC Application';
        doc /* BR-02: отказ от сессии вокалиста на этапе демо снижает стоимость записи не менее чем на 70 %. */
        require constraint { app.demoCostRatio <= 0.3 }
    }

    requirement def 'BR-03 Timbre transfer' {
        subject app : 'SVS-RVC Application';
        doc /* BR-03: тембр целевого певца переносится с сохранением мелодии и разборчивости слов. */
        require constraint { app.timbreSimilarity >= 0.75 }
        require constraint { app.wordAccuracy >= 0.9 }
    }

    requirement def 'BR-04 Local processing' {
        subject app : 'SVS-RVC Application';
        doc /* BR-04: обработка голоса и моделей выполняется локально, без передачи данных в облако. */
        require constraint { app.offline == true }
    }

    requirement def 'BR-05 Consent and marking' {
        subject app : 'SVS-RVC Application';
        doc /* BR-05: каждая модель имеет согласие владельца, а экспорт — маркировку «синтезировано». */
        require constraint { app.consentConfirmed == true }
    }

    requirement def 'BR-06 DAW-ready export' {
        subject app : 'SVS-RVC Application';
        doc /* BR-06: результат экспортируется в WAV/FLAC и открывается в DAW без конвертации. */
        require constraint { app.exportFormat == "WAV" }
    }

    requirement def 'BR-07 Live monitoring' {
        subject app : 'SVS-RVC Application';
        doc /* BR-07: live-мониторинг позволяет оценить партию при задержке не более 250 мс. */
        require constraint { app.latencyMilliseconds <= 250.0 }
    }

    requirement def 'BR-08 Voice library' {
        subject app : 'SVS-RVC Application';
        doc /* BR-08: библиотека тембров поддерживает импорт, проверку и откат версий RVC-моделей. */
    }

    requirement def 'BR-09 Render report' {
        subject app : 'SVS-RVC Application';
        doc /* BR-09: отчёт о рендере содержит модель, параметры и метрики качества для приёмки. */
    }
}
