export function play(fps: number, draw: () => void) {
  const frameDuration = 1_000 / fps;
  let lastFrameTime = 0;

  function animate(time: number) {
    if (time - lastFrameTime >= frameDuration) {
      draw();
      lastFrameTime += frameDuration;
    }

    requestAnimationFrame((time) => animate(time));
  }
  requestAnimationFrame((time) => animate(time));
}
