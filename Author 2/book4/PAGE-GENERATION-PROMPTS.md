# Author 2 Book 4: "Zoom Wonders": Page-by-Page Generation Instructions (50 pages)

> House: Wattle Wonders Publishing / pen Flora Watt. Lane A. Bold & easy thick-line interiors,
> 10-14 elements per scene, art fills a bigger area (fit 2400x2700), fun fact on every page,
> captions in Fredoka. Engine: batch_generate_a2.py (copied from book3). OpenArt CLI / nano-banana-2 for pages.
> Title: "Zoom Wonders" (validation: publishing\09-validation-zoom-wonders.md).
> Mix: land, sea, air and space vehicles, 8 of them Australian (road train, Melbourne tram, The Ghan,
> Sydney ferry, surf rescue boat, Murray River paddle steamer, Flying Doctor plane, water bomber).
> Every vehicle is a friendly character with a happy face. No logos, emblems or brand names. Nothing scary.

## Universal prompt suffix (LOCKED: append to EVERY scene prompt)

```
Bold and easy coloring book page. A rich, detailed but simple scene with 10 to 14 easy elements arranged to fill the whole page around the main vehicle (things that belong in the scene's setting, plus a few sparkles), all part of one connected scene, never a border of separate stickers or icons around the edge, each element drawn as one big simple closed shape. The composition fills almost the entire page. Whole scene floats with a plain white margin on every side; no element touches the image edges. Absolutely no rectangular frame or box line anywhere; do not draw a border. Very thick, clean, smooth black outlines (heavy, marker-friendly), pure black on plain white only. Only simple closed shapes with large open areas to color. The main vehicle stays the largest thing on the page, portrait composition. Cute, friendly, happy faces with large simple eyes. No shading, no grey, no color fill, no texture, no crosshatching. No words, letters, numbers, logos or symbols anywhere in the image. Nothing in the bottom 6 percent of the page.
```

## Failure modes: F1-F11 per AGENT-PIPELINE.md; F9 coherence audit runs after every typeset.

## The 50 pages

