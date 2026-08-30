export function play(fps: number, draw: () => void) {
  const frameDuration = 1_000 / fps;
  let lastFrameTime = 0;
  let requestId: number;

  function animate(time: number) {
    if (time - lastFrameTime >= frameDuration) {
      draw();
      lastFrameTime += frameDuration;
    }

    requestId = requestAnimationFrame((time) => animate(time));
  }
  requestId = requestAnimationFrame((time) => animate(time));
  return () => cancelAnimationFrame(requestId);
}
