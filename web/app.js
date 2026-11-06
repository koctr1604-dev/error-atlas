'use strict';
(() => {
  const entries = JSON.parse(document.getElementById('catalog').textContent);
  const categories = {all:'全部',ci:'CI / 持续集成',tls:'TLS / 证书',permissions:'权限 / 身份',packages:'包管理 / 依赖'};
  const query = document.getElementById('query');
  const results = document.getElementById('results');
  const dialog = document.getElementById('detail');
  let category = 'all';
  function el(tag, text, cls) {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (cls) node.className = cls;
    return node;
  }
  function paragraph(label, text) {
    const p = el('p');
    p.append(el('strong', label + '：'), document.createTextNode(text));
    return p;
  }
  function openEntry(entry, updateHash = true) {
    const body = document.getElementById('detail-content');
    body.replaceChildren();
    const title = el('h2', entry.error); title.id = 'detail-title';
    const label = entry.verification === 'reproduced' ? '已复现，见贡献记录' : '文档核对；未声称实机复现';
    body.append(title, el('p', entry.summary, 'summary'), el('p', `${entry.tool} · ${categories[entry.category]} · ${entry.verified_on} · ${label}`, 'verification'));
    if (entry.aliases.length) body.append(el('p', '同类报错 / 搜索词：' + entry.aliases.join(' · '), 'code-note'));
    body.append(el('h3', '确认原因，再修复'));
    entry.causes.forEach((cause, i) => {
      const box = el('section', undefined, 'cause');
      box.append(el('h4', `${i+1}. ${cause.when}`), paragraph('原因', cause.reason), paragraph('确认', cause.check), paragraph('修复', cause.fix));
      body.append(box);
    });
    if (entry.commands.length) body.append(el('h3', '命令 / 配置示例'));
    entry.commands.forEach(cmd => {
      const box = el('section', undefined, 'code-block');
      const head = el('div', undefined, 'code-head');
      const button = el('button', '复制'); button.type = 'button'; button.setAttribute('aria-label', '复制：' + cmd.label);
      const pre = el('pre'); const code = el('code', cmd.code); pre.append(code);
      button.addEventListener('click', async () => {
        try { await navigator.clipboard.writeText(cmd.code); button.textContent = '已复制'; }
        catch { const range = document.createRange(); range.selectNodeContents(code); const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range); button.textContent = '已选中，请手动复制'; }
      });
      head.append(el('h4', `${cmd.kind === 'diagnostic' ? '诊断' : '修复'} · ${cmd.label}`), button);
      box.append(head, el('p', cmd.note, 'code-note'), pre); body.append(box);
    });
    if (entry.cautions.length) {
      body.append(el('h3', '边界与注意事项')); const list = el('ul');
      entry.cautions.forEach(s => list.append(el('li', s))); body.append(list);
    }
    body.append(el('h3', '官方依据')); const list = el('ul');
    entry.sources.forEach(source => { const li=el('li'); const a=el('a',source.title); a.href=source.url; a.target='_blank'; a.rel='noopener noreferrer'; li.append(a); list.append(li); });
    body.append(list, el('p', `条目 ID：${entry.id}`, 'code-note'));
    if (!dialog.open) dialog.showModal();
    dialog.scrollTop = 0;
    if (updateHash) location.hash = entry.id;
  }
  function render() {
    const found = ErrorAtlasSearch.search(entries, query.value, category);
    results.replaceChildren();
    document.getElementById('result-count').textContent = `${found.length} 条匹配 / ${entries.length} 条收录`;
    document.querySelectorAll('.filter').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.category === category)));
    if (!found.length) {
      const empty=el('div', undefined, 'empty'); empty.append(el('h2','暂时没有匹配的条目'),el('p','尝试保留错误码或核心短语，去掉时间戳、路径和变量值，或者切换到“全部”。')); results.append(empty);
    }
    found.forEach(entry => {
      const card=el('article',undefined,'card');
      const meta=el('div',undefined,'meta'); meta.append(el('span',categories[entry.category],'badge'),el('span',entry.tool));
      const bottom=el('div',undefined,'card-bottom'); const button=el('button','查看确认与修复 ↗','open-entry'); button.type='button'; button.setAttribute('aria-label','查看：'+entry.error); button.addEventListener('click',()=>openEntry(entry));
      bottom.append(button,el('span',entry.verified_on,'date'));
      card.append(meta,el('h2',entry.error),el('p',entry.summary),bottom); results.append(card);
    });
  }
  Object.entries(categories).forEach(([id, label]) => {
    const button=el('button',label,'filter'); button.type='button'; button.dataset.category=id;
    button.append(el('small',String(id==='all'?entries.length:entries.filter(e=>e.category===id).length)));
    button.addEventListener('click',()=>{category=id;render();}); document.getElementById('filters').append(button);
  });
  document.getElementById('total-count').textContent=entries.length;
  query.addEventListener('input',render);
  document.getElementById('clear').addEventListener('click',()=>{query.value='';render();query.focus();});
  document.querySelectorAll('.examples button').forEach(button=>button.addEventListener('click',()=>{query.value=button.textContent;category='all';render();}));
  document.getElementById('close').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('close',()=>{if(location.hash) history.replaceState(null,'',location.pathname+location.search);});
  function fromHash() {let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}const entry=entries.find(e=>e.id===id);if(entry)openEntry(entry,false);else if(dialog.open)dialog.close();}
  window.addEventListener('hashchange',fromHash);
  render(); fromHash();
})();
