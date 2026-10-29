'use strict';
// Native links work without JavaScript; language preferences never force redirects.
const languageMenu=document.querySelector('.reference-language-menu');
const localeLinks=[...document.querySelectorAll('[data-locale-link]')];
const available=new Map(localeLinks.map(link=>[link.dataset.localeLink,link]));
const preferenceKey='imperial-core-language';
for(const link of localeLinks){
  link.addEventListener('click',()=>{
    try{localStorage.setItem(preferenceKey,link.dataset.localeLink);}catch{}
    if(location.hash) link.hash=location.hash;
  });
}
if(languageMenu){
  document.addEventListener('click',event=>{if(!languageMenu.contains(event.target)) languageMenu.open=false;});
  languageMenu.addEventListener('keydown',event=>{
    if(event.key==='Escape'){languageMenu.open=false;languageMenu.querySelector('summary').focus();}
  });
}
const preference=document.querySelector('.language-preference');
if(preference){
  let preferred;
  try{preferred=localStorage.getItem(preferenceKey);}catch{}
  if(!available.has(preferred)){
    const candidates=navigator.languages||[navigator.language];
    preferred=candidates.map(code=>available.has(code)?code:code.toLowerCase().startsWith('de')?'de-CH':code.split('-')[0]).find(code=>available.has(code));
  }
  if(preferred && preferred!==document.documentElement.lang && available.has(preferred)){
    const destination=available.get(preferred);
    const link=preference.querySelector('a');
    link.textContent=preference.dataset.prefix+' '+destination.textContent+' →';
    link.href=destination.href+location.hash;
    link.addEventListener('click',()=>{try{localStorage.setItem(preferenceKey,preferred);}catch{}});
    preference.hidden=false;
  }
}
const search=document.getElementById('reference-search');
if(search){
  const panel=search.closest('.reference-search');
  const cards=[...document.querySelectorAll('#reference-sections .sheet-card')];
  const indexLinks=[...document.querySelectorAll('.section-index a')];
  const status=document.getElementById('search-status');
  const empty=document.getElementById('search-empty');
  const normalize=value=>value.normalize('NFKD').replace(/\p{M}/gu,'').toLocaleLowerCase().trim();
  const corpus=cards.map(card=>normalize(card.textContent));
  function filter(){
    const terms=normalize(search.value).split(/\s+/).filter(Boolean);
    const visible=new Set();
    cards.forEach((card,index)=>{
      card.hidden=!terms.every(term=>corpus[index].includes(term));
      if(!card.hidden) visible.add(card.id);
    });
    for(const link of indexLinks)link.hidden=!visible.has(link.hash.slice(1));
    status.textContent=`${visible.size} / ${cards.length} ${status.dataset.resultsLabel}`;
    empty.hidden=visible.size!==0;
  }
  panel.hidden=false;
  search.addEventListener('input',filter);
  document.getElementById('clear-search').addEventListener('click',()=>{search.value='';filter();search.focus();});
  search.addEventListener('keydown',event=>{if(event.key==='Escape'){search.value='';filter();}});
  document.addEventListener('keydown',event=>{
    if(event.key==='/' && !event.ctrlKey && !event.metaKey && !event.altKey && !event.target.closest('input,textarea,select,[contenteditable]')){event.preventDefault();search.focus();}
  });
  window.addEventListener('hashchange',()=>{
    if(location.hash.startsWith('#section-')){search.value='';filter();document.getElementById(location.hash.slice(1))?.scrollIntoView();}
  });
}
