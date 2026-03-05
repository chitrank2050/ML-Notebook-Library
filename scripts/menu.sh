#!/usr/bin/env bash
# =============================================================================
# scripts/menu.sh — Interactive arrow-key checkbox menu for Makefile targets
#
# Usage (called by Makefile):
#   bash scripts/menu.sh clean
#   bash scripts/menu.sh obliviate
#   bash scripts/menu.sh wizard
#
# Controls:
#   ↑ / k    move cursor up
#   ↓ / j    move cursor down
#   SPACE    toggle checkbox
#   A        select / deselect all
#   ENTER    confirm and execute
#   q / ESC  cancel
# =============================================================================

set -euo pipefail

# ── ANSI ──────────────────────────────────────────────────────────────────────
RESET="\033[0m"
BOLD="\033[1m"
DIM="\033[2m"
GREEN="\033[32m"
CYAN="\033[36m"
YELLOW="\033[33m"
RED="\033[31m"
BG_ROW="\033[48;5;236m"    # dark grey highlight for cursor row
CLEAR_LINE="\033[2K"
HIDE_CURSOR="\033[?25l"
SHOW_CURSOR="\033[?25h"

# ── Checkbox UI ───────────────────────────────────────────────────────────────
# checkbox_menu <title> <label1> [label2 ...]
# Writes selected labels (newline-separated) to stdout.
# Returns 0 on confirm, 1 on cancel / nothing selected.
checkbox_menu() {
    local title="$1"; shift
    local options=("$@")
    local n=${#options[@]}
    local checked=(); local cursor=0

    for (( i=0; i<n; i++ )); do checked[$i]=0; done

    # ── separator check: rows starting with ── are non-interactive labels ────
    _is_sep() { [[ "${options[$1]}" == ──* ]]; }

    # Skip cursor past separators in the given direction (+1 or -1)
    _skip_sep() {
        local dir=$1
        local tries=0
        while _is_sep $cursor && (( tries++ < n )); do
            (( cursor = (cursor + dir + n) % n ))
        done
    }

    # Redirect all drawing to /dev/tty so it works when stdout is piped
    exec 3>/dev/tty

    local saved_stty
    saved_stty=$(stty -g 2>/dev/null || true)
    stty -echo -icanon time 0 min 0 2>/dev/null || true

    printf "%b" "$HIDE_CURSOR" >&3

    # ── draw ────────────────────────────────────────────────────────────────
    _draw() {
        local scroll_up=${1:-0}
        [[ $scroll_up -gt 0 ]] && printf "\033[%dA" "$scroll_up" >&3

        {
            printf "%b\n" "${BOLD}${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
            printf "%b\n" "${BOLD}  ${title}${RESET}"
            printf "%b\n" "${DIM}  ↑↓ move  SPACE toggle  A all  ENTER confirm  q quit${RESET}"
            printf "%b\n" "${BOLD}${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"

            for (( i=0; i<n; i++ )); do
                if _is_sep $i; then
                    # Render separator as a plain dim label — no checkbox
                    if [[ $i -eq $cursor ]]; then
                        printf "${CLEAR_LINE}%b\n" "${BG_ROW}  ${DIM}  ${options[$i]}${RESET}"
                    else
                        printf "${CLEAR_LINE}%b\n" "    ${DIM}  ${options[$i]}${RESET}"
                    fi
                else
                    local box
                    if [[ ${checked[$i]} -eq 1 ]]; then
                        box="${GREEN}[✔]${RESET}"
                    else
                        box="${DIM}[ ]${RESET}"
                    fi
                    if [[ $i -eq $cursor ]]; then
                        printf "${CLEAR_LINE}%b\n" "${BG_ROW}  ${YELLOW}▶${RESET}${BG_ROW} ${box} ${options[$i]}${RESET}"
                    else
                        printf "${CLEAR_LINE}%b\n" "    ${box} ${options[$i]}"
                    fi
                fi
            done
            printf "\n"
        } >&3
    }

    _draw 0
    local total_lines=$(( n + 5 ))   # 4 header lines + n options + 1 blank

    local cancelled=0
    while true; do
        local key seq
        IFS= read -r -s -n1 key </dev/tty 2>/dev/null || true
        if [[ "$key" == $'\x1b' ]]; then
            IFS= read -r -s -n2 -t 1 seq </dev/tty 2>/dev/null || true
            key="${key}${seq}"
        fi

        case "$key" in
            $'\x1b[A' | k | K)
                (( cursor = (cursor - 1 + n) % n ))
                _skip_sep -1
                ;;
            $'\x1b[B' | j | J)
                (( cursor = (cursor + 1) % n ))
                _skip_sep 1
                ;;
            ' ')
                # No-op on separator rows
                _is_sep $cursor || checked[$cursor]=$(( 1 - checked[$cursor] ))
                ;;
            a | A)
                local all=1
                for (( i=0; i<n; i++ )); do
                    _is_sep $i && continue
                    [[ ${checked[$i]} -eq 0 ]] && all=0 && break
                done
                local v=$(( 1 - all ))
                for (( i=0; i<n; i++ )); do
                    _is_sep $i && continue
                    checked[$i]=$v
                done
                ;;
            $'\n' | $'\r' | '') break ;;
            q | Q | $'\x1b')    cancelled=1; break ;;
        esac

        _draw "$total_lines"
    done

    # Restore terminal
    stty "$saved_stty" 2>/dev/null || true
    printf "%b" "$SHOW_CURSOR" >&3
    exec 3>&-

    if [[ $cancelled -eq 1 ]]; then
        printf "\n%b\n" "${RED}  ✖ Cancelled — no action taken.${RESET}" >/dev/tty
        return 1
    fi

    local any=0
    for (( i=0; i<n; i++ )); do
        if [[ ${checked[$i]} -eq 1 ]]; then
            printf "%s\n" "${options[$i]}"
            any=1
        fi
    done

    if [[ $any -eq 0 ]]; then
        printf "\n%b\n" "${DIM}  Nothing selected — no action taken.${RESET}" >/dev/tty
        return 1
    fi
    return 0
}

