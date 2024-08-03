document.getElementById("colorButton").addEventListener("click", () => {
  const squares = document.querySelectorAll(".square");
  const numberOfSquaresToColor = Math.random() < 0.5 ? 4 : 5;
  const selectedIndices = [];

  squares.forEach(square => {
    square.classList.remove("starred");
    square.style.animation = 'none';
    square.offsetHeight;
    square.style.animation = '';
  });

  while (selectedIndices.length < numberOfSquaresToColor) {
    const randomIndex = Math.floor(Math.random() * squares.length);
    if (!selectedIndices.includes(randomIndex)) {
      selectedIndices.push(randomIndex);
      squares[randomIndex].classList.add("starred");
    }
  }
});

document.addEventListener('DOMContentLoaded', function() {
  var header = document.getElementById('headerText');
  var text = header.textContent;
  var spans = text.split('').map(function(char, index) {
    var delay = Math.random() * 2;
    return `<span style="animation-delay: ${delay}s">${char}</span>`;
    });
  header.innerHTML = spans.join('');
});