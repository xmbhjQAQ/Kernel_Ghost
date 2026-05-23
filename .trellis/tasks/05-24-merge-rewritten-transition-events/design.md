# Design

## Approach

`index.html` already owns `intermissionPools`, collection metadata generation, random selection, and archive rendering. This task updates that data structure and ensures `submitFlag()` triggers the fifth pool after work order #005.

## Data Shape

Keep the existing event object shape:

```js
{ id, title, source, time, collectibleTitle, text }
```

Use stable IDs `event-<pool>-<index>`.

## Compatibility

Existing saved collection IDs for older event names may no longer map to current events. This is acceptable for this content rewrite. The restore path already filters unknown collectible IDs.

## Tests

Add source-level assertions that:

- pool 5 exists
- rewritten source markers are present
- `submitFlag()` triggers `withIntermissions(..., ["5"])` after `FLAG{LIN_COMMENT_PATCHED}`
