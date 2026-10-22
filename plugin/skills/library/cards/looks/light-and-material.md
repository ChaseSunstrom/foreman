---
name: light-and-material
title: "Light and material recipes"
area: looks
tags: [3d, lighting, pbr, material, three-point, rim, studio, overcast]
detect: []
related: [shader-soft-caustics, shader-performance, look-observatory, look-ceramic-studio]
---
Four light rigs and nine PBR material presets for a web 3D scene, inside the rules of `ui/scene-3d.md`: pick one rig, then presets.

## Pipeline
Fix it before the first light (`ui/scene-3d.md`, Light and material): colour textures and token colours are sRGB and converted to linear once; data textures (normal, roughness, metalness, AO) stay linear; one tone mapper for the whole project, Neutral when brand colours must survive, AgX or ACES for filmic contrast; output is sRGB, converted once. Exposure is tuned against that tone mapper and then left alone.

## Rigs
Intensities are relative to the key (1.0); Rim has no key, so its second rim is relative to the first, and Overcast's key is relative to its hemisphere light. Light tints are a warm key near `#FFF1E0` and a cool fill or rim near `#DCE8FF`, never saturated.

| Rig | Environment | Direct lights | Shadow | Reads as |
|---|---|---|---|---|
| Three-point | dim neutral hemisphere at 0.2-0.3 | 3 direct: key 45 degrees up and to one side, fill at eye level opposite at 0.25-0.5 (a 2:1-4:1 ratio), rim behind and above at 0.6-1.0 | key only | portrait of a product, a character, a hero object |
| Rim | near-black, matched to the page | 2 direct: rims behind left and right, 30 degrees up, the second at 0.6-1.0 of the first; nothing from the front | none | silhouette and drama; night themes, launches |
| Studio | soft studio HDR at 0.6-1.0, background hidden | 2 direct: key 45 degrees up and to the side, optional rim from behind at 0.5 | key only | commerce, a product page's turntable |
| Overcast | hemisphere light: sky cool white, ground a darker tint of the floor | 1 direct: a soft key from straight above at 0.3-0.5 of the hemisphere light, large shadow radius | key only | calm and even; architecture, soft clay, diagrams |

## Materials
Metalness is 0 or 1; roughness is never 0; albedo stays inside sRGB 30-240. A metal's albedo is its reflectance colour, and it needs the environment to look like metal.

| Preset | Albedo | Metal | Rough | Note |
|---|---|---|---|---|
| Matte plastic | #D8D4CC | 0 | 0.6 | most product shells |
| Soft clay | #C9876A | 0 | 0.85 | the template's pebble; pastel hues |
| Glazed ceramic | #EDEAE2 | 0 | 0.25 | add a clearcoat at 1.0, roughness 0.05 |
| Rubber | #3A3B3D | 0 | 0.9 | grips, cables, tyres |
| Felt | #8E8A82 | 0 | 1.0 | add sheen 0.5, tinted like the albedo |
| Frosted glass | #E8ECEC | 0 | 0.35 | transmission 1.0, thickness set; costly |
| Brushed aluminium | #C8CACC | 1 | 0.35 | anisotropy 0.6 along the brush |
| Polished steel | #C4C7C7 | 1 | 0.12 | needs a detailed environment map |
| Gold | #F0D08C | 1 | 0.2 | clamped to 240: true gold reflectance is brighter |

## Suits
Any three.js, Babylon or raw WebGL scene: product turntables, hero objects, configurators, 3D illustrations.
Not for: flat illustration (use the diagram recipe in `ui/scene-3d.md`: unlit or toon), 2D shader backdrops.

## Verify
- `grep -rn "toneMapping\s*=" src`: set in one place.
- Greyscale screenshot (squint test): the subject's outline still separates from the backdrop.

## Test first
Before lighting, assert the presets: every material's metalness is 0 or 1, roughness above 0, albedo channels 30-240; and that the scene has at most three direct lights and one with `castShadow`.

## Do
- Light in this order: environment, then key, then fill or rim; check the squint test after each.

## Avoid
- Mixing rigs (a rim rig plus a studio HDR): pick one and tune it.

## Review
- [ ] At most three direct lights and one shadow caster.
- [ ] One tone mapper, set once; colours that match CSS go through the same conversion.
- [ ] No material at roughness 0 or with in-between metalness outside a masked transition.
