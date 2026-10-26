import { createRequire } from "node:module";

const require = createRequire(new URL("./api/package.json", import.meta.url));
const js = require("@eslint/js");
const stylistic = require("@stylistic/eslint-plugin");
const globals = require("globals");
const nodePlugin = require("eslint-plugin-n");

export default [
  js.configs.recommended,
  {
    languageOptions: {
      sourceType: "commonjs",
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    plugins: {
      n: nodePlugin,
      "@stylistic": stylistic,
    },
    settings: {
      node: {
        version: ">=20.19",
      },
    },
    rules: {
      "n/no-deprecated-api": "error",
      "@stylistic/arrow-spacing": "error",
      "@stylistic/comma-dangle": ["error", "always-multiline"],
      "@stylistic/comma-spacing": "error",
      "@stylistic/eol-last": "error",
      "@stylistic/indent": ["error", 2],
      "@stylistic/key-spacing": "error",
      "@stylistic/keyword-spacing": "error",
      "@stylistic/no-trailing-spaces": "error",
      "@stylistic/object-curly-spacing": ["error", "always"],
      "@stylistic/quotes": ["error", "double", { avoidEscape: true }],
      "@stylistic/semi": ["error", "always"],
      "@stylistic/space-before-function-paren": [
        "error",
        { anonymous: "always", named: "always", asyncArrow: "always" },
      ],
      "@stylistic/space-infix-ops": "error",
    },
  },
];