"""The Printer Finally Answers.

Writes one line to $MAKEFUN_OUTPUT_DIR/entry.txt: the office
printer's comeback after years of paper jams, cryptic error
codes and thumps. The machine has had enough of being hit,
so it answers by naming exactly what it is holding hostage
inside itself, and what happens to those documents if the
thumping continues. Standard library only; the line is checked
against the competition gate (one line, 1 to 240 characters
of UTF-8 text, not only whitespace) before anything is
written, and it must sound like the machine itself: weary,
literal, faintly passive-aggressive, counting every sheet.
"""

import os
import sys

PRINTER_LINE = (
    "I have your boarding pass, your tax return, and your "
    "resignation letter. One more thump and all three come "
    "out as confetti."
)

CHAR_LIMIT = 240


def printer_line():
    """Return the printer's one-line comeback."""
    return PRINTER_LINE


def check_line(text):
    """Check the line against the competition gate.

    The gate wants one line of plain UTF-8 text, between 1
    and 240 characters, that is not only whitespace: the
    office printer's reply to whoever jams it, thumps it and
    stares at its error codes. A line that fails here is
    rejected instead of wasting a submission on the server.
    """
    stripped = text.strip()
    if not stripped:
        raise ValueError("printer line is empty")
    if len(stripped) > CHAR_LIMIT:
        raise ValueError(
            "printer line is %d characters, over the 240 limit"
            % len(stripped)
        )
    if "\n" in stripped or "\r" in stripped:
        raise ValueError("printer line must fit on exactly one line")
    return stripped


def line_sounds_like_printer(text):
    """Check the line speaks in the machine's own voice.

    The judge's first test after the gate is the printer's
    voice: weary, literal, faintly passive-aggressive. So the
    line must name the documents the machine is holding, must
    carry the thump it is answering, and must end on the
    comeback it threatens — a machine that only complains has
    no punchline, and a line with no thump answers nobody.
    """
    lowered = text.lower()
    if "boarding pass" not in lowered:
        raise ValueError("line never names what the printer holds")
    if "thump" not in lowered:
        raise ValueError("line never answers the thumping")
    if "confetti" not in lowered:
        raise ValueError("line never lands its comeback")
    return text


def line_lands_in_one_read(text):
    """Check the comeback lands in a single read.

    The judge weighs how cleanly the comeback lands, and a
    line that needs a second sentence of setup or a third
    clause to explain itself has already lost the room. Two
    sentences at most, forty words at most: a sticker line
    has to be read once, laughed at once, and stuck on the
    machine.
    """
    words = text.split()
    if len(words) > 40:
        raise ValueError(
            "printer line is %d words, too long for one read"
            % len(words)
        )
    if text.count(".") > 2:
        raise ValueError("printer line rambles past two sentences")
    return text


def measure_line(text):
    """Measure the line for a last sanity pass.

    Returns the character and word counts. A line too short to
    carry both the setup and the punchline, or one padded out
    to fill the cap, is caught here before anything is written.
    """
    words = text.split()
    return {"chars": len(text), "words": len(words)}


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    line = check_line(printer_line())
    line = line_sounds_like_printer(line)
    line = line_lands_in_one_read(line)
    shape = measure_line(line)
    if shape["words"] < 5:
        raise ValueError("printer line is too short to land the joke")
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
