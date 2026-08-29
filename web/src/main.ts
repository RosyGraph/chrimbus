import "./style.css";

const canvas = document.querySelector<HTMLCanvasElement>("#display");

if (!canvas) {
  throw new Error("Display canvas not found");
}

const ctx = canvas.getContext("2d");

if (!ctx) {
  throw new Error("2D canvas context unavailable");
}
