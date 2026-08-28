# Agrited Web Platform — Redesign

[![Eleventy](https://img.shields.io/badge/SSG-Eleventy_v3.0-blueviolet?style=for-the-badge&logo=eleventy)](https://www.11ty.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind_CSS_v3.4-38B2AC?style=for-the-badge&logo=tailwind-css)](https://tailwindcss.com/)
[![Alpine.js](https://img.shields.io/badge/Reactivity-Alpine.js_v3.x-8BC0D0?style=for-the-badge&logo=alpine.js)](https://alpinejs.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.style=for-the-badge)](LICENSE)

A high-performance, pixel-perfect modernization of the [Agrited Nigeria](https://www.agrited.net) web platform. Built as a static site using **Eleventy (11ty)**, this project replaces legacy web structures with an ultra-fast, accessible, and mobile-first experience designed for agricultural clients across Nigeria.

---

## Key Features

* ⚡ **Blazing Fast Performance**: Zero-client-JS core powered by static site generation (100 Lighthouse performance targets).
* 🎨 **Modern Agribusiness Aesthetics**: Custom tailwind design tokens with ambient lighting, micro-interactions, dark mode support, and glassmorphism UI elements.
* 📦 **Dynamic Product Showcase**: Filterable product catalog using Alpine.js reactive state and accessible modal dispatch systems.
* 🌐 **Data-Driven Front Matter**: Flexible layout templates (`base.html`) decoupled from content for maintainable page headers, metadata, and hero sections.
* 📱 **Fully Responsive**: Mobile-first architecture with aspect-ratio layout locks to prevent Cumulative Layout Shift (CLS).
* ♿ **Accessibility First**: Full keyboard navigation support (`role="button"`, focus rings, `tabindex` management, and ARIA primitives).

---

## Tech Stack

| Domain | Technology | Description |
| :--- | :--- | :--- |
| **Generator** | [Eleventy (11ty)](https://www.11ty.dev/) | Static site generator for template rendering |
| **Styling** | [Tailwind CSS](https://tailwindcss.com/) | Utility-first CSS framework with dark mode support |
| **Reactivity** | [Alpine.js](https://alpinejs.dev/) | Lightweight reactive JavaScript for modals and filtering |
| **Templating** | Nunjucks / HTML | Layout inheritance and modular UI inclusion |
| **Build Tooling** | PostCSS / npm scripts | Asset compilation and minification |

---

## Project Structure

```text
├── src/
│   ├── _data/              # Global site data (products, team, locations)
│   ├── _includes/          # Reusable components (nav, footer, product-card, hero)
│   │   └── layouts/        # Base layouts (base.html)
│   ├── assets/
│   │   ├── css/            # Tailwind input files
│   │   ├── js/             # Alpine.js initialization & modules
│   │   └── img/            # Optimized static media assets
│   ├── pages/              # Site pages (index, about, products, contact)
│   └── index.njk           # Homepage template
├── .eleventy.js            # 11ty engine configuration & filters
├── tailwind.config.js      # Custom theme colors (emerald, slate) & plugins
├── package.json
└── README.md