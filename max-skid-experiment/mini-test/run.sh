#!/usr/bin/env bash
set -euo pipefail

rounds=10

while (($#)); do
    case "$1" in
        --round|--rounds)
            if (($# < 2)); then
                printf '%s requires a positive integer\n' "$1" >&2
                exit 2
            fi
            rounds=$2
            shift 2
            ;;
        -h|--help)
            printf 'usage: %s [--round N]\n' "$0"
            exit 0
            ;;
        *)
            printf 'unknown argument: %s\n' "$1" >&2
            exit 2
            ;;
    esac
done

if [[ ! $rounds =~ ^[1-9][0-9]*$ ]]; then
    printf '%s\n' '--round requires a positive integer' >&2
    exit 2
fi

source_dir=$(cd "$(dirname "$0")" && pwd)
build_dir=$(mktemp -d)
trap 'rm -rf "$build_dir"' EXIT
event=br_inst_retired.cond:u

for iterations in 1 2; do
    as --64 --defsym ITERATIONS="$iterations" \
        -o "$build_dir/setup-$iterations.o" "$source_dir/setup.s"
    ld -o "$build_dir/setup-$iterations" "$build_dir/setup-$iterations.o"

    if ! output=$(perf stat -x, -r "$rounds" -e "$event" -- "$build_dir/setup-$iterations" 2>&1); then
        printf '%s\n' "$output" >&2
        exit 1
    fi

    average_count=$(printf '%s\n' "$output" | awk -F, -v event="$event" '
        $3 == event { gsub(/[[:space:]]/, "", $1); print $1; exit }
    ')

    if [[ ! $average_count =~ ^[0-9]+([.][0-9]+)?$ ]]; then
        printf 'could not read %s count from perf output:\n%s\n' "$event" "$output" >&2
        exit 1
    fi

    printf 'setup iterations: %s\nrounds: %s\nevent type: %s\nexpected events: %s\naverage counted events: %s\n\n' \
        "$iterations" "$rounds" "$event" "$((iterations * 32))" "$average_count"
done
