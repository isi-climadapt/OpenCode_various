# Book 5: Pawsome Cuties, page-by-page generation instructions (50 pages)

> Gumleaf Kids Press / Matilda Hayes. US-first book (Amazon.com primary, US spelling in all customer-facing text). Ages 4-8.
> Theme: cute puppies, kittens and other pets (bunnies, hamsters, guinea pigs, fish, birds, a turtle, a tortoise,
> ponies and small pets) in cozy everyday moments. Research: publishing\08-trend-scout-book5.md, 09-validation-book5.md.
> Style: Author 1 locked kawaii thick-outline line art, 10 to 14 elements, art box 2230x2520, fun fact on every page.
> Engine: batch_generate5.py in this folder (copied from book4/batch_generate4.py, rule 15). OpenArt CLI / nano-banana-2 only.

## Universal prompt suffix (LOCKED, append to EVERY scene prompt)

```
Bold and easy coloring book page. A rich, detailed but simple scene with 10 to 14 easy elements arranged to fill the whole page around the main character (things that belong in the scene's setting), all part of one connected scene, never a border of separate stickers or icons around the edge, each element drawn as one big simple closed shape. The composition fills almost the entire page. Whole scene floats with a plain white margin on every side; no element touches the image edges. Absolutely no rectangular frame or box line anywhere; do not draw a border. Very thick, clean, smooth black outlines (heavy, marker-friendly), pure black on plain white only. Only simple closed shapes with large open areas to color. The main character stays the largest thing on the page, portrait composition. Cute, friendly, happy faces with large simple eyes. No shading, no grey, no color fill, no texture, no crosshatching. No words, letters, numbers or text anywhere in the image. Nothing in the bottom 6 percent of the page.
```

