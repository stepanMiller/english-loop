from pathlib import Path

p = Path('src/EnglishLoop.tsx')
s = p.read_text(encoding='utf-8')

# Add an error/help state for real speech-to-text in Vocabulary Recall.
state_anchor = '''  const [listening, setListening] = useState(false);\n  const [fin, setFin] = useState(false);'''
state_replacement = '''  const [listening, setListening] = useState(false);\n  const [speechError, setSpeechError] = useState(\"\");\n  const [fin, setFin] = useState(false);'''
if state_anchor not in s:
    raise RuntimeError('Recall listening state anchor not found')
s = s.replace(state_anchor, state_replacement, 1)

# Reset any voice-input message when moving to the next recall item.
s = s.replace(
'''    else { setI(i + 1); setVal(\"\"); setState(null); setTried(false); }''',
'''    else { setI(i + 1); setVal(\"\"); setState(null); setTried(false); setSpeechError(\"\"); setListening(false); }''',
1,
)

# Replace the old fake voice demo (which inserted the correct answer) with real browser speech recognition.
old_speak = '''  const speak = () => {\n    setListening(true);\n    setTimeout(() => { setListening(false); setVal(it.en.replace(/^(\\w)/, (m) => m.toLowerCase()).replace(/\\.$/, \"\")); }, 1300);\n  };'''
new_speak = '''  const speak = () => {\n    if (listening) return;\n    setSpeechError(\"\");\n\n    const speechWindow = window as any;\n    const SpeechRecognition = speechWindow.SpeechRecognition || speechWindow.webkitSpeechRecognition;\n    if (!SpeechRecognition) {\n      setSpeechError(\"Voice input is not available in this browser. Type your answer instead.\");\n      return;\n    }\n\n    try {\n      const recognition = new SpeechRecognition();\n      recognition.lang = \"en-US\";\n      recognition.continuous = false;\n      recognition.interimResults = false;\n      recognition.maxAlternatives = 1;\n\n      recognition.onstart = () => setListening(true);\n      recognition.onresult = (event: any) => {\n        const transcript = event.results?.[0]?.[0]?.transcript?.trim() || \"\";\n        if (transcript) setVal(transcript);\n      };\n      recognition.onerror = (event: any) => {\n        const message = event.error === \"not-allowed\" || event.error === \"service-not-allowed\"\n          ? \"Microphone or speech recognition permission was denied. You can type the answer instead.\"\n          : event.error === \"no-speech\"\n            ? \"I didn't hear an answer. Tap the microphone and try again.\"\n            : \"Voice input didn't work. Tap the microphone to try again or type the answer.\";\n        setSpeechError(message);\n      };\n      recognition.onend = () => setListening(false);\n      recognition.start();\n    } catch {\n      setListening(false);\n      setSpeechError(\"Voice input couldn't start. Try again or type the answer.\");\n    }\n  };'''
if old_speak not in s:
    raise RuntimeError('Old fake Recall voice handler not found')
s = s.replace(old_speak, new_speak, 1)

# Replace the whole inactive-state action block so the help text is valid JSX.
actions = '''      {!state && (\n        <div style={{ display: \"flex\", gap: 10, marginTop: 14 }}>\n          <button className=\"el-btn el-g\" onClick={speak} style={listening ? { borderColor: \"var(--amber)\", color: \"var(--amber)\" } : undefined}>\n            <Mic size={15} /> {listening ? \"Слушаю…\" : \"Speak answer\"}\n          </button>\n          <button className=\"el-btn el-p\" style={{ flex: 1 }} disabled={!val.trim()} onClick={check}>Check</button>\n        </div>\n      )}'''
actions_new = '''      {!state && (\n        <>\n          <div style={{ display: \"flex\", gap: 10, marginTop: 14 }}>\n            <button className=\"el-btn el-g\" onClick={speak} disabled={listening} style={listening ? { borderColor: \"var(--amber)\", color: \"var(--amber)\" } : undefined}>\n              <Mic size={15} /> {listening ? \"Слушаю…\" : \"Speak answer\"}\n            </button>\n            <button className=\"el-btn el-p\" style={{ flex: 1 }} disabled={!val.trim() || listening} onClick={check}>Check</button>\n          </div>\n          {speechError && (\n            <div style={{ fontSize: 12.5, color: \"var(--amber)\", marginTop: 8, lineHeight: 1.4 }}>{speechError}</div>\n          )}\n        </>\n      )}'''
if actions not in s:
    raise RuntimeError('Recall voice action block not found')
s = s.replace(actions, actions_new, 1)

# Safety check: the correct-answer auto-fill must never remain in the built source.
for forbidden in ['setTimeout(() => { setListening(false); setVal(it.en', 'setVal(it.en.replace']:
    if forbidden in s:
        raise RuntimeError('Fake vocabulary answer autofill still present')

p.write_text(s, encoding='utf-8')
