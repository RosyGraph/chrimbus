import "./style.css";
import { drawFrame } from "./renderer";
import basic from "./basic.json";
import { validateAnimation } from "./animation";
import { play } from "./player";

const canvas = document.querySelector<HTMLCanvasElement>("#display");

if (!canvas) {
  throw new Error("Display canvas not found");
}

const ctx = canvas.getContext("2d");
if (!ctx) {
  throw new Error("2D canvas context unavailable");
}

const animation = validateAnimation(basic);
let currFrame = 0;
play(animation.fps, () => {
  drawFrame(ctx, animation.frames[currFrame]);
  currFrame = (currFrame + 1) % animation.frames.length;
});
