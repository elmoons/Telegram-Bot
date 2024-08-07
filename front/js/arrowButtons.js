document.addEventListener("DOMContentLoaded", () => {
    setupArrowButtons();
  });
  
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