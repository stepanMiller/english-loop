from pathlib import Path

p = Path('src/EnglishLoop.tsx')
s = p.read_text(encoding='utf-8')

# -------------------------------------------------------------------
# 1) Expand the demo generator: 12 complete homework variants total.
#    Weak target language intentionally recurs, but contexts/questions
#    and exercise items vary across generations.
# -------------------------------------------------------------------
if 'const EXTRA_GENERATED_HOMEWORK_PACKS = [' not in s:
    extra = r'''
const GENERATED_RECALL_POOLS = [
  [
    { ru: "Несмотря на критику, она продолжала работать над проектом.", en: "Despite being criticized, she kept going with the project.", key: ["despite being criticized", "kept going"] },
    { ru: "Мы всё подготовили заранее, но встречу всё равно перенесли.", en: "We prepared everything in advance, but the meeting was put off anyway.", key: ["in advance", "put off"] },
    { ru: "Я разберусь с этой проблемой сегодня вечером.", en: "I will look into this problem this evening.", key: ["look into"] },
    { ru: "В итоге нам пришлось вмешаться.", en: "Eventually we had to step in.", key: ["eventually", "step in"] },
    { ru: "Подумай дважды, прежде чем соглашаться.", en: "Think twice before agreeing.", key: ["think twice"] },
    { ru: "Команда смогла выполнить задачу вопреки всему.", en: "The team managed to carry out the task against the odds.", key: ["carry out", "against the odds"] },
    { ru: "Нам удалось прийти к соглашению к концу дня.", en: "We managed to reach an agreement by the end of the day.", key: ["reach an agreement"] },
    { ru: "Это наконец развеяло все мои сомнения.", en: "It finally cleared up all my doubts.", key: ["cleared up all my doubts"] },
  ],
  [
    { ru: "Как только документы будут готовы, отправь их заранее.", en: "As soon as the documents are ready, send them in advance.", key: ["as soon as", "in advance"] },
    { ru: "Мы отложили решение, чтобы сначала разобраться в деталях.", en: "We put off the decision so that we could look into the details first.", key: ["put off", "look into"] },
    { ru: "Несмотря на сложности, он продолжал двигаться к цели.", en: "Despite the difficulties, he kept going towards his goal.", key: ["despite", "kept going"] },
    { ru: "В конце концов руководителю пришлось вмешаться.", en: "Eventually the manager had to step in.", key: ["eventually", "step in"] },
    { ru: "Прежде чем вмешиваться, стоит дважды подумать.", en: "It is worth thinking twice before stepping in.", key: ["think twice", "stepping in"] },
    { ru: "Проверка была проведена вовремя.", en: "The review was carried out on time.", key: ["carried out"] },
    { ru: "Они всё-таки пришли к соглашению.", en: "They eventually reached an agreement.", key: ["eventually", "reached an agreement"] },
    { ru: "Его объяснение развеяло мои сомнения.", en: "His explanation cleared up my doubts.", key: ["cleared up my doubts"] },
  ],
  [
    { ru: "Я заранее предупредил команду об изменениях.", en: "I warned the team about the changes in advance.", key: ["in advance"] },
    { ru: "Вопрос нужно изучить до следующей встречи.", en: "The issue needs to be looked into before the next meeting.", key: ["looked into"] },
    { ru: "Встречу отменили в последний момент.", en: "The meeting was called off at the last moment.", key: ["called off", "last moment"] },
    { ru: "Несмотря на давление, мы не сдались.", en: "Despite the pressure, we did not give in.", key: ["despite", "give in"] },
    { ru: "Ситуация начала выходить из-под контроля.", en: "The situation started to get out of hand.", key: ["get out of hand"] },
    { ru: "В итоге это оказалось поворотным моментом.", en: "Eventually it turned out to be a turning point.", key: ["eventually", "turning point"] },
    { ru: "Нам пришлось вмешаться, чтобы решить конфликт.", en: "We had to step in to resolve the conflict.", key: ["step in"] },
    { ru: "Вопреки всему проект был завершён вовремя.", en: "Against the odds, the project was finished on time.", key: ["against the odds", "finished on time"] },
  ],
];

const GENERATED_GRAMMAR_POOLS = [
  [
    { s: "If they ___ us in advance, we would have prepared differently.", o: ["had warned", "warned", "would warn"], a: 0, tag: "Third Conditional", why: "Third Conditional: if + had + V3." },
    { s: "The final decision ___ before the client arrived.", o: ["had been made", "had made", "was making"], a: 0, tag: "Passive Voice", why: "Past perfect passive: had been + V3." },
    { s: "___ we reach an agreement, I will send the documents.", o: ["As soon as", "Despite", "Until"], a: 0, tag: "as soon as", why: "After as soon as, use Present Simple for future meaning." },
    { s: "We won't leave ___ the issue is completely clear.", o: ["until", "despite", "before"], a: 0, tag: "until", why: "Not ... until = не ... пока не." },
    { s: "Despite ___ criticized, she kept going.", o: ["being", "be", "was"], a: 0, tag: "despite", why: "Despite can be followed by a gerund: despite being criticized." },
    { s: "If I had looked into it earlier, I ___ the mistake.", o: ["would have noticed", "would notice", "noticed"], a: 0, tag: "Third Conditional", why: "Result clause: would have + V3." },
  ],
  [
    { s: "The meeting ___ at the last moment because the speaker was ill.", o: ["was called off", "called off", "had calling off"], a: 0, tag: "Passive Voice", why: "The meeting receives the action, so use passive voice." },
    { s: "If we ___ twice before stepping in, the conflict might not have escalated.", o: ["had thought", "thought", "would think"], a: 0, tag: "Third Conditional", why: "Unreal past condition: had + V3." },
    { s: "Call me ___ you have cleared up all the details.", o: ["as soon as", "despite", "until"], a: 0, tag: "as soon as", why: "As soon as introduces the earlier future event." },
    { s: "He kept ___ towards his goal despite the criticism.", o: ["going", "go", "to go"], a: 0, tag: "keep going", why: "Keep + gerund: keep going." },
    { s: "The task should ___ by Friday.", o: ["be carried out", "carry out", "be carry out"], a: 0, tag: "Passive Voice", why: "Modal passive: should be + V3." },
    { s: "If she had given in, things ___ different now.", o: ["would be", "would have been", "are"], a: 0, tag: "Mixed Conditional", why: "Past condition with a present result: would be." },
  ],
  [
    { s: "If the project ___ on time, we would have avoided the penalty.", o: ["had been finished", "was finished", "had finished"], a: 0, tag: "Third Conditional + Passive", why: "Past unreal condition in passive: had been + V3." },
    { s: "We had prepared everything ___, so the change was manageable.", o: ["in advance", "eventually", "until"], a: 0, tag: "in advance", why: "In advance means beforehand." },
    { s: "I didn't step in ___ the discussion got out of hand.", o: ["until", "as soon as", "despite"], a: 0, tag: "until", why: "The intervention happened only after that point." },
    { s: "Despite ___ like a failure at first, it became a turning point.", o: ["looking", "looked", "to look"], a: 0, tag: "despite", why: "Despite + gerund works here: despite looking." },
    { s: "The problem ___ into before the final decision was made.", o: ["had been looked", "had looked", "was looking"], a: 0, tag: "Passive Voice", why: "The problem receives the action: had been looked into." },
    { s: "If I had known earlier, I ___ the meeting off.", o: ["would have put", "would put", "put"], a: 0, tag: "Third Conditional", why: "Would have + V3 in the result clause." },
  ],
];

const EXTRA_GENERATED_HOMEWORK_PACKS = [
  {
    goals: [GOALS[0], GOALS[1], GOALS[4]],
    speaking: { subtitle: "A decision under pressure · 2 minutes", prompt: "Tell me about a decision you had to make quickly when you did not have all the information. What did you look into, what did you put off, and what happened eventually?", target: "Speak for 2 minutes and use at least 4 target expressions naturally.", targets: ["look into", "put off", "eventually", "in advance", "think twice", "reach an agreement"], why: "Новый контекст для тех же активных выражений" },
    writing: { subtitle: "A plan that changed · 130–160 words", prompt: "Write about a plan that changed unexpectedly and explain what you would have done differently if you had known earlier.", reqs: ["130–160 words", "use Third Conditional twice", "use four target expressions", "include one Passive Voice sentence"], targets: ["in advance", "eventually", "look into", "put off", "despite", "turning point"], why: "Связываем лексику с Third Conditional" },
    grammar: { subtitle: "Third Conditional · Passive · despite", focus: ["Third Conditional", "Passive Voice", "despite"], settings: { count: 6 }, items: GENERATED_GRAMMAR_POOLS[0], minutes: 8, why: "Новый набор предложений вместо повторения старых" },
    vocab: { subtitle: "New contexts · 8 expressions", settings: { direction: "Russian → English", count: 8 }, items: GENERATED_RECALL_POOLS[0], minutes: 8, why: "Те же цели, но новые предложения" },
  },
  {
    goals: [GOALS[0], GOALS[3], GOALS[2]],
    speaking: { subtitle: "When you stepped in · 2–3 minutes", prompt: "Describe a situation when you decided to step in because something was getting out of hand. Why did you hesitate, what did you do, and how did it end?", target: "Speak for 2–3 minutes without notes and use 5 target expressions.", targets: ["step in", "get out of hand", "think twice", "eventually", "against the odds", "keep going"], why: "Тренируем спонтанный рассказ через другой сюжет" },
    writing: { subtitle: "A conflict at work · 140–170 words", prompt: "Write about a disagreement at work that was difficult to resolve but eventually ended in an agreement.", reqs: ["140–170 words", "use at least four target expressions", "include one conditional", "use despite correctly"], targets: ["reach an agreement", "eventually", "step in", "despite", "look into", "in advance"], why: "Переносим выражения в деловой контекст" },
    grammar: { subtitle: "Conditionals · keep going · Passive", focus: ["Conditionals", "keep + gerund", "Passive Voice"], settings: { count: 6 }, items: GENERATED_GRAMMAR_POOLS[1], minutes: 9, why: "Смешанный набор по текущим слабым местам" },
    vocab: { subtitle: "Mixed recall · 8 expressions", settings: { direction: "Russian → English", count: 8 }, items: GENERATED_RECALL_POOLS[1], minutes: 8, why: "Выражения повторяются в новых формулировках" },
  },
  {
    goals: [GOALS[0], GOALS[1], GOALS[3]],
    speaking: { subtitle: "A project that looked doomed · 2 minutes", prompt: "Tell me about something that looked like a failure at first but later turned out to be useful or even a turning point.", target: "Speak continuously for 2 minutes and develop the story with a clear beginning, change, and result.", targets: ["turn out to be a turning point", "eventually", "against the odds", "keep going", "in advance", "despite"], why: "Новый сюжет с теми же автоматизируемыми связками" },
    writing: { subtitle: "Against the odds · 130–160 words", prompt: "Write about a difficult goal you achieved against the odds. Explain what almost made you give in and what kept you going.", reqs: ["130–160 words", "use at least four target expressions", "include a sentence with despite", "include one past conditional"], targets: ["against the odds", "give in", "keep going", "eventually", "despite", "in advance"], why: "Контекст достижения цели вместо работы с клиентом" },
    grammar: { subtitle: "Mixed Conditional · Passive · until", focus: ["Mixed Conditional", "Passive Voice", "until"], settings: { count: 6 }, items: GENERATED_GRAMMAR_POOLS[2], minutes: 8, why: "Другой набор грамматических контекстов" },
    vocab: { subtitle: "Active recall · 8 new contexts", settings: { direction: "Russian → English", count: 8 }, items: GENERATED_RECALL_POOLS[2], minutes: 8, why: "Без повторения исходных предложений" },
  },
  {
    goals: [GOALS[0], GOALS[4], GOALS[1]],
    speaking: { subtitle: "A meeting that went wrong · 2 minutes", prompt: "Tell me about a meeting or conversation that did not go as planned. What had been prepared in advance, what went wrong, and how was the situation resolved?", target: "Speak for 2 minutes and use 4–5 expressions from the active list.", targets: ["in advance", "reach an agreement", "look into", "eventually", "put off", "step in"], why: "Деловой разговор в новом контексте" },
    writing: { subtitle: "A cancelled plan · 120–150 words", prompt: "Write about something important that was called off at the last moment. Explain how you reacted and what happened next.", reqs: ["120–150 words", "use called off at the last moment", "use three other target expressions", "include one Passive Voice sentence"], targets: ["called off at the last moment", "eventually", "put off", "in advance", "despite", "look into"], why: "Добавляем недавние активные выражения" },
    grammar: { subtitle: "Passive · as soon as · Third Conditional", focus: ["Passive Voice", "as soon as", "Third Conditional"], settings: { count: 6 }, items: GENERATED_GRAMMAR_POOLS[0], minutes: 8, why: "Новая последовательность уже знакомых конструкций" },
    vocab: { subtitle: "Recall · changed plans", settings: { direction: "Russian → English", count: 8 }, items: GENERATED_RECALL_POOLS[1], minutes: 8, why: "Контексты про планы и решения" },
  },
  {
    goals: [GOALS[0], GOALS[3], GOALS[4]],
    speaking: { subtitle: "Something you postponed · 2–3 minutes", prompt: "Describe something important you kept putting off. Why did you postpone it, what finally made you act, and what was the result?", target: "Speak for 2–3 minutes, give reasons and examples, and use at least 5 target expressions.", targets: ["put off", "eventually", "think twice", "carry out", "despite", "keep going"], why: "Бытовой сюжет вместо рабочего" },
    writing: { subtitle: "A choice you reconsidered · 130–160 words", prompt: "Write about a choice that made you think twice. Explain what influenced you and whether you would make the same choice now.", reqs: ["130–160 words", "use one Third Conditional", "use four target expressions", "check articles"], targets: ["think twice", "eventually", "in advance", "despite", "turning point", "give in"], why: "Новая тема для свободного письма" },
    grammar: { subtitle: "Mixed Conditional · despite · Passive", focus: ["Mixed Conditional", "despite", "Passive Voice"], settings: { count: 6 }, items: GENERATED_GRAMMAR_POOLS[1], minutes: 9, why: "Повышаем вариативность грамматики" },
    vocab: { subtitle: "Personal contexts · 8 expressions", settings: { direction: "Russian → English", count: 8 }, items: GENERATED_RECALL_POOLS[2], minutes: 8, why: "Выражения в личных, а не только рабочих ситуациях" },
  },
  {
    goals: [GOALS[0], GOALS[1], GOALS[2]],
    speaking: { subtitle: "If you had known earlier · 2 minutes", prompt: "Talk about a recent situation that would have gone differently if you had known something in advance. What would you have changed?", target: "Speak for 2 minutes and naturally include at least two Third Conditional sentences.", targets: ["in advance", "eventually", "look into", "put off", "despite", "reach an agreement"], why: "Speaking напрямую связывается с Third Conditional" },
    writing: { subtitle: "What would have been different? · 140–170 words", prompt: "Write about a past situation and explain three things you would have done differently if you had had more information.", reqs: ["140–170 words", "three Third Conditional sentences", "four target expressions", "one Passive Voice sentence"], targets: ["in advance", "look into", "eventually", "despite", "carry out", "put off"], why: "Усиливаем слабую конструкцию в свободной речи и письме" },
    grammar: { subtitle: "Third Conditional intensive", focus: ["Third Conditional", "Third Conditional + Passive", "Mixed Conditional"], settings: { count: 6 }, items: GENERATED_GRAMMAR_POOLS[2], minutes: 10, why: "Фокусный грамматический блок" },
    vocab: { subtitle: "Conditional contexts · 8 expressions", settings: { direction: "Russian → English", count: 8 }, items: GENERATED_RECALL_POOLS[0], minutes: 8, why: "Лексика остаётся активной внутри новой грамматической темы" },
  },
  {
    goals: [GOALS[0], GOALS[3], GOALS[1]],
    speaking: { subtitle: "A difficult conversation · 2 minutes", prompt: "Describe a difficult conversation where you had to stay calm and reach an agreement. What made it difficult and what helped?", target: "Speak continuously for 2 minutes with a clear structure and 4 target expressions.", targets: ["reach an agreement", "step in", "think twice", "eventually", "despite", "in advance"], why: "Практика переговорной лексики" },
    writing: { subtitle: "Resolving a disagreement · 130–160 words", prompt: "Write about how you would handle a disagreement differently now compared with a few years ago.", reqs: ["130–160 words", "use a comparison between past and present", "use four target expressions", "include one conditional"], targets: ["reach an agreement", "think twice", "step in", "eventually", "despite", "keep going"], why: "Развиваем аргументацию, а не пересказ" },
    grammar: { subtitle: "Passive · until · conditionals", focus: ["Passive Voice", "until", "Conditionals"], settings: { count: 6 }, items: GENERATED_GRAMMAR_POOLS[0], minutes: 8, why: "Новый mix конструкций" },
    vocab: { subtitle: "Negotiation recall · 8 expressions", settings: { direction: "Russian → English", count: 8 }, items: GENERATED_RECALL_POOLS[1], minutes: 8, why: "Повтор через переговорные ситуации" },
  },
  {
    goals: [GOALS[0], GOALS[4], GOALS[3]],
    speaking: { subtitle: "When things got out of hand · 2–3 minutes", prompt: "Tell me about a situation that started normally but got out of hand. What were the warning signs, when did someone step in, and what did you learn?", target: "Speak for 2–3 minutes and use at least 5 active expressions.", targets: ["get out of hand", "step in", "eventually", "look into", "despite", "turning point"], why: "Новый narrative prompt с причинно-следственной структурой" },
    writing: { subtitle: "A lesson learned · 140–170 words", prompt: "Write about a mistake that eventually became useful because it changed the way you work or make decisions.", reqs: ["140–170 words", "use turned out to be a turning point", "use three additional target expressions", "include one Third Conditional sentence"], targets: ["turning point", "eventually", "look into", "in advance", "despite", "keep going"], why: "История ошибки вместо повторения одного проекта" },
    grammar: { subtitle: "Conditionals · Passive · despite", focus: ["Third/Mixed Conditional", "Passive Voice", "despite"], settings: { count: 6 }, items: GENERATED_GRAMMAR_POOLS[1], minutes: 9, why: "Комбинированный новый набор" },
    vocab: { subtitle: "Lessons learned · 8 expressions", settings: { direction: "Russian → English", count: 8 }, items: GENERATED_RECALL_POOLS[2], minutes: 8, why: "Те же target phrases в новых предложениях" },
  },
  {
    goals: [GOALS[0], GOALS[1], GOALS[4]],
    speaking: { subtitle: "A goal you kept pursuing · 2 minutes", prompt: "Tell me about a goal you kept working towards even when progress was slow. What almost made you give in and what helped you continue?", target: "Speak for 2 minutes without notes and use at least 4 expressions naturally.", targets: ["keep going", "give in", "against the odds", "eventually", "despite", "in advance"], why: "Личный контекст для автоматизации выражений" },
    writing: { subtitle: "Persistence · 120–150 words", prompt: "Write about a goal that took longer than expected but was worth pursuing.", reqs: ["120–150 words", "use against the odds", "use at least three more target expressions", "include one conditional sentence"], targets: ["against the odds", "keep going", "give in", "eventually", "despite", "turning point"], why: "Переносим лексику из work English в личный рассказ" },
    grammar: { subtitle: "Mixed Conditional · Passive · until", focus: ["Mixed Conditional", "Passive Voice", "until"], settings: { count: 6 }, items: GENERATED_GRAMMAR_POOLS[2], minutes: 8, why: "Ещё один самостоятельный набор примеров" },
    vocab: { subtitle: "Persistence recall · 8 expressions", settings: { direction: "Russian → English", count: 8 }, items: GENERATED_RECALL_POOLS[0], minutes: 8, why: "Новые фразы вокруг той же активной лексики" },
  },
];
GENERATED_HOMEWORK_PACKS.push(...EXTRA_GENERATED_HOMEWORK_PACKS);

'''
    marker = 'const STUDENTS = ['
    if marker not in s:
        raise RuntimeError('Could not find STUDENTS marker for generator expansion')
    s = s.replace(marker, extra + marker, 1)

