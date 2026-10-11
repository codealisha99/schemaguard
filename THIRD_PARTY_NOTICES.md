# UI component credits

The following Aceternity UI components by Manu Arora / Aceternity were reviewed and adapted for SchemaGuard:

- [Stateful Button](https://ui.aceternity.com/components/stateful-button), [original registry source](https://ui.aceternity.com/registry/stateful-button.json): loading indicator and outcome feedback. SchemaGuard ties feedback to actual validation results, including distinct fallback/failure states, and supports reduced motion.
- [Tabs](https://ui.aceternity.com/components/tabs), [original registry source](https://ui.aceternity.com/registry/tabs.json): shared rounded active surface. SchemaGuard implements the transition with the Web Animations API and adds keyboard navigation and ARIA tab semantics. The original stacked content animation is omitted to keep editors stable.
- [Card Hover Effect](https://ui.aceternity.com/components/card-hover-effect), [original registry source](https://ui.aceternity.com/registry/card-hover-effect.json): shared background moves between explanation cards. Keyboard focus receives the same treatment; mobile uses static cards.
- [Grid and Dot Backgrounds](https://ui.aceternity.com/components/grid-and-dot-backgrounds): a CSS dot pattern with a radial mask, adapted to the light hero palette.

These are lightweight DOM/CSS adaptations, not installed React components. The stateful button and keyboard-accessible tabs live in `app/static/components.js`; their presentation uses the shared design tokens. The previously adapted card hover effect and dot background are no longer rendered. The references above retain their attribution history. React, Tailwind, and Motion are not dependencies; the static production build uses Node. Original component sources are referenced rather than redistributed as a component library. Aceternity retains ownership of its original work; see its [license terms](https://ui.aceternity.com/licence).

Manrope and JetBrains Mono are locally hosted fonts under the SIL Open Font License. Their notices are in `app/static/fonts/`.

## Hugeicons

Interface icons are a locally served subset of [Hugeicons](https://hugeicons.com/) Stroke Rounded from `@hugeicons/core-free-icons` **4.3.5**, licensed under MIT. The original vector paths are preserved in `app/static/hugeicons.js`; the copyright and license are included in `app/static/hugeicons-LICENSE.txt`. The DOM renderer avoids a framework, network dependency, or package build step. The SchemaGuard brand mark remains a custom identity asset.
