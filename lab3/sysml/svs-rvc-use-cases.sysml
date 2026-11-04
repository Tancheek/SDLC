package 'SVS-RVC Business' {
    private import ScalarValues::*;

    /* Система, для которой формулируются бизнес-требования. */
    part def 'SVS-RVC Application' {
        attribute renderMinutes : Real;
        attribute vocalistSessions : Integer;
        attribute listenerRecognitionRatio : Real;
        attribute intelligibilityScore : Real;
        attribute offline : Boolean;
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
            doc /* Импортировать, проверять и версионировать RVC-модели. */
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

    requirement def 'BG-2 Remove vocalist session' {
        subject app : 'SVS-RVC Application';
        doc /* Убрать сессию вокалиста из чернового этапа. */
        require constraint { app.vocalistSessions == 0 }
    }

    requirement def 'BG-3 Target timbre' {
        subject app : 'SVS-RVC Application';
        doc /* Получить целевой тембр без исполнителя при разборчивом тексте. */
        require constraint { app.listenerRecognitionRatio >= 0.66 }
        require constraint { app.intelligibilityScore >= 4.0 }
    }

    requirement def 'BG-4 Local and confidential' {
        subject app : 'SVS-RVC Application';
        doc /* Обеспечить локальную обработку и конфиденциальность данных. */
        require constraint { app.offline == true }
    }

    requirement def 'BR-01 Demo in one session' {
        subject app : 'SVS-RVC Application';
        doc /* BR-01: демо-партия на 3 минуты создаётся за один рабочий сеанс не дольше 30 минут. */
        require constraint { app.renderMinutes <= 30.0 }
    }

    requirement def 'BR-02 No vocalist session' {
        subject app : 'SVS-RVC Application';
        doc /* BR-02: черновое демо создаётся без сессии вокалиста. */
        require constraint { app.vocalistSessions == 0 }
    }

    requirement def 'BR-03 Score and lyrics to audio' {
        subject app : 'SVS-RVC Application';
        doc /* BR-03: MIDI и лирика экспортируются в WAV/FLAC. */
    }

    requirement def 'BR-04 Timbre transfer' {
        subject app : 'SVS-RVC Application';
        doc /* BR-04: тембр переносится с сохранением мелодии и разборчивости слов. */
        require constraint { app.listenerRecognitionRatio >= 0.66 }
        require constraint { app.intelligibilityScore >= 4.0 }
    }

    requirement def 'BR-05 Local processing' {
        subject app : 'SVS-RVC Application';
        doc /* BR-05: синтез, модели и голосовые данные обрабатываются локально. */
        require constraint { app.offline == true }
    }

    requirement def 'BR-06 GUI scenario' {
        subject app : 'SVS-RVC Application';
        doc /* BR-06: GUI обеспечивает импорт, рендер, прослушивание и экспорт. */
    }
}
