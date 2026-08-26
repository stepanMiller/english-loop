from pathlib import Path

p = Path('src/EnglishLoop.tsx')
s = p.read_text(encoding='utf-8')

# 1) Ensure preview/refinement state is actually declared inside CreateHomework.
if 'const [generated, setGenerated] = useState(false);' not in s:
    anchor = '  const [tutorNote, setTutorNote] = useState("");\n\n  useEffect(() => {'
    replacement = '''  const [tutorNote, setTutorNote] = useState("");
  const [generated, setGenerated] = useState(false);
  const [refineNote, setRefineNote] = useState("");
  const [previewVersion, setPreviewVersion] = useState(1);

  useEffect(() => {'''
    if anchor not in s:
        raise RuntimeError('Could not find tutorNote hook anchor for preview state')
    s = s.replace(anchor, replacement, 1)

# 2) A fresh generation should open Preview v1.
gen_anchor = '    setBlocks(applyTutorInstruction(buildGeneratedBlocks(pack)));\n    setEditing(null);'
if gen_anchor in s:
    s = s.replace(
        gen_anchor,
        '    setBlocks(applyTutorInstruction(buildGeneratedBlocks(pack)));\n    setGenerated(true);\n    setPreviewVersion(1);\n    setRefineNote("");\n    setEditing(null);',
        1,
    )

# 3) Replace the broken diversify implementation with the existing generated packs.
broken = '''    if (diversify) {
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
'''
fixed = '''    if (diversify) {
      const baseIndex = generationNo >= 0 ? generationNo : 0;
      const pack = GENERATED_HOMEWORK_PACKS[(baseIndex + previewVersion) % GENERATED_HOMEWORK_PACKS.length];
      next = next.map((b) => {
        const variant = pack[b.type] || {};
        return {
          ...b,
          ...variant,
          settings: variant.settings ? { ...(b.settings || {}), ...variant.settings } : b.settings,
          key: b.key,
        };
      });
    }
'''
if broken in s:
    s = s.replace(broken, fixed, 1)

# Fail the build instead of publishing another browser-only runtime crash.
required = [
    'const [generated, setGenerated] = useState(false);',
    'const [refineNote, setRefineNote] = useState("");',
    'const [previewVersion, setPreviewVersion] = useState(1);',
    'const refineHomework = (instruction) =>',
]
for item in required:
    if item not in s:
        raise RuntimeError(f'Missing required preview code: {item}')

if 'GENERATED_VARIANTS' in s or 'generationRound' in s or 'setGenerationRound' in s:
    raise RuntimeError('Undefined preview generation identifiers remain in source')

p.write_text(s, encoding='utf-8')
