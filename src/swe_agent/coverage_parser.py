# src/coverage_parser.py
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import List


@dataclass
class FileCoverage:
    filename: str
    covered_lines: int
    total_lines: int
    coverage_percent: float


def parse_coverage_xml(xml_path: str) -> List[FileCoverage]:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    results = []

    # coverage.xml format (pytest-cov / coverage.py)
    for cls in root.findall(".//class"):
        filename = cls.attrib.get("filename")

        lines = cls.findall(".//line")
        if not lines:
            continue

        total = len(lines)
        covered = sum(1 for l in lines if int(l.attrib.get("hits", "0")) > 0)

        percent = round((covered / total) * 100, 2)

        results.append(
            FileCoverage(
                filename=filename,
                covered_lines=covered,
                total_lines=total,
                coverage_percent=percent,
            )
        )

    return sorted(results, key=lambda x: x.coverage_percent)
