# Author 2 Book 3: "Robot Wonders": Page-by-Page Generation Instructions (50 pages)

> House: Wattle Wonders Publishing / pen Flora Watt. Lane A. Bold & easy thick-line interiors,
> 10-14 elements per scene, art fills a bigger area (fit 2400x2700), fun fact on every page,
> captions in Fredoka. Engine: batch_generate_a2.py. OpenArt CLI / nano-banana-2 for pages.
> Title locked: "Robot Wonders" (validation: publishing\07-validation-robots.md).
> Mix: real robot types + friendly invented helpers; facts are about real robotics. Nothing scary or violent.

## Universal prompt suffix (LOCKED: append to EVERY scene prompt)

```
Bold and easy coloring book page. A rich, detailed but simple scene with 10 to 14 easy elements arranged to fill the whole page around the main character (things that belong in the scene's setting, plus at most two small gears and a few sparkles), all part of one connected scene, never a border of separate stickers or icons around the edge, each element drawn as one big simple closed shape. The composition fills almost the entire page. Whole scene floats with a plain white margin on every side; no element touches the image edges. Absolutely no rectangular frame or box line anywhere; do not draw a border. Very thick, clean, smooth black outlines (heavy, marker-friendly), pure black on plain white only. Only simple closed shapes with large open areas to color. The main character stays the largest thing on the page, portrait composition. Cute, friendly, happy faces with large simple eyes. No shading, no grey, no color fill, no texture, no crosshatching. No words, letters, numbers or text anywhere in the image. Nothing in the bottom 6 percent of the page.
```

## Failure modes: F1-F11 per AGENT-PIPELINE.md; F9 coherence audit runs after every typeset.

## The 50 pages

