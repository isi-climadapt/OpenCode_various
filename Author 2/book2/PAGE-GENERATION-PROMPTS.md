# Author 2 Book 2 — "Minibeast Wonders" — Page-by-Page Generation Instructions (50 pages)

> House: Wattle Wonders Publishing / pen Flora Watt. Lane A. Bold & easy thick-line interiors,
> 10-14 elements per scene, art fills a bigger area (fit 2400x2700), fun fact on every page,
> captions in Fredoka. Engine: batch_generate_a2.py. OpenArt CLI / nano-banana-2 for pages.
> Title locked: "Minibeast Wonders" (validation: publishing\05-validation-minibeasts.md).
> Mix: 35 backyard favourites + 15 Australian minibeasts.

## Universal prompt suffix (LOCKED — append to EVERY scene prompt)

```
Bold and easy coloring book page. A rich, detailed but simple scene with 10 to 14 easy elements arranged to fill the whole page around the main character (leaves, flowers, grass blades, mushrooms, pebbles, twigs, dew drops, a smiling sun, clouds, puddles and tiny bug friends), each element drawn as one big simple closed shape. The composition fills almost the entire page. Whole scene floats with a plain white margin on every side; no element touches the image edges. Absolutely no rectangular frame or box line anywhere; do not draw a border. Very thick, clean, smooth black outlines (heavy, marker-friendly), pure black on plain white only. Only simple closed shapes with large open areas to colour. The main character stays the largest thing on the page, portrait composition. Cute, friendly, happy faces with large simple eyes. No shading, no grey, no colour fill, no texture, no crosshatching. No words, letters, numbers or text anywhere in the image. Nothing in the bottom 6 percent of the page.
```

## Failure modes — F1-F11 per AGENT-PIPELINE.md; F9 coherence audit runs after every typeset.

## The 50 pages

