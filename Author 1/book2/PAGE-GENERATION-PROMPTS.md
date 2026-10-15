# Book 2 — Great Barrier Reef Ocean Friends — Page-by-Page Generation Instructions (50 pages)

> Same pipeline as Book 1 (AGENT-PIPELINE.md v2.0). OpenArt CLI / nano-banana-2 only.
> Run each prompt, save output as `raw2/page_XX.png`. Engine: `batch_generate.py` in this folder.
> Species realism note: GBR-native heroes only (validation doc publishing/04-validation-reef-ocean.md).

## Universal prompt suffix (LOCKED — includes F2/F3 mandatory phrases; append to EVERY scene prompt)

```
Bold and easy coloring book page for kids ages 3-8. A rich but simple scene around the animal with 6 to 8 easy elements suitable for its habitat (coral, sea anemones, seaweed, bubbles, starfish, shells, waves, sun rays, smaller fish friends), each element drawn as one big simple closed shape. Whole scene floats with a generous plain white margin on every side; no element touches the image edges. Absolutely no rectangular frame or box line anywhere; do not draw a border. Very thick, clean, smooth black outlines (heavy, marker-friendly), pure black on plain white only. Only simple closed shapes with large open areas to colour. The main animal stays the largest thing on the page, portrait composition. Cute, friendly, happy faces with large simple eyes. No shading, no grey, no colour fill, no texture, no crosshatching. No words, letters, numbers or text anywhere in the image. Nothing in the bottom 6 percent of the page.
```

## Known failure modes — CHECK EVERY OUTPUT (F1–F8, see PRODUCTION-STANDARD.md in book1)

F1 colour fill · F2 drawn frame · F3 edge-touch · F4 stretch · F5 caption clip · F6 drift · F7 throttle · F8 OneDrive lock. Automated audit runs after every batch; regen per retry policy (max 2 regens, then simplify scene).

## The 50 pages

