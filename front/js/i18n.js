document.addEventListener("DOMContentLoaded", () => {
  initializeLanguage();
});

function initializeLanguage() {
  setLanguage(localStorage.getItem('language') || 'EN');
}

const languageBtn = document.getElementById('language-btn');
const languageMenu = document.getElementById('language-menu');
const headerText = document.getElementById('header-text');
const numberSelectorText = document.getElementById('number-selector-text');
const startButton = document.getElementById('start-button');

const texts = {
    RU: {
        header: 'Текст',
        numberSelector: 'КОЛ-ВО КВАДРАТОВ',
        languageBtn: 'Язык: RU',
        startButton: 'Старт'
    },
    EN: {
        header: 'Text',
        numberSelector: 'NUMBER OF SQUARES',
        languageBtn: 'language: EN',
        startButton: 'Start'
    },
};

languageBtn.addEventListener('click', () => {
    const isVisible = languageMenu.style.display === 'block';
    languageMenu.style.display = isVisible ? 'none' : 'block';
});

function setLanguage(lang) {
    headerText.textContent = texts[lang].header;
    numberSelectorText.textContent = texts[lang].numberSelector;
    startButton.textContent = texts[lang].startButton;
    languageBtn.textContent = texts[lang].languageBtn;

    languageMenu.style.display = 'none';
    localStorage.setItem('language', lang);
    executeHeaderTextAnimation();
}

document.addEventListener('click', (event) => {
    if (!languageBtn.contains(event.target) && !languageMenu.contains(event.target)) {
        languageMenu.style.display = 'none';
    }
});