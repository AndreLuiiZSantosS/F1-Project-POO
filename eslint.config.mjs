import { createRequire } from "node:module";

const require = createRequire(new URL("./api/package.json", import.meta.url));
const nodePlugin = require("eslint-plugin-n");

export default [
  {
    languageOptions: {
      sourceType: "commonjs",
      globals: {
        Buffer: "readonly",
        require: "readonly",
      },
    },
    plugins: {
      n: nodePlugin,
    },
    settings: {
      node: {
        version: ">=20.19",
      },
    },
    rules: {
      "n/no-deprecated-api": "error",
    },
  },
];