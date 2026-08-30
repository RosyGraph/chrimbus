import Ajv from "ajv";
import schema from "./animation.schema.json";
import type { AnimationSchema } from "./generated/animation";

export function validateAnimation(animationJSON: unknown) {
  const ajv = new Ajv();
  const validateAnimation = ajv.compile<AnimationSchema>(schema);
  if (!validateAnimation(animationJSON)) {
    const errMsg = validateAnimation.errors
      ?.map((err) => err.message)
      .join("\n");
    throw new Error(errMsg ?? "Invalid animation");
  }
  return animationJSON;
}