# -------------------------------------------------------------------
# 2) Recall and Grammar should use the generated item pools.
# -------------------------------------------------------------------
recall_old = '''function RecallRunner({ task, onExit, onDone }) {
  const n = Math.min(task.settings?.count || 8, RECALL_ITEMS.length);
  const items = RECALL_ITEMS.slice(0, n);'''
recall_new = '''function RecallRunner({ task, onExit, onDone }) {
  const recallPool = task.items || RECALL_ITEMS;
  const n = Math.min(task.settings?.count || 8, recallPool.length);
  const items = recallPool.slice(0, n);'''
if recall_old in s:
    s = s.replace(recall_old, recall_new, 1)

start = s.find('function GrammarRunner({ task, onExit, onDone }) {')
end = s.find('/* ------------------------- Student: feedback / progress / practice', start)
if start == -1 or end == -1:
    raise RuntimeError('Could not isolate GrammarRunner')
g = s[start:end]
g = g.replace(
    '  const it = GRAMMAR_ITEMS[i];',
    '  const grammarPool = task.items || GRAMMAR_ITEMS;\n  const grammarItems = grammarPool.slice(0, Math.min(task.settings?.count || grammarPool.length, grammarPool.length));\n  const it = grammarItems[i];',
    1,
)
g = g.replace('GRAMMAR_ITEMS.length', 'grammarItems.length')
s = s[:start] + g + s[end:]

