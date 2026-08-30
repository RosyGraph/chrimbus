import type { AnimationSchema } from "./generated/animation";
import geometry from "./geometry.json";

const MAX_X = 800;
const MAX_Y = 586;

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

export function drawFrame(
  ctx: CanvasRenderingContext2D,
  frame: AnimationSchema["frames"][number],
) {
  Object.values(geometry).forEach(([x, y], i) => {
    const pixel = frame[i];
    fillCirc(ctx, x * MAX_X, y * MAX_Y, pixel);
  });
}
