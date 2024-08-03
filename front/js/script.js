document.getElementById("colorButton").addEventListener("click", () => {
  const squares = document.querySelectorAll(".square");
  const numberOfSquaresToColor = 5;
  const selectedIndices = [];

  squares.forEach(square => square.classList.remove("colored"));

  while (selectedIndices.length < numberOfSquaresToColor) {
    const randomIndex = Math.floor(Math.random() * squares.length);
    if (!selectedIndices.includes(randomIndex)) {
      selectedIndices.push(randomIndex);
      squares[randomIndex].classList.add("colored");
    }
  }
});