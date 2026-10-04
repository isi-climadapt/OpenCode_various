# Book 1 — Page-by-Page Generation Instructions (50 pages)

> For use with any image AI (ChatGPT/DALL-E, Midjourney, Ideogram, FLUX, Recraft).
> These replace the programmatic script: run each prompt, save output as `raw/page_XX.png` (replace existing files from any source).

## Universal prompt suffix (append to EVERY page prompt)

```
Bold and easy coloring book page for kids ages 3-8. A rich but simple scene around the animal with 6 to 8 easy elements suitable for its habitat (trees, clouds, stars, waves, rocks, flowers, smaller animal friends, bubbles, sun, grass or sand), each element drawn as one big simple closed shape. Very thick, clean, smooth black outlines (heavy, marker-friendly). Plain white background, no frame or border around the image edge. Only simple closed shapes with large open areas to colour. The main animal stays the largest thing on the page, portrait composition. Cute, friendly, happy faces with large simple eyes. No shading, no grey, no colour, no fill, no texture, no crosshatching. No words, letters, numbers or text anywhere in the image. Nothing in the bottom 6 percent of the page.
```

For Midjourney add: `--ar 17:22 --v 6 --style raw` (ar ~ 8.5:11)

## Production standards (checklist per image)
- Hero animal fills ≥60% of page height
- ALL shapes fully closed (no gaps in outlines)
- No fine hairlines; minimum stroke ≈ 3–5px at A4 300 DPI
- Pure black on pure white; gray = reject & regenerate
- NOTHING in the bottom 10% of the page (caption strip — typeset later)
- If two animals appear, one is small (baby/friend), hero bigger

## The 50 pages

