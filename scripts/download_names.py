"""Project-specific public filenames; canonical aliases preserve existing workflows."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def download_names(meta=None):
    meta = meta or json.loads((ROOT / 'data/release.json').read_text())
    stems = json.loads((ROOT / 'data/download-names.json').read_text())
    stems[f"does-ai-help-{meta['release']}.pdf"] = 'does-ai-help'
    return {name: f"{stem}-{meta['version']}{''.join(Path(name).suffixes)}" for name, stem in stems.items()}
