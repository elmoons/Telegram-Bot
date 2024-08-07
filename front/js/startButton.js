document.addEventListener("DOMContentLoaded", () => {
    setupStartButton();
  });

const starButton = document.getElementById("start-button");
const leftArrow = document.getElementById("left-arrow");
const rightArrow = document.getElementById("right-arrow");

  function setupStartButton() {
    starButton.addEventListener("click", () => {
      DisableButtons();
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
            EnableButtons();
          }
        }, i * 1000);
      });
    });
  }

  function DisableButtons()
  {
    starButton.disabled = true;
    leftArrow.disabled = true;
    rightArrow.disabled = true;
  }
  function EnableButtons()
  {
    starButton.disabled = false;
    leftArrow.disabled = false;
    rightArrow.disabled = false;
  }