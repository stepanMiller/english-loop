from pathlib import Path

p = Path('src/EnglishLoop.tsx')
s = p.read_text(encoding='utf-8')

# Use the demo student's requested display name.
s = s.replace('name: "Stepan Miller"', 'name: "Степан Миллер"')
s = s.replace("Based on Stepan Miller's recent practice", "На основе последней практики Степана Миллера")

# Add a free-text tutor instruction state to the generated-homework flow.
s = s.replace(
'''  const [generationNo, setGenerationNo] = useState(-1);\n  const [justGenerated, setJustGenerated] = useState(false);\n\n  useEffect(() => {''',
'''  const [generationNo, setGenerationNo] = useState(-1);\n  const [justGenerated, setJustGenerated] = useState(false);\n  const [tutorNote, setTutorNote] = useState(\"\");\n\n  useEffect(() => {'''
)

# Apply simple demo rules so tutor comments visibly affect the generated draft.
apply_logic = r'''  const applyTutorInstruction = (draft) => {
    const note = tutorNote.trim().toLowerCase();
    let out = draft.map((b) => ({ ...b }));
    if (!note) return out;

    const wantsNoWriting = note.includes("без writing") || note.includes("no writing") || note.includes("убери writing") || note.includes("без письма");
    const wantsNoGrammar = note.includes("без grammar") || note.includes("no grammar") || note.includes("убери grammar");
    const wantsMoreSpeaking = note.includes("больше speaking") || note.includes("more speaking") || note.includes("упор на speaking") || note.includes("больше говор");
    const wantsPassive = note.includes("passive") || note.includes("пассив");
    const wantsThird = note.includes("third conditional") || note.includes("3 conditional") || note.includes("третий conditional");

    if (wantsNoWriting) out = out.filter((b) => b.type !== "writing");
    if (wantsNoGrammar) out = out.filter((b) => b.type !== "grammar");

    out = out.map((b) => {
      if (b.type === "speaking" && wantsMoreSpeaking) {
        return { ...b, minutes: Math.max(12, b.minutes), subtitle: "Extended speaking · 3 minutes", target: "Speak for 3 minutes without notes and use at least 4 target expressions." };
      }
      if (b.type === "grammar" && wantsPassive) {
        return { ...b, focus: Array.from(new Set(["Passive Voice", ...(b.focus || [])])), subtitle: `Passive · ${b.subtitle}` };
      }
      if (b.type === "writing" && wantsPassive) {
        return { ...b, reqs: Array.from(new Set([...(b.reqs || []), "include one Passive Voice sentence"])) };
      }
      if (b.type === "grammar" && wantsThird) {
        return { ...b, focus: Array.from(new Set(["Third Conditional", ...(b.focus || [])])) };
      }
      if (b.type === "writing" && wantsThird) {
        return { ...b, reqs: Array.from(new Set(["use Third Conditional at least once", ...(b.reqs || [])])) };
      }
      return b;
    });

    const timeMatch = note.match(/(\\d{2})\\s*(?:мин|minutes?|min)/);
    if (timeMatch) {
      const target = Math.max(15, Math.min(60, Number(timeMatch[1])));
      const total = out.reduce((sum, b) => sum + (b.minutes || 0), 0);
      if (total > 0 && Math.abs(total - target) > 2) {
        const factor = target / total;
        out = out.map((b) => ({ ...b, minutes: Math.max(4, Math.round((b.minutes || 5) * factor)) }));
      }
    }

    return out;
  };

'''
if 'const applyTutorInstruction = (draft) =>' not in s:
    s = s.replace(
'''  const generateHomework = () => {''',
apply_logic + '''  const generateHomework = () => {'''
    )

s = s.replace('setBlocks(buildGeneratedBlocks(pack));', 'setBlocks(applyTutorInstruction(buildGeneratedBlocks(pack)));')

# Preserve the tutor instruction with the assigned homework for the demo.
s = s.replace(
'goals, tasks: blocks.map(({ key, ...b }) => b), voice, submission: {}, feedback: null, createdAt: Date.now(),',
'goals, tasks: blocks.map(({ key, ...b }) => b), voice, tutorNote: tutorNote.trim() || null, submission: {}, feedback: null, createdAt: Date.now(),'
)

# Add a tutor instruction box to the existing AI generation card.
needle = '''            <div style={{ fontSize: 14, marginTop: 7, color: "var(--ink2)", lineHeight: 1.55 }}>\n              13 active expressions · speaking slows after 40–60 sec · Third Conditional needs practice · Passive Voice errors\n            </div>\n          </div>\n          <button className="el-btn el-p" onClick={generateHomework} style={{ padding: "12px 16px", fontSize: 14.5 }}>'''
replacement = '''            <div style={{ fontSize: 14, marginTop: 7, color: "var(--ink2)", lineHeight: 1.55 }}>\n              13 active expressions · speaking slows after 40–60 sec · Third Conditional needs practice · Passive Voice errors\n            </div>\n            <label style={{ display: "block", marginTop: 13 }}>\n              <div className="el-eyebrow" style={{ marginBottom: 6 }}>Комментарий преподавателя · необязательно</div>\n              <textarea className="el-ta" rows={2} value={tutorNote} onChange={(e) => setTutorNote(e.target.value)}\n                placeholder="Например: больше speaking, добавь Passive Voice, без writing, примерно 30 минут…" />\n            </label>\n            <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginTop: 8 }}>\n              {["Больше speaking", "Добавь Passive Voice", "Third Conditional", "Без writing", "Примерно 30 минут"].map((x) => (\n                <button key={x} className="el-chip" onClick={() => setTutorNote((v) => v ? `${v}; ${x}` : x)}>{x}</button>\n              ))}\n            </div>\n          </div>\n          <button className="el-btn el-p" onClick={generateHomework} style={{ padding: "12px 16px", fontSize: 14.5 }}>'''
s = s.replace(needle, replacement)

# Echo back the instruction after generation so the effect is obvious in the demo.
s = s.replace(
'''            New prompts and exercises generated from the same learning goals.\n          </div>''',
'''            New prompts and exercises generated from the same learning goals.{tutorNote.trim() ? ` Учтено: ${tutorNote.trim()}` : ""}\n          </div>'''
)

p.write_text(s, encoding='utf-8')
