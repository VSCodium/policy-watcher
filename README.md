[@vscodium/policy-watcher](https://github.com/VSCodium/policy-watcher)
======================================================================

[![Version](https://img.shields.io/npm/v/@vscodium/policy-watcher.svg)](https://npmjs.org/package/@vscodium/policy-watcher)

## <a id="fork"></a>Why fork from microsoft/vscode-policy-watcher

`microsoft/vscode-policy-watcher` is limited to only to the `Microsoft` vendor.
`@vscodium/policy-watcher` removes that limit so it can be used by any vender.

## <a id="usage"></a>Usage

```js
const createWatcher = require("@vscodium/policy-watcher");

createWatcher(
  // vendor name
  "VSCodium",
  // product name
  "VSCodium",
  {
    UpdateMode: { type: "string" },
    SCMInputFontSize: { type: "number" },
  },
  (update) => console.log(update)
);
```

## <a id="license"></a>License

[MIT](https://github.com/VSCodium/policy-watcher/blob/master/LICENSE)