| File | Page | Scene prompt (prepend nothing, append suffix) |
|---|---|---|
| page_01 | Clownfish home | A cute cartoon clownfish swimming beside a big rounded sea anemone with fat short tentacle tubes, round bubbles rising above, two simple coral blobs below. |
| page_02 | Clownfish peek | A cute clownfish peeking out from the middle of a big sea anemone with soft tube tentacles, happy open mouth, three round bubbles and one starfish nearby. |
| page_03 | Sea turtle swim | A cute green sea turtle gliding with big rounded flippers and a dome shell with simple hexagon patches, wavy seaweed below, round bubbles around. |
| page_04 | Turtle snack | A cute sea turtle munching a long strand of seagrass, eyes closed happily, a small round sponge and two coral blobs beside it, bubbles above. |
| page_05 | Maori wrasse | A cute chubby maori wrasse with big friendly lips and swirly line patterns on its round body, waving pectoral fin, coral arch behind, bubbles. |
| page_06 | Wrasse greets diver fin | A cute maori wrasse smiling wide at a small floating bubble cluster shaped like a heart, two coral mounds and a starfish on the sandy bottom. |
| page_07 | Manta ray glide | A cute manta ray gliding with huge wide wings curved like a blanket, two little horn fins on its face, smiling, tiny fish friends below, bubbles. |
| page_08 | Manta ray loop | A cute manta ray doing a happy somersault loop with wing tips curled, trail of round bubbles behind, sun rays beaming from above. |
| page_09 | Reef shark cruise | A cute blacktip reef shark with a rounded body and tall dorsal fin tipped in solid black, smiling, swimming over three coral blobs, bubbles around. |
| page_10 | Shark friends | A cute small reef shark playing with two tiny fish friends, a big rounded coral head and swaying seaweed nearby, bubbles above. |
| page_11 | Parrotfish beak | A cute round parrotfish with a beak-like smile and one big tail fin, nibbling a small round coral lump, sand speckles as simple dots, bubbles. |
| page_12 | Parrotfish sleep sack | A cute sleepy parrotfish wrapped in a soft blanket shape of goo, eyes closed, floating beside a coral pillow mound, one small starfish below. |
| page_13 | Blue tang dart | A cute blue tang fish with a round body, big tail fan and swirl markings, darting between two tall coral towers, bubbles trailing. |
| page_14 | Tang scalpel tail | A cute blue tang showing off its tail fin with a small scalpel shape on it, a friendly tiny fish watching, anemone blob and shells below. |
| page_15 | Butterflyfish pair | Two cute butterflyfish swimming nose to nose like a heart, each with a tall stripe and a big fake eyespot near the tail, coral arch behind, bubbles. |
| page_16 | Butterflyfish snack | A cute butterflyfish nibbling a little polyp circle on a big rounded coral head, one small friend fish beside, wavy seaweed below. |
| page_17 | Seahorse hold | A cute seahorse with a curly tail wrapped around a strand of seagrass, snout like a little tube, round belly, bubbles and two coral blobs below. |
| page_18 | Seahorse dance | Two cute seahorses curling tails together like a dance, floating above a rounded sponge and shells, round bubbles rising. |
| page_19 | Giant clam smile | A cute giant clam with a big wavy open shell and soft lips smiling, sitting on the sandy bottom, two small fish friends peeking inside, bubbles. |
| page_20 | Clam pearl | A cute giant clam showing a big round pearl on its soft tongue, proud happy face, starfish and shells around the sandy bottom. |
| page_21 | Octopus hide | A cute octopus with a round head and six wavy arms peeking out of a rounded coral cave, one arm waving hello, bubbles above. |
| page_22 | Octopus disguise | A cute octopus changing its skin into simple polka-dot circles, sitting on the sandy bottom beside a shell and seaweed, surprised tiny fish watching. |
| page_23 | Jellyfish float | A cute jellyfish with a dome bell and four wavy ribbon arms floating up, three round bubbles and sun rays above, seaweed tips below. |
| page_24 | Jellyfish glow | A cute jellyfish at night surrounded by tiny star shapes and a crescent moon, soft glow lines around its dome, wavy water line above. |
| page_25 | Starfish stretch | A cute starfish with five rounded arms and a happy smile lying on the sandy bottom, two shells and a small coral mound beside it. |
| page_26 | Starfish regrow | A cute starfish waving with one brand new smaller arm, a tiny fish friend clapping its fins, round bubbles and seaweed nearby. |
| page_27 | Hermit crab home | A cute hermit crab with a big swirl shell house and tiny claws peeking out, walking beside two coral blobs and a round pebble, bubbles. |
| page_28 | Crab moving day | A cute hermit crab climbing into a bigger empty swirl shell, tiny claws waving goodbye to the small old shell behind it, one starfish cheering, shells scattered. |
| page_29 | Moray eel peek | A cute moray eel with a long wavy body peeking out of a rounded rock cave, big friendly eye and open smile, seaweed fringe on the rock, bubbles. |
| page_30 | Eel yawn | A cute moray eel doing a big open-mouth yawn on the sandy bottom, tiny fish friend surprised beside it, two shells and a coral blob. |
| page_31 | Dolphin leap | A cute bottlenose dolphin leaping in a happy arc over a rounded wave, round water droplets flying, sun rays and clouds above. |
| page_32 | Dolphin whistle | A cute dolphin smiling with round sound-wave swirls coming from its blowhole, small fish friend listening, seaweed and coral below. |
| page_33 | Dugong graze | A cute chubby dugong with a big round snout munching a seagrass meadow, round belly resting on the sand, two small fish friends above. |
| page_34 | Dugong surfacing | A cute dugong rising to the surface to breathe, little snout above a rounded wave line, sun rays above, seagrass blades below. |
| page_35 | Whale breach | A cute humpback whale breaching with knobbly head bumps and long wavy fins, big splash crown under it, clouds and sun rays above. |
| page_36 | Whale song | A cute humpback whale singing, musical swirl lines floating from its mouth, tiny fish friends listening near a coral tower below. |
| page_37 | Crocodile float | A cute saltwater crocodile floating calmly with big rounded scutes on its back, friendly smile, reeds and a round log at the river edge. |
| page_38 | Croc mum & bubs | A cute mother crocodile carrying three tiny smiling baby crocs on her snout, gentle eyes, round river pebbles and reeds below. |
| page_39 | Lionfish fan | A cute lionfish with big fanned spiky fins drawn as simple thick rays, proud smile, hovering above a coral mound, bubbles around. |
| page_40 | Lionfish spit jet | A cute lionfish blowing a round jet of water bubbles at a tiny surprised fish, coral arch and seaweed behind. |
| page_41 | Emperor angelfish | A cute emperor angelfish with bold curved stripes and a little crown shape on its head, tall dorsal fin, swimming past two coral towers. |
| page_42 | Angelfish zoom | A cute young angelfish with simple swirly rings instead of stripes zooming forward with speed lines as thin closed arcs, bubbles trailing. |
| page_43 | Cleaner shrimp station | A cute cleaner shrimp with long thin wavy antennae and round body waving at a big happy fish visitor, coral signpost blob behind, bubbles. |
| page_44 | Shrimp dance | A cute cleaner shrimp doing a happy wiggle dance, tiny music swirls nearby, big fish friend smiling with open mouth, seaweed below. |
| page_45 | Leafy sea dragon | A cute leafy sea dragon with leaf shapes growing along its curved body, floating like seaweed in disguise, round bubbles and seaweed around. |
| page_46 | Cuttlefish blink | A cute cuttlefish with big W-shaped eyes and a wavy side fin, skin showing two big polka dots, hovering over a rounded coral head. |
| page_47 | Coral trout team-up | A cute coral trout with round spots pointing at a tiny fish hiding spot while a friendly octopus watches, two coral mounds and sand dots. |
| page_48 | Brain coral garden | A big round brain coral with wavy groove lines smiling, surrounded by three simple coral blobs, a starfish, shells and rising bubbles. |
| page_49 | Sea eagle dive | A cute white-bellied sea eagle with wide wings and a hooked beak swooping over a rounded wave, round splash droplets, fish friend below. |
| page_50 | Hatchling moon race | A cute baby sea turtle with tiny flippers racing across the sandy beach toward a rounded wave, crescent moon and stars above, one shell beside. |