| File | Page | Scene prompt (prepend nothing, append suffix) |
|---|---|---|
| page_01 | Ladybird lunch | A cute round ladybird with big spots and a happy face sitting on a big leaf, munching tiny round aphids, surrounded by a rose flower, three more leaves, two aphid friends, a dew drop, a smiling sun, a cloud and grass blades. |
| page_02 | Ladybird spots | A cute ladybird showing off its big round spots with a proud smile, a cartoon bird looking surprised nearby, surrounded by two daisies, three leaves, a pebble, a cloud, a smiling sun and grass blades. |
| page_03 | Honeybee flowers | A cute fuzzy honeybee with striped body and round wings flying between big flowers with a happy face, surrounded by four flowers, two leaves, a small beehive in the distance, a smiling sun, clouds and dew drops. |
| page_04 | Honeybee dance | A cute honeybee doing a happy wiggle dance on a honeycomb, two bee friends watching and clapping, surrounded by hexagon honeycomb cells, a flower, three dots of pollen, a smiling sun and a cloud. |
| page_05 | Queen bee | A cute queen bee wearing a tiny crown sitting proudly on honeycomb with three worker bee friends around her, surrounded by hexagon cells, two round eggs, a flower, a honey drop and a smiling sun. |
| page_06 | Butterfly feet | A cute butterfly with big round patterned wings standing on a flower and tasting it with its feet, happy face, surrounded by three flowers, two leaves, a caterpillar friend, a smiling sun, clouds and grass blades. |
| page_07 | Caterpillar grows | A cute chubby caterpillar with round body segments and a big smile next to a small old skin it just wriggled out of, surrounded by three big leaves with bite holes, a flower, a twig, dew drops and a smiling sun. |
| page_08 | Chrysalis | A cute chrysalis hanging from a twig with a sleepy happy face, a butterfly peeking out from the top, surrounded by four leaves, a flower, a ladybird friend, a smiling sun, a cloud and dew drops. |
| page_09 | Ulysses butterfly | A cute Ulysses butterfly with big rounded wings and wide wing bands flying over tropical leaves with a happy face, surrounded by a palm frond, two big flowers, a fern, a smiling sun, clouds and a little waterfall. |
| page_10 | Gum moth caterpillar | A cute emperor gum moth caterpillar with round bumps along its back munching a single big gum leaf with a big smile, sitting on a short small twig that ends well inside the page, surrounded by four loose gum leaves, three gum nuts, a small koala face peeking from a little round bush, a smiling sun and two clouds, square composition with white space all around. |
| page_11 | Strong ant | A cute ant carrying a big leaf high above its head with a proud smile, surrounded by two ant friends carrying crumbs, pebbles, a big strawberry, grass blades, a mushroom, a smiling sun and a cloud. |
| page_12 | Ant nest | A cute ant waving at the entrance of an underground nest shown as round connected rooms, with ant friends resting in the rooms, surrounded by grass on top, a flower, pebbles, round food crumbs, a smiling sun and a cloud. |
| page_13 | Bull ant | A cute bull ant with big round eyes and big friendly jaws standing on a log with a happy face, surrounded by gum leaves, pebbles, a small termite friend, grass tufts, a smiling sun, a cloud and a small bush. |
| page_14 | Dragonfly | A cute dragonfly with four long round-tipped wings hovering over a pond with a happy face, surrounded by lily pads, a lotus flower, reeds, a frog friend, ripples, a smiling sun and a cloud. |
| page_15 | Firefly | A cute firefly with a big round glowing tail and a happy face flying at night, surrounded by a crescent moon, five stars, two firefly friends, tall grass, a mushroom and a little tree. |
| page_16 | Glow-worms | Cute glow-worms hanging from a cave roof on long dangling threads, each with a tiny glowing dot and a happy face, surrounded by rounded cave rocks, a little stream, ferns, a smiling bat friend and stars of light dots. |
| page_17 | Christmas beetle | A cute round Christmas beetle with a shiny shell and a happy face sitting on a gum leaf beside a small Christmas bauble, surrounded by gum leaves, gum nuts, a smiling sun, a cloud, a flower and grass blades. |
| page_18 | Rainbow stag beetle | A cute rainbow stag beetle with big curved jaws and a shiny round shell standing proudly on a mossy log, surrounded by ferns, a mushroom, leaves, pebbles, a smiling sun and a cloud. |
| page_19 | Dung beetle | A cute dung beetle pushing a big round ball bigger than itself up a little hill with a determined happy face, surrounded by grass tufts, pebbles, a flower, a smiling sun, clouds and a cow far away. |
| page_20 | Jewel beetle | A cute jewel beetle with a shiny oval shell and a sparkly happy face sitting on a flower, with little sparkle star shapes around its shell, surrounded by leaves, two flowers, a smiling sun, a cloud and dew drops. |
| page_21 | Weevil | A cute weevil with a long curved snout and a big smile sitting on an acorn, surrounded by oak leaves, two acorns, pebbles, a mushroom, a smiling sun, a cloud and grass blades. |
| page_22 | Grasshopper | A cute grasshopper with long bent back legs jumping happily over a flower, surrounded by tall grass blades, two flowers, a ladybird friend, pebbles, a smiling sun and clouds. |
| page_23 | Cricket song | A cute cricket with long antennae playing a happy song by rubbing its wings, with simple music notes floating up, surrounded by grass, a crescent moon, stars, a mushroom and a log. |
| page_24 | Katydid | A cute katydid with wings shaped exactly like green leaves hiding among real leaves with a cheeky smile, a puzzled bird searching nearby, surrounded by big leaves, a flower, a twig, a smiling sun and a cloud. |
| page_25 | Green grocer cicada | A cute cicada with big round eyes and clear patterned wings singing loudly while sitting on a short round tree stump that ends well inside the page, with simple sound wave lines, surrounded by loose gum leaves, a smiling sun, two clouds, flowers, grass tufts and a small bird covering its ears, square composition with white space all around. |
| page_26 | Praying mantis | A cute praying mantis with folded front legs turning its head to look over its shoulder with a friendly smile, surrounded by leaves, a flower, a butterfly friend, grass blades, a smiling sun and a cloud. |
| page_27 | Stick insect | A cute stick insect with long thin legs hiding on a branch and looking exactly like a twig, peeking with a playful smile, surrounded by twigs, leaves, a confused bird, a smiling sun and a cloud. |
| page_28 | Snail house | A cute snail with a big swirly shell house on its back and a happy face, a tiny round window and door drawn on the shell, surrounded by leaves, a mushroom, pebbles, dew drops, a smiling sun and a cloud. |
| page_29 | Snail trail | A cute snail gliding along a wavy slime trail across a garden path with a happy face, surrounded by flowers, leaves, a puddle, rain drops, a cloud, a smiling sun and pebbles. |
| page_30 | Earthworm | A cute earthworm with ring segments poking up from the soil with a happy face, surrounded by soil layers, roots, pebbles, a carrot underground, grass on top, a smiling sun and a cloud. |
| page_31 | Giant earthworm | A cute giant earthworm stretching very long in wavy loops through the soil next to a ruler stick, with a proud happy face, surrounded by soil, roots, pebbles, grass on top, a smiling sun and a cloud. |
| page_32 | Spider legs | A cute round spider with eight legs and a friendly smile waving four legs hello, sitting on a leaf, surrounded by flowers, grass blades, a ladybird friend, dew drops, a smiling sun and a cloud. |
| page_33 | Spider silk | A cute spider sitting in the middle of a big round web with dew drops on the threads and a happy face, surrounded by two branches, leaves, a flower, a smiling sun and a cloud. |
| page_34 | Huntsman | A cute huntsman spider with long legs and a gentle smile peeking out from behind loose tree bark, surrounded by gum leaves, a branch, a gum nut, a smiling sun, a cloud and grass. |
| page_35 | Peacock spider | A cute tiny peacock spider lifting a big round fan on its back and dancing with a happy face, simple dance motion lines around it, surrounded by flowers, leaves, grass, a smiling sun and a cloud. |
| page_36 | Blue-banded bee | A cute blue-banded bee with bold stripes on its body flying to a big flower with a happy face, surrounded by three flowers, leaves, a tomato plant, a smiling sun and clouds. |
| page_37 | Stingless bee | A cute tiny native bee with no sting waving happily beside a round wooden hive box, surrounded by bee friends, flowers, leaves, a honey drop, a smiling sun and a cloud. |
| page_38 | Leaf-cutter bee | A cute leaf-cutter bee carrying a round piece of leaf with a happy face, a leaf with neat round holes cut out beside it, surrounded by flowers, a hollow twig nest, a smiling sun and clouds. |
| page_39 | Moth | A cute fluffy moth with big feathery antennae flying at night with a happy face, surrounded by a crescent moon, stars, a glowing round lantern, a flower, leaves and a cloud. |
| page_40 | Bogong moth | A cute bogong moth flying over rounded mountains toward a cave with a happy face, two moth friends flying behind, surrounded by snowy peaks, a crescent moon, stars, gum trees and a cloud. |
| page_41 | Termite mound | A cute termite waving in front of a giant tall termite mound with round holes, two termite friends peeking out, surrounded by grass tufts, a small bush, a smiling sun, clouds and a lizard far away. |
| page_42 | Centipede | A cute long centipede with many little legs walking across a log with a happy face, surrounded by leaves, a mushroom, pebbles, grass blades, a smiling sun and a cloud. |
| page_43 | Millipede | A cute round millipede with many tiny legs curled into a happy swirl on the ground, surrounded by fallen leaves, a mushroom, a pine cone, pebbles, a smiling sun and a cloud. |
| page_44 | Slater | A cute slater with round armour plates rolled into a tight ball with a shy smile, a second slater friend walking beside it, surrounded by leaves, a rock, a mushroom, a smiling sun and a cloud. |
| page_45 | Water strider | A cute water strider with long thin legs standing on top of a pond with a happy face, little dimples in the water under its feet, surrounded by lily pads, reeds, a frog, a smiling sun and a cloud. |
| page_46 | Mud dauber wasp | A cute mud dauber wasp with a skinny waist building a nest from little round mud balls with a happy face, surrounded by a puddle, flowers, leaves, a smiling sun and a cloud. |
| page_47 | Burrowing cockroach | A cute giant burrowing cockroach with a round shell and a sleepy happy face resting at the entrance of its burrow, surrounded by sandy soil, gum leaves, pebbles, grass tufts, a smiling sun and a cloud. |
| page_48 | Lacewing | A cute lacewing with big see-through wings full of simple net lines and a happy face resting on a leaf, surrounded by flowers, leaves, dew drops, a smiling sun and a cloud. |
| page_49 | Six legs | A cute ant explorer with six legs and three round body parts holding a magnifying glass with a happy face, surrounded by a leaf, a flower, pebbles, a beetle friend, a smiling sun and a cloud. |
| page_50 | Garden party | A happy garden party of cute minibeasts: a ladybird, a bee, a butterfly, a snail and an ant sitting around a mushroom table with tiny cupcakes, surrounded by flowers, leaves, bunting, a smiling sun and clouds. |
