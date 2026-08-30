import "./style.css";
import { drawFrame } from "./renderer";
import basic from "./basic.json";
import { validateAnimation } from "./animation";
import { play } from "./player";

const canvas = document.querySelector<HTMLCanvasElement>("#display");
const errDisplay = document.querySelector<HTMLElement>("#error");

if (!canvas || !errDisplay) {
  throw new Error("Unexpected error: missing html elements");
}

const ctx = canvas.getContext("2d");
if (!ctx) {
  throw new Error("2D canvas context unavailable");
}
const animation = validateAnimation(basic);
let currFrame = 0;
let stop = play(animation.fps, () => {
  drawFrame(ctx, animation.frames[currFrame]);
  currFrame = (currFrame + 1) % animation.frames.length;
});

const upload = document.querySelector<HTMLInputElement>("#animation-upload");
if (!upload) {
  throw new Error("Animation upload not found");
}
upload.addEventListener("change", async () => {
  const file = upload.files?.[0];
  if (!file) {
    return;
  }
  try {
    const text = await file.text();
    const data: unknown = JSON.parse(text);
    const uploadedAnimation = validateAnimation(data);
    errDisplay.textContent = "";
    stop();
    stop = play(uploadedAnimation.fps, () => {
      drawFrame(ctx, uploadedAnimation.frames[currFrame]);
      currFrame = (currFrame + 1) % uploadedAnimation.frames.length;
    });
  } catch (error) {
    errDisplay.textContent =
      error instanceof Error ? error.message : "invalid animation";
  }
});
