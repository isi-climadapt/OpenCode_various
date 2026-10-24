# Book 6: Yummy Cuties, page-by-page generation instructions (50 pages)

> Gumleaf Kids Press / Matilda Hayes. US-first book (Amazon.com primary, US spelling in all customer-facing text). Ages 4-8.
> Theme: cute animals with sweet treats and tasty food (cupcakes, ice cream, pancakes, pizza, fruit, veggies, picnics),
> with a true food fact on every page. Research: publishing\10-trend-scout-book6.md, 11-validation-book6.md.
> Style: Author 1 locked kawaii thick-outline line art, 10 to 14 elements, art box 2230x2520, fun fact on every page.
> Engine: batch_generate6.py in this folder (copied from book5/batch_generate5.py, rule 15). OpenArt CLI / nano-banana-2 only.

## Universal prompt suffix (LOCKED, append to EVERY scene prompt)

```
Bold and easy coloring book page. A rich, detailed but simple scene with 10 to 14 easy elements arranged to fill the whole page around the main character (things that belong in the scene's setting), all part of one connected scene, never a border of separate stickers or icons around the edge, each element drawn as one big simple closed shape. The composition fills almost the entire page. Whole scene floats with a plain white margin on every side; no element touches the image edges. Absolutely no rectangular frame or box line anywhere; do not draw a border. Very thick, clean, smooth black outlines (heavy, marker-friendly), pure black on plain white only. Only simple closed shapes with large open areas to color. The main character stays the largest thing on the page, portrait composition. Cute, friendly, happy faces with large simple eyes. No shading, no grey, no color fill, no texture, no crosshatching. No words, letters, numbers or text anywhere in the image. Nothing in the bottom 6 percent of the page.
```

Prompt rules: no labeled props (bottles, jars, shakers, boxes, cartons, wrappers, signs, menus and price tags print words on them); no color words (food and animal names only); setting elements named per scene, never a generic sticker list. No boxes, windows or shop fronts as the main shape (they prime frames, book 4 finding). Candles are plain, never number candles.

## Failure modes: F1 to F13 per AGENT-PIPELINE.md; F9 coherence audit runs after every typeset.

## The 50 pages

