# Стратегическая оценка и следующая большая цель (2026-08-17)

## Что мы реально сделали и почему это важно (честная самооценка)

1. **Научный результат.** Для семейства CHR (единственный известный
   однопараметрический интерполятор «гравитация ↔ струна») мы дали полную
   анатомию положительности: закрытые формулы каждой траекторной границы
   (мастер-формула), доказанную теорему для второго ножа, коллапс всех
   ножей к степени первого, и главный физический вывод —
   **уникальность струны градуирована размерностью**: в D=4 семейство
   выживает целиком (струна ничем не выделена), в высоких D струна стоит
   ровно на границе выживания (D=23 — точно). Это конкретный, проверяемый
   вклад в вопрос «обязана ли гравитация быть струнной».
2. **Методологический результат (возможно, важнее).** Мы показали, что
   вопросы положительности S-матричного бутстрапа переводятся в
   МАШИННО-ПРОВЕРЯЕМЫЕ сертификатные доказательства (Пойя/Бернштейн/Декарт
   у мыса/изоляция корней, всё в точной арифметике) с независимой
   адверсариальной проверкой. В бутстрап-литературе доминируют численные
   сканы и асимптотики; конвейер сертификатов — наша ниша.
3. **Процессный результат.** Лаборатория с гейтами (заморозка, критик,
   errata, полная воспроизводимость) на скорости ИИ. Четыре DOI за двое
   суток с нулём пойманных извне ошибок — потому что ловим их сами и
   публикуем поимки.

## Ближайший саммит (недели): ONE BOUNDARY

- Дожать нож 4 (лемма Декарта у мыса — в прувере сейчас), конвейер j=5..8,
  режим фиксированного спина (l=0,2,4 при n→∞) — последний нетривиальный
  кусок; затем ГЛАВНАЯ ТЕОРЕМА ПОЛНОТЫ и ФЛАГМАН (~25 стр.): берег +
  мастер-формула + лезвия + коллапс + полнота. Цель: arXiv (ждём
  эндорсмент) → журнал (JHEP/PRD).

## Следующая БОЛЬШАЯ цель (амбиция уровня программы, месяцы)

**«ATLAS OF CONSISTENT 4D GRAVITIES» — атлас неструнных гравитаций.**
Наш же вывод («в D=4 струна ничем не выделена») — это не конец, а дверь:
если не струна, то ЧТО живёт в D=4? План:
1. Расширить пространство анзацев за пределы CHR: общие дуально-резонансные
   резидуумы (не квадраты Похгаммеров), двухпараметрические деформации,
   несимметричные спектры — и прогнать через сертификатный конвейер.
2. Для каждого выжившего класса — карта EFT-коэффициентов (наш циферблат λ
   уже прототип) и ЧЕСТНЫЙ порог различимости: какая точность наблюдений
   (ГВ-фаза, пост-ньютоновские члены) потребовалась бы. Скорее всего ответ
   «планковски подавлено» — тогда это строгая no-go/threshold статья, тоже
   ценная и цитируемая.
3. Методологический флаг: выделить сертификатный конвейер в открытый
   инструмент «certified-bootstrap» (любой исследователь загружает свой
   анзац — получает доказанные границы, не сканы). Это умножит цитируемость
   и втянет комьюнити в нашу инфраструктуру.

Формат мечты основателя (письмо-предсказание экспериментаторам) живёт в
пункте 2: даже отрицательный порог — это письмо «вот что нужно измерить,
чтобы отличить», честное и смелое.

## Порядок исполнения
Саммит (полнота+флагман) → Атлас этап 1 → циферблаты и пороги → tooling.
Каждая веха: ригор полный, выход — сайт+дашборд; статьи решаю объявлять я.

---

# ATLAS OF NON-STRING GRAVITIES — three microproblem cards (2026-08-17)

Written after the night that produced the CHR closed form. Each card carries
a DETERMINISTIC falsifier (charter requirement): a machine-checkable test
whose failure kills the card, no human judgement involved.

## CARD A1 — Beyond CHR: are squared-Pochhammer residues the ONLY solution?

