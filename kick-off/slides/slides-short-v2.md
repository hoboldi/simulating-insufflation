---
marp: true
math: mathjax
paginate: true
size: 16:9
title: "Simulating Insufflation · Kick-off (v2)"
style: |
  /* palette: sim #58C4DD · vision #F0AC5F · gas/together #83C167 · highlight #F7D96F */
  section {
    background: #000;
    color: #EAEAEA;
    font-family: Calibri, Carlito, "Helvetica Neue", Arial, sans-serif;
    font-size: 22px;
    padding: 43px 58px 40px 58px;
    justify-content: flex-start !important;
    place-content: start !important;
  }
  /* slide number bottom-left, keeps bottom-right free for the camera */
  section::after { left: 58px; right: auto; bottom: 14px; color: #666; font-size: 13px; }
  h1, h2, h3 { font-family: Cambria, Caladea, Georgia, serif; font-weight: 400; color: #fff; margin: 0; }
  h1 { font-size: 40px; margin: 0 0 22px 0; }
  strong, b { color: #fff; }
  .tag { font-size: 14px; letter-spacing: .14em; text-transform: uppercase; color: #8A8A8A; margin-bottom: 6px; }
  .muted { color: #8A8A8A; }
  .soft { color: #CFCFCF; }
  .sim { color: #58C4DD; } .vis { color: #F0AC5F; } .gas { color: #83C167; } .hl { color: #F7D96F; }
  .note { font-size: 15px; color: #8A8A8A; }
  .foot { position: absolute; left: 58px; right: 58px; bottom: 44px; }
  .foot.hlt { color: #F7D96F; font-size: 18px; }
  table { border-collapse: collapse; width: 100%; display: table; font-size: 19px; }
  table, thead, tbody, tr, th, td { background: transparent !important; }
  section table, section table td, section table th { border: 0 !important; }
  section table td, section table th { border-bottom: 1px solid #333 !important; padding: 8px 12px; text-align: left; vertical-align: top; }
  th { color: #8A8A8A; font-weight: 400; font-size: 15px; letter-spacing: .06em; text-transform: uppercase; }

  /* title */
  section.title { justify-content: center !important; place-content: safe center !important; }
  section.title h1 { font-size: 58px; margin: 0; }
  section.title .sub { font-size: 22px; color: #8A8A8A; margin-top: 18px; }
  section.title .names { font-size: 19px; margin-top: 64px; }
  section.title .tutor { font-size: 17px; color: #8A8A8A; margin-top: 10px; }

  /* problem */
  .bigvideo { width: 812px; height: 460px; display: block; }

  /* motivation */
  .two { display: grid; grid-template-columns: 1fr 1fr; gap: 38px; }
  .card { border: 1px solid #3A3A3A; border-radius: 10px; background: #0D0D0D; padding: 18px 26px 20px 26px; }
  .card h3 { font-size: 23px; margin-bottom: 8px; }
  .card p { font-size: 16px; line-height: 1.35; color: #CFCFCF; margin: 0 0 12px 0; }
  .card img { width: 100%; display: block; }

  /* starting point */
  .top { display: grid; grid-template-columns: 507px 250px 1fr; gap: 36px; }
  .top img { width: 100%; height: 283px; object-fit: cover; display: block; }
  .cap { font-size: 13px; color: #8A8A8A; margin-top: 6px; }
  .cap2 { display: flex; justify-content: space-around; font-size: 13px; color: #8A8A8A; margin-top: 6px; }
  .facts p { font-size: 17px; line-height: 1.3; margin: 0 0 12px 0; color: #CFCFCF; }
  .facts b { display: block; }
  .questions { width: 845px; border-top: 1px solid #333; margin-top: 20px; padding-top: 10px; }
  .questions h3 { font-size: 22px; margin-bottom: 6px; }
  .questions li { font-size: 17px; color: #CFCFCF; margin: 4px 0; }

  /* Bano */
  .lead { font-size: 16px; color: #CFCFCF; margin: -8px 0 14px 0; }
  .bano { display: grid; grid-template-columns: 250px 1fr 270px; gap: 18px; align-items: stretch; }
  .panel { border: 1px solid #3A3A3A; border-radius: 10px; padding: 12px 14px; text-align: center; }
  .panel h3 { font-size: 17px; line-height: 1.2; margin-bottom: 10px; }
  .panel img { width: 100%; border-radius: 4px; display: block; }
  .panel .c { font-size: 13px; color: #CFCFCF; margin-top: 10px; }
  .steps { display: flex; gap: 8px; margin: 14px 0 10px 0; }
  .steps div { flex: 1; border: 1px solid #58C4DD; background: rgba(88,196,221,.10); border-radius: 6px; padding: 6px 4px; font-size: 14px; }
  .steps div span { display: block; color: #8A8A8A; font-size: 11px; }
  .steps div i { display: block; font-style: normal; color: #8A8A8A; font-size: 12px; margin-top: 6px; }

  /* flows (3D vision, MPM, joint) */
  .flow { display: flex; align-items: center; gap: 12px; margin: 10px 0 30px 0; }
  .flow .st { flex: 1; border: 1px solid #F0AC5F; background: rgba(240,172,95,.10); border-radius: 8px; padding: 14px 10px; text-align: center; font-size: 17px; }
  .flow.s .st { border-color: #58C4DD; background: rgba(88,196,221,.10); }
  .flow .ar { color: #8A8A8A; font-size: 22px; }
  .pair { display: grid; grid-template-columns: 1fr 1fr; gap: 48px; }
  .pair h3 { font-family: Calibri, Carlito, sans-serif; font-size: 21px; color: #F0AC5F; margin-bottom: 8px; }
  .pair p { font-size: 17px; margin: 0 0 6px 0; }
  .mpmviz { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; text-align: center; font-size: 28px; color: #8A8A8A; margin: 8px 0 18px 0; }
  .dots { letter-spacing: 12px; line-height: 1.1; color: #58C4DD; font-size: 22px; }
  .dots.g { color: #83C167; } .dots.o { color: #F0AC5F; }
  .joint { display: grid; grid-template-columns: 190px 30px 230px 40px 1fr; row-gap: 40px; align-items: center; margin-top: 18px; }
  .joint .st { border: 1px solid #58C4DD; background: rgba(88,196,221,.10); border-radius: 8px; padding: 12px; text-align: center; font-size: 17px; }
  .joint .st.v { border-color: #F0AC5F; background: rgba(240,172,95,.10); }
  .joint .big { grid-row: 1 / span 2; grid-column: 5; border: 1px solid #83C167; background: rgba(131,193,103,.10); border-radius: 10px; padding: 26px; text-align: center; font-size: 18px; }
  .joint .big span { display: block; color: #83C167; font-size: 16px; margin-top: 14px; }
  .joint .ar { color: #8A8A8A; text-align: center; font-size: 22px; }

  /* timeline */
  .frame { font-size: 15px; color: #8A8A8A; margin-bottom: 24px; }
  .tlg { display: grid; grid-template-columns: 150px repeat(5, 1fr); row-gap: 10px; column-gap: 6px; position: relative; }
  .tlg .h { font-size: 13px; letter-spacing: .1em; text-transform: uppercase; color: #8A8A8A; border-bottom: 1px solid #333; padding-bottom: 6px; }
  .tlg .h.done { color: #555; }
  .tlg .ln { font-family: Cambria, Caladea, serif; font-size: 21px; align-self: center; }
  .bar { border-radius: 6px; padding: 9px 10px; font-size: 15px; line-height: 1.2; border: 1px solid; color: #EAEAEA; }
  .bar.s { border-color: #58C4DD; background: rgba(88,196,221,.16); }
  .bar.v { border-color: #F0AC5F; background: rgba(240,172,95,.16); }
  .bar.g { border-color: #83C167; background: rgba(131,193,103,.16); }
  .bar.y { border-color: #F7D96F; background: rgba(247,217,111,.14); }
  .bar.done { border-color: #555; background: rgba(85,85,85,.25); color: #AAA; }
  .holiday { position: absolute; top: 34px; bottom: -26px; left: calc(150px + (100% - 150px) * 0.51); width: calc((100% - 150px) * 0.15);
             background: rgba(255,255,255,.07); font-size: 11px; color: #777; display: flex; align-items: flex-end; justify-content: center; padding-bottom: 4px; }
  .ms { position: relative; margin: 50px 0 0 156px; height: 70px; border-top: 1px solid #555; }
  .ms div { position: absolute; top: -8px; width: 160px; margin-left: -80px; text-align: center; font-size: 15px; }
  .ms div::before { content: ""; display: block; width: 14px; height: 14px; border-radius: 50%; margin: 0 auto 8px; border: 1.5px solid #F7D96F; background: #000; }
  .ms div.done::before { background: #F7D96F; }
  .ms span { display: block; color: #8A8A8A; }

  /* goals */
  .goal { display: grid; grid-template-columns: 70px 1fr; gap: 10px; margin: 0 0 34px 0; font-size: 22px; }
  .goal .n { color: #58C4DD; font-size: 26px; }

  /* long-term */
  .lt { display: grid; grid-template-columns: 1fr 330px; gap: 30px; }
  .lt img { width: 100%; display: block; }
  .lt li { font-size: 19px; margin: 0 0 10px 0; }
  .refs p { font-size: 19px; margin: 0 0 12px 0; }
---

<!-- _class: title -->
<!-- _paginate: false -->

<div class="tag">AI in Surgery · WS 26/27 · Kick-off</div>

# Simulating Insufflation

<div class="sub">From the pre-operative CT to the insufflated abdomen, tuned with laparoscopic video</div>

<div class="names">Adrian Nikaeen &nbsp;·&nbsp; Boldizsar Horvath &nbsp;·&nbsp; Daria Rekretiuk &nbsp;·&nbsp; Emilian Denkov</div>
<div class="tutor">Tutor: Maximilian Fehrentz &nbsp;&nbsp;|&nbsp;&nbsp; 27.11.2026</div>

---

<div class="tag">01 · Problem</div>

# Insufflation changes the anatomy

<video class="bigvideo" src="assets/problem_ct_insufflation.mp4" poster="assets/problem_ct_insufflation_poster.png" autoplay loop muted playsinline></video>

<!--
- Surgery is planned on the pre-operative CT, which is taken without gas.
- In the OR CO2 is blown into the gap between the abdominal wall and the organs, held at 12 to 15 mmHg.
- The wall lifts by several centimetres and the organs are pushed down. The back lies on the table and stays fixed.
- So the pre-op CT no longer matches the patient. Planned trocar positions and wall vessels are off.
- And in patients nobody takes a second CT after insufflation, so the real insufflated anatomy is unknown. (Only for our pigs we have one.)
-->

---

<div class="tag">02 · Motivation</div>

# Why it also matters for guidance and simulation

<div class="two">
<div class="card">
<h3><span class="sim">1</span>&nbsp; Intra-operative guidance</h3>
<p>After insufflation the organs shift and deform. The pre-op 3D mesh no longer matches the camera image, so a rigid registration is not enough. A good prediction of the insufflated anatomy gives the registration a much better starting point.</p>
<img src="assets/dejavu_liver.png" alt="DejaVu 2017, liver case (Haouchine et al., Fig. 3)">
</div>
<div class="card">
<h3><span class="gas">2</span>&nbsp; Surgical physics simulation</h3>
<p>Simulators for rehearsal, tool–tissue interaction or cutting start from the pre-op CT shape. Without insufflation, every later step runs on the wrong geometry. DejaVu names this deformation as an open problem.</p>
<img src="assets/dejavu_kidney.png" alt="DejaVu 2017, kidney case (Haouchine et al., Fig. 3)">
</div>
</div>

<div class="foot hlt" style="right: 300px"><b class="hl">Why start with insufflation?</b> It is the first deformation in every laparoscopy, before any cutting, and for the porcine cases we have the post-insufflation CT as ground truth.</div>

<!--
MOTIVATION (about 1 min)
- Two reasons beyond planning.
- 1, guidance: overlaying the pre-op model on the video needs a registration. After insufflation the organs have moved, so a rigid alignment fails. If we can predict the insufflated anatomy, registration starts much closer to the truth.
- 2, simulation: any physics simulator (rehearsal like DejaVu, tool-tissue interaction, cutting) starts from the pre-op shape. If insufflation is missing, everything afterwards is computed on the wrong geometry. DejaVu's authors name exactly this deformation as an open problem.
- Images are from DejaVu (Haouchine et al. 2017), not our results.
- Why insufflation first: it happens in every laparoscopy, before cutting, and the pig CTs give us ground truth.
-->

---

<div class="tag">03 · Starting point &amp; research questions</div>

# Where we start, where we go

<div class="top">
<div>
<img src="assets/newton_sim.png" alt="Interactive insufflation simulator in NVIDIA Newton">
<div class="cap"><b>Where we start:</b> interactive insufflation simulator in NVIDIA Newton</div>
</div>
<div>
<img src="assets/ct_pair.png" alt="Sagittal CT: human pre-op vs. simulated at 12 mmHg">
<div class="cap2"><span>pre-op CT</span><span>simulated, 12 mmHg</span></div>
</div>
<div class="facts">
<p><b>What exists</b>A pressure-driven soft-tissue simulation of the abdomen in Newton, with many open issues.</p>
<p><b class="hl">Ground truth</b>The real post-insufflation CTs of our 16&nbsp;porcine.</p>
<p><b class="gas">Where we go</b>A simulation that approximates the real insufflation.</p>
</div>
</div>

<div class="questions">

### Questions to answer

- How does soft-tissue simulation work, and which methods are relevant?
- How far can we get modelling tissue properties, attachment points and the abdominal wall, using only our existing semantics and agents?

</div>

<!--
WHERE WE START, WHERE WE GO (about 1 min)
- Starting point: Max's interactive insufflation simulator in NVIDIA Newton. A pressure-driven soft-tissue skeleton exists, with many open issues.
- Example on the right: a human pre-op CT and the simulated state at 12 mmHg.
- Ground truth for us: the real post-insufflation CTs of the 16 pigs.
- Questions: how does soft-tissue simulation work and which methods matter? How far do we get with tissue properties, attachment points and the abdominal wall using only the semantics (segmentations) and agents we already have?
- Transition: the next slides show how Bano et al. 2012 did this, which is our starting baseline.
-->

---

<div class="tag">04 · Literature · Simulation</div>

# Bano et al. 2012: from pre-op CT to predicted anatomy

<div class="lead">Anatomy before insufflation → biomechanical simulation → estimated shape after insufflation.</div>

<div class="bano">
<div class="panel">
<h3>Initial state<br>Pre-operative CT</h3>
<img src="assets/bano_ct.jpg" alt="Pre-operative CT">
<div class="c">Before CO₂ insufflation</div>
</div>
<div class="panel">
<h3>Simulation pipeline</h3>
<div class="steps">
<div><span>1</span>Segment<i>3D anatomy</i></div>
<div><span>2</span>Mesh<i>surface + volume</i></div>
<div><span>3</span>Materials<i>tissue stiffness</i></div>
<div><span>4</span>Simulate<i>FEM + pressure</i></div>
<div><span>5</span>Evaluate<i>against CT</i></div>
</div>
<div class="c hl">Pressure-driven tissue deformation with contacts</div>
</div>
<div class="panel">
<h3>Output<br>Predicted insufflated anatomy</h3>
<img src="assets/bano_predicted.jpg" alt="Predicted insufflated anatomy">
<div class="c">Estimated post-gas shape</div>
</div>
</div>

<div class="foot" style="bottom: 40px">
<div class="hl" style="font-size: 16px">Bano et al. report mean errors of roughly 3–6 mm for selected structures in two porcine subjects.</div>
<div class="note" style="font-size: 12px">Images are illustrative; they are not actual patient scans or measured predictions from the paper.</div>
</div>

<!--
LITERATURE: SIMULATION, Bano et al. MICCAI 2012 (about 1 min)
- Pre-op CT is segmented into three regions: abdominal wall, abdominal viscera, thoracic viscera. Arteries optional if contrast.
- Tetrahedral volume meshes for FEM, surface meshes for collision.
- Material: wall E = 24 kPa (nu = 0.49), viscera 15 kPa, thoracic 7 kPa, diaphragm ten times the wall. Measured values, not fitted.
- Simulation in SOFA: inverse gravity first (the CT already contains gravity), then 12 mmHg on the inner wall surface, back fixed on the table.
- Result on 2 pigs: about 3 to 4 mm mean error for skin, wall and organs, about 5 mm for the arteries.
- This is our step 1 baseline.
-->

---

<div class="tag">05 · Data</div>

# What we work with

| | <span class="hl">Porcine · 16 cases</span> | <span class="hl">Human · 3 cases</span> |
|---|---|---|
| CT | Before and after insufflation | Pre-op contrast CT only |
| Segmentations | Vessels, ureters, tumour mimic; organs being added | Organs |
| Video | Tracked monocular | Tracked stereo |
| Evaluation | Post-insufflation CT reference | Qualitative check; registration varies |

<div class="foot note">Data remain on the chair’s cluster. Representative project images still need to be added.</div>

---

<div class="tag">06 · 3D vision</div>

# From laparoscopic video to 3D

<div class="flow">
<div class="st">Tracked laparoscopic video</div><div class="ar">→</div>
<div class="st">Depth estimation</div><div class="ar">→</div>
<div class="st">3D surface in CT coordinates</div>
</div>

<div class="pair">
<div>

### Porcine data
Monocular video · Depth Anything 3

Recover and verify scale using available tracking and calibration.

</div>
<div>

### Human data
Stereo video · FoundationStereo

Assess reconstruction and registration quality.

</div>
</div>

<div class="foot note">Related work: BridgeSplat (MICCAI 2025). Method details to be confirmed by Pair B.</div>

---

<div class="tag">07 · Simulation · MPM</div>

# MPM: linking computer vision and simulation

<div class="vis" style="font-size: 20px; margin-bottom: 4px">Material Point Method</div>

Particles carry tissue properties and motion; a background grid is used to compute forces and update motion.

<div class="flow s" style="margin-bottom: 6px">
<div class="st">CT + reconstructed surface</div><div class="ar">→</div>
<div class="st">Material points ↔ grid</div><div class="ar">→</div>
<div class="st">Deformed geometry</div>
</div>

<div class="mpmviz">
<div class="dots">●●●●●●<br>●●●●●●<br>●●●●●●</div>
<div class="dots g">▦▦▦▦▦▦<br>▦▦▦▦▦▦<br>▦▦▦▦▦▦</div>
<div class="dots o">●&nbsp;●&nbsp;●&nbsp;●<br>&nbsp;●&nbsp;●&nbsp;●&nbsp;●<br>&nbsp;&nbsp;●&nbsp;●&nbsp;●&nbsp;●</div>
</div>

<div class="foot vis" style="font-size: 18px">Proposed coupling: initialize a physical representation from aligned geometry, simulate deformation, compare with video observations.</div>

<!--
MPM transfers particle mass and momentum to a grid, updates the grid using forces, then transfers updates back to particles. Video observations constrain the geometry; material parameters and boundary conditions still need to be specified. EndoGSim is a related example. This is a proposed interface, not a completed implementation.
-->

---

<div class="tag">08 · Joint approach</div>

# Putting both modalities together

<div class="joint">
<div class="st">Pre-op CT</div><div class="ar">→</div><div class="st">FEM insufflation baseline</div><div class="ar">↘</div>
<div class="big">Shared CT space<br>MPM coupling (proposed)<span>Compare and refine using video</span></div>
<div class="st v">Tracked video</div><div class="ar">→</div><div class="st v">Reconstructed 3D surface</div><div class="ar">↗</div>
</div>

<div class="foot hlt">Evaluate baseline vs. refined geometry against post-insufflation CT (porcine).</div>

<!--
The post-insufflation CT is a reference for evaluation, not an input to video-guided refinement. The exact MPM interface remains to be defined.
-->

---

<div class="tag">09 · Timeline &amp; organisation</div>

# Plan

<div class="frame"><b>Course frame:</b> 16.10 pitches · 19.10 matching · Nov OR visits · 27.11 kick-off presentations · mid–late Jan final presentations (before exam season, Prof. Navab attends)</div>

<div class="tlg">
  <div></div><div class="h done">Nov</div><div class="h">Dec I</div><div class="h">Dec II</div><div class="h">Jan I</div><div class="h">Jan II</div>

  <div class="ln sim">Simulation</div>
  <div class="bar done">Reading: FEM, Bano, DejaVu</div>
  <div class="bar s">Bano setup on 1 pig</div>
  <div class="bar s">Benchmark 16 pigs</div>
  <div class="bar s">Improve + human cases</div>
  <div></div>

  <div class="ln vis">3D vision</div>
  <div class="bar done">Reading: BridgeSplat, DA3</div>
  <div class="bar v" style="grid-column: span 2">Video↔CT visualizer, DA3 tests</div>
  <div class="bar v">Reconstruct early minutes</div>
  <div></div>

  <div class="ln gas">Together</div>
  <div></div><div></div><div></div>
  <div class="bar g">Tune sim to video</div>
  <div class="bar y">Evaluate + final pres.</div>

  <div class="holiday">holidays</div>
</div>

<div class="ms">
  <div class="done" style="left: 3%">early Nov<span>Project start</span></div>
  <div class="done" style="left: 18%">27.11<span>Kick-off pres.</span></div>
  <div style="left: 40%">mid Dec<span>Bano baseline runs</span></div>
  <div style="left: 62%">early Jan<span>16-pig benchmark</span></div>
  <div style="left: 91%">mid–late Jan<span>Final presentation</span></div>
</div>

<div class="foot note" style="font-size: 16px">Owners: Simulation · Adrian, Daria &nbsp;|&nbsp; 3D vision · Boldizsar, Emilian &nbsp;|&nbsp; Interface: shared CT coordinate frame + surface meshes</div>

<!--
TIMELINE (about 1 min)
- Course frame from Max: pitches mid October, matching, OR visits in November, kick-off presentations now, final presentations mid to late January before exam season.
- We started in early November with the reading (simulation: FEM, Bano, DejaVu. Vision: BridgeSplat, Depth Anything 3, FoundationStereo).
- December: Bano baseline on one pig, then the benchmark over all 16 pigs. In parallel the vision side builds a video-to-CT visualizer and tests depth estimation.
- January: improve the simulation and try the human cases, reconstruct the first minutes of surgery from video, tune the simulation to it, evaluate with and without video, final presentation.
- Holidays end of December are blocked out.
-->

---

<div class="tag">10 · Project goals</div>

# What we aim to achieve

<div class="goal"><div class="n">01</div><div>Establish a CT-based insufflation baseline and assess how far existing methods get on our data.</div></div>
<div class="goal"><div class="n">02</div><div>Reconstruct visible anatomy from tracked video and align it with the CT representation.</div></div>
<div class="goal"><div class="n">03</div><div>Bring both modalities into a shared simulation environment and evaluate video-guided refinement.</div></div>

<div class="foot hlt">Insufflation is our initial use case for multimodal coupling.</div>

---

<div class="tag">11 · Long-term vision</div>

# What this could enable next

<div class="lt">
<div>
<img src="assets/dejavu_liver.png" alt="DejaVu 2017, liver case">
<p class="gas" style="font-size: 22px; margin-top: 22px">CT + video kept in sync through a biomechanical model</p>
</div>
<div>

- Reconstruct tools in 3D
- Transfer observed tool–tissue interactions into simulation
- Estimate deformation of structures hidden from the camera

</div>
</div>

<div class="foot note">Future research direction, not a deliverable of the current project.</div>

<!--
If initial alignment works, tools could be reconstructed with depth estimation and segmentation (e.g. SAM), then used to drive physical simulation. Internal deformation would be a model estimate, not directly observed in the video.
-->

---

<div class="tag">References</div>

# Related work

<div class="refs">

Bano J. et al. Simulation of Pneumoperitoneum for Laparoscopic Surgery Planning. MICCAI 2012.

Haouchine N. et al. DejaVu: Intra-operative Simulation for Surgical Gesture Rehearsal. MICCAI 2017.

BridgeSplat (MICCAI 2025); Depth Anything 3; FoundationStereo; EndoGSim.

</div>

<div class="foot note">Published figures supplied by the team. MPM and joint workflow diagrams are schematic.</div>

---

<!-- _paginate: false -->
<div class="tag">Backup</div>

# Beyond Bano

| | What it does | What is missing for us |
|---|---|---|
| **Bano et al.** <span class="muted">MICCAI 2012</span> | FEM insufflation from the pre-op CT with measured tissue values | No video. Only 2 pigs, one material for all organs |
| **DejaVu** <span class="muted">MICCAI 2017</span> | FEM organ model (SOFA) registered to one laparoscopic frame, deformation rendered into the real image | Manual rigid 3D/2D registration. Insufflation deformation named as open problem |
| **MPM** <span class="muted">e.g. EndoGSim</span> | Material carried by particles, physics on a background grid. No mesh to build | Different trade-off vs. FEM, fits Gaussian splats from video |

<div class="foot" style="font-family: Cambria, Caladea, serif; font-size: 22px"><span class="hl">Bano: physics without video &nbsp;·&nbsp; DejaVu: video with rigid registration</span> &nbsp;·&nbsp; <span class="gas">us: physics tuned by video</span></div>

<!--
BACKUP, only if asked how our project differs from the literature.
- DejaVu (Haouchine et al.): pre-op mesh + physical model in SOFA, manually registered to a single intra-op image, then appearance and lighting are estimated so simulated gestures look real.
- Its discussion explicitly says the registration has to handle the large deformation from insufflation pressure, and that patient-specific parameters are an open challenge. That is our gap.
- MPM: one sentence of contrast with FEM, EndoGSim as example.
-->
