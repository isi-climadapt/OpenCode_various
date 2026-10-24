# Author 2 Book 5: "Roar Wonders": Page-by-Page Generation Instructions (50 pages)

> House: Wattle Wonders Publishing / pen Flora Watt. Lane A. Bold & easy thick-line interiors,
> 10-14 elements per scene, art fills a bigger area (fit 2400x2700), fun fact on every page,
> captions in Fredoka. Engine: batch_generate_a2.py (copied from book4, rule 15). OpenArt CLI / nano-banana-2 for pages.
> Title: "Roar Wonders" (validation: publishing\11-validation-roar-wonders.md).
> Mix: a trip around the world by habitat. Africa 14 (savanna, wetlands, rainforest, Madagascar),
> South America 7, Asia 8, North America 10, deserts 5, rivers 2, polar 2, Australia 2.
> No sea animals (Author 1 Ocean Friends); only two polar animals (Author 1 Snowy Cuties).
> Every animal is a friendly character with a happy face. Nothing scary: no hunting scenes, no bared teeth.
> Scene elements are things found in that habitat. No color words in prompts.

## Universal prompt suffix (LOCKED: append to EVERY scene prompt)

```
Bold and easy coloring book page. A rich, detailed but simple scene with 10 to 14 easy elements arranged to fill the whole page around the main animal (things that belong in the animal's habitat, plus a few sparkles), all part of one connected scene, never a border of separate stickers or icons around the edge, each element drawn as one big simple closed shape. The composition fills almost the entire page. Whole scene floats with a plain white margin on every side; no element touches the image edges. Absolutely no rectangular frame or box line anywhere; do not draw a border. Very thick, clean, smooth black outlines (heavy, marker-friendly), pure black on plain white only. Only simple closed shapes with large open areas to color. The main animal stays the largest thing on the page, portrait composition. Cute, friendly, happy faces with large simple eyes. No shading, no grey, no color fill, no texture, no crosshatching, no fur strokes. No words, letters, numbers, logos or symbols anywhere in the image. Nothing in the bottom 6 percent of the page.
```

Regeneration wording for edge or frame flags (F2/F3), added in front of the suffix on rerolls only:

```
The whole scene is one floating vignette in the middle of the page, like an island, with a wide plain white margin on all four sides; the ground ends in a soft rounded edge well inside the page and nothing reaches the edges.
```

## Failure modes: F1-F13 per AGENT-PIPELINE.md; F9 coherence audit runs after every typeset.

## The 50 pages

