import "./style.css";
import { drawFrame } from "./renderer";
import basic from "./examples/basic.json";
import { validateAnimation } from "./animation";
import { play } from "./player";

const canvas = document.querySelector<HTMLCanvasElement>("#display");
const errDisplay = document.querySelector<HTMLElement>("#error");
const examplesDiv = document.querySelector<HTMLDivElement>("#examples");

if (!canvas || !errDisplay || !examplesDiv) {
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
function setAnimation(ctx: CanvasRenderingContext2D, data: unknown) {
  const animation = validateAnimation(data);
  let currFrame = 0;

  stop();

  stop = play(animation.fps, () => {
    drawFrame(ctx, animation.frames[currFrame]);
    currFrame = (currFrame + 1) % animation.frames.length;
  });
}

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
    errDisplay.textContent = "";
    stop();
    setAnimation(ctx, data);
  } catch (error) {
    errDisplay.textContent =
      error instanceof Error ? error.message : "invalid animation";
  }
});

const files = import.meta.glob("./examples/*", {
  eager: true,
});
const examples = Object.entries(files).map(([path, module]) => ({
  name: path.split("/").pop()!.replace(".json", ""),
  data: (module as { default: unknown }).default,
}));

examples.forEach(({ name, data }) => {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "file-button";
  button.textContent = name;
  button.addEventListener("click", () => {
    setAnimation(ctx, data);
  });
  examplesDiv.appendChild(button);
});