# -------------------------------------------------------------------
# 3) Generated Speaking/ Writing targets should actually reach Student.
# -------------------------------------------------------------------
start = s.find('function SpeakingRunner({ task, onExit, onDone }) {')
end = s.find('/* ------------------------- Student: Writing', start)
if start == -1 or end == -1:
    raise RuntimeError('Could not isolate SpeakingRunner')
sp = s[start:end]
sp = sp.replace('{SPEAK_TARGETS.map((t) =>', '{(task.targets || SPEAK_TARGETS).map((t) =>', 1)
sp = sp.replace(
    '      mimeType: blobRef.current.type, recordedAt: Date.now(), used: [],',
    '      mimeType: blobRef.current.type, recordedAt: Date.now(), used: [], targets: task.targets || SPEAK_TARGETS,',
    1,
)
s = s[:start] + sp + s[end:]

start = s.find('function SpeakingReview({ sp, marks, setMarks }) {')
end = s.find('function WritingReview({ wr, notes, setNotes }) {', start)
if start == -1 or end == -1:
    raise RuntimeError('Could not isolate SpeakingReview')
spr = s[start:end]
spr = spr.replace(
    '  const audioRef = useRef(null);',
    '  const audioRef = useRef(null);\n  const reviewTargets = sp.targets || SPEAK_TARGETS;',
    1,
)
spr = spr.replace('{SPEAK_TARGETS.map((t) =>', '{reviewTargets.map((t) =>', 1)
spr = spr.replace('targets={SPEAK_TARGETS.concat(["kept going"])}', 'targets={reviewTargets.concat(["kept going"])}', 1)
s = s[:start] + spr + s[end:]

