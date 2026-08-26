from pathlib import Path

p = Path('src/EnglishLoop.tsx')
s = p.read_text(encoding='utf-8')

# Add state for iterative refinement after the first generated draft.
s = s.replace(
'''  const [generated, setGenerated] = useState(false);\n\n  useEffect(() => {''',
'''  const [generated, setGenerated] = useState(false);\n  const [refineNote, setRefineNote] = useState(\"\");\n  const [previewVersion, setPreviewVersion] = useState(1);\n\n  useEffect(() => {'''
)

refine_logic = r'''  const refineHomework = (instruction) => {
    const raw = (instruction || refineNote).trim();
    if (!raw) return;
    const note = raw.toLowerCase();
    const harder = note.includes("сложнее") || note.includes("усложни") || note.includes("harder") || note.includes("challenge");
    const easier = note.includes("легче") || note.includes("проще") || note.includes("облегчи") || note.includes("easier") || note.includes("simpler");
    const diversify = note.includes("разнообраз") || note.includes("другой вариант") || note.includes("другие задания") || note.includes("divers");
    const level = (note.match(/\\b(a1|a2|b1|b2|c1|c2)\\b/i) || [])[1]?.toUpperCase();

    let next = blocks.map((b) => ({ ...b }));

    if (diversify) {
      next = next.map((b) => {
        const pool = GENERATED_VARIANTS[b.type] || [];
        if (!pool.length) return b;
        const currentPrompt = b.prompt || b.subtitle || "";
        const candidates = pool.filter((v) => (v.prompt || v.subtitle || "") !== currentPrompt);
        const variant = (candidates.length ? candidates : pool)[generationRound % (candidates.length || pool.length)];
        return { ...b, ...variant, key: b.key };
      });
      setGenerationRound((x) => x + 1);
    }

    next = next.map((b) => {
      let out = { ...b };
      if (harder) {
        if (b.type === "speaking") out = { ...out, minutes: Math.max(12, (b.minutes || 8) + 3), subtitle: `Challenge · ${b.subtitle || "Speaking"}`, target: "Speak for 3 minutes without notes, develop your answer with examples, and use at least 5 target expressions naturally." };
        if (b.type === "writing") out = { ...out, minutes: Math.max(12, (b.minutes || 10) + 2), reqs: Array.from(new Set([...(b.reqs || []), "use at least five target expressions", "include one complex conditional sentence"])) };
        if (b.type === "grammar") out = { ...out, minutes: (b.minutes || 7) + 2, settings: { ...(b.settings || {}), count: Math.max(8, ((b.settings || {}).count || 6) + 2) } };
        if (b.type === "vocab") out = { ...out, minutes: (b.minutes || 8) + 2, settings: { ...(b.settings || {}), count: Math.max(10, ((b.settings || {}).count || 8) + 2) } };
      }
      if (easier) {
        if (b.type === "speaking") out = { ...out, minutes: Math.max(6, (b.minutes || 8) - 2), subtitle: `Guided · ${b.subtitle || "Speaking"}`, target: "Speak for 60–90 seconds. You may use the prompts and focus on 2–3 target expressions." };
        if (b.type === "writing") out = { ...out, minutes: Math.max(7, (b.minutes || 10) - 2), reqs: (b.reqs || []).slice(0, Math.max(2, Math.min(3, (b.reqs || []).length))) };
        if (b.type === "grammar") out = { ...out, minutes: Math.max(5, (b.minutes || 7) - 2), settings: { ...(b.settings || {}), count: Math.max(4, ((b.settings || {}).count || 6) - 2) } };
        if (b.type === "vocab") out = { ...out, minutes: Math.max(5, (b.minutes || 8) - 2), settings: { ...(b.settings || {}), count: Math.max(6, ((b.settings || {}).count || 8) - 2) } };
      }
      if (level) {
        const levelMinutes = { A1: 6, A2: 7, B1: 8, B2: 10, C1: 12, C2: 14 }[level] || b.minutes;
        out.minutes = Math.max(out.minutes || 0, levelMinutes);
        out.subtitle = `${out.subtitle || out.title} · ${level}`;
        if (out.type === "speaking") {
          const levelTargets = { A1: 2, A2: 2, B1: 3, B2: 4, C1: 5, C2: 6 }[level];
          out.target = `${level} target: speak continuously and use at least ${levelTargets} target expressions in your own examples.`;
        }
        if (out.type === "grammar") {
          const levelCount = { A1: 4, A2: 5, B1: 6, B2: 7, C1: 9, C2: 10 }[level];
          out.settings = { ...(out.settings || {}), count: levelCount };
        }
      }
      return { ...out, why: `${out.why || ""}${out.why ? " · " : ""}Tutor refinement: ${raw}` };
    });

    setBlocks(next);
    setGenerated(true);
    setPreviewVersion((x) => x + 1);
    notify(`Preview обновлён: ${raw}`);
  };

'''
if 'const refineHomework = (instruction) =>' not in s:
    s = s.replace('  const assign = () => {', refine_logic + '  const assign = () => {')