| File | Page | Scene prompt (prepend nothing, append suffix) |
|---|---|---|
| page_01 | Koala napping | A cute koala napping, curled happily on a thick eucalyptus tree branch, closed sleepy eyes, two big round ears, a few simple gum leaves around the branch. |
| page_02 | Koala snacking | A cute chubby koala hugging a eucalyptus tree trunk, opening its mouth to eat a gum leaf, big oval ears with open centres, simple leaf shapes around. |
| page_03 | Kangaroo | A cute cartoon kangaroo standing upright on two big feet, long strong tail curving behind, small arms tucked to its chest, happy smile, one tall grass tuft nearby. |
| page_04 | Kangaroo & joey | A cute mother kangaroo standing upright, a smiling baby joey peeking out of her pouch between her front paws, simple round shapes, one grass tuft. |
| page_05 | Wallaby | A cute small wallaby standing on a smooth rock, ears alert, cheeks round, tail resting on the ground, cloud in the sky. |
| page_06 | Wombat | A cute chubby wombat sitting on the ground like a loaf of bread, front paws tiny and rounded, small ears, happy closed-mouth smile, grass tufts on both sides. |
| page_07 | Wombat at burrow | A cute round wombat standing at the entrance of a big simple burrow hole dug into a smooth hill, half-turned towards the hole, excited expression. |
| page_08 | Platypus swimming | A cute platypus swimming in calm water, duck-like bill smiling, big webbed front feet paddling, flat tail, three simple water wave lines below, two bubbles. |
| page_09 | Quokka | A cute quokka sitting like a small happy potato, round cheeks, huge smile, tiny rounded ears, its long tail curled around its body, small grass tuft. |
| page_10 | Quokka selfie | A cute smiling quokka sitting up tall holding a tiny old-fashioned camera in its paws, cheeks round, a flower beside it. (generic object only, no brand) |
| page_11 | Emu | A cute emu with a long neck, round fluffy scribble-feathered body, two skinny legs mid-stride, big friendly eyes, three hair tufts on its head. |
| page_12 | Kookaburra | A cute kookaburra perched on a thick branch, big beak, plump chest, eyes squeezed in a happy laugh, a few simple leaves at the branch tip. |
| page_13 | Galah | A cute galah bird with a rounded chest and crest standing proud, holding its head up proudly, two simple heart shapes floating beside it. |
| page_14 | Cockatoo | A cute sulphur-crested cockatoo perched upright on a branch, big curved crest on its head, chest puffed, wing slightly lifted to wave. |
| page_15 | Magpie | A cute magpie standing on the grass with its head tilted singing, beak open and small musical notes in the air, round body. |
| page_16 | Lorikeet | A cute rainbow lorikeet clinging to a branch upside-down, cheeky tongue out, brush-tip tongue visible, berries hanging above it. |
| page_17 | Cassowary | A cute friendly cassowary with a chunky round body, tall helmet casque on its head, neck wattle, sturdy legs, standing by a tropical leaf. |
| page_18 | Brolga dancing | A cute brolga crane with a slim curvy neck, mid-dance pose with one wing lifted, long thin legs, small flowers around its feet. |
| page_19 | Jabiru stork | A cute black-necked stork standing on one long leg in shallow water, big beak, simple ripple circles around its legs, fish silhouette swimming below. |
| page_20 | Wedge-tailed eagle | A cute friendly wedge-tailed eagle perched on a rock top, wings folded, proud chest, rounded head with small curved beak, clouds behind. |
| page_21 | Pelican | A cute pelican standing by the water, big beak pouch full of one little smiling fish, round belly, wing folded, one lighthouse-free seaside background with simple waves. |
| page_22 | Echidna | A cute echidna walking happily, soft سلام spikes on its back drawn as simple triangles, long snout, tiny eyes, one ant trail winding ahead of it. |
| page_23 | Echidna lunch | A cute echidna eating: one ant on a simple leaf in front of it, spikes big and rounded like little triangles, closed content eyes. |
| page_24 | Dingo | A cute dingo sitting with an ear up and one ear flopped, pointed muzzle, big fluffy curled tail, sitting beside one simple bone shape on the ground. |
| page_25 | Tasmanian devil | A cute chubby Tasmanian devil with big round belly, tiny ears, wide smile showing two little teeth, sitting like a seashell pearl, simple sketch clouds. |
| page_26 | Frill-necked lizard | A cute frill-necked lizard standing proud, big umbrella-like circular frill open around its head (with simple scallop edges), smile and one wink, sun in the sky. |
| page_27 | Blue-tongue lizard | A cute blue-tongue lizard lying relaxed on a smooth rock, sticking out a slightly wavy flat tongue, chunky friendly legs, one rocking cloud. |
| page_28 | Goanna | A cute goanna with a long wavy tail striding over two simple rounded rocks, round belly, pattern-free skin with 3 simple oval spots, tongue out. |
| page_29 | Bilby | A cute bilby with giant long ears, long pointed snout, sitting next to a small sand mound with a burrow entrance, moon and one star in the sky. |
| page_30 | Numbat | A cute numbat standing on hind legs, long thin sticky tongue out licking a tiny ant on a log, big bushy tail curled behind, stripes-free simple pattern as four short bands on its back. |
| page_31 | Quoll | A cute spotted quoll with soft round spots (only big dots), tiny pink nose, twig and two leaves underfoot. |
| page_32 | Hopping mouse | A cute tiny hopping mouse standing on hind legs with big round ears, a few desert grains of sand dots, two tiny spinifex grass tufts. |
| page_33 | Bandicoot | A cute bandicoot digging a small hole in the ground, one front paw raised in dig position, long pointed nose, big cheerful eyes, dirt specks flying. |
| page_34 | Bettong | A cute bettong carrying a tiny bundle of leaves in its curled tail (tail drawn as strong arm), chubby cheeks, hopping pose. |
| page_35 | Potoroo | A cute potoroo sniffing a small mushroom on the forest floor, long nose, sitting on haunches, one fern leaf nearby. |
| page_36 | Possum | A cute ringtail possum curled around a thick branch like a cinnamon roll, big round eyes, tail wrapped with a small bow (tail curls the branch), four gum leaves. |
| page_37 | Sugar glider | A cute sugar glider mid-glide between two branches, arms and legs stretched, gliding membrane open like a comfy blanket between them, big sparkle eyes, two stars in the sky. |
| page_38 | Camel | A cute cartoon camel with two humps and a long eyelashy face, sitting calmly on desert dunes, one large sun and two simple sand hills. |
| page_39 | Sea turtle | A cute sea turtle swimming, big round shell divided into 5 simple puzzle-piece shapes (big and colourable), smiling face, three wave lines, two bubbles. |
| page_40 | Dugong | A cute round dugong floating underwater, big snout, smiling, one small seagrass leaf in its mouth, three wave lines above it. |
| page_41 | Dolphin jumping | A cute dolphin leaping in a happy arc above the water, belly round, flipper waving, three splash droplets, smiley face. |
| page_42 | Little penguin | A cute little penguin standing on a smooth iceberg rock, flipper wings slightly out, big eyes, small beak, two drops of water flying around. |
| page_43 | Seahorse | A cute seahorse curled around a wide piece of seaweed from the sea floor, spiky little crown on its head, cheeks, curly tail, three bubbles. |
| page_44 | Clownfish | A cute clownfish (2 simple stripes only) swimming beside a simple 3-tentacle anemone, big fins, cheeky face, bubbles above. |
| page_45 | Jellyfish | A cute smiling jellyfish with a bell-shaped head and only 5 wavy tentacles below, large simple circles inside the bell, two bubbles. |
| page_46 | Octopus | A cute round octopus with exactly 6 chunky curling legs (count them), big happy smile, one bubble forming a heart shape. |
| page_47 | Hermit crab | A cute hermit crab peeking out of a big spiral shell sitting on the sea floor sand, tiny claws waving hello, one starfish nearby. |
| page_48 | Baby whale | A cute baby humpback whale with a smiling face, small fin, spout blowhole spray of 3 simple droplets, waves below, one tiny fish friend. |
| page_49 | Frogs & lily pad | A cute green tree frog sitting on a big round lily pad, eyes bulging happily, one foot waving, simple circled pond ripples. |
| page_50 | Butterfly garden | A cute chunky butterfly with symmetric big wings floating above one daisy-like flower, simple round patterns on both wings (4 big circles each), smiling. |

