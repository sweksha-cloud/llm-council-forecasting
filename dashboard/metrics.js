// Scoring for the dashboard. Mirrors scoring/proper.py, scoring/calibration.py and
// scoring/discrimination.py and scoring/classification.py exactly; tests/test_dashboard.py checks the two agree.
// p = probability the event happens, y = 1 if it happened. Lower Brier/log is better.

const Metrics = (() => {
  const EPS = 1e-6;
  const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;

  const brier = (p, y) => (p - y) ** 2;
  const logScore = (p, y) => {
    const q = Math.min(Math.max(p, EPS), 1 - EPS);
    return -Math.log(y === 1 ? q : 1 - q);
  };
  // Right side of 0.5; exactly 0.5 counts half.
  const hit = (p, y) => (p === 0.5 ? 0.5 : (p > 0.5) === (y === 1) ? 1 : 0);

  function bins(ps, ys, n = 10) {
    const groups = Array.from({ length: n }, () => []);
    ps.forEach((p, i) => groups[Math.min(Math.floor(p * n), n - 1)].push([p, ys[i]]));
    return groups.map((g, i) => g.length ? {
      lower: i / n, upper: (i + 1) / n, count: g.length,
      meanForecast: mean(g.map((x) => x[0])), observedRate: mean(g.map((x) => x[1])),
    } : null).filter(Boolean);
  }

  const ece = (ps, ys, n = 10) =>
    bins(ps, ys, n).reduce((s, b) => s + b.count * Math.abs(b.meanForecast - b.observedRate), 0) / ps.length;

  function averageRanks(xs) {
    const order = xs.map((_, i) => i).sort((a, b) => xs[a] - xs[b]);
    const ranks = new Array(xs.length);
    for (let i = 0; i < order.length;) {
      let j = i;
      while (j + 1 < order.length && xs[order[j + 1]] === xs[order[i]]) j++;
      for (let k = i; k <= j; k++) ranks[order[k]] = (i + j) / 2 + 1;
      i = j + 1;
    }
    return ranks;
  }

  function auroc(ps, ys) {
    const nPos = ys.filter((y) => y === 1).length, nNeg = ys.length - nPos;
    if (!nPos || !nNeg) return null;
    const ranks = averageRanks(ps);
    const posSum = ranks.reduce((s, r, i) => s + (ys[i] === 1 ? r : 0), 0);
    return (posSum - nPos * (nPos + 1) / 2) / (nPos * nNeg);
  }

  // Yes/No calls vs outcomes (above 0.5 = Yes, below = No, exactly 0.5 = no call).
  function confusion(ps, ys) {
    const c = { tp: 0, fp: 0, tn: 0, fn: 0 };
    ps.forEach((p, i) => {
      if (p === 0.5) return;
      if (p > 0.5) ys[i] === 1 ? c.tp++ : c.fp++;
      else ys[i] === 1 ? c.fn++ : c.tn++;
    });
    return c;
  }
  function balancedAccuracy({ tp, fp, tn, fn }) {
    if (!(tp + fn) || !(tn + fp)) return null;
    return (tp / (tp + fn) + tn / (tn + fp)) / 2;
  }
  function mcc({ tp, fp, tn, fn }) {
    if (!(tp + fp + tn + fn)) return null;
    const d = Math.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn));
    return d ? (tp * tn - fp * fn) / d : 0;
  }

  // Brier skill vs a reference on paired [p, ref, y] rows: 1 - Brier / reference Brier. > 0 = better.
  // Not reported below MIN_N pairs (as in scoring/report.py): on a few questions the ratio is noise.
  const MIN_N = 30;
  function skill(pairs) {
    if (pairs.length < MIN_N) return null;
    const ref = pairs.reduce((s, [, r, y]) => s + brier(r, y), 0);
    return ref ? 1 - pairs.reduce((s, [p, , y]) => s + brier(p, y), 0) / ref : null;
  }

  // All metrics for one list of (probability, outcome) pairs.
  function score(ps, ys) {
    if (!ps.length) return null;
    return {
      n: ps.length,
      brier: mean(ps.map((p, i) => brier(p, ys[i]))),
      log: mean(ps.map((p, i) => logScore(p, ys[i]))),
      accuracy: mean(ps.map((p, i) => hit(p, ys[i]))),
      ece: ece(ps, ys),
      sharpness: mean(ps.map((p) => Math.abs(p - 0.5))),
      auroc: auroc(ps, ys),
      balancedAccuracy: balancedAccuracy(confusion(ps, ys)),
      mcc: mcc(confusion(ps, ys)),
    };
  }

  // Paired Brier difference a - b with a 95% bootstrap interval (seeded, so it's stable on reload).
  function pairedDiff(pairs, nBoot = 1000, seed = 7) {
    if (pairs.length < 2) return null;
    const diffs = pairs.map(([a, b, y]) => brier(a, y) - brier(b, y));
    let s = seed >>> 0;
    const rand = () => { s = (s + 0x6D2B79F5) >>> 0; let t = s; t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
    const boots = [];
    for (let b = 0; b < nBoot; b++) {
      let sum = 0;
      for (let i = 0; i < diffs.length; i++) sum += diffs[Math.floor(rand() * diffs.length)];
      boots.push(sum / diffs.length);
    }
    boots.sort((x, y) => x - y);
    return { n: pairs.length, diff: mean(diffs), lo: boots[Math.floor(0.025 * nBoot)], hi: boots[Math.floor(0.975 * nBoot) - 1] };
  }

  const meanPool = (ps) => mean(ps);
  const medianPool = (ps) => {
    const s = [...ps].sort((a, b) => a - b), m = s.length >> 1;
    return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
  };

  return { MIN_N, brier, logScore, hit, bins, ece, auroc, confusion, balancedAccuracy, mcc, skill, score, pairedDiff, meanPool, medianPool };
})();

if (typeof module !== "undefined") module.exports = Metrics;
