"""Validate every article's transcription_tei.xml against TEI P5 (schema/tei_all.rng).

    uv run --with lxml python3 scripts/validate_tei.py
Writes reports/tei_validation.md and exits non-zero if any file fails.
"""
import glob, os, sys
from lxml import etree

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = etree.RelaxNG(etree.parse(os.path.join(ROOT, "schema", "tei_all.rng")))
lines, bad = [], 0
for f in sorted(glob.glob(os.path.join(ROOT, "07a Articles", "*", "transcription_tei.xml"))):
    name = os.path.basename(os.path.dirname(f))
    try:
        ok = rng.validate(etree.parse(f))
        errs = [] if ok else [f"line {e.line}: {e.message}" for e in rng.error_log][:10]
    except etree.XMLSyntaxError as e:
        ok, errs = False, [f"not well-formed: {e}"]
    bad += not ok
    lines.append(f"- {'valid' if ok else 'INVALID'}: {name}" + "".join(f"\n    - {e}" for e in errs))
report = f"# TEI validation (TEI P5 tei_all)\n\n{len(lines) - bad} of {len(lines)} files valid.\n\n" + "\n".join(lines) + "\n"
open(os.path.join(ROOT, "reports", "tei_validation.md"), "w").write(report)
print(report[:3000])
sys.exit(1 if bad else 0)