# -------------------------------------------------------------------
# 4) Live Writing draft sync Student -> Teacher on the same device.
# -------------------------------------------------------------------
start = s.find('function WritingRunner({ task, onExit, onDone, notify }) {')
end = s.find('/* ------------------------- Student: Grammar', start)
if start == -1 or end == -1:
    raise RuntimeError('Could not isolate WritingRunner')
wr = s[start:end]
wr = wr.replace(
    'function WritingRunner({ task, onExit, onDone, notify }) {',
    'function WritingRunner({ task, onExit, onDone, notify, initialData, onDraft }) {',
    1,
)
wr = wr.replace('  const [text, setText] = useState("");', '  const [text, setText] = useState(initialData?.text || "");', 1)
wr = wr.replace(
    '  const words = countWords(text);\n  const used = usedTargets(text, WRITE_TARGETS);\n  const ok = words >= 40;',
    '''  const words = countWords(text);
  const writingTargets = task.targets || WRITE_TARGETS;
  const used = usedTargets(text, writingTargets);
  const ok = words >= 40;

  useEffect(() => {
    if (!text.trim() || typeof onDraft !== "function") return;
    const timer = window.setTimeout(() => {
      onDraft({ words, text, used, targets: writingTargets, draft: true, updatedAt: Date.now() });
    }, 350);
    return () => window.clearTimeout(timer);
  }, [text]);''',
    1,
)
wr = wr.replace(
    'onClick={() => onDone("writing", { words, text, used })}',
    'onClick={() => onDone("writing", { words, text, used, targets: writingTargets, draft: false })}',
    1,
)
wr = wr.replace(
    '<button className="el-btn el-g" onClick={() => notify("Draft saved")}>Save draft</button>',
    '<button className="el-btn el-g" onClick={() => { onDraft?.({ words, text, used, targets: writingTargets, draft: true, updatedAt: Date.now() }); notify("Draft saved"); }}>Save draft</button>',
    1,
)
s = s[:start] + wr + s[end:]

