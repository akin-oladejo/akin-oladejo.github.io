let viewportHeight = window.innerHeight;
let viewportWidth = window.innerWidth;

let side_right = document.getElementById('side-right');

// make page proportionate size throughout resize like cssgrids.com
function fixSideSize() {
    let scale = viewportHeight / window.innerHeight;

}

// function to hide scrollbar when not scrolling
function toggleScrollBar() {
    // let scrollbar = document.querySelector(scrollbars)
}

const $icon = document.querySelector('.button2');
const $arrow = document.querySelector('.arrow');

$icon.onmouseover = () => {
  $arrow.animate([
    {left: '0'},
    {left: '10px'},
    {left: '0'}
  ],{
    duration: 1000,
    iterations: 2
  });
}