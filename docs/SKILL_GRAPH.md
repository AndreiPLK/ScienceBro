# Skill graph health (auto: tools/skill_audit.py)

Skills scanned: 46

## Orphans (no memory pointer, no skill links — invisible at recall time)

- art-bible
- game-screenshot-check
- godot-visualization
- goofy-audio-pipeline
- hotblood-vision
- lowpoly-environment
- nk-arena-style
- procgen-levels
- shooter-feel-systems
- sidera
- solution-research
- super-qa
- unreal-editor-truths

## Stale (> 21 days untouched)

- goofy-audio-pipeline (40d)
- lab (29d)
- nova (29d)
- solution-research (23d)
- studio (29d)

## Weak descriptions (< 40 chars — recall depends on these)

- hotblood-vision
- prohodimec

## Link graph

- blender-game-assets -> godot-core, godot-gamedev
- chertezhnik -> prohodimec
- creative-director -> prohodimec
- explain-to-everyone -> science-reporting
- firebird-fast-pass -> forge, producer, prohodimec
- forge -> lab, nova, producer, prohodimec, studio
- game-screenshot-check -> prohodimec
- godot-core -> godot-gamedev
- godot-visualization -> clay-velvet-style, godot-core, studio
- hotblood-vision -> lab
- lab -> forge, nova, studio
- lab-mechanics -> lab, professor, publication-pipeline, sciencebro-scientist, work-vigil
- level-building -> creative-director, prohodimec
- night-shift -> work-vigil
- nova -> forge, lab, producer, studio
- pashi -> firebird-fast-pass, forge, lab, producer, prohodimec
- producer -> lab, nova, prohodimec, studio
- professor -> science-reporting
- prover-v2 -> lab
- publication-pipeline -> lab
- reality-production -> audio-director
- ref-board -> board-of-directors
- science-night-production -> sciencebro-vigil
- science-reporting -> reality-production
- sciencebro-scientist -> reality-production, science-reporting, sciencebro-research-loop
- shooter-feel-systems -> blender-game-assets, godot-core, godot-gamedev
- sidera -> audio-director, reality-production, ref-board, studio, video-inserts
- solution-research -> creative-director, level-building
- studio -> lab, nova
- super-qa -> chertezhnik, pashi, prohodimec
- unreal-editor-truths -> firebird-fast-pass, prohodimec, unreal-mcp-workflow
- video-inserts -> ref-board
