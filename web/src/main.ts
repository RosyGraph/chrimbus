import "./style.css";

const canvas = document.querySelector<HTMLCanvasElement>("#display");

if (!canvas) {
  throw new Error("Display canvas not found");
}

const ctx = canvas.getContext("2d");

if (!ctx) {
  throw new Error("2D canvas context unavailable");
}

function fillCirc(x, y, r, g, b) {
  ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
  ctx.beginPath();
  ctx.arc(x, y, 5, 0, Math.PI * 2);
  ctx.fill();
}
[
  { x: 100, y: 100, r: 255, g: 0, b: 0 },
  { x: 120, y: 110, r: 255, g: 255, b: 0 },
  { x: 140, y: 120, r: 0, g: 255, b: 0 },
  { x: 160, y: 130, r: 0, g: 255, b: 255 },
].forEach(({ x, y, r, g, b }) => {
  fillCirc(x, y, r, g, b);
});
