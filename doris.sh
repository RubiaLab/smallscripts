#!/usr/bin/env bash

# Doris – DOI to RIS Tool 🦉
# Author: RubiaLab
# Email: rubialab@rubialab.de
# Version 1.0
#
# Fetches bibliographic data from a DOI and saves in RIS (default),
# optionally BibTeX and CSL-JSON formats.

set -euo pipefail

show_help() {
    cat <<EOF
Usage: doris <DOI> [options]

Options:
  --bib            Also save BibTeX file
  --json           Also save CSL-JSON file
  --no-browser     Do not open the DOI URL automatically in the browser
  --outdir DIR     Output directory (default: current directory)
  --help           Show this help message and exit

Examples:
  doris 10.1038/s41586-020-2649-2
  doris 10.1038/s41586-020-2649-2 --bib --json --outdir ./library

EOF
}

if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

DOI=""
FETCH_BIB=false
FETCH_JSON=false
OPEN_BROWSER=true
OUTDIR="."

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --bib)
            FETCH_BIB=true
            shift
            ;;
        --json)
            FETCH_JSON=true
            shift
            ;;
        --no-browser)
            OPEN_BROWSER=false
            shift
            ;;
        --outdir)
            if [ -z "${2:-}" ]; then
                echo "❌ Error: --outdir requires a directory argument."
                exit 1
            fi
            OUTDIR="$2"
            shift 2
            ;;
        --help)
            show_help
            exit 0
            ;;
        -*)
            echo "❌ Error: Unknown option $1"
            show_help
            exit 1
            ;;
        *)
            if [ -z "$DOI" ]; then
                DOI="$1"
                shift
            else
                echo "❌ Error: Multiple DOIs or unknown arguments provided."
                show_help
                exit 1
            fi
            ;;
    esac
done

if [ -z "$DOI" ]; then
    echo "❌ Error: No DOI provided."
    exit 1
fi

# Check if OUTDIR exists or create it
if [ ! -d "$OUTDIR" ]; then
    mkdir -p "$OUTDIR" || {
        echo "❌ Error: Could not create directory $OUTDIR."
        exit 1
    }
fi

URL="https://doi.org/$DOI"

# Fetch RIS data (default)
RIS=$(curl -fsSLH "Accept: application/x-research-info-systems" "$URL") || {
    echo "❌ Error: Could not connect to $URL."
    exit 1
}

if [ -z "$RIS" ]; then
    echo "❌ Error: Could not retrieve RIS data."
    exit 1
fi

# Extract first author (AU line)
AUTHOR=$(echo "$RIS" | grep '^AU' | head -n1 | cut -d'-' -f2 | sed 's/,.*//' | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')
[ -z "$AUTHOR" ] && AUTHOR="unknown"

# Extract year (PY line)
YEAR=$(echo "$RIS" | grep '^PY' | grep -o '[0-9]\{4\}' | head -n1)
[ -z "$YEAR" ] && YEAR="nodate"

# Sanitize DOI for filename (letters, digits, underscore only)
SAFE_DOI=$(echo "$DOI" | tr '/' '_' | tr -cd '[:alnum:]_')

# Base filename
BASENAME="${AUTHOR}${YEAR}"

# Save RIS file
RIS_PATH="${OUTDIR}/${BASENAME}.ris"
echo "$RIS" > "$RIS_PATH"
echo "✅ RIS saved: $RIS_PATH"

# Optionally save BibTeX
if [ "$FETCH_BIB" = true ]; then
    BIB=$(curl -fsSLH "Accept: application/x-bibtex" "$URL") || {
        echo "⚠️  Warning: Could not retrieve BibTeX data."
        BIB=""
    }
    if [ -n "$BIB" ]; then
        BIB_PATH="${OUTDIR}/${BASENAME}.bib"
        echo "$BIB" > "$BIB_PATH"
        echo "✅ BibTeX saved: $BIB_PATH"
    fi
fi

# Optionally save CSL-JSON
if [ "$FETCH_JSON" = true ]; then
    CSL=$(curl -fsSLH "Accept: application/vnd.citationstyles.csl+json" "$URL") || {
        echo "⚠️  Warning: Could not retrieve JSON data."
        CSL=""
    }
    if [ -n "$CSL" ]; then
        JSON_PATH="${OUTDIR}/${BASENAME}.json"
        echo "$CSL" > "$JSON_PATH"
        echo "✅ CSL-JSON saved: $JSON_PATH"
    fi
fi

# Open URL in browser (optional)
if [ "$OPEN_BROWSER" = true ]; then
    if command -v xdg-open >/dev/null; then
        xdg-open "$URL" >/dev/null 2>&1 &
    elif command -v open >/dev/null; then
        open "$URL" >/dev/null 2>&1 &
    else
        echo "⚠️  Warning: No known browser opener found."
    fi
fi