# StudentApp: persist drafts into the shared homework state + localStorage.
student_start = s.find('function StudentApp({ hw, setHw, notify, jumpToTeacher }) {')
student_end = s.find('/* ------------------------- Student: today', student_start)
if student_start == -1 or student_end == -1:
    raise RuntimeError('Could not isolate StudentApp')
sa = s[student_start:student_end]
if 'const saveDraft = (type, data) =>' not in sa:
    anchor = '  const submitAll = () => {'
    draft_logic = '''  const saveDraft = (type, data) => {
    if (!active) return;
    const submissionKey = type === "vocab" ? "recall" : type;
    setProgressByHomework((all) => ({
      ...all,
      [active.id]: { ...(all[active.id] || {}), [type]: data },
    }));
    setHw((db) => {
      const current = db[active.id];
      if (!current) return db;
      return {
        ...db,
        [active.id]: {
          ...current,
          status: current.status === "assigned" ? "in_progress" : current.status,
          submission: { ...(current.submission || {}), [submissionKey]: data },
          draftUpdatedAt: Date.now(),
        },
      };
    });
  };

'''
    if anchor not in sa:
        raise RuntimeError('Could not find submitAll anchor in StudentApp')
    sa = sa.replace(anchor, draft_logic + anchor, 1)

sa = sa.replace(
    ': run.type === "writing" ? <WritingRunner {...props} />',
    ': run.type === "writing" ? <WritingRunner {...props} initialData={progress.writing} onDraft={(data) => saveDraft("writing", data)} />',
    1,
)
s = s[:student_start] + sa + s[student_end:]

