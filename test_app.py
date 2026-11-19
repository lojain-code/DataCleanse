# DataCleanse - test the Streamlit site (Workshop 2)
# Run from the project folder:   python test_app.py
# It opens app.py in a hidden test browser, checks every STUDENT PART and prints PASS or FAIL.
import os
import sys
import logging
logging.getLogger("streamlit").setLevel(logging.ERROR)
from streamlit.testing.v1 import AppTest

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())

CFG = {'p1': ['Rows', 'Cities', 'Average score'], 'p2': 2, 'p3': [('slider', 'Age bins'), ('slider', 'Score bins')], 'p3n': 2, 'p4': ['Rows before', 'Rows after', 'Missing values', 'Duplicate rows'], 'p4w': [('file_uploader', 'Upload a CSV file')]}


def walk(node):
    yield node
    for child in getattr(node, "children", {}).values():
        yield from walk(child)


def count_images(at):
    return sum(1 for x in walk(at.main) if type(x).__name__ == "Image")


def count_downloads(at):
    return sum(1 for x in walk(at.main) if type(x).__name__ == "DownloadButton")


def find(widgets, label):
    for w in widgets:
        if w.label == label:
            return w
    return None


def metric_labels(at):
    return [m.label for m in at.metric]


results = []


def check(name, ok, why=""):
    results.append(ok)
    print(("PASS - " if ok else "FAIL - ") + name + ("" if ok else "   <- " + why))


at = AppTest.from_file("app.py", default_timeout=60).run()
if len(at.exception) > 0:
    check("App starts without an error", False, str(at.exception[0].value)[:150])
    print("Fix the error above first. Result: 0 checks passed.")
    sys.exit(0)
check("App starts without an error", True)

# ---------- Part 1
labels = metric_labels(at)
check("Part 1 - metrics " + ", ".join(CFG["p1"]), all(m in labels for m in CFG["p1"]), "metrics found: " + str(labels))
check("Part 1 - the table (st.dataframe) is shown", len(at.dataframe) >= 1, "no st.dataframe on the page")

# ---------- Part 2
n = count_images(at)
check("Part 2 - at least {} charts are shown".format(CFG["p2"]), n >= CFG["p2"], "images found: " + str(n))

# ---------- Part 3
ok3 = True
why3 = ""
for kind, label in CFG["p3"]:
    w = find(getattr(at, kind), label)
    if w is None:
        ok3 = False
        why3 = kind + " '" + label + "' not found"
        break
check("Part 3 - widgets exist: " + ", ".join(l for k, l in CFG["p3"]), ok3, why3)
if ok3:
    for kind, label in CFG["p3"]:
        w = find(getattr(at, kind), label)
        if kind == "selectbox":
            w.select(w.options[-1])
        elif kind == "slider":
            w.set_value(w.max)
        elif kind == "multiselect":
            w.set_value([w.options[0]])
    at.run()
    check("Part 3 - changing the widgets works (no error)", len(at.exception) == 0, str(at.exception[0].value)[:150] if len(at.exception) else "")
    check("Part 3 - charts are still shown after the change", count_images(at) >= CFG["p2"] + CFG["p3n"], "images found: " + str(count_images(at)))
    if CFG.get("p3_edge"):
        kind, label, value, kind2 = CFG["p3_edge"]
        find(getattr(at, kind), label).set_value(value)
        at.run()
        check("Part 3 - empty choice shows a warning, not an error", len(at.exception) == 0 and len(at.warning) >= 1, "no st.warning or an exception")
        find(getattr(at, kind), label).set_value(CFG["p3_edge_restore"])
        at.run()

# ---------- Part 4
labels = metric_labels(at)
check("Part 4 - metrics " + ", ".join(CFG["p4"]), all(m in labels for m in CFG["p4"]), "metrics found: " + str(labels))
ok4 = True
for kind, label in CFG["p4w"]:
    if find(getattr(at, kind), label) is None:
        ok4 = False
        check("Part 4 - " + kind + " '" + label + "' exists", False, "not found")
if ok4:
    check("Part 4 - all widgets exist", True)
check("Part 4 - download button exists", count_downloads(at) >= 1, "no st.download_button")
if CFG.get("p4_edge") and ok4:
    for kind, label, value in CFG["p4_edge"]:
        w = find(getattr(at, kind), label)
        w.set_value(value if value != "ALL" else list(w.options))
    at.run()
    check("Part 4 - edge case is handled (message, no crash)", len(at.exception) == 0 and (len(at.error) + len(at.warning)) >= 1, "exception or no message")

print()
print(sum(results), "of", len(results), "checks passed")
if sum(results) == len(results):
    print("All checks passed - your site is ready to demo.")
else:
    print("Read the FAIL lines, fix that part in app.py, and run this test again.")
