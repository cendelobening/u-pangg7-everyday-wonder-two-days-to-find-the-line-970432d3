"""Everyday Wonder: one sentence that makes a small everyday moment strange.

The moment: the breath-held pause just before the kettle clicks off.
The tilt: the water is not merely heating -- it is weighing whether to
stay water or become weather.
"""

import os
import stat
import tempfile

SENTENCE = (
    "For one held breath before the kettle clicks, the water seems to weigh "
    "staying water against becoming weather."
)

MAX_CHARS = 200


def main():
    sentence = SENTENCE
    if not 1 <= len(sentence) <= MAX_CHARS:
        raise SystemExit("sentence length %d outside 1..%d" % (len(sentence), MAX_CHARS))
    if sentence != sentence.strip() or "\n" in sentence or "\r" in sentence:
        raise SystemExit("sentence must be a single line with no edge whitespace")
    if sentence.count(".") != 1 or not sentence.endswith("."):
        raise SystemExit("entry must be exactly one sentence")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")

    data = sentence.encode("utf-8")
    # Char count (the gate's unit) and byte count differ only for non-ASCII;
    # verify the decoded text, not just the raw bytes, round-trips exactly.
    if len(data.decode("utf-8")) != len(sentence):
        raise SystemExit("utf-8 round-trip changed the sentence")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
        os.chmod(tmp, 0o644)
        os.replace(tmp, target)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    os.chmod(target, 0o644)

    with open(target, "rb") as fh:
        back = fh.read()
    if back != data:
        raise SystemExit("read-back mismatch")
    if back.decode("utf-8") != sentence:
        raise SystemExit("read-back text mismatch")
    if back.endswith(b"\n") or back.endswith(b"\r"):
        raise SystemExit("output must not end with a newline")
    mode = stat.S_IMODE(os.stat(target).st_mode)
    if mode != 0o644:
        raise SystemExit("output mode is %o, expected 644" % mode)
    print("wrote %s (%d chars)" % (target, len(sentence)))


if __name__ == "__main__":
    main()