Prompt rules: no labeled props (bottles, jars, shakers print words on them); no color words (an animal's name only, e.g. "retriever puppy", never "golden"); setting elements named per scene, never a generic sticker list. No boxes, tanks, cages, hutches or windows as the main shape (they prime frames, book 4 finding).

## Failure modes: F1 to F13 per AGENT-PIPELINE.md; F9 coherence audit runs after every typeset.

## The 50 pages

| File | Page | Scene prompt (prepend nothing, append suffix) |
|---|---|---|
| page_01 | Puppy bath | A cute puppy dog sitting in a round bathtub full of big soap bubbles with a happy grin, a rubber duck floating beside it, with a scrub brush, a round sponge, a towel, a bath mat and bubbles floating up. |
| page_02 | Kitten yarn | A cute kitten pouncing on a big ball of yarn with the loose yarn looping around its paws, with a knitting basket, two more yarn balls, a cushion, a potted plant and a rug. |
| page_03 | Bunny binky | A cute bunny rabbit jumping high in the air and twisting with joy in a garden, with carrots growing in the soil, flowers, a little picket fence, a watering can, a butterfly and a smiling sun. |
| page_04 | Hamster cheeks | A cute hamster with big puffy cheeks stuffed full of seeds, sitting next to a pile of sunflower seeds, with a little wooden house, a food bowl, a running wheel, a peanut and bedding shavings. |
| page_05 | Pet fishbowl | A cute pet fish with long flowing fins swimming happily in a round fishbowl with a little castle, pebbles, a water plant and bubbles, the bowl on a small round table with a potted plant and a little toy boat. |
| page_06 | Retriever fetch | A cute retriever puppy running across a park with a tennis ball in its mouth and ears flapping, with a tree, a park bench, a flying disc on the grass, flowers, a cloud and a butterfly. |
| page_07 | Cat whiskers | A cute cat with long whiskers sniffing a flower in a garden, with flower pots, a watering can, a birdbath, a butterfly, a snail and leafy plants. |
| page_08 | Guinea pig popcorn | A cute guinea pig hopping straight up in the air with joy, with a pile of hay, a carrot, a lettuce leaf, a cucumber slice, a little wooden hideout and a food bowl. |
| page_09 | Talking parrot | A cute parrot with a curved beak perched on a wooden play stand, flapping one wing as if saying hello, with a little bell, a swing, a cracker, a fruit bowl and a potted palm. |
| page_10 | Pet turtle | A cute pet turtle with a round patterned shell sunbathing on a rock in a small garden pond, with lily pads, a water lily flower, reeds, pebbles, a dragonfly and a smiling sun. |
| page_11 | Pony meadow | A cute pony with a fluffy mane and tail trotting through a meadow, with a barn, a wooden fence, hay bales, flowers, a horseshoe on the fence post and a cloud. |
| page_12 | Dachshund dig | A cute long dachshund puppy with short legs digging happily in a garden bed, with flowers, a garden shovel, a flower pot, a bone peeking from the soil, a butterfly and a bush. |
| page_13 | Corgi herding | A cute corgi puppy with big ears and short legs herding three little ducks across a farmyard, with a barn, a wooden fence, a duck pond, flowers and a cloud. |
| page_14 | Pug pillow | A cute pug with a wrinkly face and curly tail snoozing on a big round pillow, with a chew toy, a food bowl, a cozy blanket, a ball and a potted plant. |
| page_15 | Dalmatian firehouse | A cute dalmatian puppy with round spots sitting proudly beside a fire truck wearing a little firefighter helmet, with a fire hydrant, a coiled hose, a ladder, a bell and a cloud. |
| page_16 | Beagle sniff | A cute beagle with long floppy ears following a trail of paw prints through a garden with its nose to the ground, with flowers, a garden path, a tree, a bush, a butterfly and a cloud. |
| page_17 | Poodle pom-poms | A cute poodle with fluffy pom-pom fur standing proudly at a grooming station, with a hair dryer, a comb, a brush, a bow, a mirror on a stand and a spray bottle. |
| page_18 | Chihuahua tote | A cute tiny chihuahua with big ears peeking out of a round tote bag, with a sun hat, a pair of sunglasses, a water bottle, flowers, a park bench and a cloud. |
| page_19 | Cat nap | A cute cat curled up asleep on a round cushion on a rug, wearing a little sleeping cap, with a little mouse toy, a potted plant, a ball of yarn and a cozy blanket. |
| page_20 | Purring cat | A cute cat purring happily on a cozy armchair with its eyes closed, with a blanket, a ball of yarn, a lamp, a teacup on a side table, a cushion and a sleeping mouse toy. |
| page_21 | Cat landing | A cute cat landing on its four feet after a jump, with a bookshelf of rounded books, a toy mouse, a potted plant, a cushion, a feather toy and a rug. |
| page_22 | Kitten drink | A cute kitten lapping water from a bowl with its little tongue out, with a food bowl, a fish-shaped toy, a mat, a potted plant, a ball and a feather wand. |
| page_23 | Cat tree | A cute cat sitting at the top of a tall cat tree with round platforms, a dangling toy ball and a little cozy hideout, with another kitten climbing up, a potted plant and a scratching post. |
| page_24 | Kneading kitten | A cute kitten kneading a fluffy blanket with its front paws and a happy face, with a pillow, a ball of yarn, a mouse toy, a potted plant and a cozy basket. |
| page_25 | Bunny ears | A cute bunny rabbit standing up on its back legs with its long ears turned to listen, in a vegetable garden with lettuce, carrots, cabbages, a watering can, a butterfly and flowers. |
| page_26 | Bunny hay | A cute bunny rabbit munching a big mouthful of hay from a hay pile, with a carrot, a little wooden hideout, a food bowl, a water bottle on a stand and a few dandelions. |
| page_27 | Hamster wheel | A cute hamster running fast on a round exercise wheel with a happy face, with a little wooden house, a seed bowl, a tunnel tube, a water bottle on a stand and bedding shavings. |
| page_28 | Guinea pig chat | Two cute guinea pigs squeaking happily at each other with their mouths open, sharing a pile of veggies with a carrot, a pepper, lettuce leaves and a cucumber, with hay and a hideout. |
| page_29 | Budgie bell | A cute budgie bird with a round chest perched on a swing, ringing a little bell with its beak, with a mirror on a stand, a seed bowl, a millet spray, a ladder toy and a potted plant. |
| page_30 | Tortoise strawberry | A cute tortoise with a big dome shell munching a strawberry in a garden, with strawberry plants, leaves, a flat stepping stone, a snail friend, flowers and a smiling sun. |
| page_31 | Hedgehog garden | A cute hedgehog curled up into a round prickly ball with only its happy face peeking out, sitting in a garden, with mushrooms, an acorn, a log, a flower, a snail and a butterfly. |
| page_32 | Crested gecko | A cute crested gecko with big round eyes and a little crest above its eyes licking its eye with its tongue, sitting on a leafy branch with big leaves, a small rock, a fern and a water dish. |
| page_33 | Axolotl | A cute axolotl with feathery gills on both sides of its head smiling in a pond, with water plants, pebbles, bubbles, a smooth rock, a little shell and floating leaves. |
| page_34 | Ferret dooking | A cute ferret hopping sideways with a happy open mouth near a play tunnel, with a ball, a hammock, a toy mouse, a round dish and a soft blanket. |
| page_35 | Chinchilla dust bath | A cute fluffy chinchilla rolling happily in a round bowl of dust with puffs of dust around it, with a wooden ledge, a hay pile, a chew stick, a food bowl and a small hideout. |
| page_36 | Pony nap | A cute pony dozing while standing up in a stable yard with its eyes closed and a peaceful smile, with a hay net, a water bucket, a wooden fence, a crescent moon, stars and a sleeping cat friend on the fence. |
| page_37 | Best friends | A cute puppy and a cute kitten cuddled up together in one round basket, both smiling, with a blanket, a ball, a yarn ball, a bone toy, a pillow and a potted plant. |
| page_38 | Vet check-up | A cute puppy sitting on a vet's check-up table with a bandage on one paw and a brave smile, with a stethoscope, a bone-shaped treat, a teddy bear, a bandage roll and a kitten waiting on a chair. |
| page_39 | Puppy walk | A cute puppy dog carrying its own leash in its mouth on a park path, with a tree, a lamp post, a park bench, flowers, a fire hydrant and a cloud. |
| page_40 | Puppy teething | A cute puppy chewing on a squeaky toy bone with its baby teeth, lying on a rug with a chewed slipper, a rope toy, a ball, a round dish and a cushion. |
| page_41 | Pet birthday | A cute puppy in a party hat at a pet birthday party with a bone-shaped cake with candles, a kitten friend in a party hat, balloons, wrapped presents and streamers. |
| page_42 | Newborn kittens | Three tiny cute newborn kittens snuggled with their eyes still closed next to their smiling mother cat in a round basket, with a blanket, a pillow and a yarn ball. |
| page_43 | Buried bone | A cute puppy dog burying a big bone in a garden hole with its paws, with a garden shovel, flowers, a flower pot, a doghouse in the background, a butterfly and a cloud. |
| page_44 | Cat and fish | A cute cat sitting beside a round fishbowl on a small round table, watching a little pet fish with wide curious eyes and one paw lifted, with a water plant and pebbles in the bowl, a potted plant, a ball of yarn and a cushion. |
| page_45 | Bunny teeth | A cute bunny rabbit with two big front teeth chewing on a wooden chew stick, sitting on soft grass with dandelions, a carrot, an apple slice, a clover patch and a butterfly. |
| page_46 | Puppy pool | A cute labrador puppy dog paddling in a round wading pool with a happy splash, with a beach ball, a rubber duck, a sun umbrella, a towel, a bucket and a smiling sun. |
| page_47 | Betta bubbles | A cute betta fish with long flowing fins and tail blowing a cluster of bubbles at the top of the water in a round bowl, with a water plant, a floating leaf, pebbles and a small ornament rock. |
| page_48 | Cockatiel crest | A cute cockatiel bird with a tall curly crest on its head raised in excitement, perched on a branch, with round cheeks, a millet spray, a seed bowl, a bell toy and leaves. |
| page_49 | Pet sleepover | A cute puppy, kitten and bunny sleeping together in a big pile of pillows and blankets with peaceful smiles, with a crescent moon, stars, a teddy bear and a night light. |
| page_50 | Pawsome Cuties party | A cute puppy, kitten, bunny, hamster and parrot having a happy pet party together, with balloons, a cake, wrapped presents, a ball, streamers and a yarn ball. |
