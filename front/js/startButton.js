document.addEventListener("DOMContentLoaded", () => {
    setupStartButton();
  });
  
  function setupStartButton() {
    const starButton = document.getElementById("start-button");
  
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