# -------------------------------------------------------------------
# 5) Teacher home can inspect a live draft instead of only mock reviews.
# -------------------------------------------------------------------
home_start = s.find('const Row = ({ h }) => {')
home_end = s.find('  return (\n    <>', home_start)
if home_start != -1 and home_end != -1:
    row = s[home_start:home_end]
    if 'const hasStudentWork' not in row:
        row = row.replace(
            '    const task = h.submission?.speaking ? "Speaking response" : h.tasks[0]?.title || h.title;',
            '    const task = h.submission?.speaking ? "Speaking response" : h.submission?.writing ? "Writing draft" : h.tasks[0]?.title || h.title;\n    const hasStudentWork = Object.keys(h.submission || {}).length > 0;',
            1,
        )
    row = row.replace(
        '''        {h.status === "needs_review" ? (
          <button className="el-btn el-p" onClick={() => go("review", h.id)}>Review</button>
        ) : h.status === "feedback_sent" ? (
          <button className="el-btn el-g" onClick={() => go("results", h.id)}>Results</button>
        ) : (
          <button className="el-btn el-g" onClick={() => go("student", h.student)}>Open student</button>
        )}''',
        '''        {h.status === "needs_review" ? (
          <button className="el-btn el-p" onClick={() => go("review", h.id)}>Review</button>
        ) : h.status === "in_progress" && hasStudentWork ? (
          <button className="el-btn el-g" onClick={() => go("review", h.id)}>View draft</button>
        ) : h.status === "feedback_sent" ? (
          <button className="el-btn el-g" onClick={() => go("results", h.id)}>Results</button>
        ) : (
          <button className="el-btn el-g" onClick={() => go("student", h.student)}>Open student</button>
        )}''',
        1,
    )
    s = s[:home_start] + row + s[home_end:]