| File | Page | Scene prompt (prepend nothing, append suffix) |
|---|---|---|
| page_01 | Mars rover | A cute six-wheeled Mars rover with a camera head and a happy face rolling over bumpy rocks, a small drill arm reaching to a rock, surrounded by Mars hills, craters, two small moons, stars, a smiling sun and a tiny helicopter friend. |
| page_02 | Mars helicopter | A cute little helicopter with two long spinning blades and four thin legs flying above Mars with a happy face, the rover friend waving below, surrounded by rocky hills, rocks, craters, stars and a smiling sun. Shown as one rounded floating vignette with plenty of white space all around; no walls, floor, water or ground reaching the page edges. |
| page_03 | Moon rover | A cute round-topped Moon rover with eight wheels and a happy face driving across the Moon, wheel tracks behind it, surrounded by craters, the Earth in the sky, stars, a flag pole and moon rocks. |
| page_04 | Station arm | A cute long bendy robot arm on the space station gently holding a big round cargo pod with a happy face on its hand, surrounded by the space station, solar panels, the Earth below, stars and a floating astronaut waving. |
| page_05 | Robot vacuum | A cute round robot vacuum with a happy face rolling across a floor and stopping at the top of the stairs, little sensor sparkles at its front, surrounded by a rug, a sock, a ball, a cat on a cushion, a plant and a lamp. |
| page_06 | Robot lawn mower | A cute robot lawn mower with a happy face trimming grass in neat stripes, a thin boundary wire around the lawn, surrounded by flowers, a garden gnome, a tree, a fence, a smiling sun and clouds. |
| page_07 | Factory arm | A cute big factory robot arm with a happy face building a toy car on a moving belt, a crescent moon and a sun both in the window, surrounded by gears, bolts, toy cars, a light bulb and tools. |
| page_08 | Robot dog | A cute four-legged robot dog with a happy face climbing a short staircase and pressing a door handle with its arm, surrounded by a door, a ball, a bone shape, a plant, a smiling sun and sparkles. Shown as one rounded floating vignette with plenty of white space all around; no walls, floor, water or ground reaching the page edges. |
| page_09 | Underwater robot | A cute submarine-shaped underwater robot with lights and a happy face exploring the deep sea, surrounded by fish, a jellyfish, coral, bubbles, a treasure chest, seaweed and a whale far away. Shown as one rounded floating vignette with plenty of white space all around; no walls, floor, water or ground reaching the page edges. |
| page_10 | Deep-sea explorer | A cute deep-sea robot with a bright lamp and a happy face diving down past layers of the ocean, surrounded by glowing anglerfish, bubbles, a squid, a crab on the sea floor, rocks and seaweed. |
| page_11 | Farm robot | A cute farm robot with a basket and gentle gripper hands picking strawberries with a happy face, surrounded by strawberry plants, a weed being pulled, a scarecrow, a barn, a smiling sun and clouds. |
| page_12 | Milking robot | A cute milking robot station with a happy face and a happy cow walking in by herself, surrounded by a milk bucket, hay bales, a barn, a fence, a smiling sun and a little chicken. |
| page_13 | Delivery robot | A cute six-wheeled delivery robot with a parcel box on top and a happy face rolling along a sidewalk, surrounded by houses, a tree, a letterbox, a dog waving, a smiling sun and clouds. |
| page_14 | Warehouse robot | A cute flat warehouse robot with a happy face carrying a whole tall shelf of boxes on its back, surrounded by boxes, a conveyor belt, a worker waving, gears, light bulbs and stars. Shown as one rounded floating vignette with plenty of white space all around; no walls, floor, water or ground reaching the page edges. |
| page_15 | Surgery robot | A cute hospital robot with four careful arms and a happy face helping a doctor, a teddy bear patient smiling on a bed, surrounded by a heart monitor, a bandage, a stethoscope, a plant and stars. |
| page_16 | Firefighting robot | A cute tank-tracked firefighting robot with a water hose and a happy face spraying water at a small campfire-style flame, surrounded by a fire truck, a firefighter waving, buckets, clouds and a smiling sun. |
| page_17 | Rescue snake robot | A cute snake-like rescue robot made of round segments with a camera head and a happy face wriggling through a pile of rocks, surrounded by bricks, a rescue helmet, a dog with a vest, stars and a smiling sun. Shown as one rounded floating vignette with plenty of white space all around; no walls, floor, water or ground reaching the page edges. |
| page_18 | Solar panel cleaner | A cute robot with a soft brush and a happy face cleaning a row of solar panels in the desert, surrounded by sand dunes, a cactus, the smiling sun, clouds and sparkles. |
| page_19 | Pool robot | A cute pool cleaning robot with a happy face climbing up the wall of a swimming pool, surrounded by water ripples, a rubber duck, a pool ladder, a beach ball, a smiling sun and bubbles. |
| page_20 | Humanoid robot | A cute friendly humanoid robot shaped like a person with a round head, arms and legs, waving hello with a happy face, surrounded by gears, stars, light bulbs, a smiling sun and two tiny robot friends. |
| page_21 | Backflip robot | A cute two-legged robot doing a backflip in the air with a happy face, motion arcs around it, surrounded by a soft mat, cones, a trophy, stars, sparkles and a smiling sun. |
| page_22 | Robot hand | A cute big robot hand with a happy face on its palm gently holding an egg without cracking it, surrounded by eggs in a carton, a feather, gears, sparkles and a smiling sun. |
| page_23 | Kitchen robot | A cute kitchen robot with a chef hat and a happy face flipping a burger on a grill and sliding a pizza out of an oven, surrounded by plates, a salad bowl, a spatula, sparkles and steam swirls. |
| page_24 | What is a robot | A cute robot thinking with a light bulb above its head and a happy face, holding a magnifying glass, surrounded by gears, a brain-shaped computer chip, an eye-shaped sensor, wheels, stars and sparkles. |
| page_25 | Robot band | A cute robot band: one robot playing the piano, one on drums and one blowing a trumpet, all with happy faces, surrounded by music notes, a stage, lights, stars and a smiling sun. |
| page_26 | Robot artist | A cute robot artist with a beret and a happy face painting a sunflower picture with a real brush on an easel, surrounded by paint pots, brushes, a palette, a vase of sunflowers and sparkles. |
| page_27 | Robot pet | A cute round robot puppy pet wagging its tail with a happy face while a child pats it, surrounded by a cushion, a ball, a bone, a toy box, hearts and a smiling sun. |
| page_28 | Hard work | A cute strong robot happily lifting a big pile of boxes with a happy face, a tiny robot helper cheering, surrounded by a cart, bricks, tools, gears, a smiling sun and clouds. |
| page_29 | School robots | Cute kids at a school table building and coding a small wheeled robot with a happy face, surrounded by a laptop, building blocks, wires, a lightning bolt, books and stars. |
| page_30 | Line follower | A cute small robot car with a happy face following a curvy black line drawn on the floor with its light sensors, surrounded by cones, a finish flag, gears, stars and sparkles. |
| page_31 | Solar robot | A cute outdoor robot with solar panels on its back like wings and a happy face soaking up sunshine, surrounded by the big smiling sun, flowers, a tree, clouds and sparkles. |
| page_32 | Charging dock | A cute sleepy robot vacuum with a happy face driving back to its charging dock, a battery icon shape glowing, surrounded by a couch, a rug, a lamp, a plant, a crescent moon in the window and stars. |
| page_33 | Self-driving tractor | A cute self-driving tractor with a happy face and no driver plowing a huge farm field, surrounded by crop rows, a windmill, a farmhouse, hay bales, a smiling sun and clouds. |
| page_34 | Drone | A cute four-rotor drone with a camera and a happy face flying above a park taking a photo, surrounded by trees, a kite, birds, a lake, a smiling sun and clouds. |
| page_35 | Robot mine truck | A cute giant robot mine truck with huge wheels and a happy face carrying a big pile of rocks in the Australian outback, surrounded by rocky hills, a kangaroo, gum trees, a smiling sun and clouds. |
| page_36 | Reef robot | A cute underwater reef robot with a happy face swimming over the Great Barrier Reef, a crown-of-thorns starfish nearby, surrounded by coral, a turtle, clownfish, bubbles and seaweed. |
| page_37 | Satellite helper | A cute space robot with a happy face docking with an old satellite to help it keep working, surrounded by the Earth, stars, solar panels, a moon and sparkles. |
| page_38 | Voyager | A cute Voyager space probe with a big dish antenna and a happy face flying far away past all the planets, surrounded by Saturn with rings, Jupiter, Neptune, stars and comets. |
| page_39 | Comet lander | A cute three-legged robot lander with a happy face landing on a bumpy comet, surrounded by comet dust, rocks, a mother spacecraft above, stars and a smiling sun. |
| page_40 | Driverless train | A cute driverless metro train with a happy face gliding along a track past a city with no driver on board, surrounded by a station, buildings, a bridge, passengers waving, a smiling sun and clouds. |
| page_41 | Hospital helper | A cute tall hospital delivery robot with a happy face carrying meals and medicine down a corridor, surrounded by doors, a nurse waving, a flower vase, balloons and stars. Shown as one rounded floating vignette with plenty of white space all around; no walls, floor, water or ground reaching the page edges. |
| page_42 | Robot penguin | A cute little robot penguin chick on wheels with a happy face rolling among real penguins on the ice, surrounded by penguins, icebergs, snowflakes, a fish and a smiling sun. |
| page_43 | Robot fish | A cute robot fish with a happy face swimming with a school of real fish, surrounded by bubbles, coral, seaweed, a starfish, a shell and gentle waves. |
| page_44 | Robot bee | A cute tiny flying robot bee with clear wings and a happy face visiting a flower beside a real bee, surrounded by flowers, a beehive, leaves, a smiling sun and sparkles. |
| page_45 | Recycling robot | A cute recycling robot with camera eyes and a happy face sorting plastic bottles and paper into the right bins, surrounded by recycling bins, cans, boxes, a tree, a smiling sun and sparkles. |
| page_46 | Cube solver | A cute robot with fast arms and a happy face solving a puzzle cube in a blur of motion lines, surrounded by puzzle pieces, a stopwatch, a trophy, stars and sparkles. |
| page_47 | Robot soccer | Cute small robots with happy faces playing soccer on a field, one kicking the ball toward a goal, surrounded by a goal net, a scoreboard shape, flags, a trophy, a smiling sun and clouds. |
| page_48 | Museum guide | A cute friendly museum guide robot with a happy face showing a dinosaur skeleton to children, surrounded by paintings, a vase, a rope barrier, footprints, stars and sparkles. |
| page_49 | Robot parts | A cute robot standing proudly with its parts shown around it: eye sensors, a computer brain, motors, wheels and a battery, all with happy faces, surrounded by gears, bolts and stars. |
| page_50 | Robot party | A happy robot party: a robot vacuum, a robot dog, a humanoid robot and a drone dancing around a table with a cake and balloons, surrounded by bunting, music notes, gears, stars and a smiling sun. |
