from pathlib import Path

p = Path('src/EnglishLoop.tsx')
s = p.read_text(encoding='utf-8')

s = s.replace('{ id: "ahav", name: "Ahav", tracks:', '{ id: "ahav", name: "Stepan Miller", tracks:')
s = s.replace('Good evening, Ahav', 'Good evening, Stepan')

packs = r'''
const GENERATED_HOMEWORK_PACKS = [
  {
    goals: [GOALS[0], GOALS[1], GOALS[2]],
    speaking: {
      subtitle: "Changed plans · 2 minutes",
      prompt: "Tell me about a day when your plans changed at the last minute. What happened, what did you do first, and how did the situation end?",
      target: "Speak for 2 minutes without notes and use at least 4 target expressions.",
      targets: ["eventually", "in advance", "look into", "keep going", "despite", "put off"],
      why: "На последних попытках свободная речь замедлялась после 40–60 секунд",
    },
    writing: {
      subtitle: "A decision you would change · 130–160 words",
      prompt: "Write about a decision you made in the past that you would change now.",
      reqs: ["130–160 words", "use Third Conditional at least twice", "use three target expressions", "check articles and sentence structure"],
      why: "Third Conditional пока требует осознанного контроля",
    },
    grammar: { subtitle: "Third Conditional · Passive · until", focus: ["Third Conditional", "Passive Voice", "until / as soon as"], why: "Повторяем конструкции, где были ошибки и паузы", settings: { count: 6 }, minutes: 8 },
    vocab: { subtitle: "Russian → English · 9 expressions", settings: { direction: "Russian → English", count: 9 }, why: "eventually, carry out и look into ещё не полностью автоматизированы", minutes: 8 },
  },
  {
    goals: [GOALS[0], GOALS[3], GOALS[4]],
    speaking: {
      subtitle: "Work under pressure · 2–3 minutes",
      prompt: "Describe a situation at work when several problems appeared at once. Explain what you looked into first, what you put off, and how you eventually solved it.",
      target: "Speak for 2–3 minutes and use at least 5 target expressions naturally.",
      targets: ["look into", "put off", "eventually", "carry out", "in advance", "against the odds"],
      why: "Нужна более длинная спонтанная речь без подготовленного текста",
    },
    writing: {
      subtitle: "When a project went wrong · 140–170 words",
      prompt: "Write about a project that looked like a failure at first but later turned out to be a turning point.",
      reqs: ["140–170 words", "use at least four target expressions", "include one Passive Voice sentence", "include one Third Conditional sentence"],
      why: "Переносим активные выражения из recall в свободное письмо",
    },
    grammar: { subtitle: "Passive · Third Conditional · before/as soon as", focus: ["Passive Voice", "Third Conditional", "before / as soon as"], why: "Смешиваем уже изученные конструкции в новом контексте", settings: { count: 7 }, minutes: 9 },
    vocab: { subtitle: "Mixed recall · 10 expressions", settings: { direction: "Russian → English", count: 10 }, why: "Слабые выражения повторяются чаще, уверенные — реже", minutes: 9 },
  },
  {
    goals: [GOALS[0], GOALS[1], GOALS[3]],
    speaking: {
      subtitle: "A difficult choice · 2 minutes",
      prompt: "Tell me about a time when you had to think twice before stepping in. What were the risks, what did you decide, and what happened eventually?",
      target: "Speak continuously for 2 minutes and use 4–5 target expressions without prompts.",
      targets: ["think twice before stepping in", "step in", "eventually", "reach an agreement", "despite", "in advance"],
      why: "Отрабатываем быстрый доступ к выражениям в новом сюжете",
    },
    writing: {
      subtitle: "A conflict resolved · 120–150 words",
      prompt: "Write about a disagreement that was eventually resolved. Explain how the people reached an agreement.",
      reqs: ["120–150 words", "use at least three target expressions", "use despite correctly", "include one conditional sentence"],
      why: "despite и условные конструкции должны появляться без подсказки",
    },
    grammar: { subtitle: "despite · keep/keeps · conditionals", focus: ["despite + noun/gerund", "keep / keeps", "Conditionals"], why: "Точечно повторяем текущие ошибки из speaking", settings: { count: 6 }, minutes: 8 },
    vocab: { subtitle: "Active recall · 8 expressions", settings: { direction: "Russian → English", count: 8 }, why: "Автоматизация выражений, которые ещё вызывают паузу", minutes: 7 },
  },
];

'''
if 'const GENERATED_HOMEWORK_PACKS = [' not in s:
    s = s.replace('const STUDENTS = [', packs + 'const STUDENTS = [')

s = s.replace(
'''  const [recSec, setRecSec] = useState(0);\n\n  useEffect(() => {''',
'''  const [recSec, setRecSec] = useState(0);\n  const [generationNo, setGenerationNo] = useState(-1);\n  const [justGenerated, setJustGenerated] = useState(false);\n\n  useEffect(() => {''')

