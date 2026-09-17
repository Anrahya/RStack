# Small TypeScript patterns

Use these only when they express a current invariant. These examples are
illustrative, not claims about symbols found in the user's repository.

## State variants

```ts
type Result<T> =
  | { kind: "ok"; value: T }
  | { kind: "error"; message: string };

function describe(result: Result<string>): string {
  switch (result.kind) {
    case "ok": return result.value;
    case "error": return result.message;
    default: {
      const unexpected: never = result;
      return unexpected;
    }
  }
}
```

This disallows an "ok" result without a value. It does not by itself validate JSON.

## Runtime boundary

```ts
function readName(value: unknown): string {
  if (typeof value !== "string" || value.trim().length === 0) {
    throw new TypeError("A non-empty name is required");
  }
  return value.trim();
}
```

For complex objects, use the project's existing parser/schema library. A return
annotation does not make an unchecked `JSON.parse` value safe.

## Literal values and compatibility

```ts
type Method = "GET" | "POST";
const route = { method: "GET", path: "/status" } as const satisfies {
  method: Method;
  path: string;
};
```

Use `as const` deliberately for literals and readonly fields. Use `satisfies` for
a compatibility check. Neither substitutes for a runtime check of external input.

## Stronger collections only when needed

```ts
type NonEmpty<T> = readonly [T, ...T[]];
function first<T>(items: NonEmpty<T>): T { return items[0]; }
```

A normal array is still the correct type for an operation that supports emptiness.
Do not convert external arrays by assertion; validate length at the actual boundary.
