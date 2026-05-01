import os
import json

THRESHOLD_MB = 95
VOLUME_ROOT_MARKERS = ["lakes", "configs", "scripts"]

def find_volume_root(start_path):
    """Walk upward until we find a directory containing volume markers."""
    path = os.path.abspath(start_path)
    while True:
        if any(os.path.isdir(os.path.join(path, m)) for m in VOLUME_ROOT_MARKERS):
            return path
        parent = os.path.dirname(path)
        if parent == path:
            raise RuntimeError("Could not locate volume root.")
        path = parent

def scan_large_files(volume_root):
    """Return list of files >= threshold MB with relative paths."""
    results = []
    for root, dirs, files in os.walk(volume_root):
        for f in files:
            full = os.path.join(root, f)
            size_mb = os.path.getsize(full) / (1024 * 1024)
            if size_mb >= THRESHOLD_MB:
                rel = os.path.relpath(full, volume_root)
                results.append({"path": rel.replace("\\", "/"), "size_mb": round(size_mb, 2)})
    return sorted(results, key=lambda x: x["path"])

def write_manifest(volume_root, manifest):
    out_path = os.path.join(volume_root, "large_file_manifest.json")
    with open(out_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"[OK] Wrote manifest: {out_path}")

def write_markdown(volume_root, manifest):
    out_path = os.path.join(volume_root, "LARGE_FILE_DOWNLOAD.md")

    md = []
    md.append("# 📦 LARGE_FILE_DOWNLOAD.md")
    md.append("### Auto‑generated manifest of sovereign lakes >95 MB\n")
    md.append("This file was generated automatically by `build_large_file_manifest.py`.\n")
    md.append("---\n")
    md.append("# 🔗 Download Location (Google Drive)\n")
    md.append("**PLACEHOLDER — INSERT GOOGLE DRIVE LINK HERE**\n")
    md.append("```\n<INSERT LINK HERE>\n```\n")
    md.append("---\n")
    md.append("# 📁 Required Large Files\n")
    md.append("Each entry lists the relative path and size.\n")
    md.append("---\n")

    # Group by top-level directory
    groups = {}
    for entry in manifest:
        top = entry["path"].split("/")[0]
        groups.setdefault(top, []).append(entry)

    for group, items in groups.items():
        md.append(f"## {group}\n")
        md.append("```\n")
        for e in items:
            md.append(f"{e['path']:70s} {e['size_mb']} MB")
        md.append("```\n---\n")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print(f"[OK] Wrote Markdown: {out_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    volume_root = find_volume_root(script_dir)
    print(f"Volume root detected: {volume_root}")

    manifest = scan_large_files(volume_root)
    write_manifest(volume_root, manifest)
    write_markdown(volume_root, manifest)

if __name__ == "__main__":
    main()
