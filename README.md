# 🔌 NoNamedCat KiCad Plugin Repository

[![KiCad Compatibility](https://img.shields.io/badge/KiCad-7.0%20|%208.0%20|%209.0%20|%2010.0+-blue.svg)](https://kicad.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Web Catalog](https://img.shields.io/badge/Web-Catalog-orange.svg)](https://nonamedcat.github.io/nonamedcat-kicad/)

Official third-party repository for KiCad's **Plugin and Content Manager (PCM)**. This repository distributes curated, automated design extensions and workflow accelerators directly to your KiCad installation.

---

## 📌 Repository URL

Add this URL to your KiCad installation to receive automatic plugin updates and one-click installs:

```text
https://nonamedcat.github.io/nonamedcat-kicad/repository.json
```

🌐 **[Browse the Web Catalog](https://nonamedcat.github.io/nonamedcat-kicad/)**

---

## 🚀 Quick Setup in KiCad

1. Open KiCad and launch the **Plugin and Content Manager (PCM)**.
2. Click the **Manage** / **Repository Settings** button (gear icon or bottom bar).
3. Click **+** (Add Repository) and enter:
   - **Name:** `NoNamedCat Plugins`
   - **URL:** `https://nonamedcat.github.io/nonamedcat-kicad/repository.json`
4. Click **Save** / **OK**.
5. Switch to the **Plugins** tab, find the plugin you want, click **Install**, and press **Apply Pending Changes**.

---

## 📦 Featured Plugins

### 🔹 [JLC Library Gen](https://github.com/NoNamedCat/JLC_Library_Gen)
> *Seamless JLCPCB & LCSC component search and automated CAD injection for KiCad.*

* **In-App Search:** Search through millions of JLCPCB/LCSC SMT components directly inside KiCad without switching to an external browser.
* **Visual Verification:** Preview component datasheets, 2D footprints, and full 3D CAD renders before placing parts into your design.
* **Automatic Schematic & PCB Placement:** Automatically downloads and injects symbols and footprints into your schematic with accurate pin mappings, manufacturer info, and LCSC part numbers.
* **BOM & SMT Ready:** Generates compliant Bill of Materials (BOM) attributes and rotation-verified footprints ready for JLCPCB SMT assembly.
* **Automated Dependency Handling:** Transparent background setup for required conversion engines (`easyeda2kicad`).

---

## 📋 Compatibility

| Software | Supported Versions | Platform |
| :--- | :--- | :--- |
| **KiCad** | 7.0, 8.0, 9.0, 10.0+ | Windows, macOS, Linux |

---

## 📄 License

All plugins distributed through this repository are open-source under the [MIT License](LICENSE).  
Maintained by **[NoNamedCat](https://github.com/NoNamedCat)**.
