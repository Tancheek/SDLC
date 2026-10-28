package 'SVS-RVC UI' {
    private import ScalarValues::*;

    /* Структура GUI, соответствующая мокапам lab3/mockups/*.png. */
    part def 'SVS-RVC GUI' {
        part mainWindow : 'Main Window';
        part renderDialog : 'Render Dialog'[0..1];
        part liveMonitor : 'Live Monitor'[0..1];
        part modelManager : 'Model Manager'[0..1];
    }

    part def 'Main Window' {
        attribute title : String;
        part projectTree : 'Project Tree';
        part scoreEditor : 'Score Editor';
        part lyricsPanel : 'Lyrics Panel';
        part voiceInspector : 'Voice Inspector';
        part transport : 'Transport';
        part statusBar : 'Status Bar';
    }

    part def 'Project Tree' {
        attribute items : String[*];
    }

    part def 'Score Editor' {
        attribute bars : Integer;
        attribute trackName : String;
        attribute tempo : Real;
        attribute timeSignature : String;
        part notes : 'Note'[*];
    }

    part def 'Note' {
        attribute pitch : String;
        attribute startBeat : Real;
        attribute durationBeats : Real;
        attribute syllable : String;
    }

    part def 'Lyrics Panel' {
        attribute text : String;
        attribute language : String;
        part syllables : String[*];
    }

    part def 'Voice Inspector' {
        part modelCard : 'Model Card';
        attribute transferStrength : Real;
        attribute pitchShiftSemitones : Real;
        attribute breathiness : Real;
        attribute formantShift : Real;
        attribute presetName : String;
    }

    part def 'Model Card' {
        attribute modelName : String;
        attribute sampleRate : Integer;
        attribute license : String;
        attribute consent : Boolean;
    }

    part def 'Transport' {
        attribute positionBar : Integer;
        attribute playing : Boolean;
        attribute rtf : Real;
        attribute cpuLoad : Real;
    }

    part def 'Status Bar' {
        attribute sampleRate : Integer;
        attribute audioBackend : String;
        attribute message : String;
    }

    part def 'Render Dialog' {
        attribute format : String;
        attribute bitDepth : Integer;
        attribute normalizeLoudness : Boolean;
        attribute exportStem : Boolean;
        attribute addWatermark : Boolean;
        attribute progressPercent : Real;
        attribute currentBar : Integer;
        attribute totalBars : Integer;
    }

    part def 'Live Monitor' {
        attribute latencyMilliseconds : Real;
        attribute bufferSamples : Integer;
        attribute xruns : Integer;
        attribute currentNote : String;
        part inputMeter : 'Level Meter';
        part outputMeter : 'Level Meter';
        part midiKeyboard : 'MIDI Keyboard';
    }

    part def 'Level Meter' {
        attribute levelDb : Real;
        attribute peakDb : Real;
    }

    part def 'MIDI Keyboard' {
        attribute octaveRange : String;
        attribute activeNotes : String[*];
    }

    part def 'Model Manager' {
        attribute searchQuery : String;
        part models : 'Model Card'[*];
        part importPanel : 'Import Panel';
    }

    part def 'Import Panel' {
        attribute checkpointPath : String;
        attribute indexPath : String;
        attribute validationStatus : String;
    }
}
