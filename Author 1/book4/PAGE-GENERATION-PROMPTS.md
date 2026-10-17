# Book 4: Snowy Cuties, page-by-page generation instructions (50 pages)

> Gumleaf Kids Press / Matilda Hayes. US-first book (Amazon.com primary, US spelling in all customer-facing text).
> Theme: cute snow and arctic animals doing cozy winter things, with 10 holiday pages (41 to 50) so it sells as a
> Christmas gift and keeps selling through February. Research: publishing\06-trend-scout-book4.md.
> Style: Author 1 locked kawaii thick-outline line art, 10 to 14 elements, art box 2230x2520, fun fact on every page.
> Engine: batch_generate4.py in this folder. OpenArt CLI / nano-banana-2 only.

## Universal prompt suffix (LOCKED, append to EVERY scene prompt)

```
Bold and easy coloring book page. A rich, detailed but simple scene with 10 to 14 easy elements arranged to fill the whole page around the main character (things that belong in the scene's setting, plus a few snowflakes), all part of one connected scene, never a border of separate stickers or icons around the edge, each element drawn as one big simple closed shape. The composition fills almost the entire page. Whole scene floats with a plain white margin on every side; no element touches the image edges. Absolutely no rectangular frame or box line anywhere; do not draw a border. Very thick, clean, smooth black outlines (heavy, marker-friendly), pure black on plain white only. Only simple closed shapes with large open areas to color. The main character stays the largest thing on the page, portrait composition. Cute, friendly, happy faces with large simple eyes. No shading, no grey, no color fill, no texture, no crosshatching. No words, letters, numbers or text anywhere in the image. Nothing in the bottom 6 percent of the page.
```

