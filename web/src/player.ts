export function play(fps: number, draw: () => void) {
  const frameDuration = 1_000 / fps;
  let lastFrameTime: number | undefined;
  let requestId: number;

  function animate(time: number) {
    if (lastFrameTime === undefined) {
      lastFrameTime = time;
    }
    const elapsed = time - lastFrameTime;
    if (elapsed >= frameDuration) {
      draw();
      lastFrameTime = time - (elapsed % frameDuration);
    }
    requestId = requestAnimationFrame(animate);
  }

  requestId = requestAnimationFrame(animate);
  return () => cancelAnimationFrame(requestId);
}
