# 1/test_coverage_parser.py
from src.coverage_parser import parse_coverage_xml,FileCoverage


def test_parse_coverage_xml(tmp_path):
    xml = tmp_path / "coverage.xml"
    xml.write_text(
        """<?xml version="1.0" ?>
        <coverage>
          <packages>
            <package>
              <classes>
                <class filename="a.py">
                  <lines>
                    <line number="1" hits="1"/>
                    <line number="2" hits="0"/>
                  </lines>
                </class>
                <class filename="b.py">
                  <lines>
                    <line number="1" hits="0"/>
                    <line number="2" hits="0"/>
                  </lines>
                </class>
              </classes>
            </package>
          </packages>
        </coverage>
        """
    )

    result = parse_coverage_xml(str(xml))

    assert len(result) == 2
    assert isinstance(result[0], FileCoverage)

    # b.py should be worst coverage
    assert result[0].filename == "b.py"
    assert result[0].coverage_percent == 0.0

    # a.py should be 50%
    assert result[1].filename == "a.py"
    assert result[1].coverage_percent == 50.0
