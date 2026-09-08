(function () {
  "use strict";
  const core = window.WorldBuilderCore;
  let bundle = core.clone(window.INITIAL_BUNDLE);
  let causalModel = null, causalReview = null, mechanicsSource = null, mechanicsApproved = false;
  let mechanicGuidance = "", generationMeta = null, runResult = null, liveBusy = false, liveLog = [];
  let runPolicy = "scripted", runTurns = 12;
  const LIVE_MODEL = "openrouter/openai/gpt-5.6-luna";
  let active = new URLSearchParams(location.search).get("section") || "world";
  const sections = ["world", "components", "entities", "actions", "mechanics", "presentation", "run", "logs", "export"];
  if (!sections.includes(active)) active = "world";

  const editor = document.getElementById("editor");
  const preview = document.getElementById("json-preview");
  const errorsBox = document.getElementById("validation-errors");
  const badge = document.getElementById("validation-badge");
  const downloadBtn = document.getElementById("download-bundle");

  function el(tag, cls, text) {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text !== undefined) node.textContent = text;
    return node;
  }
  function button(text, cls, fn) {
    const b = el("button", cls, text); b.type = "button"; b.addEventListener("click", fn); return b;
  }
  function field(label, value, fn, opts={}) {
    const wrap = el("label", "field"); wrap.append(el("span", "field-label", label));
    const input = opts.textarea ? el("textarea", "input") : el("input", "input");
    if (!opts.textarea) input.type = opts.type || "text";
    input.value = value ?? "";
    input.placeholder = opts.placeholder || "";
    input.addEventListener(opts.event || "input", () => fn(input.value, input));
    wrap.append(input); return wrap;
  }
  function selectField(label, value, options, fn) {
    const wrap=el("label","field"); wrap.append(el("span","field-label",label)); const s=el("select","input");
    options.forEach(([v,t])=>{const o=el("option",null,t);o.value=v;if(v===value)o.selected=true;s.append(o);});
    s.addEventListener("change",()=>fn(s.value)); wrap.append(s); return wrap;
  }
  function sectionHead(title, copy) {
    const h=el("div","section-head"); const box=el("div"); box.append(el("h2",null,title),el("p","muted",copy)); h.append(box); return h;
  }
  function card(title) { const c=el("section","card"); if(title)c.append(el("h3",null,title)); return c; }
  function sync() {
    if (mechanicsStale()) mechanicsApproved = false;
    preview.textContent = JSON.stringify(bundle, null, 2);
    const result = core.validateBundle(bundle);
    badge.textContent = result.ok ? "Valid bundle" : `${result.errors.length} issue${result.errors.length===1?"":"s"}`;
    badge.className = `status ${result.ok ? "ok" : "bad"}`;
    errorsBox.replaceChildren();
    if (result.ok) errorsBox.append(el("div","validation-ok","Ready to export and scaffold."));
    else result.errors.slice(0,12).forEach(x=>errorsBox.append(el("div","validation-error",x)));
    if (result.errors.length>12) errorsBox.append(el("div","validation-error",`+ ${result.errors.length-12} more`));
    downloadBtn.disabled = !result.ok;
    document.getElementById("world-name").textContent = bundle.world?.label || "Untitled world";
    document.getElementById("counts").textContent = `${bundle.entities?.length||0} entities · ${bundle.components?.length||0} components · ${bundle.actions?.length||0} action signatures`;
  }
  function rerender() { renderNav(); renderSection(); sync(); }
  function renderNav() {
    document.querySelectorAll("[data-section]").forEach(b=>b.classList.toggle("active",b.dataset.section===active));
  }
  function parseCategories(text) { return text.split(",").map(x=>x.trim()).filter(Boolean); }
  function parseDefault(kind, text) {
    if (kind === "string" || kind === "entity_ref") return text;
    if (kind === "entity_ref_or_null") return text.trim() ? text : null;
    if (kind === "integer") { const n=Number(text); return Number.isInteger(n)?n:text; }
    if (kind === "number") { const n=Number(text); return Number.isFinite(n)?n:text; }
    if (kind === "boolean") return text === "true";
    if (kind === "string_list") return text.split(",").map(x=>x.trim()).filter(Boolean);
    return text;
  }
  function defaultText(kind, value) {
    if (kind === "string_list") return Array.isArray(value)?value.join(", "):String(value??"");
    if (value === null || value === undefined) return "";
    return String(value);
  }
  function bundleKey() { return JSON.stringify(bundle); }
  function mechanicsStale() { return !!mechanicsSource && mechanicsSource !== bundleKey(); }
  function recordLiveLog(direction, path, value, status=null) {
    const row={at:new Date().toISOString(),direction,path,value};
    if(status!==null) row.status=status;
    liveLog.push(row);
  }
  function liveLogText(display=false) {
    return JSON.stringify(liveLog,(key,value)=>display && key==="replay_html" && typeof value==="string" ? `[replay_html hidden on-screen: ${value.length} chars; use Copy complete raw logs for the exact payload]` : value,2);
  }
  function openLogs() { active="logs"; history.replaceState(null,"",`?section=${active}`); rerender(); }
  async function api(path, body) {
    recordLiveLog("request",path,body);
    const response = await fetch(`/world-builder/api${path}`, {
      method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify(body)
    });
    const text=await response.text();
    let payload = {}; try { payload = text ? JSON.parse(text) : {}; } catch { payload={raw_response:text}; }
    recordLiveLog("response",path,payload,response.status);
    if (!response.ok) throw new Error(payload.error || `API request failed (${response.status})`);
    return payload;
  }
  function liveMessage(text, kind="muted") { const d=el("div",`live-message ${kind}`,text); return d; }
  function codeList(title, values) {
    const box=el("div","authority-block"); box.append(el("div","field-label",title));
    const list=el("div","code-list"); (values||[]).forEach(v=>list.append(el("code",null,String(v))));
    if(!(values||[]).length) list.append(el("span","muted","none")); box.append(list); return box;
  }
  function jsonRows(title, rows) {
    const box=el("div","authority-block"); box.append(el("div","field-label",title));
    (rows||[]).forEach(row=>box.append(el("pre","mini-json",JSON.stringify(row,null,2)))); return box;
  }
  function renderWorld() {
    editor.append(sectionHead("World", "Name the represented world and its shared starting location."));
    const c=card(); const w=bundle.world ||= {id:"new-world",label:"New world",summary:"Describe the represented world.",location:"world",content_version:1};
    c.append(field("World id",w.id,v=>{w.id=v;sync()}),field("Label",w.label,v=>{w.label=v;sync()}),field("Summary",w.summary,v=>{w.summary=v;sync()},{textarea:true}),field("Shared location",w.location,v=>{w.location=v;sync()}),field("Content version",w.content_version,v=>{const n=Number(v);w.content_version=Number.isInteger(n)?n:v;sync()},{type:"number"})); editor.append(c);
  }
  function renderComponents() {
    const head=sectionHead("Components", "Define typed state carried by entities. Relationship fields use entity_ref or entity_ref_or_null.");
    head.append(button("+ Component","primary",()=>{bundle.components.push({name:`component_${bundle.components.length+1}`,fields:[{name:"value",type:"string",default:"value"}]});rerender()})); editor.append(head);
    bundle.components.forEach((comp,ci)=>{
      const c=card(); const top=el("div","card-top"); top.append(el("h3",null,comp.name||`Component ${ci+1}`),button("Remove","danger",()=>{bundle.components.splice(ci,1);rerender()})); c.append(top);
      c.append(field("Component name",comp.name,v=>{comp.name=v;sync()}));
      const table=el("div","rows");
      comp.fields.forEach((f,fi)=>{
        const row=el("div","row-grid component-row");
        row.append(field("Field",f.name,v=>{f.name=v;sync()}));
        row.append(selectField("Type",f.type,core.FIELD_TYPES.map(x=>[x,x]),v=>{f.type=v;f.default=core.defaultForType(v);rerender()}));
        if(f.type==="boolean") row.append(selectField("Default",String(f.default),[["false","false"],["true","true"]],v=>{f.default=v==="true";sync()}));
        else row.append(field("Default",defaultText(f.type,f.default),v=>{f.default=parseDefault(f.type,v);sync()}));
        row.append(button("×","icon danger",()=>{comp.fields.splice(fi,1);rerender()})); table.append(row);
      });
      c.append(table,button("+ Field","secondary",()=>{comp.fields.push({name:`field_${comp.fields.length+1}`,type:"string",default:"value"});rerender()})); editor.append(c);
    });
    if(!bundle.components.length) editor.append(el("div","empty","No custom components yet. Built-in location, ownership and portability are available on entities."));
  }
  function renderEntities() {
    const head=sectionHead("Entities", "Create represented things and attach component values. Component values are JSON so the bundle remains explicit.");
    head.append(button("+ Entity","primary",()=>{bundle.entities.push({id:`entity-${bundle.entities.length+1}`,label:"New entity",categories:["thing"],components:{}});rerender()})); editor.append(head);
    bundle.entities.forEach((entity,ei)=>{
      const c=card(); const top=el("div","card-top");top.append(el("h3",null,entity.label||entity.id||`Entity ${ei+1}`),button("Remove","danger",()=>{bundle.entities.splice(ei,1);rerender()}));c.append(top);
      c.append(field("Entity id",entity.id,v=>{entity.id=v;sync()}),field("Label",entity.label,v=>{entity.label=v;sync()}),field("Categories (comma-separated)",(entity.categories||[]).join(", "),v=>{entity.categories=parseCategories(v);sync()}),field("Location override",entity.location||"",v=>{if(v.trim())entity.location=v;else delete entity.location;sync()},{placeholder:bundle.world?.location||"world default"}));
      c.append(selectField("Portable",entity.portable===undefined?"unset":String(entity.portable),[["unset","Not specified"],["true","Portable"],["false","Not portable"]],v=>{if(v==="unset")delete entity.portable;else entity.portable=v==="true";sync()}));
      c.append(field("Owner ref",entity.owner_ref||"",v=>{if(v.trim())entity.owner_ref=v;else delete entity.owner_ref;sync()},{placeholder:"place:location / actor:id / unowned"}));
      const compField=field("Component values (JSON)",JSON.stringify(entity.components||{},null,2),(v,input)=>{try{entity.components=JSON.parse(v||"{}");input.classList.remove("invalid");sync()}catch{input.classList.add("invalid");}},{textarea:true,event:"change"}); c.append(compField); editor.append(c);
    });
  }
  function renderActions() {
    const head=sectionHead("Action signatures", "Signatures describe intent shape only. They do not define checks, effects or write authority.");
    head.append(button("+ Action signature","primary",()=>{bundle.actions.push({kind:`action-${bundle.actions.length+1}`,description:"Describe the intent.",fields:[]});rerender()})); editor.append(head);
    const warning=el("div","boundary"); warning.append(el("strong",null,"Causal boundary"),document.createTextNode(" — the starter will generate a refusing rule stub for every signature here. Mechanics must still be implemented and reviewed in code.")); editor.append(warning);
    bundle.actions.forEach((action,ai)=>{
      const c=card();const top=el("div","card-top");top.append(el("h3",null,action.kind||`Action ${ai+1}`),button("Remove","danger",()=>{bundle.actions.splice(ai,1);rerender()}));c.append(top);
      c.append(field("Action kind",action.kind,v=>{action.kind=v;sync()}),field("Description",action.description,v=>{action.description=v;sync()},{textarea:true}));
      const rows=el("div","rows"); action.fields.forEach((f,fi)=>{const row=el("div","row-grid action-row");row.append(field("Field",f.name,v=>{f.name=v;sync()}),selectField("Type",f.type,core.ACTION_TYPES.map(x=>[x,x]),v=>{f.type=v;sync()}),button("×","icon danger",()=>{action.fields.splice(fi,1);rerender()}));rows.append(row)});c.append(rows,button("+ Field","secondary",()=>{action.fields.push({name:`target_${action.fields.length+1}`,type:"entity_ref"});rerender()}));editor.append(c);
    });
  }
  function objectRows(obj, kind, options) {
    const box=el("div","rows"); const entries=Object.entries(obj||{});
    entries.forEach(([key,val],i)=>{const row=el("div","row-grid presentation-row");row.append(field(kind==="asset"?"Asset id":"Category",key,v=>{delete obj[key];obj[v]=val;rerender()},{event:"change"}));
      if(kind==="asset") {row.append(selectField("Kind",val.kind,[["emoji","emoji"],["text","text"]],v=>{val.kind=v;sync()}),field("Value",val.value,v=>{val.value=v;sync()}));}
      else row.append(selectField(kind==="category"?"Asset":"Role",String(val),options(),v=>{obj[key]=v;sync()}));
      row.append(button("×","icon danger",()=>{delete obj[key];rerender()}));box.append(row)}); return box;
  }
  async function generateMechanics() {
    const check=core.validateBundle(bundle);
    if(!check.ok){alert("Fix bundle validation issues before generating mechanics.");return;}
    if(!(bundle.actions||[]).length){alert("Add at least one action signature first.");return;}
    liveBusy=true; runResult=null; rerender();
    try{
      const payload=await api("/generate-mechanics",{bundle,model:LIVE_MODEL,guidance:mechanicGuidance});
      causalModel=payload.causal_model; causalReview=payload.review; mechanicsSource=bundleKey(); mechanicsApproved=false;
      generationMeta={cost_usd:payload.cost_usd||0,daily_cost_usd:payload.daily_cost_usd,model:payload.model||LIVE_MODEL,trace_id:payload.trace_id||null};
    }catch(err){alert(`Mechanics generation failed: ${err.message}`);active="logs";}
    finally{liveBusy=false;rerender();}
  }
  function renderMechanics() {
    const head=sectionHead("Causal mechanics","Generate a constrained mechanics proposal, inspect the compiler-derived authority, then explicitly approve it before any run.");
    const gen=button(liveBusy?"Generating…":(causalModel?"Regenerate mechanics":"Generate causal mechanics"),"primary",generateMechanics);
    gen.disabled=liveBusy || !core.validateBundle(bundle).ok || !(bundle.actions||[]).length; head.append(gen); editor.append(head);
    const boundary=el("div","boundary");boundary.append(el("strong",null,"LLM proposes; compiler governs."),document.createTextNode(" The model cannot write Python or declare its own write scope. State paths, participants, checks and effects must compile against the represented world. A rejected proposal never installs."));editor.append(boundary);
    const guide=card("Optional guidance"); guide.append(field("What should the mechanics mean?",mechanicGuidance,v=>{mechanicGuidance=v;},{textarea:true,placeholder:"Example: Picking a fruit should transfer ownership, but do not invent a new completion state unless the world represents one."}));editor.append(guide);
    if(!causalModel){editor.append(liveMessage(liveBusy?"Asking the bounded mechanics proposer and compiling its answer…":"No causal mechanics have been generated yet."));return;}
    const stale=mechanicsStale();
    if(stale) editor.append(liveMessage("World structure changed after these mechanics were generated. Regenerate before approving or running.","warn"));
    if(generationMeta){const meta=card("Generation receipt");meta.append(el("div","receipt",`${generationMeta.model} · $${Number(generationMeta.cost_usd||0).toFixed(6)} this proposal${generationMeta.daily_cost_usd==null?"":` · $${Number(generationMeta.daily_cost_usd).toFixed(4)} World Builder today`}${generationMeta.trace_id?` · ${generationMeta.trace_id}`:""}`),button("Open full logs","secondary",openLogs));editor.append(meta);}
    (causalReview?.mechanics||[]).forEach(row=>{
      const c=card(`${row.action_kind} · ${row.mechanic_id}`); c.append(el("p","mechanic-rationale",row.rationale||""));
      const grid=el("div","authority-grid");grid.append(codeList("Derived reads",row.reads),codeList("Derived writes",row.writes));c.append(grid,jsonRows("Checks",row.checks),jsonRows("Effects",row.effects),codeList("Limits",row.limits),codeList("Declared tests",row.tests));editor.append(c);
    });
    const terminal=card("Terminal condition"); terminal.append(causalReview?.terminal?el("pre","mini-json",JSON.stringify(causalReview.terminal,null,2)):liveMessage("No terminal condition was proposed. A run can still stop when no actions remain or at its turn ceiling."));editor.append(terminal);
    const approve=button(mechanicsApproved?"✓ Mechanics approved":"Approve mechanics for run",mechanicsApproved?"secondary":"primary",()=>{if(!stale){mechanicsApproved=true;runResult=null;rerender();}});approve.disabled=stale||mechanicsApproved;editor.append(approve);
  }
  function renderPresentation() {
    editor.append(sectionHead("Presentation", "Presentation suggests how the eventual Automatic replay should look. It never changes world truth."));
    const p=bundle.presentation ||= {assets:{},category_assets:{},station_roles:{}};
    let c=card("Assets");c.append(objectRows(p.assets,"asset",()=>[]),button("+ Asset","secondary",()=>{let n=1;while(p.assets[`asset_${n}`])n++;p.assets[`asset_${n}`]={kind:"emoji",value:"◼"};rerender()}));editor.append(c);
    c=card("Category → asset");c.append(objectRows(p.category_assets,"category",()=>Object.keys(p.assets).map(x=>[x,x])),button("+ Binding","secondary",()=>{let n=1;while(p.category_assets[`category_${n}`])n++;p.category_assets[`category_${n}`]=Object.keys(p.assets)[0]||"";rerender()}));editor.append(c);
    c=card("Station roles");c.append(objectRows(p.station_roles,"role",()=>[["source","source"],["workstation","workstation"],["surface","surface"],["goal","goal"]]),button("+ Station role","secondary",()=>{let n=1;while(p.station_roles[`station_${n}`])n++;p.station_roles[`station_${n}`]="surface";rerender()}));editor.append(c);
  }
  async function startFreshRun() {
    if(!causalModel || mechanicsStale() || !mechanicsApproved){alert("Generate and approve current mechanics first.");return;}
    liveBusy=true;runResult=null;rerender();
    try{
      runResult=await api("/run",{bundle,causal_model:causalModel,approved:true,policy:runPolicy,turns:runTurns,model:LIVE_MODEL});
    }catch(err){alert(`Run failed: ${err.message}`);active="logs";}
    finally{liveBusy=false;rerender();}
  }
  function renderRun() {
    const head=sectionHead("Run this world","Start a fresh simulation from the current represented world and approved mechanics, then watch the resulting graphical replay here.");
    const run=button(liveBusy?"Running…":"Run fresh simulation","primary",startFreshRun);run.disabled=liveBusy||!causalModel||mechanicsStale()||!mechanicsApproved;head.append(run);editor.append(head);
    if(!causalModel) editor.append(liveMessage("Generate causal mechanics first."));
    else if(mechanicsStale()) editor.append(liveMessage("Mechanics are stale because the world changed. Regenerate them first.","warn"));
    else if(!mechanicsApproved) editor.append(liveMessage("Review and approve the generated mechanics before running.","warn"));
    const controls=card("Run controls");
    controls.append(selectField("Policy",runPolicy,[["scripted","Scripted · deterministic first available · $0"],["llm","LLM · chooses among engine-offered actions"]],v=>{runPolicy=v;runResult=null;sync()}));
    controls.append(field("Turn ceiling",runTurns,v=>{const n=Number(v);runTurns=Number.isInteger(n)?Math.max(1,Math.min(30,n)):12;},{type:"number"}));
    if(runPolicy==="llm") controls.append(liveMessage(`LLM policy uses ${LIVE_MODEL}. The model selects action IDs only; installed mechanics compute consequences. Each public run is budget- and rate-limited.`));
    editor.append(controls);
    if(runResult){
      const summary=card("Fresh run result");const sm=runResult.summary||{};summary.append(el("div","receipt",`${sm.turns||0} turn(s) · ${sm.accepted_actions||0} accepted action(s) · terminal ${sm.terminal_reached?"reached":"not reached"} · $${Number(runResult.cost_usd||0).toFixed(6)}${runResult.trace_id?` · ${runResult.trace_id}`:""}`),button("Open full logs","secondary",openLogs));editor.append(summary);
      const frame=document.createElement("iframe");frame.className="run-frame";frame.setAttribute("sandbox","allow-scripts");frame.srcdoc=runResult.replay_html||"";editor.append(frame);
    }
  }
  function renderLogs() {
    const head=sectionHead("Full logs","Inspect the complete request/response history for mechanics generation and runs. Full engine traces, compiler review, costs, trace ids, refusals and policy reasoning are retained here for debugging.");
    head.append(button("Copy complete raw logs","primary",async()=>{await copyText(liveLogText(false)+"\n");}));editor.append(head);
    const boundary=el("div","boundary");boundary.append(el("strong",null,"Debug from evidence, not summaries."),document.createTextNode(" The on-screen view preserves every request, causal model, compiler review and execution trace. Replay HTML is collapsed only in this view to keep it readable; Copy complete raw logs includes the exact replay HTML too."));editor.append(boundary);
    if(!liveLog.length){editor.append(liveMessage("No live API calls have been made in this browser session yet."));return;}
    const controls=card("Log controls");controls.append(el("div","receipt",`${liveLog.length} request/response record(s)`),button("Clear logs","secondary",()=>{if(confirm("Clear this browser session's logs?")){liveLog=[];rerender();}}));editor.append(controls);
    const pre=el("pre","mini-json",liveLogText(true));pre.style.whiteSpace="pre";pre.style.maxHeight="72vh";pre.style.overflow="auto";editor.append(pre);
  }
  function renderExport() {
    editor.append(sectionHead("Review & export", "Optional code-first handoff. You can build, generate mechanics, and run on this page without downloading anything."));
    const c=card("What happens next");
    const ol=el("ol","steps");["Use Download only if you want the bundle as a code artifact.","The code-first scaffold preserves the same represented state and action signatures.","Generated causal mechanics remain a separate reviewed declaration rather than hidden browser behavior."].forEach(x=>ol.append(el("li",null,x)));c.append(ol);editor.append(c);
    const b=el("div","boundary");b.append(el("strong",null,"Signatures still are not causal law."),document.createTextNode(" Causal effects come only from a separately generated, compiler-validated, explicitly approved mechanics declaration."));editor.append(b);
  }
  function renderSection() {
    editor.replaceChildren();
    ({world:renderWorld,components:renderComponents,entities:renderEntities,actions:renderActions,mechanics:renderMechanics,presentation:renderPresentation,run:renderRun,logs:renderLogs,export:renderExport})[active]();
  }
  document.querySelectorAll("[data-section]").forEach(b=>b.addEventListener("click",()=>{active=b.dataset.section;history.replaceState(null,"",`?section=${active}`);rerender()}));
  document.getElementById("import-bundle").addEventListener("click",()=>document.getElementById("file-input").click());
  document.getElementById("file-input").addEventListener("change",async e=>{const file=e.target.files?.[0];if(!file)return;try{const value=JSON.parse(await file.text());if(!value||typeof value!=="object")throw new Error("not an object");bundle=value;causalModel=null;causalReview=null;mechanicsSource=null;mechanicsApproved=false;runResult=null;active="world";rerender()}catch(err){alert(`Could not import JSON: ${err.message}`)}finally{e.target.value=""}});
  document.getElementById("reset-example").addEventListener("click",()=>{if(confirm("Reset to the embedded Orchard example?")){bundle=core.clone(window.INITIAL_BUNDLE);causalModel=null;causalReview=null;mechanicsSource=null;mechanicsApproved=false;runResult=null;active="world";rerender()}});
  downloadBtn.addEventListener("click",()=>{const r=core.validateBundle(bundle);if(!r.ok)return;const blob=new Blob([JSON.stringify(bundle,null,2)+"\n"],{type:"application/json"});const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download=`${bundle.world.id}-authoring-v0.json`;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)});
  async function copyText(text) {
    try { if (navigator.clipboard && window.isSecureContext) { await navigator.clipboard.writeText(text); return; } } catch {}
    const area=document.createElement("textarea");area.value=text;area.style.position="fixed";area.style.opacity="0";document.body.append(area);area.select();document.execCommand("copy");area.remove();
  }
  document.getElementById("copy-json").addEventListener("click",async()=>{await copyText(JSON.stringify(bundle,null,2)+"\n");});
  document.getElementById("copy-command").addEventListener("click",async()=>{const id=bundle.world?.id||"world";await copyText(`python scripts/scaffold_world.py ${id}-authoring-v0.json --output-root reference_worlds`);});
  rerender();
})();