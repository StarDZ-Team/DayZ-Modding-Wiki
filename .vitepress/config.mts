import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'
import { buildMemoryPlugin } from './build-memory.mts'

function sidebar(lang: string = 'en') {
  const l = `/${lang}`
  return [
    {
      text: 'Part 1: Enforce Script',
      collapsed: false,
      items: [
        { text: 'Variables & Types', link: `${l}/01-enforce-script/01-variables-types` },
        { text: 'Control Flow', link: `${l}/01-enforce-script/05-control-flow` },
        { text: 'Functions & Methods', link: `${l}/01-enforce-script/13-functions-methods` },
        { text: 'Arrays, Maps & Sets', link: `${l}/01-enforce-script/02-arrays-maps-sets` },
        { text: 'String Operations', link: `${l}/01-enforce-script/06-strings` },
        { text: 'Math & Vectors', link: `${l}/01-enforce-script/07-math-vectors` },
        { text: 'Classes & Inheritance', link: `${l}/01-enforce-script/03-classes-inheritance` },
        { text: 'Modded Classes', link: `${l}/01-enforce-script/04-modded-classes` },
        { text: 'Memory Management', link: `${l}/01-enforce-script/08-memory-management` },
        { text: 'Casting & Reflection', link: `${l}/01-enforce-script/09-casting-reflection` },
        { text: 'Enums & Preprocessor', link: `${l}/01-enforce-script/10-enums-preprocessor` },
        { text: 'Error Handling', link: `${l}/01-enforce-script/11-error-handling` },
        { text: 'What Does NOT Exist', link: `${l}/01-enforce-script/12-gotchas` },
      ]
    },
    {
      text: 'Part 2: Mod Structure',
      collapsed: true,
      items: [
        { text: 'The 5-Layer Hierarchy', link: `${l}/02-mod-structure/01-five-layers` },
        { text: 'config.cpp Deep Dive', link: `${l}/02-mod-structure/02-config-cpp` },
        { text: 'mod.cpp & Workshop', link: `${l}/02-mod-structure/03-mod-cpp` },
        { text: 'Anatomy of a Minimal Mod', link: `${l}/02-mod-structure/04-minimum-viable-mod` },
        { text: 'File Organization', link: `${l}/02-mod-structure/05-file-organization` },
        { text: 'Server/Client Architecture', link: `${l}/02-mod-structure/06-server-client-split` },
      ]
    },
    {
      text: 'Part 3: GUI & Layout',
      collapsed: true,
      items: [
        { text: 'Widget Types', link: `${l}/03-gui-system/01-widget-types` },
        { text: 'Layout File Format', link: `${l}/03-gui-system/02-layout-files` },
        { text: 'Sizing & Positioning', link: `${l}/03-gui-system/03-sizing-positioning` },
        { text: 'Container Widgets', link: `${l}/03-gui-system/04-containers` },
        { text: 'Programmatic Creation', link: `${l}/03-gui-system/05-programmatic-widgets` },
        { text: 'Event Handling', link: `${l}/03-gui-system/06-event-handling` },
        { text: 'Styles, Fonts & Images', link: `${l}/03-gui-system/07-styles-fonts` },
        { text: 'Dialogs & Modals', link: `${l}/03-gui-system/08-dialogs-modals` },
        { text: 'UI Architecture Patterns', link: `${l}/03-gui-system/09-real-mod-patterns` },
        { text: 'Advanced Widgets', link: `${l}/03-gui-system/10-advanced-widgets` },
      ]
    },
    {
      text: 'Part 4: File Formats & Tools',
      collapsed: true,
      items: [
        { text: 'Textures', link: `${l}/04-file-formats/01-textures` },
        { text: '3D Models', link: `${l}/04-file-formats/02-models` },
        { text: 'Building Modeling', link: `${l}/04-file-formats/08-building-modeling` },
        { text: 'Materials', link: `${l}/04-file-formats/03-materials` },
        { text: 'Audio', link: `${l}/04-file-formats/04-audio` },
        { text: 'DayZ Tools Workflow', link: `${l}/04-file-formats/05-dayz-tools` },
        { text: 'PBO Packing', link: `${l}/04-file-formats/06-pbo-packing` },
        { text: 'Workbench Guide', link: `${l}/04-file-formats/07-workbench-guide` },
      ]
    },
    {
      text: 'Part 5: Configuration Files',
      collapsed: true,
      items: [
        { text: 'stringtable.csv', link: `${l}/05-config-files/01-stringtable` },
        { text: 'Inputs.xml', link: `${l}/05-config-files/02-inputs-xml` },
        { text: 'Credits.json', link: `${l}/05-config-files/03-credits-json` },
        { text: 'ImageSet Format', link: `${l}/05-config-files/04-imagesets` },
        { text: 'Server Configuration', link: `${l}/05-config-files/05-server-configs` },
        { text: 'Spawning Gear', link: `${l}/05-config-files/06-spawning-gear` },
      ]
    },
    {
      text: 'Part 6: Engine API',
      collapsed: true,
      items: [
        { text: 'Entity System', link: `${l}/06-engine-api/01-entity-system` },
        { text: 'Vehicle System', link: `${l}/06-engine-api/02-vehicles` },
        { text: 'Weather System', link: `${l}/06-engine-api/03-weather` },
        { text: 'Camera System', link: `${l}/06-engine-api/04-cameras` },
        { text: 'Post-Process Effects', link: `${l}/06-engine-api/05-ppe` },
        { text: 'Notification System', link: `${l}/06-engine-api/06-notifications` },
        { text: 'Timers & CallQueue', link: `${l}/06-engine-api/07-timers` },
        { text: 'File I/O & JSON', link: `${l}/06-engine-api/08-file-io` },
        { text: 'Networking & RPC', link: `${l}/06-engine-api/09-networking` },
        { text: 'Central Economy Script API', link: `${l}/06-engine-api/10-central-economy` },
        { text: 'Mission Hooks', link: `${l}/06-engine-api/11-mission-hooks` },
        { text: 'Action System', link: `${l}/06-engine-api/12-action-system` },
        { text: 'Input System', link: `${l}/06-engine-api/13-input-system` },
        { text: 'Player System', link: `${l}/06-engine-api/14-player-system` },
        { text: 'Sound System', link: `${l}/06-engine-api/15-sound-system` },
        { text: 'Crafting System', link: `${l}/06-engine-api/16-crafting-system` },
        { text: 'Construction System', link: `${l}/06-engine-api/17-construction-system` },
        { text: 'Animation System', link: `${l}/06-engine-api/18-animation-system` },
        { text: 'Terrain & World Queries', link: `${l}/06-engine-api/19-terrain-queries` },
        { text: 'Particle & Effects', link: `${l}/06-engine-api/20-particle-effects` },
        { text: 'Zombie & AI System', link: `${l}/06-engine-api/21-zombie-ai-system` },
        { text: 'Admin & Server', link: `${l}/06-engine-api/22-admin-server` },
      ]
    },
    {
      text: 'Part 7: Patterns & Practices',
      collapsed: true,
      items: [
        { text: 'Singleton Pattern', link: `${l}/07-patterns/01-singletons` },
        { text: 'Module/Plugin Systems', link: `${l}/07-patterns/02-module-systems` },
        { text: 'RPC Communication', link: `${l}/07-patterns/03-rpc-patterns` },
        { text: 'Config Persistence', link: `${l}/07-patterns/04-config-persistence` },
        { text: 'Permission Systems', link: `${l}/07-patterns/05-permissions` },
        { text: 'Event-Driven Architecture', link: `${l}/07-patterns/06-events` },
        { text: 'Performance Optimization', link: `${l}/07-patterns/07-performance` },
      ]
    },
    {
      text: 'Part 8: Tutorials',
      collapsed: true,
      items: [
        { text: 'Your First Mod', link: `${l}/08-tutorials/01-first-mod` },
        { text: 'Custom Item', link: `${l}/08-tutorials/02-custom-item` },
        { text: 'Admin Panel', link: `${l}/08-tutorials/03-admin-panel` },
        { text: 'Chat Commands', link: `${l}/08-tutorials/04-chat-commands` },
        { text: 'Starting from a Mod Template', link: `${l}/08-tutorials/05-mod-template` },
        { text: 'Debugging & Testing', link: `${l}/08-tutorials/06-debugging-testing` },
        { text: 'Publishing to Workshop', link: `${l}/08-tutorials/07-publishing-workshop` },
        { text: 'HUD Overlay', link: `${l}/08-tutorials/08-hud-overlay` },
        { text: 'Professional Template', link: `${l}/08-tutorials/09-professional-template` },
        { text: 'Vehicle Mod', link: `${l}/08-tutorials/10-vehicle-mod` },
        { text: 'Clothing Mod', link: `${l}/08-tutorials/11-clothing-mod` },
        { text: lang === 'en' ? 'Shop UI & Safe Refusal' : 'Trading System', link: `${l}/08-tutorials/12-trading-system` },
      ]
    },
    {
      text: 'Part 9: Server Administration',
      collapsed: true,
      items: [
        { text: 'Server Setup', link: `${l}/09-server-admin/01-server-setup` },
        { text: 'Directory Structure', link: `${l}/09-server-admin/02-directory-structure` },
        { text: 'serverDZ.cfg Reference', link: `${l}/09-server-admin/03-server-cfg` },
        { text: 'Loot Economy Deep Dive', link: `${l}/09-server-admin/04-loot-economy` },
        { text: 'Vehicle & Event Spawning', link: `${l}/09-server-admin/05-vehicle-spawning` },
        { text: 'Player Spawning', link: `${l}/09-server-admin/06-player-spawning` },
        { text: 'Persistence & World State', link: `${l}/09-server-admin/07-persistence` },
        { text: 'Performance Tuning', link: `${l}/09-server-admin/08-performance` },
        { text: 'Access Control', link: `${l}/09-server-admin/09-access-control` },
        { text: 'Mod Management', link: `${l}/09-server-admin/10-mod-management` },
        { text: 'Server Troubleshooting', link: `${l}/09-server-admin/11-troubleshooting` },
        { text: 'Advanced Topics', link: `${l}/09-server-admin/12-advanced` },
        { text: 'World Systems', link: `${l}/06-engine-api/23-world-systems` },
      ]
    },
    {
      text: 'Reference',
      collapsed: true,
      items: [
        { text: 'API Quick Reference', link: `${l}/06-engine-api/quick-reference` },
        { text: 'Diag Menu', link: `${l}/08-tutorials/13-diag-menu` },
        { text: 'Cheatsheet', link: `${l}/cheatsheet` },
        { text: 'Glossary', link: `${l}/glossary` },
        { text: 'FAQ', link: `${l}/faq` },
        { text: 'Troubleshooting', link: `${l}/troubleshooting` },
      ]
    },
  ]
}

