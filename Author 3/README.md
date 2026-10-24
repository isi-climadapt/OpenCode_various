# Author 3: illustrated story books (Hattie Moss / Saltbush Story House)

Third author line. A different product from Authors 1 and 2: illustrated picture
books with a recurring Australian animal character, modelled on the format and
approach of Alice Hemming's squirrel books (format and approach only, never her
text, characters, titles or art).

Folders:

- `publishing\`: competitor research, brand identity, validations
- `book1\`, `book2\`...: one book per folder
- `scripts\`: shared builders (interior, cover wrap, A+)

Rules that carry over from `AGENT-PIPELINE.md`: OpenArt CLI for all art, all
lettering typeset in code (never AI text), US primary market and US spelling in
customer-facing text (rule 13), no em dashes in any book text (rule 12), A+ set
with the # | Module | Image | Alt text table (rule 11), KDP print specs verified
before shipping. Colouring-only stages (line-art tracing, 108-page format,
caption rules) don't apply.

Hard rule 16 applies here too: the age band comes from the step 1 research (autocomplete demand,
bestsellers' reading ages, fit) and is the only band used in any customer-facing field. Book 1:
Ages 3-5 (`publishing\03-age-band.md`).

Barcode (pipeline F12): KDP prints it 2 x 1.2 in, 0.25 in from the spine fold and bottom trim
of the back cover. Copy `book1\create_cover_wrap.py` for new books: its `barcode_area()` and
`check_barcode()` place the white zone there and stop the build if anything covers it.

Hard rule 15 applies here too: build every stage from the latest layout, copying
scripts from Author 3's most recently changed book (check git log and git status
first), and port any newer layout before the next checkpoint.
Hard rule 17 (AGENT-PIPELINE.md): only two user approvals per book, the topic/theme pick and the front cover. Everything else, including credit spend, contact sheet, back cover, A+ and commit + push, runs without stopping.
