import "./style.css";
import { drawFrame } from "./renderer";
import { validateAnimation } from "./animation";
import { play } from "./player";

const DEFAULT_EXAMPLE = "basic";

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

let stop = () => {};
function setAnimation(ctx: CanvasRenderingContext2D, data: unknown) {
  const animation = validateAnimation(data);
  let currFrame = 0;
  stop();
  stop = play(animation.fps, () => {
    drawFrame(ctx, animation.frames[currFrame]);
    currFrame = (currFrame + 1) % animation.frames.length;
  });
}

const files = import.meta.glob("./examples/*", {
  eager: true,
});
const examples = Object.fromEntries(
  Object.entries(files).map(([path, module]) => {
    return [
      path.split("/").pop()!.replace(".json", ""),
      (module as { default: unknown }).default,
    ];
  }),
);
setAnimation(ctx, examples[DEFAULT_EXAMPLE]);

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

Object.entries(examples).forEach(([name, data]) => {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "file-button";
  button.textContent = name;
  button.addEventListener("click", () => {
    setAnimation(ctx, data);
  });
  examplesDiv.appendChild(button);
});