export default withMermaid(
  defineConfig({
    title: 'DayZ Modding Wiki',
    description: 'Community documentation for DayZ modding — Enforce Script, mod structure, GUI, engine API, tutorials, and server administration in 12 languages',

    head: [
      ['link', { rel: 'icon', type: 'image/png', href: '/DayZ-Modding-Wiki/favicon.png' }],
      ['meta', { name: 'theme-color', content: '#1a1a2e' }],
      ['meta', { property: 'og:type', content: 'website' }],
      ['meta', { property: 'og:title', content: 'DayZ Modding Wiki' }],
      ['meta', { property: 'og:description', content: 'The most comprehensive DayZ modding documentation ever created' }],
    ],

    base: '/DayZ-Modding-Wiki/',
    srcExclude: ['AGENTS.md', 'CONTRIBUTING.md', 'CLAUDE.md', 'TEMP/**'],
    // VitePress uses this for local-search indexing and for the page-rendering
    // pass; at 1260 pages the default of 64 keeps dozens of fully rendered pages
    // resident at once. It does NOT bound Rollup's bundling memory -- see
    // .vitepress/build-memory.mts and .audit/en-2026-09-11/build-REPORT.md.
    buildConcurrency: 8,
    cleanUrls: true,
    lastUpdated: true,
    ignoreDeadLinks: [
      /LICENCE/,
      /CONTRIBUTING/,
      /04-scripting-guide/,
    ],

    locales: {
      en: { label: 'English', lang: 'en', link: '/en/' },
      pt: { label: 'Português', lang: 'pt-BR', link: '/pt/' },
      de: { label: 'Deutsch', lang: 'de', link: '/de/' },
      ru: { label: 'Русский', lang: 'ru', link: '/ru/' },
      es: { label: 'Español', lang: 'es', link: '/es/' },
      fr: { label: 'Français', lang: 'fr', link: '/fr/' },
      ja: { label: '日本語', lang: 'ja', link: '/ja/' },
      'zh-hans': { label: '简体中文', lang: 'zh-CN', link: '/zh-hans/' },
      cs: { label: 'Čeština', lang: 'cs', link: '/cs/' },
      pl: { label: 'Polski', lang: 'pl', link: '/pl/' },
      hu: { label: 'Magyar', lang: 'hu', link: '/hu/' },
      it: { label: 'Italiano', lang: 'it', link: '/it/' },
    },

    themeConfig: {
      logo: '/images/wiki-logo.png',
      siteTitle: 'DayZ Modding Wiki',

      nav: [
        { text: 'Guide', link: '/en/01-enforce-script/01-variables-types' },
        { text: 'API Reference', link: '/en/06-engine-api/quick-reference' },
        { text: 'Tutorials', link: '/en/08-tutorials/01-first-mod' },
        { text: 'Server Admin', link: '/en/09-server-admin/01-server-setup' },
        {
          text: 'Quick Links',
          items: [
            { text: 'Cheatsheet', link: '/en/cheatsheet' },
            { text: 'Glossary', link: '/en/glossary' },
            { text: 'FAQ', link: '/en/faq' },
            { text: 'Troubleshooting', link: '/en/troubleshooting' },
          ]
        }
      ],

      sidebar: {
        '/en/': sidebar('en'),
        '/pt/': sidebar('pt'),
        '/de/': sidebar('de'),
        '/ru/': sidebar('ru'),
        '/es/': sidebar('es'),
        '/fr/': sidebar('fr'),
        '/ja/': sidebar('ja'),
        '/zh-hans/': sidebar('zh-hans'),
        '/cs/': sidebar('cs'),
        '/pl/': sidebar('pl'),
        '/hu/': sidebar('hu'),
        '/it/': sidebar('it'),
      },

      socialLinks: [
        { icon: 'github', link: 'https://github.com/StarDZ-Team/DayZ-Modding-WIKI' },
      ],

      editLink: {
        pattern: 'https://github.com/StarDZ-Team/DayZ-Modding-WIKI/edit/main/:path',
        text: 'Edit this page on GitHub'
      },

      search: {
        provider: 'local',
      },

      footer: {
        message: 'Released under CC BY-SA 4.0 | Code examples under MIT License',
        copyright: '© 2026 StarDZ Team'
      },

      outline: {
        level: [2, 3],
        label: 'On this page'
      },
    },

    markdown: {
      lineNumbers: true,
    },

    vite: {
      plugins: [buildMemoryPlugin()],
      build: {
        chunkSizeWarningLimit: 3000,
      },
    },

    mermaid: {
      theme: 'dark',
    },
  })
)
