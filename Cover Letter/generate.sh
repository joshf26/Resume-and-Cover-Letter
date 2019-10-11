#!/usr/bin/env bash
cp default_config.ini config.ini && vim config.ini && python3 coverletter.py && xdg-open coverletter.html
