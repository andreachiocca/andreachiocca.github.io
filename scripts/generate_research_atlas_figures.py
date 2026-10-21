"""Generate/verify stress-arrow coordinates for the static Research Atlas fatigue schematic.

The SVG's design stays editable, while this script owns the traction-derived
arrow geometry. No measurement or fatigue-life result is encoded.
"""
import argparse
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "_includes/research_figures/fatigue.svg"
SIGMA = [[0.0, 0.0, 0.6], [0.0, 0.0, 0.0], [0.6, 0.0, 1.0]]
NORMAL = (1 / math.sqrt(2), 0.0, 1 / math.sqrt(2))


def traction_components(sigma: list[list[float]], normal: tuple[float, float, float]) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    if len(sigma) != 3 or any(len(row) != 3 for row in sigma):
        raise ValueError("Expected a 3x3 Cauchy stress tensor")
    if any(abs(sigma[i][j]-sigma[j][i]) > 1e-10 for i in range(3) for j in range(3)):
        raise ValueError("Classical Cauchy stress tensor must be symmetric")
    length = math.sqrt(sum(value * value for value in normal))
    if length < 1e-12:
        raise ValueError("Plane normal cannot have zero length")
    n = tuple(value / length for value in normal)
    total = tuple(sum(sigma[i][j]*n[j] for j in range(3)) for i in range(3))
    sigma_n = sum(total[i]*n[i] for i in range(3))
    direct = tuple(sigma_n*value for value in n)
    shear = tuple(total[i]-direct[i] for i in range(3))
    return direct, shear


def project_iso(vector: tuple[float, float, float]) -> tuple[float, float]:
    x, y, z = vector
    return (math.sqrt(3) / 2 * (x - y), (x + y) / 2 - z)


def stress_paths():
    direct, tangent = traction_components(SIGMA, NORMAL)
    total = tuple(direct[i] + tangent[i] for i in range(3))
    result = {}
    for name, vector in (("normal", direct), ("shear", tangent), ("resultant", total)):
        x, y = project_iso(vector)
        result[name] = f"M240.00 160.00 L{240 + 75*x:.2f} {160 + 75*y:.2f}"
    return result


def normalize_svg(content):
    for key, segment in stress_paths().items():
        pattern = r'(<path data-stress-arrow="' + key + r'" d=")[^"]*(")'
        content, count = re.subn(pattern, lambda match: match.group(1)+segment+match.group(2), content)
        if count != 1:
            raise ValueError(f"Expected one stress arrow for {key}; found {count}")
    return content


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    existing = TARGET.read_text(encoding="utf-8")
    corrected = normalize_svg(existing)
    if args.check:
        if existing != corrected:
            raise SystemExit("Fatigue traction SVG out of sync; run generator without --check")
        print("PASS: Research fatigue traction geometry matches symmetric tensor and plane normal")
    else:
        TARGET.write_text(corrected, encoding="utf-8")
        print("Updated fatigue stress-vector geometry")


if __name__ == "__main__":
    main()