# Make the right-hand summary explicitly a preview while the draft is being edited.
s = s.replace(
'''      <div className="el-eyebrow">Homework for {s.name}</div>''',
'''      <div className="el-eyebrow">{generated ? `Preview · v${previewVersion}` : "Homework draft"} · {s.name}</div>'''
)

preview_panel = r'''
          {generated && (
            <section style={{ marginBottom: 26 }} className="el-fadein">
              <div className="el-card" style={{ padding: 18, borderColor: "#D8D4C8", background: "#FFFEFA" }}>
                <div style={{ display: "flex", justifyContent: "space-between", gap: 12, alignItems: "flex-start", flexWrap: "wrap" }}>
                  <div>
                    <div className="el-eyebrow" style={{ color: "var(--accent)" }}>Homework preview · version {previewVersion}</div>
                    <h2 style={{ fontSize: 18, fontWeight: 600, margin: "5px 0 5px" }}>Посмотрите черновик и уточните его</h2>
                    <p style={{ fontSize: 13.5, color: "var(--ink2)", margin: 0, maxWidth: 620 }}>
                      Ни одно изменение ещё не отправлено ученику. Можно несколько раз менять сложность, уровень и состав заданий, а затем нажать Assign.
                    </p>
                  </div>
                  <span className="el-pill" style={{ background: "var(--sunk)", color: "var(--ink2)" }}>Not assigned</span>
                </div>

                <div style={{ display: "flex", gap: 7, flexWrap: "wrap", marginTop: 14 }}>
                  {["Сделай сложнее", "Сделай легче", "Разнообразь", "Уровень B1", "Уровень B2", "Уровень C1"].map((x) => (
                    <button key={x} className="el-chip" onClick={() => refineHomework(x)}>{x}</button>
                  ))}
                </div>

                <div style={{ display: "grid", gridTemplateColumns: narrow ? "1fr" : "1fr auto", gap: 9, alignItems: "end", marginTop: 12 }}>
                  <label>
                    <div className="el-eyebrow" style={{ marginBottom: 6 }}>Что изменить в этой версии?</div>
                    <textarea className="el-ta" rows={2} value={refineNote} onChange={(e) => setRefineNote(e.target.value)}
                      placeholder="Например: speaking оставь сложным, writing сделай короче, добавь больше бытовых ситуаций, уровень B2…" />
                  </label>
                  <button className="el-btn el-p" disabled={!refineNote.trim()} onClick={() => refineHomework(refineNote)} style={{ minHeight: 42 }}>
                    <Sparkles size={15} /> Update preview
                  </button>
                </div>
              </div>
            </section>
          )}

'''
marker = '''          <section style={{ marginBottom: 30 }}>\n            <h2 style={{ fontSize: 15.5, fontWeight: 600, margin: "0 0 4px" }}>Goals for this homework</h2>'''
if 'Homework preview · version {previewVersion}' not in s:
    s = s.replace(marker, preview_panel + marker)

p.write_text(s, encoding='utf-8')
