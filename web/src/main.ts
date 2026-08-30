import "./style.css";
import geometry from "./geometry.json";
import basic from "./basic.json";
import type { AnimationSchema } from "./generated/animation";
import Ajv from "ajv";
import schema from "./animation.schema.json";

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

function fillCirc(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  pixel: AnimationSchema["frames"][number][number],
) {
  const [r, g, b] = pixel;
  ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
  ctx.beginPath();
  ctx.arc(x, y, 5, 0, Math.PI * 2);
  ctx.fill();
}

const ajv = new Ajv();
const validateAnimation = ajv.compile<AnimationSchema>(schema);
const animation: unknown = basic;
if (!validateAnimation(animation)) {
  throw new Error("Invalid animation");
}
const frameDuration = 1_000 / animation.fps;
let lastFrameTime = 0;

let currFrame = 0;
function draw(ctx: CanvasRenderingContext2D, animation: AnimationSchema) {
  const frame = animation.frames[currFrame];
  Object.values(geometry).forEach(([x, y], i) => {
    const pixel = frame[i];
    fillCirc(ctx, x * MAX_X, y * MAX_Y, pixel);
  });
  currFrame = (currFrame + 1) % animation.frames.length;
}
function animate(time: number, draw: () => void) {
  if (time - lastFrameTime >= frameDuration) {
    draw();
    lastFrameTime += frameDuration;
  }

  requestAnimationFrame((time) => animate(time, draw));
}
requestAnimationFrame((time) => animate(time, () => draw(ctx, animation)));
