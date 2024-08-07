// headerAnimation.js
document.addEventListener("DOMContentLoaded", () => {
    executeHeaderTextAnimation();
  });
  
  function executeHeaderTextAnimation(){
    var header = document.getElementById('header-text');
    var text = header.textContent;
    var spans = text.split('').map(function (char, index) {
      var delay = Math.random() * 2;
      return `<span style="animation-delay: ${delay}s">${char}</span>`;
    });
    header.innerHTML = spans.join('');
  }