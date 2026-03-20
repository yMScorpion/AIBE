Runtime TypeError


Failed to fetch

src\lib\api.ts (15:21) @ fetcher


  13 |
  14 | async function fetcher<T>(path: string, init?: RequestInit): Promise<T> {
> 15 |   const res = await fetch(`${BASE}${path}`, {
     |                     ^
  16 |     ...init,
  17 |     headers: { "Content-Type": "application/json", ...init?.headers },
  18 |   });
Call Stack
50

Hide 46 ignore-listed frame(s)
fetcher
src\lib\api.ts (15:21)
Object.summary
src\lib\api.ts (61:20)
Page.useCallback[fetchCosts]
src\app\page.tsx (64:36)
Page.useEffect
src\app\page.tsx (76:10)
Object.react_stack_bottom_frame
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (23668:1)
runWithFiberInDEV
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (871:1)
commitHookEffectListMount
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (12344:1)
commitHookPassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (12465:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14386:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14379:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14379:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14513:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14513:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14379:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14389:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14379:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14389:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14379:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14379:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14379:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14389:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14379:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14379:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14513:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14513:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14379:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14379:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14389:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)
commitPassiveMountOnFiber
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14513:1)
recursivelyTraversePassiveMountEffects
node_modules\next\dist\compiled\react-dom\cjs\react-dom-client.development.js (14359:1)