generator_logic = r'''  const buildGeneratedBlocks = (pack) => LIBRARY.map((base) => {
    const custom = pack[base.type] || {};
    return {
      ...base,
      ...custom,
      settings: custom.settings ? { ...(base.settings || {}), ...custom.settings } : base.settings,
      key: `${base.id}-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
    };
  });

  const generateHomework = () => {
    const next = (generationNo + 1) % GENERATED_HOMEWORK_PACKS.length;
    const pack = GENERATED_HOMEWORK_PACKS[next];
    setGenerationNo(next);
    setGoals(pack.goals);
    setBlocks(buildGeneratedBlocks(pack));
    setEditing(null);
    setJustGenerated(true);
    notify(`Новая практика для ${s.name} сгенерирована`);
    setTimeout(() => setJustGenerated(false), 1800);
  };

  const regenerateBlock = (key) => {
    const next = (generationNo + 1) % GENERATED_HOMEWORK_PACKS.length;
    const pack = GENERATED_HOMEWORK_PACKS[next];
    setGenerationNo(next);
    setBlocks((current) => current.map((b) => {
      if (b.key !== key) return b;
      const custom = pack[b.type] || {};
      return { ...b, ...custom, settings: custom.settings ? { ...(b.settings || {}), ...custom.settings } : b.settings };
    }));
    setJustGenerated(true);
    setTimeout(() => setJustGenerated(false), 1200);
  };

'''
if 'const generateHomework = () =>' not in s:
    s = s.replace(
        '  const missing = LIBRARY.filter((l) => !blocks.some((b) => b.type === l.type));\n\n  const assign = () => {',
        '  const missing = LIBRARY.filter((l) => !blocks.some((b) => b.type === l.type));\n\n' + generator_logic + '  const assign = () => {'
    )

s = s.replace(
'''      <div className="el-eyebrow">Homework for {s.name}</div>\n      <div style={{ marginTop: 14, display: "grid", gap: 9 }}>''',
'''      <div className="el-eyebrow">Homework for {s.name}</div>\n      <div style={{ marginTop: 8, fontSize: 12.5, color: "var(--accent)", display: "flex", gap: 6, alignItems: "center" }}>\n        <Sparkles size={12} /> AI-generated draft · tutor approval required\n      </div>\n      <div style={{ marginTop: 14, display: "grid", gap: 9 }}>''')

hero = r'''      <p style={{ color: "var(--ink2)", marginTop: 0, marginBottom: 18 }}>
        Система сама собирает новую практику по текущим целям и слабым местам ученика. Преподавателю остаётся проверить и нажать Assign.
      </p>

      <div className="el-card" style={{ padding: 18, marginBottom: 22, background: "var(--soft)", borderColor: "#CFE0D9" }}>
        <div style={{ display: "flex", alignItems: narrow ? "stretch" : "center", flexDirection: narrow ? "column" : "row", gap: 14 }}>
          <div style={{ flex: 1 }}>
            <div className="el-eyebrow" style={{ color: "var(--accent)" }}>Based on Stepan Miller's recent practice</div>
            <div style={{ fontSize: 14, marginTop: 7, color: "var(--ink2)", lineHeight: 1.55 }}>
              13 active expressions · speaking slows after 40–60 sec · Third Conditional needs practice · Passive Voice errors
            </div>
          </div>
          <button className="el-btn el-p" onClick={generateHomework} style={{ padding: "12px 16px", fontSize: 14.5 }}>
            <Sparkles size={16} /> {generationNo < 0 ? "Generate homework" : "Generate again"}
          </button>
        </div>
        {justGenerated && (
          <div className="el-fadein" style={{ fontSize: 12.5, color: "var(--accent)", marginTop: 10 }}>
            New prompts and exercises generated from the same learning goals.
          </div>
        )}
      </div>

'''
s = s.replace(
'''      <p style={{ color: "var(--ink2)", marginTop: 0, marginBottom: 26 }}>
        Соберите практику за две минуты. Всё уже предзаполнено по прошлому занятию — правьте только то, что нужно.
      </p>

''', hero)

s = s.replace(
'''                  onMove={move} onRemove={removeBlock} patch={patch} />''',
'''                  onMove={move} onRemove={removeBlock} onRegenerate={regenerateBlock} patch={patch} />''')
s = s.replace(
'function BlockCard({ b, i, last, open, onToggle, onMove, onRemove, patch }) {',
'function BlockCard({ b, i, last, open, onToggle, onMove, onRemove, onRegenerate, patch }) {')
s = s.replace(
'''          <button className="el-btn el-q" title="Изменить" onClick={onToggle}><Pencil size={14} /></button>''',
'''          <button className="el-btn el-q" title="Сгенерировать другой вариант" onClick={() => onRegenerate(b.key)}><Sparkles size={14} /></button>\n          <button className="el-btn el-q" title="Изменить" onClick={onToggle}><Pencil size={14} /></button>''')

p.write_text(s, encoding='utf-8')
