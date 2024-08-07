document.addEventListener("DOMContentLoaded", () => {
  setupGrid();
  setupArrowButtons();
  setupStarButton();
  initializeLanguage();
});

function setupGrid() {
  const container = document.querySelector(".grid-container");
  const numSquares = 25;

  for (let i = 0; i < numSquares; i++) {
    const square = document.createElement("div");
    square.classList.add("square");
    container.appendChild(square);
  }
}

function setupArrowButtons() {
  const leftArrow = document.getElementById("left-arrow");
  const rightArrow = document.getElementById("right-arrow");
  const numberDisplay = document.getElementById("number-display");

  const values = [1, 3, 5];
  let index = 0;

  leftArrow.addEventListener("click", () => {
    if (index > 0) {
      index--;
      numberDisplay.textContent = values[index];
    }
  });

  rightArrow.addEventListener("click", () => {
    if (index < values.length - 1) {
      index++;
      numberDisplay.textContent = values[index];
    }
  });
}

function executeHeaderTextAnimation(){
  var header = document.getElementById('header-text');
  var text = header.textContent;
  var spans = text.split('').map(function (char, index) {
    var delay = Math.random() * 2;
    return `<span style="animation-delay: ${delay}s">${char}</span>`;
  });
  header.innerHTML = spans.join('');
}

function setupStarButton() {
  const starButton = document.getElementById("star-button");

  starButton.addEventListener("click", () => {
    starButton.disabled = true;
    const squares = document.querySelectorAll(".square");
    const numberOfSquaresToColor = Math.random() < 0.5 ? 4 : 5;
    const selectedIndices = [];

    squares.forEach(square => {
      square.classList.remove("starred");
      square.style.animation = "none";
      square.offsetHeight;
      square.style.animation = "";
    });

    while (selectedIndices.length < numberOfSquaresToColor) {
      const randomIndex = Math.floor(Math.random() * squares.length);
      if (!selectedIndices.includes(randomIndex)) {
        selectedIndices.push(randomIndex);
      }
    }
    selectedIndices.forEach((index, i) => {
      setTimeout(() => {
        squares[index].classList.add("starred");
        if (i === selectedIndices.length - 1) {
          starButton.disabled = false;
        }
      }, i * 1000);
    });
  });
}

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
