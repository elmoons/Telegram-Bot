document.addEventListener("DOMContentLoaded", () => {
    initializeLanguage();
  });
  
  const translations = {
    en: {
        headerText: "Text",
        numberSelectorText: "AMOUNT OF CUBES",
        button: "Русский"
    },
    ru: {
        headerText: "Текст",
        numberSelectorText: "КОЛ-ВО КВАДРАТОВ",
        button: "English"
    }
  };
  
  let currentLanguage = 'en';
  
  function toggleLanguage() {
    currentLanguage = currentLanguage === 'en' ? 'ru' : 'en';
    setLanguage(currentLanguage);
    executeHeaderTextAnimation();
  }
  
  function setLanguage(language) {
    document.getElementById('header-text').innerText = translations[language].headerText;
    document.getElementById('number-selector-text').innerText = translations[language].numberSelectorText;
    document.getElementById('language-button').innerText = translations[language].button;
    localStorage.setItem('language', language);
  }
  
  function initializeLanguage() {
    currentLanguage = localStorage.getItem('language') || 'en';
    setLanguage(currentLanguage);
    executeHeaderTextAnimation();
  }