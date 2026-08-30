import Ajv from "ajv";
import schema from "./animation.schema.json";
import type { AnimationSchema } from "./generated/animation";

export function validateAnimation(animationJSON: unknown) {
  const ajv = new Ajv();
  const validateAnimation = ajv.compile<AnimationSchema>(schema);
  if (!validateAnimation(animationJSON)) {
    throw new Error("Invalid animation");
  }
  return animationJSON;
}
