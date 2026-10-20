// What the site scores: setups (with baselines and the market) and the filtered questions.
// Every number comes from dashboard/metrics.js; this only decides which forecasts go in.
// The setups are assembled as on the dashboard (dashboard/template.html, model()), and
// tests/test_site.py checks the result against scoring/report.py.

const Site = ((M) => {
  // Setups for one dataset, including the pooled baselines, always-No and the market.
  function model(ds) {
    const setups = ds.setups.map((s, i) => ({ ...s, idx: i, seconds: ds.seconds?.[s.id] ?? null }));
    // Pools use council members only (as scoring/report.py does), else every single model.
    const councilMembers = [...new Set(setups.filter((s) => s.kind === "council").flatMap((s) => s.members || []))];
    const singles = councilMembers.length ? councilMembers : setups.filter((s) => s.kind === "single").map((s) => s.idx);
    const rows = ds.questions.map((q) => {
      const ps = q.f.map((c) => (c ? c.p : undefined));
      const extra = {};
      const sp = singles.map((i) => ps[i]).filter((p) => p != null);
      if (singles.length >= 2) {
        extra["baseline:mean"] = sp.length >= 2 ? M.meanPool(sp) : null;
        extra["baseline:median"] = sp.length >= 2 ? M.medianPool(sp) : null;
      }
      if (q.market != null) extra.market = q.market;
      extra["baseline:always_no"] = 0;
      return { ...q, ps, extra };
    });
    // A pool needs every member's answer, so it costs their time and size added up.
    const sum = (key) => {
      const xs = singles.map((i) => setups[i][key]);
      return xs.length && xs.every((x) => x != null) ? xs.reduce((a, b) => a + b, 0) : null;
    };
    const all = [...setups];
    if (singles.length >= 2) {
      all.push({ id: "baseline:mean", label: "Mean of single models", kind: "baseline", members: singles, seconds: sum("seconds"), params: sum("params") });
      all.push({ id: "baseline:median", label: "Median of single models", kind: "baseline", members: singles, seconds: sum("seconds"), params: sum("params") });
    }
    all.push({ id: "baseline:always_no", label: "Always No", kind: "baseline", members: [], seconds: null, params: null });
    if (rows.some((r) => r.market != null)) all.push({ id: "market", label: "Market price", kind: "market", members: [], seconds: null, params: null });
    all.forEach((s) => { s.get = s.idx != null ? (r) => r.ps[s.idx] : (r) => r.extra[s.id]; });
    return { setups: all, rows };
  }

  // Questions passing the filters (source, topic, month the question closes).
  function filter(rows, f = {}) {
    return rows.filter((r) => (!f.source || f.source === "all" || r.source === f.source)
      && (!f.topic || f.topic === "all" || r.topic === f.topic)
      && (!f.month || f.month === "all" || r.close.slice(0, 7) === f.month));
  }

  // "answered": each setup on the questions it answered. "common": only questions every setup answered.
  function scored(model, rows, mode) {
    const resolved = rows.filter((r) => r.y != null);
    if (mode !== "common") return resolved;
    const active = model.setups.filter((s) => resolved.some((r) => s.get(r) != null));
    return resolved.filter((r) => active.every((s) => s.get(r) != null));
  }

  // One row per setup: every metric, coverage, abstain-as-50% Brier, skill vs market, judge score.
  function board(model, rows, mode = "answered") {
    const resolved = scored(model, rows, mode);
    const market = model.setups.find((s) => s.id === "market");
    return model.setups.map((s) => {
      const ans = resolved.filter((r) => s.get(r) != null);
      const ps = ans.map(s.get), ys = ans.map((r) => r.y);
      const res = M.score(ps, ys);
      const judges = ans.map((r) => (s.idx != null ? r.f[s.idx]?.j : undefined)).filter((j) => j != null);
      const filled = resolved.map((r) => s.get(r) ?? 0.5);
      return {
        setup: s, answered: ans.length, total: resolved.length,
        coverage: resolved.length ? ans.length / resolved.length : null,
        ...(res || {}),
        brierFill: resolved.length ? M.score(filled, resolved.map((r) => r.y)).brier : null,
        skill: market && s !== market
          ? M.skill(ans.filter((r) => market.get(r) != null).map((r) => [s.get(r), market.get(r), r.y])) : null,
        judge: judges.length ? judges.reduce((a, b) => a + b, 0) / judges.length : null,
        bins: ans.length ? M.bins(ps, ys) : [],
        seconds: s.seconds ?? null, params: s.params ?? null,
      };
    });
  }

  return { model, filter, scored, board };
})(typeof Metrics !== "undefined" ? Metrics : require("../dashboard/metrics.js"));

if (typeof module !== "undefined") module.exports = Site;