- exact statement: consider residues R(n,t) = [Q_n(t)]^2 with Q_n a monic
  degree-(n-1) polynomial with REAL roots, plus crossing + the CHR spectrum
  mu(n) = (n+lam-1)/lam. Question: does positivity for all n force Q_n to be
  the Pochhammer ((1+lam)/2 + lam t)_{n-1} up to normalisation?
- north_star_relevance: this is literally "must consistent gravity be
  string-like" one level deeper — not "which lambda survives" but "which
  FUNCTIONAL FORM survives".
- assumptions: tree level, four points, real simple poles, finite spin per
  level, polynomial residues, D free.
- known theorem / prior art: CHR (2408.03362) bootstrapped the family under
  the Pochhammer ansatz; hypergeometric deformations (2409.09561, 2403.00906)
  relax it in a different direction (q-deformation).
- suspected open gap: nobody varied Q_n's ROOTS while keeping the spectrum.
- deterministic evaluator: parametrise Q_n's roots as r_k = -(a + k b)/lam
  plus a perturbation vector eps (dim n-1); compute a_{n,2n-2j} via our
  closed form generalisation; TEST: does any eps != 0 with |eps| <= 0.1
  keep all knives j <= 8 positive for n <= 20 at D = 10?
- deterministic falsifier: an exact rational eps making all knives positive
  => uniqueness FALSE (a genuinely new amplitude family found — the bigger
  prize); zero such eps after a 10^6-point exact scan => uniqueness
  SUPPORTED (then attempt proof via the closed form).
- expected computation: our v2 engine, minutes per (n, eps) batch.
- maximum legitimate claim: "within this ansatz and this scan, no
  non-Pochhammer square survives" — NOT "string is unique".
- kill criteria: if the perturbed residues violate crossing identically
  (then the ansatz is empty and the card is void).

## CARD A2 — The discriminability threshold: could a surviving non-string
## gravity ever be MEASURED?

- exact statement: for the surviving D=4 band (our published result: the
  whole lambda-family survives in D=4), compute the leading EFT Wilson
  coefficients (alpha_i(lambda)) and the induced deviation in a physical
  observable (post-Newtonian phase of a gravitational-wave inspiral) as a
  function of lambda and the string scale.
- north_star_relevance: converts a mathematical survival statement into a
  falsifiable physical prediction — the founder's dream format ("a letter
  to experimentalists").
- deterministic evaluator: compute the alpha_i from the CHR low-energy
  expansion exactly (we already have the machinery); map to the standard
  ppE parametrisation; compare against published LIGO/Virgo/LISA bounds.
- deterministic falsifier: if the induced ppE coefficient exceeds current
  bounds for some lambda range => that range is EXCLUDED BY EXPERIMENT
  (a real physical exclusion, publishable); if it is below LISA's projected
  sensitivity for the whole band => an honest no-go/threshold paper.
- maximum legitimate claim: bounds and thresholds, never "gravity is X".

## CARD A3 — certified-bootstrap: the tool as the contribution

- exact statement: package the v2 engine (exact Q(sqrt3) polynomial
  arithmetic, Bernstein/orthant/Descartes certificates, Z3 cross-check,
  deterministic artifact gate) as a library where a researcher supplies a
  residue ansatz and receives PROVEN bounds instead of numerical scans.
- north_star_relevance: multiplies the North Star's reach — every other
  bootstrap family becomes checkable with our machinery.
- deterministic evaluator: reproduce three published positivity results
  from the literature (Veneziano D<=10 spin-0 case, Coon leading trajectory,
  our own blade theorem) using ONLY the library's public API.
- deterministic falsifier: if any of the three cannot be reproduced within
  a fixed compute budget, the library is not yet a contribution.
- note: the night's discovery that positivity is MANIFEST in the right chart
  (for j<=8) is the library's key selling point — and its boundary at j=9
  is the first documented limitation, which must ship with it.

## Selection (by charter score: importance x falsifiability x novelty x
## verifier availability x speed to first artifact)

A1 wins: it attacks the North Star directly, has an exact falsifier, and our
engine can run it TODAY. A2 second (needs EFT matching, no new machinery).
A3 third (engineering, ships after the flagship).
