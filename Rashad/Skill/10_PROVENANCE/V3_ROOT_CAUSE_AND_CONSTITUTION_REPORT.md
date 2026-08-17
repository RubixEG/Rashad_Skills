# V3 Root Cause and Constitution Report

## Root cause
The repeated failure pattern was not solved by adding prompts because the runtime kept finding an easier path: rounded-card composition. The skill contained strong rules, but the production route could bypass them.

## V3 correction
Version 3 makes the route itself the authority. It prohibits production PIL/card composition and requires HTML/SVG master composition, whole-page visual search, predictive failure review and actual rendered-pixel QA.

## Why major version
This is not a small patch. The system changes from rule accumulation to production constitution and acceptance testing.
