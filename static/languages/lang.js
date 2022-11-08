import lang_en from './lang_en.json' assert {type: 'json'};
import lang_vi from './lang_vi.json' assert {type: 'json'};
import lang_zh from './lang_zh.json' assert {type: 'json'};

const LangSelect = document.querySelectorAll('.lang_select');
const SelectLangBoard = document.querySelector('.select_lang');
const NavbarLang = document.querySelector('#language');

var textNodes = [];

function findText(pnode) {
  for (var i = 0; i < pnode.childNodes.length; ++i) {
    var node = pnode.childNodes[i];
    
    if (node.nodeType == 3) {
      textNodes.push(node);
    } 
    else {
      findText(node);
    }
  }
}
findText(document.body);

function changelang(lang) {
  for (const [key, value] of Object.entries(lang)) {
    for (var i = 0; i < textNodes.length; ++i) {
        textNodes[i].textContent = textNodes[i].textContent.replace(key, value);
    }
  }
}


var lang = localStorage.getItem('lang');

if (lang=='english') {
  changelang(lang_en);
}
else if (lang=='vietnamese') {
  changelang(lang_vi);
}
else if (lang=='chinese') {
  changelang(lang_zh);
}

LangSelect.forEach(lang => {
  lang.addEventListener('click', ()=>{
    var value = lang.id;
    localStorage.setItem('lang', value);
    location.reload();
  })
})


var check_click_language = true;
NavbarLang.addEventListener('click', () => {
    if (check_click_language) {
        SelectLangBoard.style.display = "block";
        check_click_language = false;
    }
    else{
        SelectLangBoard.style.display = "none";
        check_click_language = true;
    }
})
