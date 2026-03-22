
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
import sys
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

sys.path.insert(0, r'C:\Users\ASUS\Desktop\quantium-starter-repo\output')

from visualisation import app


def test_header_present(dash_duo):
    """Test 1 — Check the header is present"""
    dash_duo.start_server(app)
    dash_duo.wait_for_element('#header', timeout=10)
    header = dash_duo.find_element('#header')
    assert header is not None
    assert 'Pink Morsel' in header.text


def test_chart_present(dash_duo):
    """Test 2 — Check the line chart is present"""
    dash_duo.start_server(app)
    dash_duo.wait_for_element('#sales-line-chart', timeout=10)
    chart = dash_duo.find_element('#sales-line-chart')
    assert chart is not None


def test_region_picker_present(dash_duo):
    """Test 3 — Check the region picker is present"""
    dash_duo.start_server(app)
    dash_duo.wait_for_element('#region-picker', timeout=10)
    picker = dash_duo.find_element('#region-picker')
    assert picker is not None