# Review screen: new generated homework must not inherit canned teacher feedback.
review_start = s.find('function ReviewScreen({ hwId, hw, setHw, go, notify }) {')
review_end = s.find('/* ------------------------- Teacher: results', review_start)
if review_start == -1 or review_end == -1:
    raise RuntimeError('Could not isolate ReviewScreen')
rv = s[review_start:review_end]
rv = rv.replace(
    '  const sub = h.submission || {};',
    '  const sub = h.submission || {};\n  const isLiveDraft = h.status === "in_progress";',
    1,
)
rv = rv.replace(
    '  const [marks, setMarks] = useState([{ at: 0.26, text: "Речь встала на шесть секунд — на занятии потренируем короткие связки." }]);',
    '  const [marks, setMarks] = useState(h.createdAt ? [] : [{ at: 0.26, text: "Речь встала на шесть секунд — на занятии потренируем короткие связки." }]);',
    1,
)
rv = rv.replace(
    '''  const [text, setText] = useState(
    "Good progress. Your speech was more continuous, and “eventually” appeared naturally. Next time, try to use “look into” and “carry out” without looking at the list."
  );''',
    '''  const [text, setText] = useState(
    h.createdAt ? "" : "Good progress. Your speech was more continuous, and “eventually” appeared naturally. Next time, try to use “look into” and “carry out” without looking at the list."
  );''',
    1,
)
# Add an explicit live-draft banner before review tabs.
tabs_anchor = '      <div style={{ display: "flex", gap: 6, margin: "22px 0 20px", flexWrap: "wrap" }}>'
if tabs_anchor in rv and 'Student is still working' not in rv:
    banner = '''      {isLiveDraft && (
        <div className="el-card el-fadein" style={{ padding: 14, marginTop: 16, background: "#EDF1F7", borderColor: "#D7DFEA" }}>
          <div style={{ fontSize: 14, fontWeight: 600, color: "#3B5C88" }}>Live draft · Student is still working</div>
          <div style={{ fontSize: 12.5, color: "var(--ink2)", marginTop: 4 }}>Это реальные данные из режима Student. Writing обновляется автоматически во время набора текста.</div>
        </div>
      )}

'''
    rv = rv.replace(tabs_anchor, banner + tabs_anchor, 1)