## Fun-fact captions (typeset by assembler below each image)

| Page | Fact caption (one line) |
|---|---|
| 01 | Koalas sleep up to 20 hours a day! |
| 02 | Koalas eat almost only eucalyptus leaves. |
| 03 | A kangaroo can hop over 9 metres in one jump. |
| 04 | Baby kangaroos are called joeys. |
| 05 | Wallabies use their tail like a fifth leg. |
| 06 | Wombats do cube-shaped poos! |
| 07 | Wombats dig long tunnel homes called burrows. |
| 08 | Platypus has a duck bill and webbed feet. |
| 09 | A quokka's smile can brighten anyone's day. |
| 10 | Quokkas are very curious and love to pose. |
| 11 | Emus can't fly, but they can run very fast. |
| 12 | Kookaburras laugh to greet the morning. |
| 13 | Galahs mate for life — best friends forever. |
| 14 | Cockatoos love to dance to music. |
| 15 | Magpies can sing many different tunes. |
| 16 | Lorikeets drink nectar with brush-tipped tongues. |
| 17 | Cassowaries have a helmet called a casque. |
| 18 | Brolgas do beautiful dancing in pairs. |
| 19 | Jabirus are Australia's tallest flying bird. |
| 20 | Wedge-tailed eagles can see tiny animals from the sky. |
| 21 | Pelicans use their beak pouch like a shopping bag. |
| 22 | Echidnas are covered in special spikes. |
| 23 | Echidnas love to munch on ants and termites. |
| 24 | Dingoes are Australia's wild dogs. |
| 25 | Tasmanian devils make VERY loud growls. |
| 26 | Frill-necked lizards have a big neck umbrella. |
| 27 | Blue-tongue lizards have bright blue tongues. |
| 28 | Goannas can climb trees! |
| 29 | Bilbies have enormous ears to hear insects. |
| 30 | Numbats eat up to 20,000 termites a day. |
| 31 | Quolls carry their babies on their back. |
| 32 | Hopping mice barely need any water to live. |
| 33 | Bandicoots dig little star-shaped holes. |
| 34 | Bettongs are tiny kangaroo cousins. |
| 35 | Potoroos are very shy forest hoppers. |
| 36 | Possums sleep all day in tree hollows. |
| 37 | Sugar gliders can glide like a parachute. |
| 38 | Camels can survive long desert adventures. |
| 39 | Sea turtles can live over 80 years. |
| 40 | Dugongs are the ocean's gentle cows. |
| 41 | Dolphins talk to each other with clicks. |
| 42 | Little penguins are the smallest penguins in the world. |
| 43 | Male seahorses carry the babies! |
| 44 | Clownfish live safely inside anemones. |
| 45 | Jellyfish have no brain but still get around. |
| 46 | Octopuses have three hearts. |
| 47 | Hermit crabs borrow shells as houses. |
| 48 | Baby whales drink lots and lots of milk. |
| 49 | Tree frogs have sticky toes for climbing. |
| 50 | Butterflies taste with their feet! |

## Assembly note (next agent)
Drop generated images into `book1/raw/page_01..50.png` (2550×3300, white bg). The assembler adds: title page, copyright, "This book belongs to", colour-tips page, gallery certificate, 3 keepsake pages → 108pp PDF per KDP spec (no bleed for this build, margins ≥0.375", safe area respected; captions typeset at 0.35" from bottom edge, min gutter 0.375" as page count <151).

**KDP disclosure reminder:** if pages are AI-generated, answer "AI-generated (with human review/editing)" honestly in the upload questionnaire.
