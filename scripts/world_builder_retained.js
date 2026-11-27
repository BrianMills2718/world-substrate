// Retained simulation from the Waltzman workbench. The adjacent JSON is its public case record.
(() => {
  const recordUrl = new URL('world_builder_retained.json', document.currentScript.src);
  const source = 'https://brianmills.dev/waltzman/assets/cso-case.json';
  const style = `
    .retained-case{max-width:46rem;margin-inline:auto;color:var(--text);line-height:1.55}
    .retained-case h2{font-size:clamp(1.5rem,4vw,2.2rem);line-height:1.15;margin:.25em 0 .4em}
    .retained-case h3{margin:1.5em 0 .45em;font-size:1.2rem}
    .retained-case p{margin:.65em 0 1em}
    .retained-case small,.retained-case label{color:var(--muted)}
    .retained-case [role=tablist]{display:flex;gap:1.5rem;margin:1.3rem 0;border-bottom:1px solid var(--line)}
    .retained-case [role=tab]{background:transparent;color:var(--muted);padding:.7rem .15rem;border:0;border-bottom:3px solid transparent;font:inherit;cursor:pointer}
    .retained-case [aria-selected=true]{color:inherit;border-color:currentColor;font-weight:700}
    .retained-case [hidden]{display:none}
    .retained-case button,.retained-case select{font:inherit;cursor:pointer}
    .retained-case select{max-width:100%;display:block;margin:.25rem 0 1rem;padding:.55rem}
    .retained-case dl{display:grid;grid-template-columns:auto 1fr;gap:.55rem 1.25rem;margin:0}
    .retained-case dd{margin:0}
    .retained-case blockquote{margin:.3em 0 1.3em;padding-left:1rem;border-left:3px solid var(--line);line-height:1.6}
    .retained-case footer{margin-top:2rem;font-size:.85rem;color:var(--muted);overflow-wrap:anywhere}
  `;
  function el(tag, value) {
    const node = document.createElement(tag);
    if (value !== undefined) node.textContent = value;
    return node;
  }

  function show(record, wrap) {
    const total = record.agent_count;
    const requests = record.final_requests;
    const tabs = el('div');
    tabs.setAttribute('role', 'tablist');
    tabs.setAttribute('aria-label', 'Case views');
    const result = el('section');
    const evidence = el('section');
    const views = [result, evidence];
    const buttons = ['Result', 'Evidence'].map((name, index) => {
      const tab = el('button', name);
      tab.type = 'button';
      tab.id = 'retained-tab-' + index;
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', 'retained-view-' + index);
      views[index].id = 'retained-view-' + index;
      views[index].setAttribute('role', 'tabpanel');
      views[index].setAttribute('aria-labelledby', tab.id);
      tabs.append(tab);
      tab.onclick = () => select(index);
      tab.onkeydown = event => {
        if (!['ArrowRight','ArrowLeft','Home','End'].includes(event.key)) return;
        event.preventDefault();
        select(event.key === 'Home' ? 0 : event.key === 'End' ? 1 : 1 - index, true);
      };
      return tab;
    });
    function select(active, focus = false) {
      views.forEach((view, i) => {
        view.hidden = i !== active;
        buttons[i].setAttribute('aria-selected', String(i === active));
        buttons[i].tabIndex = i === active ? 0 : -1;
      });
      if (focus) buttons[active].focus();
    }

    const rounds = el('dl');
    for (const round of record.rounds) {
      const conditional = round.decisions.conditional;
      rounds.append(el('dt', 'Round ' + round.round), el('dd', round.decisions.support + ' supported outright' +
        (conditional ? ' · ' + conditional + ' conditional' : '')));
    }
    const openEvidence = el('button', 'Read the paired statements');
    openEvidence.type = 'button';
    openEvidence.className = 'secondary';
    openEvidence.onclick = () => select(1, true);
    result.append(el('h3', 'The joint response was approved'), rounds,
      el('p', 'Outright support returned after the scenario supplied a prewritten package of commitments. ' +
        (total - requests.none) + ' of ' + total + ' still requested something in the final round — ' +
        requests.resources + ' asked for resources, ' + requests.safeguards + ' for safeguards and ' +
        requests.validation + ' for validation.'), openEvidence);

    const picker = el('select');
    picker.id = 'retained-participant';
    const label = el('label', 'Simulated participant');
    label.htmlFor = picker.id;
    const quotes = el('div');
    const pairs = record.paired_rationales;
    for (const pair of pairs) {
      const name = pair.actor_id.replaceAll('_',' ');
      const option = el('option', name[0].toUpperCase() + name.slice(1));
      option.value = pair.actor_id;
      picker.append(option);
    }
    picker.value = 'regional_legal_oversight_lead';
    function statements() {
      const pair = pairs.find(item => item.actor_id === picker.value);
      quotes.replaceChildren();
      for (const [round, stance] of [[2, pair.under_pressure], [3, pair.after_stabilization]]) {
        const decision = stance.decision === 'conditional' ? 'Conditional support' : 'Outright support';
        quotes.append(el('h3', 'Round ' + round + ' · ' + decision), el('blockquote', stance.rationale));
      }
    }
    picker.onchange = statements;
    statements();
    evidence.append(label, picker, quotes);
    const footer = el('footer');
    const link = el('a','Original case record');
    link.href = source;
    footer.append('Earlier workbench simulation · ' + record.source_run_id + ' · ', link);
    wrap.replaceChildren(el('style', style), el('small', 'Completed example · ' + total + ' simulated participants'),
      el('h2','Should the coalition activate its joint response?'), tabs, result, evidence, footer);
    select(0);
  }

  async function open(container) {
    const wrap = el('article');
    wrap.className = 'retained-case';
    wrap.append(el('p', 'Opening the completed example…'));
    container.replaceChildren(wrap);
    try {
      const response = await fetch(recordUrl);
      if (!response.ok) throw new Error('Case unavailable');
      show(await response.json(), wrap);
    } catch {
      const link = el('a', 'Open the original case');
      link.href = 'https://brianmills.dev/waltzman/?view=case&case_step=5';
      wrap.replaceChildren(el('p', 'The saved example could not be loaded.'), link);
    }
  }

  window.WorldBuilderRetained = {open};
})();