# Don't send final feedback while the student is still editing the draft.
rv = rv.replace(
    '''        <button className="el-btn el-p" style={{ width: "100%", marginTop: 14, padding: "12px" }} onClick={send}>
          <Send size={15} /> Send feedback
        </button>''',
    '''        <button className="el-btn el-p" disabled={isLiveDraft} style={{ width: "100%", marginTop: 14, padding: "12px", opacity: isLiveDraft ? .55 : 1 }} onClick={send}>
          <Send size={15} /> {isLiveDraft ? "Waiting for student submission" : "Send feedback"}
        </button>''',
    1,
)
s = s[:review_start] + rv + s[review_end:]

# Writing Review must tolerate draft data and show its status clearly.
start = s.find('function WritingReview({ wr, notes, setNotes }) {')
end = s.find('function ReviewScreen({ hwId, hw, setHw, go, notify }) {', start)
if start == -1 or end == -1:
    raise RuntimeError('Could not isolate WritingReview')
wreview = s[start:end]
wreview = wreview.replace(
    '  const custom = wr.text !== SAMPLE_ESSAY;',
    '  const custom = wr.text !== SAMPLE_ESSAY;\n  const reviewWriteTargets = wr.targets || WRITE_TARGETS;',
    1,
)
wreview = wreview.replace('{wr.used.length} из 6', '{(wr.used || []).length} из {reviewWriteTargets.length}', 1)
wreview = wreview.replace('<Highlighted text={wr.text} targets={WRITE_TARGETS} />', '<Highlighted text={wr.text} targets={reviewWriteTargets} />', 1)
wreview = wreview.replace(
    '{custom && <div style={{ fontSize: 12.5, color: "var(--ink3)", marginTop: 14 }}>Это текст, который вы только что написали в режиме ученика.</div>}',
    '{custom && <div style={{ fontSize: 12.5, color: wr.draft ? "#3B5C88" : "var(--ink3)", marginTop: 14 }}>{wr.draft ? "Live draft — текст автоматически синхронизируется из режима ученика." : "Это текст, который вы только что написали в режиме ученика."}</div>}',
    1,
)
s = s[:start] + wreview + s[end:]

# Build-time safety checks.
required = [
    'EXTRA_GENERATED_HOMEWORK_PACKS',
    'GENERATED_HOMEWORK_PACKS.push(...EXTRA_GENERATED_HOMEWORK_PACKS)',
    'const recallPool = task.items || RECALL_ITEMS;',
    'const grammarPool = task.items || GRAMMAR_ITEMS;',
    'const saveDraft = (type, data) =>',
    'View draft',
    'Live draft · Student is still working',
]
for item in required:
    if item not in s:
        raise RuntimeError(f'Missing live-sync/variety feature: {item}')

p.write_text(s, encoding='utf-8')
