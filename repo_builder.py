#!/usr/bin/env python3
import os
import sys
import json
import time
import zipfile
import hashlib
import shutil

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(REPO_ROOT, "config.json")
PACKAGES_DIR = os.path.join(REPO_ROOT, "packages")

DEFAULT_CONFIG = {
    "repo_name": "NoNamedCat KiCad Plugins",
    "maintainer": {
        "name": "NoNamedCat",
        "contact": {
            "web": "https://github.com/NoNamedCat"
        }
    },
    "base_url": "https://nonamedcat.github.io/nonamedcat-kicad-pcm"
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def calculate_sha256(filepath_or_bytes):
    if isinstance(filepath_or_bytes, bytes):
        return hashlib.sha256(filepath_or_bytes).hexdigest()
    with open(filepath_or_bytes, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def ensure_gitattributes():
    attr_path = os.path.join(REPO_ROOT, ".gitattributes")
    content = "*.json text eol=lf\n*.zip binary\n*.png binary\n*.jpg binary\n"
    with open(attr_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

def build_repository():
    config = load_config()
    base_url = config["base_url"].rstrip("/")

    ensure_gitattributes()
    os.makedirs(PACKAGES_DIR, exist_ok=True)

    all_packages = []
    plugin_summary_list = []

    print(f"\n📦 Building KiCad PCM Repository: '{config['repo_name']}'")
    print(f"🔗 Base URL: {base_url}\n")

    for pkg_id in sorted(os.listdir(PACKAGES_DIR)):
        pkg_path = os.path.join(PACKAGES_DIR, pkg_id)
        if not os.path.isdir(pkg_path):
            continue

        meta_file = os.path.join(pkg_path, "metadata.json")
        if not os.path.exists(meta_file):
            print(f"⚠️  Skipping {pkg_id}: metadata.json missing.")
            continue

        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)

        zips = [f for f in os.listdir(pkg_path) if f.endswith(".zip")]
        if not zips:
            print(f"⚠️  Skipping {pkg_id}: No .zip package file found.")
            continue

        zips.sort()
        latest_zip = zips[-1]
        zip_path = os.path.join(pkg_path, latest_zip)

        zip_sha256 = calculate_sha256(zip_path)
        zip_size = os.path.getsize(zip_path)
        download_url = f"{base_url}/packages/{pkg_id}/{latest_zip}"

        install_size = zip_size * 3
        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                install_size = sum(info.file_size for info in zf.infolist())
        except Exception:
            pass

        if "versions" in meta and len(meta["versions"]) > 0:
            for v in meta["versions"]:
                v["download_sha256"] = zip_sha256
                v["download_url"] = download_url
                v["download_size"] = zip_size
                v["install_size"] = install_size

        all_packages.append(meta)

        icon_url = f"{base_url}/packages/{pkg_id}/icon.png" if os.path.exists(os.path.join(pkg_path, "icon.png")) else ""
        plugin_summary_list.append({
            "name": meta.get("name", pkg_id),
            "id": pkg_id,
            "version": meta.get("versions", [{}])[0].get("version", "1.0.0"),
            "description": meta.get("description", ""),
            "author": meta.get("author", {}).get("name", "Unknown"),
            "homepage": meta.get("resources", {}).get("homepage", ""),
            "icon_url": icon_url,
            "zip_name": latest_zip
        })

        print(f"  ✅ Added Package: {meta.get('name')} ({pkg_id})")
        print(f"     Version: {meta.get('versions', [{}])[0].get('version')} | Size: {zip_size} bytes")
        print(f"     URL: {download_url}\n")

    packages_data = {"packages": all_packages}
    packages_json_str = json.dumps(packages_data, indent=4)
    packages_json_bytes = packages_json_str.encode("utf-8").replace(b"\r\n", b"\n")

    packages_path = os.path.join(REPO_ROOT, "packages.json")
    with open(packages_path, "wb") as f:
        f.write(packages_json_bytes)

    packages_sha256 = hashlib.sha256(packages_json_bytes).hexdigest()

    ts = int(time.time())
    utc_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(ts))

    repo_data = {
        "$schema": "https://go.kicad.org/pcm/schemas/v1#/definitions/Repository",
        "name": config["repo_name"],
        "maintainer": config["maintainer"],
        "packages": {
            "sha256": packages_sha256,
            "update_time_utc": utc_str,
            "update_timestamp": ts,
            "url": f"{base_url}/packages.json"
        }
    }

    repo_path = os.path.join(REPO_ROOT, "repository.json")
    with open(repo_path, "wb") as f:
        f.write(json.dumps(repo_data, indent=4).encode("utf-8").replace(b"\r\n", b"\n"))

    generate_html_index(config, plugin_summary_list)

    print("════════════════════════════════════════════════════════════════")
    print("🎉 REPOSITORY BUILD COMPLETE!")
    print(f"   Packages count:   {len(all_packages)}")
    print(f"   packages.json SHA: {packages_sha256}")
    print(f"   Repository URL:   {base_url}/repository.json")
    print("════════════════════════════════════════════════════════════════\n")

def generate_html_index(config, plugins):
    cards_html = ""
    for p in plugins:
        icon_tag = f'<img src="{p["icon_url"]}" width="48" height="48" style="border-radius:6px;margin-right:12px;">' if p["icon_url"] else ""
        cards_html += f'''
        <div class="card">
            <div style="display:flex;align-items:center;">
                {icon_tag}
                <div>
                    <h3 style="margin:0;">{p['name']} <span class="badge">v{p['version']}</span></h3>
                    <small style="color:#666;">by {p['author']} &bull; <code>{p['id']}</code></small>
                </div>
            </div>
            <p style="margin:12px 0 8px 0;color:#333;">{p['description']}</p>
            <div>
                {f'<a href="{p["homepage"]}" target="_blank" class="btn">GitHub Repo</a>' if p['homepage'] else ''}
            </div>
        </div>
        '''

    base_url = config["base_url"].rstrip("/")
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config['repo_name']}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; background: #f8f9fa; color: #212529; }}
        h1 {{ color: #1a2744; margin-bottom: 8px; }}
        .repo-box {{ background: #e8f4fd; border-left: 5px solid #1976d2; padding: 16px 20px; border-radius: 6px; margin: 24px 0; }}
        code {{ background: #e9ecef; padding: 3px 8px; border-radius: 4px; font-family: monospace; font-size: 0.95em; color: #d63384; }}
        .card {{ background: #ffffff; border: 1px solid #dee2e6; border-radius: 8px; padding: 20px; margin-bottom: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.04); }}
        .badge {{ background: #28a745; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75em; vertical-align: middle; }}
        .btn {{ display: inline-block; padding: 6px 12px; background: #0d6efd; color: white; text-decoration: none; border-radius: 4px; font-size: 0.85em; margin-top: 8px; }}
        .btn:hover {{ background: #0b5ed7; }}
        ol {{ line-height: 1.6; }}
    </style>
</head>
<body>
    <h1>🔌 {config['repo_name']}</h1>
    <p>Official KiCad Plugin & Content Manager (PCM) Repository</p>

    <div class="repo-box">
        <strong>📌 Repository URL to add in KiCad PCM:</strong><br><br>
        <code>{base_url}/repository.json</code>
    </div>

    <h2>📖 How to Install Plugins from this Repository</h2>
    <ol>
        <li>Open <strong>KiCad</strong> &rarr; <strong>Plugin and Content Manager (PCM)</strong>.</li>
        <li>Click <strong>Manage Repositories…</strong> at the bottom.</li>
        <li>Click <strong>+</strong> and paste: <code>{base_url}/repository.json</code></li>
        <li>Click <strong>OK</strong> &rarr; All plugins below will appear in your PCM catalog!</li>
    </ol>

    <h2>📦 Available Plugins ({len(plugins)})</h2>
    {cards_html}

</body>
</html>
'''

    with open(os.path.join(REPO_ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    build_repository()
