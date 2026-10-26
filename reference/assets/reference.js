'use strict';
const selector=document.getElementById('language-select');
if(selector) selector.addEventListener('change',()=>{const paths={"en":"/IMPERIAL-Core-Public/reference/","uk":"/IMPERIAL-Core-Public/reference/uk/","ja":"/IMPERIAL-Core-Public/reference/ja/","zh":"/IMPERIAL-Core-Public/reference/zh/","de-CH":"/IMPERIAL-Core-Public/reference/de-CH/","ru":"/IMPERIAL-Core-Public/reference/ru/"};if(Object.hasOwn(paths,selector.value)) location.assign(paths[selector.value]+location.hash);});
