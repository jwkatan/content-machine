# Swimm Design Philosophy



## Anti-Patterns

- **Center-everything layouts** — Default to left-aligned text with purposeful grid placement. Centering every heading and paragraph creates a weak vertical axis and looks like a template.
- **Gradients everywhere** — One hero gradient per composition. Multiple gradient backgrounds compete and flatten the visual hierarchy.
- **Pure grays** — All neutrals must be blue-tinted (the Gray palette runs #415892 to #FDFCFE). Pure #808080 or #CCCCCC grays break the brand's cohesive warmth.
- **Stock-feeling layouts** — No handshake imagery, sticky-note boards, or people-pointing-at-screens compositions. If it could be a Shutterstock search result, reject it.
- **Photorealistic imagery or human figures** — The brand is abstract and geometric. No photos, no faces, no silhouettes.
- **Gaussian blur or bokeh effects** — Depth comes from layering and opacity, not from soft focus.
- **Box-shadows** — The system achieves all depth through SVG radial gradients, blend modes (`mix-blend-mode: lighten` for dark surface glow, `multiply` for screenshot fades, `screen` for warm transition glow), and opacity layering. Adding `box-shadow` to elements breaks the design language.
- **Cartoonish or playful illustration** — Maintain enterprise tone. No mascots, no rounded-corner pastel friendliness, no startup whimsy.
- **Heavy gradients that dominate** — Gradients support the composition; they do not become it. If the gradient is the first thing the eye notices, dial it back.
- **Skeuomorphic elements** — No faux-3D buttons, drop shadows mimicking physical objects, or textured surfaces pretending to be paper or metal.
- **Repeating wallpaper patterns** — Dot-matrix patterns are organic and vary in density. Tiled or repeating textures look mechanical and cheap.
- **Flat card backgrounds on light surfaces** — Every card on a light surface gets the Light-100 radial gradient (`--gradient-light-100`) as its background. A solid Gray-100 card is a wireframe, not a finished design. The asymmetric radial bloom (origin at ~33% from left, 0% from top) creates the illusion of a light source and distinguishes the surface from the page background.
- **Symmetric gradient origins** — Radial gradient origins must be asymmetric. The standard is approximately 33% from the left edge, 0% from top. Centered gradients (50% 50%) look AI-generated because they lack the directional intention of hand-crafted design.
- **Same layout three times in a row** — Consecutive identical compositions (three card grids in sequence, or three heading-paragraph-visual sections) are the hallmark of LLM-generated design. Every adjacent section must use a visually distinct layout pattern.
- **Predictable card counts** — Do not default to 3 cards. Consider 2, 4, or 6 layouts.
