document.getElementById("colorButton").addEventListener("click", () => {
  const squares = document.querySelectorAll(".square");
  const numberOfSquaresToColor = Math.random() < 0.5 ? 4 : 5;
  const selectedIndices = [];

  squares.forEach(square => square.classList.remove("starred"));

  while (selectedIndices.length < numberOfSquaresToColor) {
    const randomIndex = Math.floor(Math.random() * squares.length);
    if (!selectedIndices.includes(randomIndex)) {
      selectedIndices.push(randomIndex);
      squares[randomIndex].classList.add("starred");
    }
  }
});