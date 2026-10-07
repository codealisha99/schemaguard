# UI component credits

The following Aceternity UI components by Manu Arora / Aceternity were reviewed and adapted for SchemaGuard:

- [Stateful Button](https://ui.aceternity.com/components/stateful-button), [original registry source](https://ui.aceternity.com/registry/stateful-button.json): loading indicator and outcome feedback. SchemaGuard ties feedback to actual validation results, including distinct fallback/failure states, and supports reduced motion.
- [Tabs](https://ui.aceternity.com/components/tabs), [original registry source](https://ui.aceternity.com/registry/tabs.json): shared rounded active surface. SchemaGuard implements the transition with the Web Animations API and adds keyboard navigation and ARIA tab semantics. The original stacked content animation is omitted to keep editors stable.
- [Card Hover Effect](https://ui.aceternity.com/components/card-hover-effect), [original registry source](https://ui.aceternity.com/registry/card-hover-effect.json): shared background moves between explanation cards. Keyboard focus receives the same treatment; mobile uses static cards.
- [Grid and Dot Backgrounds](https://ui.aceternity.com/components/grid-and-dot-backgrounds): a CSS dot pattern with a radial mask, adapted to the light hero palette.

These are lightweight DOM/CSS adaptations, not installed React components. They live in `app/static/components.js` and the Aceternity section of `app/static/style.css`. React, Tailwind, Motion, and a Node build step are not required. Original component sources are referenced rather than redistributed as a component library. Aceternity retains ownership of its original work; see its [license terms](https://ui.aceternity.com/licence).

Manrope and JetBrains Mono are locally hosted fonts under the SIL Open Font License. Their notices are in `app/static/fonts/`.