| File | Page | Scene prompt (prepend nothing, append suffix) |
|---|---|---|
| page_01 | Cupcake baker | A cute bunny rabbit baker in a chef hat piping a tall swirl of frosting onto a big cupcake, standing at a little round table with more cupcakes on a round cake stand, a mixing bowl, a whisk, a rolling pin, an oven mitt and sprinkles. |
| page_02 | Pancake stack | A cute piglet sitting at a breakfast table with a tall stack of fluffy pancakes topped with a pat of butter and dripping syrup, with a little syrup pitcher, strawberries, a fork, a plate and a flower in a cup. |
| page_03 | Honeycomb bear | A cute bear cub hugging a big round piece of honeycomb with honey dripping, sitting under a tree with a round beehive hanging from a branch, smiling bees, flowers, a honey dipper and a cloud. |
| page_04 | Strawberry patch | A cute hedgehog carrying a basket full of big strawberries through a strawberry patch, with strawberry plants, leaves, flowers, a butterfly, a snail and a smiling sun. |
| page_05 | Ice cream cone | A cute penguin holding a tall ice cream cone with three round scoops and a cherry on top, under a striped beach umbrella, with more waffle cones in a stand, a bowl of ice cream, a seagull, sand and a smiling sun. |
| page_06 | Popcorn night | A cute kitten on a cozy sofa hugging a big round bowl of popcorn with popcorn pieces popping up into the air, with a cushion, a blanket, a lamp, a slipper and a sleeping puppy friend. |
| page_07 | Pizza chef | A cute puppy dog chef in a chef hat tossing pizza dough in the air, with a big round pizza with cheese and tomato slices on a round table, basil leaves, a rolling pin, a pizza peel and a round brick oven. |
| page_08 | Banana monkey | A cute monkey peeling a big banana while hanging from a jungle branch by its tail, with a bunch of bananas, big palm leaves, a coconut, flowers and a parrot friend. |
| page_09 | Watermelon picnic | A cute baby hippo eating a big slice of watermelon on a picnic blanket, with a whole watermelon, a picnic basket, a sandwich, a lemonade pitcher, flowers and a smiling sun. |
| page_10 | Carrot pull | A cute bunny rabbit pulling a giant carrot out of the soil in a vegetable garden, with more carrot tops, lettuce, a watering can, a garden spade, a butterfly and a cloud. |
| page_11 | Apple orchard | A cute giraffe picking a round apple from the top of a tall apple tree with its long neck, with apples on the branches, a basket of apples on the grass, a ladder, flowers and a bird. |
| page_12 | Pineapple sloth | A cute sloth hanging from a tree branch and hugging a big pineapple, with palm leaves, a pineapple plant growing below, tropical flowers, a butterfly and a smiling sun. |
| page_13 | Peanut elephant | A cute baby elephant holding a peanut in its curled trunk, sitting beside a big pile of peanuts in their shells, with peanut plants, a bowl, flowers, a mouse friend and a cloud. |
| page_14 | Cacao tree | A cute red panda holding a big cacao pod under a cacao tree with more pods growing on its trunk, with a bowl of chocolate pieces, a mug of hot chocolate, big leaves and a butterfly. |
| page_15 | Cotton candy fair | A cute lamb holding a big fluffy cloud of cotton candy on a stick in a sunny park, with a carousel horse, a Ferris wheel, balloons, a tree, flowers and bunting flags. |
| page_16 | Ice pop day | A cute tiger cub licking an ice pop on a stick on a hot sunny day, sitting on a beach towel, with a sandcastle, a bucket and spade, a beach ball, a seashell and a smiling sun. |
| page_17 | Spaghetti slurp | A cute piglet slurping a long strand of spaghetti from a big bowl of spaghetti and meatballs, with a fork, a basket of bread, a tomato, basil leaves and a candle on the table. |
| page_18 | Sushi rolls | A cute kitten rolling sushi with a bamboo mat, with a plate of sushi rolls, a bowl of rice, chopsticks, a little fish friend smiling, a teapot and a teacup. |
| page_19 | Corn field | A cute mouse hugging a big ear of corn with its husk peeled back, in a corn field with tall corn plants, a scarecrow, a crow friend, a wooden fence and a cloud. |
| page_20 | Blueberry bush | A cute bear cub picking blueberries from a big blueberry bush into a round pail, with berries on the branches, leaves, a butterfly, a ladybug, flowers and a cloud. |
| page_21 | Lemonade | A cute duckling pouring lemonade from a round pitcher into a glass at a little round picnic table, with a small lemon tree full of lemons growing in a big flower pot beside it, lemon slices, a straw, flowers and a smiling sun. |
| page_22 | Grape vine | A cute frog sitting under a grape vine holding a big bunch of grapes, with more grapes hanging from the vine, big leaves, a tray of raisins drying, a snail and a smiling sun. |
| page_23 | Broccoli forest | A cute turtle walking through a little forest of giant broccoli trees, with a carrot, peas in a pod, a mushroom, a ladybug, flowers and a cloud. |
| page_24 | Potato dig | A cute mole digging up big round potatoes in a garden, with potato plants, a little garden fork, a basket of potatoes, a worm friend, flowers and a cloud. |
| page_25 | Avocado toast | A cute capybara holding a slice of avocado toast at a breakfast table, with a whole avocado cut in half showing its big seed, a plate, a cup of juice, a little orange on its head and a flower. |
| page_26 | Tomato garden | A cute baby goat sniffing big round tomatoes growing on a tomato plant, with a basket of tomatoes, a tomato flower, a watering can, a garden stake, a butterfly and a cloud. |
| page_27 | Pumpkin patch | A cute mouse sitting on top of a big round pumpkin in a garden patch, with pumpkin vines, leaves, a small pumpkin cut open showing its seeds, a wheelbarrow, a bird and a smiling sun. |
| page_28 | Coconut beach | A cute otter floating on its back in the sea hugging a coconut, near a sandy beach with a palm tree, more coconuts, a seashell, a starfish, waves and a smiling sun. |
| page_29 | Cookie picnic | A cute puppy dog and a cute kitten friend sharing a big plate of round chocolate chip cookies on a picnic blanket in a garden, with two glasses of milk, a picnic basket, a cookie in the puppy's paw, flowers, a butterfly and a cloud. |
| page_30 | Donut stack | A cute panda holding a tall stack of donuts with sprinkles and icing, at a table with a plate of donuts, a donut on a stand, a cup of cocoa, sprinkles and a flower in a cup. |
| page_31 | Pretzel seal | A cute seal pup balancing a giant twisty pretzel on its nose on a rock by the sea, with a bowl of little pretzels, a beach ball, waves, a seagull and a smiling sun. |
| page_32 | Bread baker | A cute alpaca baker in a chef hat holding a round loaf of fresh bread, with a long loaf of bread, a basket of bread rolls, a bunch of wheat, a rolling pin and a bowl of flour. |
| page_33 | Waffle breakfast | A cute koala sitting at a breakfast table with a big square waffle topped with berries and whipped cream, with a waffle iron, a little syrup pitcher, a bowl of berries, a cup and a flower. |
| page_34 | Hot cocoa | A cute hedgehog wrapped in a blanket holding a big mug of hot cocoa with marshmallows floating on top, with a bowl of marshmallows, a cozy cushion, a lamp, a slipper and a cookie on a plate. |
| page_35 | Milkshake | A cute cow calf sipping a tall milkshake with a straw and whipped cream on top, sitting at a little round table in a flowery meadow, with a second milkshake, a cherry, a bowl of ice cream, a spoon, a tree and a cloud. |
| page_36 | Big sandwich | A cute baby hippo stacking a tall sandwich with bread, lettuce, cheese and tomato slices, at a table with a plate, a pickle, an apple, a cup of juice and a picnic basket. |
| page_37 | Cinnamon rolls | A cute lamb holding a tray of swirly cinnamon rolls with icing, with a cinnamon stick bundle, a mixing bowl, a rolling pin, an oven mitt, a plate and a cup of cocoa. |
| page_38 | Kiwi and kiwi | A cute round kiwi bird with a long beak standing next to a big kiwifruit cut in half showing its seeds, with more kiwifruit, ferns, leaves, a little log, a mushroom and a smiling sun. |
| page_39 | Tea party | A cute bunny, a cute kitten and a cute mouse having a tea party at a little round table, with a teapot, teacups, a plate of little cakes, a cake stand, a flower vase and bunting. |
| page_40 | S'mores campfire | A cute beaver and a cute squirrel toasting marshmallows on sticks over a small campfire, with a plate of s'mores, a log seat, a tent, pine trees, a crescent moon and stars. |
| page_41 | Birthday cake | A cute lion cub in a party hat with a big round birthday cake with plain candles and frosting swirls, with balloons, wrapped presents, streamers, a cupcake and a party horn. |
| page_42 | Swiss cheese | A cute mouse peeking out through a hole in a big wedge of Swiss cheese full of round holes, with a plate of cheese cubes, crackers, a grape bunch, a cheese knife and a little mouse friend. |
| page_43 | Maple syrup | A cute squirrel pouring maple syrup from a little pitcher onto a stack of pancakes, beside a maple tree with a bucket hanging on its trunk to catch the sap, with maple leaves and a cloud. |
| page_44 | Bamboo lunch | A cute panda sitting in a bamboo forest munching a bamboo stalk, with tall bamboo stalks, bamboo leaves, a bowl of dumplings, a small stream, a rock and a butterfly. |
| page_45 | Orange grove | A cute baby orangutan hugging a big round orange under an orange tree full of oranges, with an orange cut in half, a basket of oranges, leaves, flowers and a smiling sun. |
| page_46 | Apple pie | A cute bear cub holding a round apple pie with a lattice top, with a basket of apples, an apple cut in half, a rolling pin, an oven mitt, a plate and a flower in a cup. |
| page_47 | Egg nest | A cute fluffy baby chick standing next to its smiling mother hen on a straw nest of eggs, with one egg hatching, a barn, a wooden fence, flowers and a cloud. |
| page_48 | Mango toucan | A cute toucan with a big curved beak holding a mango, perched on a branch of a mango tree with mangoes hanging, with a cashew fruit, big leaves, tropical flowers and a butterfly. |
| page_49 | Cranberry bog | A cute duckling paddling in a cranberry bog full of floating round cranberries, with cranberry plants, reeds, lily pads, a frog friend, a dragonfly and a smiling sun. |
| page_50 | Yummy Cuties feast | A cute bunny, bear cub, panda, penguin, kitten and puppy sharing a big happy feast at one long picnic table, with a cake, cupcakes, a bowl of fruit, a pizza, balloons and bunting. |
