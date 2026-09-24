# Fuente interna consultada

URL: https://drive.google.com/file/d/1hCktz02YRv1BK2oRZPSeIlN2hjoBWyM4/view
Consulta: 2026-09-23. Snapshot histórico; sin comprobación del runtime actual.

---
id: HarMoCAP
type: project
project: HarMoCAP
source_paths: ["HarMoCAP/README.md", "HarMoCAP/AGENTS.md", "HarMoCAP/BITACORA.md", "HarMoCAP/docs/INTERFACE_SPEC.md", "HarMoCAP/Biblioteca/INDEX.md"]
hash: null
last_compiled_at: 2026-07-27
links: [editorial-altermundi, editorial-altermundi.biblioteca, phideus, memoria-colectiva, datasets, gpu-priorityd]
---
# HarMoCAP — movimiento corporal a modulación armónica

> Path: `/mnt/m2-1TB/HarMoCAP/` (~38G). Pipeline de pose/tracking en tiempo real hacia controles de modulación del ecosistema Harmonic Beacon.

## Qué es

Capas de percepción (pose YOLO/Ultralytics), temporalidad (identidad, tracking), representación de movimiento y emisión de un **contrato OSC versionado** para consumidores (p. ej. harmonic-weaver / kits de Nico). Separa utilidad ingenieril de cualquier claim HIT o clínico.

## Estado (2026-07)

- Modelos y kits en repo (`harmocap-m-pose-ft2.*`, `harmocap-nico-kit/`, `runs/`, `outputs/`).
- **Contratos OSC sucesivos** (cada uno con `contract_id` nuevo; el receptor viejo gatea el stream):
  - **1.2** — mensaje `/harmocap/v1/crowd` (agregados de multitud) + modos grupo/masa.
  - **1.3** — tempo por persona (`tempo_bpm`, `beat_phase`, `tempo_conf`); vector 21→24 features; fix de validez de `qom`/expansion en video real.
  - **1.4** — masa por densidad (`mass_present`, `mass_active`) en modo masa.
- La línea en vivo de consumidores que seguía en 1.1 acumula el salto **1.1 → 1.4** (conviene migrar una sola vez).

## Relaciones

- **[[editorial-altermundi]] / biblioteca** — pack técnico inicial y marco Beacon/HIT.
- **[[phideus]]** — programa teórico compartido, sin dependencia de código.
- **[[datasets]]** — COCO/pose compartidos en el disco.
- **[[memoria-colectiva]]** — mensajes recursivos e inbox de contratos.

## Notas

- Excluir `data/`, `runs/`, `outputs/`, modelos `.pt/.onnx`, `.git`.
- Tamaño creció por pesos y corridas; el submapa no inventaría métricas de latencia no citadas en docs.
