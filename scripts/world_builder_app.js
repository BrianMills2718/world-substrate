(function () {
  "use strict";
  const core = window.WorldBuilderCore;
  let bundle = core.clone(window.INITIAL_BUNDLE);
  let active = new URLSearchParams(location.search).get("section") || "world";
  const sections = ["world", "components", "entities", "actions", "presentation", "export"];
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
  function renderPresentation() {
    editor.append(sectionHead("Presentation", "Presentation suggests how the eventual Automatic replay should look. It never changes world truth."));
    const p=bundle.presentation ||= {assets:{},category_assets:{},station_roles:{}};
    let c=card("Assets");c.append(objectRows(p.assets,"asset",()=>[]),button("+ Asset","secondary",()=>{let n=1;while(p.assets[`asset_${n}`])n++;p.assets[`asset_${n}`]={kind:"emoji",value:"◼"};rerender()}));editor.append(c);
    c=card("Category → asset");c.append(objectRows(p.category_assets,"category",()=>Object.keys(p.assets).map(x=>[x,x])),button("+ Binding","secondary",()=>{let n=1;while(p.category_assets[`category_${n}`])n++;p.category_assets[`category_${n}`]=Object.keys(p.assets)[0]||"";rerender()}));editor.append(c);
    c=card("Station roles");c.append(objectRows(p.station_roles,"role",()=>[["source","source"],["workstation","workstation"],["surface","surface"],["goal","goal"]]),button("+ Station role","secondary",()=>{let n=1;while(p.station_roles[`station_${n}`])n++;p.station_roles[`station_${n}`]="surface";rerender()}));editor.append(c);
  }
  function renderExport() {
    editor.append(sectionHead("Review & export", "Export this exact bundle, then scaffold the code-first world package from it."));
    const c=card("What happens next");
    const ol=el("ol","steps");["Download the valid authoring bundle.","Run the scaffold command shown on the right.","Implement causal mechanics in the generated refusing stubs.","Derive a terminal predicate from represented state.","Retain a deterministic run, then bootstrap an Automatic replay."].forEach(x=>ol.append(el("li",null,x)));c.append(ol);editor.append(c);
    const b=el("div","boundary");b.append(el("strong",null,"The builder does not author causal effects."),document.createTextNode(" It authors structure, signatures, and presentation intent. This is intentional."));editor.append(b);
  }
  function renderSection() {
    editor.replaceChildren();
    ({world:renderWorld,components:renderComponents,entities:renderEntities,actions:renderActions,presentation:renderPresentation,export:renderExport})[active]();
  }
  document.querySelectorAll("[data-section]").forEach(b=>b.addEventListener("click",()=>{active=b.dataset.section;history.replaceState(null,"",`?section=${active}`);rerender()}));
  document.getElementById("import-bundle").addEventListener("click",()=>document.getElementById("file-input").click());
  document.getElementById("file-input").addEventListener("change",async e=>{const file=e.target.files?.[0];if(!file)return;try{const value=JSON.parse(await file.text());if(!value||typeof value!=="object")throw new Error("not an object");bundle=value;active="world";rerender()}catch(err){alert(`Could not import JSON: ${err.message}`)}finally{e.target.value=""}});
  document.getElementById("reset-example").addEventListener("click",()=>{if(confirm("Reset to the embedded Orchard example?")){bundle=core.clone(window.INITIAL_BUNDLE);active="world";rerender()}});
  downloadBtn.addEventListener("click",()=>{const r=core.validateBundle(bundle);if(!r.ok)return;const blob=new Blob([JSON.stringify(bundle,null,2)+"\n"],{type:"application/json"});const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download=`${bundle.world.id}-authoring-v0.json`;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)});
  async function copyText(text) {
    try { if (navigator.clipboard && window.isSecureContext) { await navigator.clipboard.writeText(text); return; } } catch {}
    const area=document.createElement("textarea");area.value=text;area.style.position="fixed";area.style.opacity="0";document.body.append(area);area.select();document.execCommand("copy");area.remove();
  }
  document.getElementById("copy-json").addEventListener("click",async()=>{await copyText(JSON.stringify(bundle,null,2)+"\n");});
  document.getElementById("copy-command").addEventListener("click",async()=>{const id=bundle.world?.id||"world";await copyText(`python scripts/scaffold_world.py ${id}-authoring-v0.json --output-root reference_worlds`);});
  rerender();
})();