| File | Page | Scene prompt (prepend nothing, append suffix) |
|---|---|---|
| page_01 | Fire truck | A cute fire truck with a happy face and a tall ladder reaching up to rescue a kitten from a tree, a firefighter climbing the ladder, surrounded by a house, a fire hydrant, a hose, a dog, a smiling sun and clouds. |
| page_02 | School bus | A cute school bus with a happy face and a stop sign arm stopping to pick up smiling kids with backpacks, surrounded by a school building, a tree, a crossing guard, a smiling sun and clouds. |
| page_03 | Ambulance | A cute ambulance with one happy face on its front (no extra faces), plain sides with stripes and no cross or symbols, and a siren light on its roof driving to the hospital, a friendly paramedic waving, surrounded by a plain hospital building with round windows and no symbols on it, a stretcher, a tree, a smiling sun and clouds. |
| page_04 | Garbage truck | A cute garbage truck with a happy face lifting a trash can with its arm, surrounded by trash cans, a recycling bin, houses, a cat on a fence, a tree, a smiling sun and clouds. |
| page_05 | Tow truck | A cute tow truck with a happy face pulling a small car with a flat tire on its hook, the little car smiling too, surrounded by a road, traffic cones, a gas pump, a tree, a smiling sun and clouds. |
| page_06 | Ice cream truck | A cute ice cream truck with a happy face and a big cone on its roof, kids lining up for ice cream, surrounded by a park, a bench, a tree, music notes, a smiling sun and clouds. |
| page_07 | Monster truck | A cute monster truck with a happy face and huge chunky tires jumping over a dirt ramp, surrounded by dirt hills, flags, a crowd of smiling fans, stars, a smiling sun and clouds. |
| page_08 | Race car | A cute low race car with a happy face and a big wing on the back speeding around a curve on a racetrack, motion lines behind it, surrounded by tires, a checkered flag, cones, a trophy, a smiling sun and clouds. |
| page_09 | Semi truck | A cute big semi truck with a happy face and a long trailer driving down a highway with lots of wheels, surrounded by road signs, hills, trees, a bridge, a smiling sun and clouds. |
| page_10 | Road train | A cute Australian road train with a happy face pulling three long trailers across the red outback, surrounded by a kangaroo, gum trees, rocks, a windmill, a smiling sun and clouds. |
| page_11 | Car carrier | A cute car carrier truck with a happy face carrying smiling little cars on its top and bottom decks, surrounded by a road, trees, a town, a smiling sun and clouds. |
| page_12 | Electric car | A cute small electric car with a happy face plugged into a charging post with a cable, a lightning bolt shape above it, surrounded by a house, a tree, flowers, a smiling sun and clouds. |
| page_13 | Camper van | A cute camper van with a happy face parked at a campsite with its door open, surrounded by a tent, a campfire, a picnic table, trees, mountains, a crescent moon and stars. |
| page_14 | Tractor | A cute farm tractor with a happy face and giant back wheels driving through a muddy field, surrounded by a barn, a fence, hay bales, a cow, a chicken, a smiling sun and clouds. |
| page_15 | Combine harvester | A cute combine harvester with a happy face cutting a field of wheat with its spinning reel, surrounded by wheat stalks, a grain truck, a farmhouse, birds, a smiling sun and clouds. |
| page_16 | Excavator | A cute excavator with a happy face digging dirt with its bucket arm on a building site, surrounded by dirt piles, traffic cones, a hard hat, a fence, a smiling sun and clouds. |
| page_17 | Bulldozer | A cute bulldozer with a happy face and caterpillar tracks pushing a pile of dirt and rocks with its big flat blade, surrounded by rocks, cones, a dirt hill, a worker waving, a smiling sun and clouds. |
| page_18 | Dump truck | A cute dump truck with a happy face tipping its back up high to slide out a load of rocks, surrounded by a rock pile, cones, a shovel, a construction sign shape, a smiling sun and clouds. |
| page_19 | Cement mixer | A cute cement mixer truck with a happy face and a big round spinning drum pouring concrete down a chute, surrounded by bricks, a wheelbarrow, a worker with a trowel, cones, a smiling sun and clouds. |
| page_20 | Tower crane | A very tall cute tower crane with a happy face lifting a stack of building beams high above a new building, surrounded by the building frame, a worker waving, birds, a smiling sun and clouds. |
| page_21 | Road roller | A cute road roller with a happy face and a giant round front drum pressing a new road flat and smooth, surrounded by road cones, a road sign shape, a worker with a rake, a smiling sun and clouds. |
| page_22 | Snowplow | A cute snowplow truck with a happy face pushing snow off a road with its big front blade, surrounded by snowbanks, pine trees, a snowman, a house, snowflakes and clouds. |
| page_23 | Bicycle | A cute bicycle with a happy face and a basket of flowers being ridden by a smiling child with a helmet along a park path, surrounded by trees, a pond, ducks, a bench, a smiling sun and clouds. |
| page_24 | Motorcycle | A cute motorcycle with a happy face leaning into a curve on a winding road, a rider in a helmet on board, surrounded by hills, trees, a road sign shape, birds, a smiling sun and clouds. |
| page_25 | Melbourne tram | A cute old-style city tram with a happy face and a pole touching the wires above, rolling down a Melbourne street, surrounded by shops, a tram stop, people waving, a tree, a smiling sun and clouds. |
| page_26 | Steam train | A cute steam train with a happy face and big puffs of steam from its chimney pulling carriages over a bridge, surrounded by hills, trees, a river, a station, a smiling sun and clouds. |
| page_27 | Bullet train | A cute sleek bullet train with a happy face and a long pointy nose zooming past a snowy mountain, motion lines behind it, surrounded by blossom trees, a bridge, houses, a smiling sun and clouds. |
| page_28 | The Ghan | A cute long passenger train with a big round friendly front, one happy face on its front and many simple carriages traveling across the Australian desert, surrounded by camels, red sand dunes, rocky hills, desert plants, a smiling sun and clouds. |
| page_29 | Cable car | A cute San Francisco cable car with a happy face and open sides climbing a steep city hill, passengers holding on and waving, surrounded by houses, a bridge far away, a tree, a smiling sun and clouds. |
| page_30 | Tugboat | A cute little tugboat with a happy face pushing a giant ship into the harbor, surrounded by waves, a lighthouse, seagulls, a buoy, a smiling sun and clouds. |
| page_31 | Sailboat | A cute sailboat with a happy face and a big puffy sail gliding across the sea in the wind, surrounded by waves, a dolphin, seagulls, an island with a palm tree, a smiling sun and clouds. |
| page_32 | Submarine | A cute round submarine with a happy face, a periscope and round windows diving under the sea, surrounded by fish, bubbles, an octopus, seaweed, coral, a shell and a starfish. |
| page_33 | Sydney ferry | A cute harbor ferry boat with a happy face carrying waving passengers across Sydney Harbour, the Opera House and the Harbour Bridge behind, surrounded by waves, seagulls, a smiling sun and clouds. |
| page_34 | Hovercraft | A cute hovercraft with a happy face and a big fan on the back floating from the water up onto a sandy beach, surrounded by waves, splashes, a beach umbrella, a crab, a smiling sun and clouds. |
| page_35 | Surf rescue boat | A cute inflatable rubber rescue boat with a happy face bouncing over a wave with two lifesavers in caps, surrounded by waves, a surfboard, a flag on the beach, a lifesaver tower, a smiling sun and clouds. |
| page_36 | Container ship | A cute huge container ship with a happy face carrying stacks of big metal boxes across the ocean, surrounded by waves, a whale, seagulls, a port crane far away, a smiling sun and clouds. |
| page_37 | Paddle steamer | A cute old paddle steamer boat with a happy face, a tall chimney and a big paddle wheel on a river, surrounded by gum trees, a riverbank, pelicans, a jetty, a smiling sun and clouds. |
| page_38 | Icebreaker | A cute icebreaker ship with a happy face and a strong pointed front crunching through sea ice, surrounded by ice chunks, penguins, a seal, icebergs, snowflakes and clouds. |
| page_39 | Hot air balloon | A cute round hot air balloon with a happy face and a basket with two waving people floating over fields, surrounded by clouds, birds, other small balloons far away, hills, a smiling sun. |
| page_40 | Helicopter | A cute helicopter with a happy face and spinning blades hovering above a city park, surrounded by buildings, trees, a helipad circle, birds, a smiling sun and clouds. |
| page_41 | Jumbo jet | A cute big jumbo jet airplane with a happy face, round windows and four engines taking off from a runway, surrounded by an airport tower, clouds, birds, a smiling sun and a windsock. |
| page_42 | Flying Doctor plane | A cute small twin-propeller plane with a happy face landing on a dirt airstrip in the Australian outback, a doctor waving from the door, surrounded by a farmhouse, a windmill, a kangaroo, gum trees, a smiling sun and clouds. |
| page_43 | Seaplane | A cute seaplane with a happy face and two big floats instead of wheels landing on a calm lake, surrounded by splashes, a wooden dock, pine trees, mountains, ducks, a smiling sun and clouds. |
| page_44 | Glider | A cute long-winged glider with no engine and a happy face soaring high above hills, swirly lines of rising warm air under it, surrounded by clouds, birds, fields, a smiling sun. |
| page_45 | First airplane | A cute old-fashioned biplane with two sets of wings, a happy face and wooden propellers making its first flight over sand dunes, two smiling brothers cheering below, surrounded by grass, birds, a smiling sun and clouds. |
| page_46 | Water bomber | A cute water bomber plane with a happy face scooping water from a lake and spraying it over a small fire in the forest, surrounded by trees, splashes, mountains, clouds and a smiling sun. |
| page_47 | Blimp | A cute big blimp airship with a happy face and a small cabin underneath floating over a sports stadium, surrounded by clouds, birds, flags, a smiling sun. |
| page_48 | Rocket | A cute tall rocket with a happy face blasting off from a launch pad with big puffy clouds of smoke, surrounded by a launch tower, stars, the Moon, a planet with rings and sparkles. |
| page_49 | Space shuttle | A cute space shuttle shaped like a plane with big triangle wings, a tall tail fin and a happy face on its nose, rolling down a long runway with a small parachute open behind it after its trip to space, surrounded by the airport tower, clouds, a few stars and a smiling sun. |
| page_50 | Moon buggy | A cute open Moon buggy with a happy face and big wire wheels driven by two waving astronauts across the Moon, surrounded by craters, moon rocks, a flag pole, a lander, the Earth in the sky and stars. |
