import pytest
from boom.simple_hit_detector import SimpleHitDetector

def test_no_values_no_hit():
    detector = SimpleHitDetector(100, 50)
    assert detector.detect_hit([]) == False

def test_value_on_limit_is_hit():
    detector = SimpleHitDetector(100, 50)
    assert detector.detect_hit([50]) == True

def test_values_under_limit_no_hit():
    detector = SimpleHitDetector(100, 10)
    assert detector.detect_hit([0,1,2,3,4,5,6,7,8,9]) == False

def test_values_under_and_over_limit_is_hit():
    detector = SimpleHitDetector(100, 10)
    assert detector.detect_hit([7, 8, 9, 10, 11, 12]) == True

def test_get_last_hit_fraction_default():
    detector = SimpleHitDetector(100, 10)
    assert detector.get_last_hit_fraction() == 0

def test_get_last_hit_fraction_no_hits():
    detector = SimpleHitDetector(100, 10)
    detector.detect_hit([0,1,2])
    assert detector.get_last_hit_fraction() == 0

def test_get_last_hit_fraction_hit_10_percentage():
    detector = SimpleHitDetector(100, 10)
    detector.detect_hit([10])
    assert detector.get_last_hit_fraction() == 0.1

def test_get_last_hit_fraction_gives_fraction_based_on_last_value_when_multiple_are_given():
    detector = SimpleHitDetector(100, 10)
    detector.detect_hit([10, 30, 50])
    assert detector.get_last_hit_fraction() == 0.5

def test_change_hit_value():
    detector = SimpleHitDetector(100, 10)
    assert detector.detect_hit([50]) == True
    detector.set_hit_value(80)
    assert detector.detect_hit([50]) == False
