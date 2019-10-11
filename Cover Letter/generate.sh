#!/usr/bin/env bash
cp default_config.ini config.ini && "${EDITOR:-vim}" config.ini && python3 coverletter.py && xdg-open coverletter.html