| File | Page | Scene prompt (prepend nothing, append suffix) |
|---|---|---|
| page_01 | Lion | A cute lion with a big fluffy mane and a happy face roaring a friendly roar while sitting proudly on a large flat rock on the African savanna, surrounded by tall grass tufts, an acacia tree, a lion cub playing beside him, a few rounded bushes, a smiling sun and clouds. |
| page_02 | Elephant | A cute elephant with a happy face flapping its big ears and spraying a fountain of water from its trunk at a watering hole, a baby elephant splashing beside it, surrounded by splashes, reeds, an acacia tree, a small bird on its back, rocks and a smiling sun. |
| page_03 | Giraffe | A very tall cute giraffe with a happy face and patchy spots stretching its long neck to nibble leaves at the top of an acacia tree, surrounded by grass tufts, a small bird on its horns, a baby giraffe, bushes, clouds and a smiling sun. |
| page_04 | Zebra | A cute zebra with bold stripes and a happy face trotting across the grassy savanna next to a smaller zebra foal, surrounded by grass tufts, an acacia tree, a termite mound, a few rounded bushes, butterflies, clouds and a smiling sun. |
| page_05 | Hippo | A cute round hippo with a happy face peeking out of a river with only its big head and back above the water, a small bird sitting on its nose, surrounded by ripples, bubbles, water lilies, reeds, a riverbank with rocks and a smiling sun. |
| page_06 | Cheetah | A cute spotted cheetah with a happy face and a long tail running fast across the savanna in a big stretched leap, speed lines behind it, surrounded by grass tufts, an acacia tree, small rocks, a termite mound, clouds and a smiling sun. |
| page_07 | Rhino | A cute chunky rhino with two rounded horns on its nose and a happy face standing in a cool mud puddle, a small bird riding on its back, surrounded by mud splashes, grass tufts, a rounded bush, an acacia tree, clouds and a smiling sun. |
| page_08 | Meerkat | A cute meerkat with a happy face standing tall on its back legs on top of a sandy mound, keeping watch, three smaller meerkats peeking out of burrow holes below, surrounded by grass tufts, rocks, a small cactus-like bush, clouds and a smiling sun. |
| page_09 | Ostrich | A cute tall ostrich with a long neck, big fluffy feathers and a happy face standing proudly beside a nest with three giant round eggs, surrounded by grass tufts, an acacia tree, rocks, a few rounded bushes, clouds and a smiling sun. |
| page_10 | Warthog | A cute round warthog with small curved tusks, a tufty mane and a happy face kneeling on its front knees to nibble short grass, surrounded by grass tufts, a burrow hole, a termite mound, an acacia tree, flowers, clouds and a smiling sun. |
| page_11 | Flamingo | A cute flamingo with a happy face standing on one long leg in a shallow lake, its neck in a graceful curve, two more flamingos in the background, surrounded by ripples, reeds, small rocks, water lilies, clouds and a smiling sun. |
| page_12 | Gorilla | A cute gentle gorilla with a happy face sitting in a cozy round nest of big leaves on the rainforest floor, a baby gorilla snuggled beside it, surrounded by large jungle leaves, a thick tree trunk, hanging vines, ferns, flowers and a butterfly. |
| page_13 | Lemur | A cute ring-tailed lemur with a happy face and a very long striped tail held high like a question mark, walking along a tree branch with two smaller lemurs following, surrounded by big leaves, a baobab tree, flowers, a butterfly and a smiling sun. |
| page_14 | Chameleon | A cute chameleon with a curly tail, a happy face and big round eyes sitting on a twisty branch, shooting out its long tongue toward a buzzing bug, surrounded by big leaves, flowers, hanging vines, a butterfly and dewdrops. |
| page_15 | Sloth | A cute sloth with a happy sleepy face and long curved claws hanging upside down from a rainforest branch, a baby sloth hugging its tummy, surrounded by big leaves, hanging vines, flowers, a butterfly and a smiling sun peeking through the leaves. |
| page_16 | Toucan | A cute toucan with a giant curved beak and a happy face perched on a rainforest branch, holding a round berry in its beak, surrounded by big leaves, tropical flowers, hanging vines, berries, a butterfly and a smiling sun. |
| page_17 | Jaguar | A cute spotted jaguar with a happy face swimming across a calm jungle river with its head above the water, surrounded by ripples, splashes, water lilies, big leaves, a riverbank with roots, hanging vines and a butterfly. |
| page_18 | Tree frog | A cute tree frog with huge round eyes, a happy face and round sticky toe pads clinging to a big rainforest leaf, surrounded by more big leaves, raindrops, a flower, a dragonfly, hanging vines and a smaller frog on another leaf. |
| page_19 | Macaw | A cute macaw parrot with a long tail, a happy face and a strong curved beak climbing along a branch using its beak and feet, a second macaw beside it, surrounded by big leaves, tropical flowers, nuts, hanging vines and a smiling sun. |
| page_20 | Capybara | A cute round capybara with a happy face sitting calmly at the edge of a river, a small bird sitting on its head, two baby capybaras beside it, surrounded by ripples, reeds, water lilies, grass tufts, rocks and a smiling sun. |
| page_21 | Llama | A cute fluffy llama with a happy face, long neck and tall ears standing on a grassy mountain meadow beside another llama, little music notes floating between them as they hum, surrounded by rounded mountains, grass tufts, flowers, rocks, clouds and a smiling sun. |
| page_22 | Giant panda | A cute round giant panda with a happy face and big eye patches sitting on the ground munching a stalk of bamboo, a pile of bamboo stalks beside it, surrounded by tall bamboo plants, leaves, rocks, a baby panda, clouds and a smiling sun. |
| page_23 | Red panda | A cute red panda with a happy face, pointy ears and a big fluffy ringed tail resting on a high tree branch, surrounded by leaves, pine cones, a bird's nest, flowers, rounded mountains in the distance, clouds and a smiling sun. |
| page_24 | Tiger | A cute striped tiger with a happy face lying on a big rock beside a jungle stream, its long tail curled, surrounded by ripples, tall grass, big leaves, bamboo, flowers, a butterfly and a smiling sun. |
| page_25 | Orangutan | A cute shaggy orangutan with a happy face holding a giant leaf over its head like an umbrella in the rain, sitting on a tree branch, a baby orangutan under the leaf too, surrounded by raindrops, big leaves, hanging vines, flowers and clouds. |
| page_26 | Snow leopard | A cute spotted snow leopard with a happy face and a long fluffy tail sitting on a rocky mountain ledge, surrounded by rounded mountain peaks, snowflakes, rocks, a small pine tree, clouds and a smiling sun. |
| page_27 | Yak | A cute shaggy yak with a happy face, curved horns and long hanging fur standing on a high mountain path, surrounded by rounded mountain peaks, plain rocks, grass tufts, flowers, a small stream, clouds and a smiling sun. |
| page_28 | Komodo dragon | A cute friendly komodo dragon lizard with a happy face and a long tail walking on a sandy island beach, surrounded by palm trees, rocks, a small hill, grass tufts, shells, clouds and a smiling sun. |
| page_29 | Peacock | A cute peacock with a happy face and a huge open fan of tail feathers with big round eye-spot shapes, standing in a garden, a peahen without a fan beside it, surrounded by flowers, grass tufts, a rounded bush, a stone path, clouds and a smiling sun. |
| page_30 | Grizzly bear | A cute big grizzly bear with a happy face standing in a rushing river at the bottom of a small waterfall, a smiling salmon fish leaping up the waterfall beside it, surrounded by splashes, rocks, pine trees, rounded mountains, clouds and a smiling sun. |
| page_31 | Moose | A cute moose with a happy face and big wide antlers standing in a calm forest lake, water plants dangling from its mouth, surrounded by ripples, water lilies, pine trees, rounded mountains, reeds, clouds and a smiling sun. |
| page_32 | Beaver | A cute beaver with a happy face, two big front teeth and a flat paddle tail carrying a stick toward its dam of sticks and mud in a stream, surrounded by ripples, logs, a tree stump with tooth marks, pine trees, reeds and a smiling sun. |
| page_33 | Wolf | A cute friendly wolf with a happy face and a bushy tail sitting on a hill in the forest, its pack of wolves nearby with three playful pups tumbling beside it, surrounded by pine trees, rocks, grass tufts, flowers, a big round moon and stars. |
| page_34 | Bald eagle | A cute bald eagle with a happy face, a hooked beak and wide spread wings landing on a giant nest of sticks at the top of a tall pine tree, two fluffy chicks in the nest, surrounded by pine branches, rounded mountains, a river below, clouds and a smiling sun. |
| page_35 | Raccoon | A cute raccoon with a happy face, a mask around its eyes and a ringed tail using its little front paws to wash an apple at the edge of a creek, surrounded by ripples, rocks, ferns, a hollow log, mushrooms, trees and a moon. |
| page_36 | Owl | A cute round owl with a happy face, big round eyes and ear tufts flying silently with soft wide wings past a big tree, surrounded by a tree hollow, leaves, a branch, a crescent moon, stars, clouds and pine trees. |
| page_37 | Bison | A cute big shaggy bison with a happy face, a big hump and small curved horns running across a wide grassy prairie, speed lines behind it, surrounded by grass tufts, wildflowers, rolling hills, a few rocks, clouds and a smiling sun. |
| page_38 | Hummingbird | A cute tiny hummingbird with a happy face, a long thin beak and fast blurry wing lines hovering beside a big trumpet-shaped flower, a second hummingbird flying backwards, surrounded by more flowers, leaves, a vine, a butterfly and a smiling sun. |
| page_39 | Prairie dog | Two cute prairie dogs with happy faces standing up on their back legs outside their burrow and touching noses in a friendly kiss, surrounded by burrow holes, mounds of dirt, grass tufts, wildflowers, a small baby prairie dog, clouds and a smiling sun. |
| page_40 | Camel | A cute camel with one big round hump, long eyelashes and a happy face walking across rolling sand dunes, surrounded by a palm tree oasis with a small pool, rocks, a cactus, footprints in the sand, clouds and a smiling sun. |
| page_41 | Fennec fox | A cute small fennec fox with gigantic ears and a happy face sitting on a sand dune at the entrance of its burrow, surrounded by rolling dunes, rocks, a desert plant, footprints, a crescent moon and stars. |
| page_42 | Armadillo | A cute armadillo with a happy face and a banded shell, and beside it a second armadillo rolled up into a tight round ball, in the desert, surrounded by cactus plants, rocks, a burrow hole, desert flowers, clouds and a smiling sun. |
| page_43 | Desert tortoise | A cute desert tortoise with a happy face and a domed patterned shell walking toward the entrance of its burrow under a rock, surrounded by cactus plants, desert flowers, rocks, sand, clouds and a smiling sun. |
| page_44 | Roadrunner | A cute roadrunner bird with a happy face, a crest on its head and a long tail running fast across the desert, speed lines and puffs of dust behind it, surrounded by cactus plants, rocks, a mesa, desert flowers, clouds and a smiling sun. |
| page_45 | Alligator | A cute friendly alligator with a happy closed-mouth smile and a long bumpy tail floating in a calm swamp with its eyes and back above the water, surrounded by ripples, lily pads, a frog, cattails, a mossy tree, a dragonfly and a smiling sun. |
| page_46 | River otter | A cute river otter with a happy face and a long tail sliding down a muddy riverbank into the water with a big splash, a second otter waiting its turn at the top, surrounded by splashes, rocks, reeds, a log, pine trees and a smiling sun. |
| page_47 | Polar bear | A cute fluffy polar bear with a happy face walking across a sheet of ice, one big round paw lifted to show its padded sole, surrounded by ice blocks, snowy hills, snowflakes, a small icy pond, clouds and a smiling sun. |
| page_48 | Emperor penguin | A cute round emperor penguin with a happy face, a short beak and a plump body with two small flippers, swimming headfirst downward through the water, a short trail of bubbles above it, a small fish smiling nearby, surrounded by a flat ice shelf at the top, more bubbles, a smaller penguin swimming, seaweed, rocks below and sparkles. |
| page_49 | Kangaroo | A cute kangaroo mom with a happy face standing on her strong back legs with a tiny baby joey peeking out of her pouch, surrounded by gum trees, grass tufts, rocks, bushes, wildflowers, clouds and a smiling sun. |
| page_50 | Koala | A cute fluffy koala with a happy face, round ears and a big nose hugging a gum tree trunk and holding a leaf in its paw, showing its little fingers, a baby koala on its back, surrounded by gum leaves, branches, flowers, clouds and a smiling sun. |