# ── Helpers ───────────────────────────────────────────────────────────────────
MAKE_CMD="${MAKE:-make}"

run_clean_cache() {
    $MAKE_CMD --no-print-directory _clean_cache
}

run_clean_models() {
    $MAKE_CMD --no-print-directory _clean_models
}

run_clean_venv() {
    $MAKE_CMD --no-print-directory _clean_venv
}

dispatch_selection() {
    local opt="$1"
    case "$opt" in
        Cache*)   run_clean_cache   || true ;;
        Saved*)   run_clean_models  || true ;;
        Virtual*) run_clean_venv    || true ;;
        I*)       $MAKE_CMD --no-print-directory init      || true ;;
        S*)       $MAKE_CMD --no-print-directory install   || true ;;
        D*)       $MAKE_CMD --no-print-directory dev       || true ;;
        L*)       $MAKE_CMD --no-print-directory lint      || true ;;
        F*)       $MAKE_CMD --no-print-directory format    || true ;;
        C*)       $MAKE_CMD --no-print-directory clean     || true ;;
        O*)       $MAKE_CMD --no-print-directory obliviate || true ;;
    esac
}

# ── Modes ─────────────────────────────────────────────────────────────────────
MODE="${1:-wizard}"

case "$MODE" in
    # ── make clean ────────────────────────────────────────────────────────────
    clean)
        _TMP=$(mktemp)
        if checkbox_menu "🧹  Clean — select what to remove" \
            "Cache files    (__pycache__, .pyc, dist, .ruff_cache…)" \
            "Saved models   (models/)" > "$_TMP"; then
            while IFS= read -r opt; do dispatch_selection "$opt"; done < "$_TMP"
        fi
        rm -f "$_TMP"
        ;;

    # ── make obliviate ────────────────────────────────────────────────────────
    obliviate)
        _TMP=$(mktemp)
        if checkbox_menu "☠️   Obliviate — select what to obliterate" \
            "Cache files    (__pycache__, .pyc, dist, .ruff_cache…)" \
            "Saved models   (models/)" \
            "Virtual env    (.venv)" > "$_TMP"; then
            while IFS= read -r opt; do dispatch_selection "$opt"; done < "$_TMP"
            printf "\n%b\n" "${BOLD}${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
            printf "%b\n"   "  To set up again:"
            printf "%b\n"   "  → Run ${YELLOW}make init${RESET} to create venv"
            printf "%b\n"   "  → Run ${YELLOW}make install${RESET} to install deps"
            printf "%b\n"   "${BOLD}${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
        fi
        rm -f "$_TMP"
        ;;

    # ── make menu (full wizard) ───────────────────────────────────────────────
    wizard)
        _TMP=$(mktemp)
        if checkbox_menu "⚡  ML-Notebook-Library — what to do?" \
            "I – Init        Create virtual environment" \
            "S – Install     Sync dependencies from pyproject.toml" \
            "D – Dev         Launch Jupyter Lab" \
            "L – Lint        Check code quality with ruff" \
            "F – Format      Auto-format code with ruff" \
            "── Cleanup ──────────────────────────────────" \
            "X – Cache       Remove __pycache__, .pyc, dist, .ruff_cache…" \
            "M – Models      Remove saved models (models/)" \
            "V – Venv        Remove virtual environment (.venv)" > "$_TMP"; then
            # Execute in dependency order: destructive first, then setup, then dev tools
            grep -q "^V" "$_TMP" && run_clean_venv    || true
            grep -q "^X" "$_TMP" && run_clean_cache   || true
            grep -q "^M" "$_TMP" && run_clean_models  || true
            grep -q "^I" "$_TMP" && $MAKE_CMD --no-print-directory init    || true
            grep -q "^S" "$_TMP" && $MAKE_CMD --no-print-directory install || true
            grep -q "^D" "$_TMP" && $MAKE_CMD --no-print-directory dev     || true
            grep -q "^L" "$_TMP" && $MAKE_CMD --no-print-directory lint    || true
            grep -q "^F" "$_TMP" && $MAKE_CMD --no-print-directory format  || true
        fi
        rm -f "$_TMP"
        ;;

    *)
        printf "Usage: %s [clean|obliviate|wizard]\n" "$0" >&2
        exit 1
        ;;
esac
