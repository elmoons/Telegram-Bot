document.addEventListener("DOMContentLoaded", () => {
    setupGrid();
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