Prompt rules: no color words (an animal's name only, e.g. "fox", "bear", "cardinal bird"); setting elements named per scene, never a generic sticker list.

## Failure modes: F1 to F11 per AGENT-PIPELINE.md; F9 coherence audit runs after every typeset.

## The 50 pages

| File | Page | Scene prompt (prepend nothing, append suffix) |
|---|---|---|
| page_01 | Penguin sledding | A cute penguin sliding down a snowy hill on its belly with flippers spread out and a big grin, a penguin friend cheering at the bottom, with rounded snowdrifts, two pine trees, an ice block, a snowy rock and falling snowflakes. |
| page_02 | Polar bear snowman | A cute polar bear building a snowman with a carrot nose and stick arms, patting on the round head with both paws, beside a bucket and a small shovel, with snowy mounds, two pine trees, a snowball pile and snowflakes. |
| page_03 | Arctic fox tail | A cute arctic fox curled up asleep on a snowy hill with its big fluffy tail wrapped around itself like a blanket, a crescent moon, three stars, two pine trees and soft snowdrifts around it. |
| page_04 | Snowy owl | A cute snowy owl with big round eyes perched on a snowy pine branch during the day, a smiling sun behind a cloud, pine cones on the branch, snowy hills below and a little mouse friend peeking from a snow hole. |
| page_05 | Reindeer nose | A cute reindeer with round antlers and a big happy nose standing in a snowy field, breathing out a little puff of cloud, with two pine trees, a wooden fence, a snowy hill and snowflakes. |
| page_06 | Harp seal pup | A cute fluffy baby harp seal with big round eyes lying on a smooth ice floe, its mother seal smiling beside it, with gentle water ripples, two ice chunks, a snowy cliff and snowflakes. |
| page_07 | Walrus tusks | A cute walrus with two long rounded tusks and a bushy mustache hooking its tusks onto an ice edge to pull itself up, with water ripples, a fish friend, ice chunks, a snowy cliff and a smiling sun. |
| page_08 | Penguin huddle | Five cute emperor penguins huddled close together in a round group, the middle one smiling cozily, with snowflakes falling, icy hills behind, a crescent moon, stars and a small ice block. |
| page_09 | Narwhal | A cute narwhal with one long spiral tusk swimming under floating ice, a beluga friend nearby, with bubbles, two fish, ice floes above, water ripples and a starfish on a rock. |
| page_10 | Singing beluga | A cute smiling beluga whale with a round forehead singing, little music note swirls rising from the water, with ice floes, two fish, bubbles, a snowy shore and a seal friend listening. |
| page_11 | Moose swimming | A cute moose with big round antlers swimming in a calm lake with only its head and antlers above the water, holding a water plant in its mouth, with lily pads, reeds, snowy pine trees on the shore and snowflakes. |
| page_12 | Arctic hare hop | A cute arctic hare hopping on its two back legs across the snow with a joyful face, with snowy hills, little paw prints, two pine trees, a snowy rock, a smiling sun and snowflakes. |
| page_13 | Snowshoe hare | A cute snowshoe hare with big fluffy back feet sitting in deep snow next to its burrow, with a winter shrub, two pine trees, a snowy log, pine cones and falling snowflakes. |
| page_14 | Husky nap | A cute husky puppy curled up asleep in the snow with its fluffy tail over its nose, beside a small wooden dog house, a bowl, a sled leaning on the house, snowy pine trees and snowflakes. |
| page_15 | Puffin flight | A cute puffin with a big rounded beak flapping its wings fast over the sea, little motion swirls by its wings, with a rocky cliff, waves, a fish in its beak, a cloud and a puffin friend on the cliff. |
| page_16 | Sleepy bear | A cute bear sleeping in a cozy den under a snowy hill, curled up with a smile and a tiny nightcap, with roots, a pillow of leaves, snow on the hill above, a pine tree and a crescent moon. |
| page_17 | Chipmunk pantry | A cute chipmunk with puffy cheeks sitting on a snowy log and hugging an acorn, with a small pile of acorns and seeds beside it, a pine cone, a mushroom, a little snowy bush and snowflakes. |
| page_18 | Cardinal on branch | A cute cardinal bird with a pointy crest perched on a snowy branch with round berries, singing happily, with a bird feeder hanging nearby, a pine tree, a snowy fence and snowflakes. |
| page_19 | Chickadee seeds | A cute round chickadee hiding a seed in the bark of a snowy tree, with a pine cone, a sunflower head, two more seeds, a small birdhouse, snowy branches and snowflakes. |
| page_20 | Snow leopard | A cute snow leopard cub with big round spots sitting on a snowy mountain rock with its long fluffy tail wrapped around its neck like a scarf, with snowy peaks, a pine tree and snowflakes. |
| page_21 | Red panda bamboo | A cute red panda sitting in the snow holding a bamboo stalk with its front paws and munching, with bamboo leaves, a snowy log, a snowy pine tree, round snowballs and snowflakes. |
| page_22 | Mountain goat | A cute mountain goat with small curved horns and a fluffy beard standing proudly on a snowy mountain ledge, with rounded rocks, a pine tree, snowy peaks, a cloud and a smiling sun. |
| page_23 | Bison snow sweep | A cute bison with a big fluffy head sweeping snow aside with its head to find grass tufts underneath, with snowy hills, a pine tree, grass tufts, a cloud and snowflakes. |
| page_24 | Sea otter float | A cute sea otter floating on its back in the water with a big smile, holding a shell on its tummy, with gentle waves, kelp leaves, a rock, a seagull friend and snowy mountains on the shore. |
| page_25 | Ermine | A cute ermine with a long slim body standing up on its back legs in the snow, its tail tip shown as a small dark tip, with snowy grass tufts, a log, a pine tree, a snowy rock and snowflakes. |
| page_26 | Musk ox | A cute musk ox with a long shaggy coat and curled horns standing in a snowy meadow with a calm smile, a baby musk ox beside it, with snowy hills, a cloud and snowflakes. |
| page_27 | Lynx paws | A cute lynx with tufted ears and big furry paws walking on top of the deep snow with a happy face, with paw prints, two pine trees, a snowy log, a crescent moon and snowflakes. |
| page_28 | Raccoon nap | A cute raccoon with a striped tail napping inside a hollow tree, peeking out with sleepy eyes, with a snowy branch above, an acorn pile, a pine tree and snowflakes. |
| page_29 | Deer coat | A cute deer with a fluffy winter coat and a little tail standing in a snowy forest clearing, nibbling a twig, with pine trees, a snowy bush, a log, a smiling sun and snowflakes. |
| page_30 | Fox pounce | A cute fox leaping high in a curved arc and diving nose first into the snow, with a tiny mouse hole below, snowy hills, two pine trees, paw prints and snowflakes. |
| page_31 | Bunny snowflakes | A cute bunny catching big snowflakes on its tongue, each snowflake drawn as a large six-pointed shape, with snowy hills, a pine tree, a snowman friend in the distance and a cloud. |
| page_32 | Penguin snowflake | A cute penguin holding up one giant six-sided snowflake like a trophy with a proud smile, with smaller snowflakes falling, an ice block, snowy hills and a penguin friend clapping. |
| page_33 | Penguin swimming | A cute penguin swimming fast underwater with flippers spread like wings, a trail of bubbles behind it, with fish friends, ice floes above, a rock and seaweed. |
| page_34 | Polar bear swim | A cute polar bear swimming in calm icy water with a happy face and paws paddling, with floating ice chunks, a smiling sun, water ripples, a seal friend on an ice floe and snowflakes. |
| page_35 | Bear hot cocoa | A cute bear wrapped in a blanket holding a big mug of hot cocoa with marshmallows and a curl of steam, sitting by a frosty window, with a candle, a cushion, a plate of cookies and snowflakes outside. |
| page_36 | Igloo friends | A cute penguin and seal waving from the round doorway of a dome-shaped igloo made of snow blocks, with snowy hills, an ice block, a sled, a crescent moon and stars. |
| page_37 | Arctic fox paws | A cute arctic fox walking across the ice lifting one paw to show its fluffy furry paw pads, with snowy rocks, paw prints, ice chunks, a snowy hill and snowflakes. |
| page_38 | Otters holding hands | Two cute sea otters floating on their backs holding paws so they stay together, both smiling, with gentle waves, kelp leaves, a crescent moon, stars and a rock. |
| page_39 | Snowball fight | A cute raccoon and a bunny having a friendly snowball fight behind two snow forts, snowballs flying in the air, with a snowball pile, a pine tree, snowy hills and snowflakes. |
| page_40 | Snow angels | A cute polar bear cub lying on its back in fresh snow, flapping its arms and legs to make a snow angel, giggling, with a snowman friend, a pine tree, a pile of snowballs, a smiling sun and snowflakes. |
| page_41 | Reindeer tree | Two cute reindeer, both with antlers, decorating a Christmas tree with round ornaments and a star on top, holding a garland between them, with wrapped presents under the tree and snowflakes outside a window. |
| page_42 | Penguin egg | A cute emperor penguin dad standing with a round egg balanced on top of his feet, tucked under his fluffy belly, smiling proudly, with snowy hills, an ice block, a crescent moon, stars and snowflakes. |
| page_43 | Stockings | A cute polar bear hanging stockings on a cozy fireplace mantel, sniffing a plate of cookies on a small table, with a crackling fire, a garland, a clock, a rug and a wrapped present. |
| page_44 | Gingerbread house | A cute mouse in a little apron decorating a big gingerbread house with gumdrops and candy canes, with icing on the roof, a gingerbread man friend, a mixing bowl and a candy cane fence. |
| page_45 | Owl lights | A cute owl turning its head to look back over its shoulder while hanging a string of round holiday lights on a snowy pine tree, with ornaments, a star on top, snowflakes and a full moon. |
| page_46 | Fox cookies | A cute fox in a chef hat cutting gingerbread cookies with cookie cutters on a table, with a rolling pin, a tray of star and tree cookies, a mixing bowl, oven mitts and a frosty window. |
| page_47 | Caroling moose | A cute moose with big ears singing carols in a winter scarf, holding a songbook with two bunny friends singing beside it, with a street lamp, music note swirls, snowy pine trees and snowflakes. |
| page_48 | Husky sleigh | Two cute huskies pulling a small wooden sleigh piled with wrapped presents through the snow, with snowy pine trees, a winding snowy path, snowflakes and a crescent moon. |
| page_49 | Seal wreath | A cute harp seal popping its head up through a round hole in the ice, wearing a small holiday wreath on its head like a crown with a happy face, with bubbles, an ice floe, snowflakes and a penguin friend waving. |
| page_50 | Snowy Cuties party | A cute penguin, polar bear, arctic fox and reindeer having a cozy winter party together, with hot cocoa mugs, a snowman, a decorated pine tree, wrapped presents, string lights and snowflakes. |
