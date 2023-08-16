# A Python programming experiment with ChatGPT

Scot W. Stevenson
This version: 2023-08-16

> **This code is not intended for actual use.** It was generated as a learning
> experience. If you use it, you not only do so at your own risk, but are
> probably a fool. 

This is an experiment to see how ChatGPT can be used to create Python programs.
The problem was to take images generated by A1111 Version 1.5.1 of Stable
Diffusion XL, which contain meta-data as part of the PNG files, and create a
"benchmark" (an overview with thumbnails) for various combinations of artists
and image prompts. 

To do this, a few image files were generated. ChatGPT 4.0 was then provided with
a prompt describing the desired output and giving suggestions for the tools to
use. This original prompt is included here. The first output of the program,
which produces a PDF, was then interactively debugged. Using this as a base,
versions for HTML and Excel were generated interactively. 

The HTML version was then further refined in a dialog with ChatGPT to add
command line parameters for verbose and the output file as well as take care of
some error conditions when the parsing of the PNG metadata fails. No attempt was
made to correct all errors. 

Then, a second prompt was used to ask ChatGPT to rewrite the HTML version of the
program in a "simpler" form that just lists the pictures of the artists in rows.
The prompts was included to a pop-up that appears when the user clicks
on a thumbnail. Again, the first output of the program was refined in a dialog
with ChatGPT. Also again, no attempt was made to find all errors. 

## The bad

The original version of the code that the prompt produced was not functional.

* The subprocess call to the ImageMagick `identify` program was missing single
  quotation marks (`identify -format '%[parameters]' ./<FILE NAME>`)

* The parsing of the artist's name did not work at all initially (and is still
  very fragile in the hand-corrected version).

* The location of the `identify` program was hardcoded. Since this was with
  homebrew on a Mac with macOS, it lives in `/opt` and not `/usr/bin.` I had not
  specified homebrew and macOS, so this is on me.

* I had requested the code to produce today's date in the ISO format. The
  machine does use the variable name `date`, but returns the name of the folder
  instead.

* The AI tends to use "magic numbers" in the text instead of defining constants
  at the beginning and referring to them. However, after I had made these
  changes per hand, it made use of the constant. 

* The "simple" rewrite first attempted to create a pop-up that was immediately
  blocked by the web browser.


## The good

* Excluding the time it took to generate the images themselves (and a multi-hour
  break to play _7 Days to Die_ with my son), I had functional programs for PDF,
  HTML, and Excel in about four hours. As I was unfamiliar with the
  libraries for PDFs and Excel, there is no way I would have been able to
  produce a program with these functions in this time frame without the AI.

* The rewrite to the "simple" version was most impressive and only took minutes,
  including the time to fix the pop-up issue. I would not have been able to type
  in the code this fast even if I had known exactly what to write. 

* The machine does not make typos or indentation errors. 

* Though the AI made mistakes, it responded extremely well to feedback and
  immediately came up with working suggestions. When I did copy and paste
  things by hand and made indentation errors, it figured _that_ out immediately
  from the cryptic output.


## Learning points

This was a very simple example. If this were to be a tool that I would use all
the time, I would want to have a single program where I pass on the desired
output format as a parameter. This would be the next step to try.

* A longer, detailed, and specific prompt will get you far towards a functional
  program. 

* Simple HTML outputs can be defined by ASCII art.

* The AI definitely makes mistakes even when instructions to the contrary were
  given (as with the date here). This confirms the suggestion to think of the AI
  as a "slightly distracted" helper, such as an assistant who keeps looking at
  their mobile phone instead of paying attention.

* The recommendation not to look for the perfect prompt is confirmed. Though
  the prompts were good starting points, development worked best
  as a "dialogue" with the AI that produced into incremental
  corrections and additions to the code.

* For production level code, the AI generated-version would need to be
  rewritten in some places. 

Note that I did not ask the AI to produce test routines.


## Requirements

Various Libraries might need to be installed depending on your system, for
instance 

``` 
pip install fpdf pillow
``` 

Test prompts: 
* a cute female elf reading a book in a magic library
* an orc and an elf drinking at a marble fountain
* a happy party of beautiful elves in the forest at night

Common negative prompt: 
* nude, nsfw 

Artists:
* Alphonse Mucha
* Edouard Manet
* Pieter Bruegel the Elder
* Rembrandt
* William-Aldophe Bouguereau

Not all combinations were included to force the machine to deal with empty
cells.

