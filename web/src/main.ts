import "./style.css";
import geometry from "./geometry.json";

const MAX_X = 800;
const MAX_Y = 586;

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

Object.values(geometry).forEach(([x, y]) => {
  fillCirc(x * MAX_X, y * MAX_Y, 255, 255, 255);
});
