---
marp: true
math: mathjax
paginate: true
size: 16:9
title: "Simulating Insufflation · Kick-off"
style: |
  /* palette: sim #58C4DD · vision #F0AC5F · gas/together #83C167 · highlight #F7D96F */
  section {
    background: #000;
    color: #EAEAEA;
    font-family: Calibri, Carlito, "Helvetica Neue", Arial, sans-serif;
    font-size: 25px;
    padding: 46px 64px 40px 64px;
    justify-content: flex-start;
  }
  h1, h2, h3 { font-family: Cambria, Caladea, Georgia, serif; font-weight: 400; }
  h1 { color: #ffffff; font-size: 40px; margin: 0 0 18px 0; display: inline-block; }
  h2 { color: #8A8A8A; font-size: 28px; }
  strong { color: #ffffff; }
  em { color: #F7D96F; font-style: normal; }
  code { background: #161616; color: #EAEAEA; }
  table { font-size: 22px; border-collapse: collapse; }
  table, thead, tbody, tr, th, td { background: transparent !important; }
  th { color: #8A8A8A; font-weight: 400; font-size: 17px; letter-spacing: .06em; text-transform: uppercase; }
  section table, section table td, section table th { border: 0 !important; }
  section table td, section table th { border-bottom: 1px solid #333 !important; padding: 7px 12px; }
  section::after { color: #555; font-size: 14px; }
  footer { color: #555; font-size: 16px; left: 64px; bottom: 14px; }
  .muted { color: #8A8A8A; font-size: 20px; }
  .tag { font-size: 14px; letter-spacing: .14em; text-transform: uppercase; color: #8A8A8A; margin-bottom: 6px; }
  .box { border: 1px solid #83C167; border-radius: 8px; padding: 6px 16px; background: rgba(131,193,103,.10); margin-top: 14px; }
  .warn { border: 1px solid #F7D96F; border-radius: 8px; padding: 6px 16px; background: rgba(247,217,111,.08); margin-top: 14px; }
  .box p, .warn p { margin: 4px 0; }
  .cols { display: grid; grid-template-columns: 1fr 1fr; gap: 36px; align-items: center; }
  .wide { display: grid; grid-template-columns: 3fr 2fr; gap: 28px; align-items: center; font-size: 23px; }
  img { background: transparent; }
  section.title { justify-content: center; }
  .paper { background: #ffffff; border-radius: 10px; padding: 10px 14px; display: table; margin: 4px 0 8px 0; }
  .paper img { display: block; }
  .video { background: #ffffff; border-radius: 10px; padding: 6px; display: table; margin: 4px auto 8px auto; }
  .video video { display: block; }
  .small { font-size: 22px; }
  .tight { font-size: 19px; gap: 24px; align-items: start; margin-top: 8px; }
  .refs { font-size: 18px; line-height: 1.35; }
  .refs li { margin: 2px 0; }
  .params { display: grid; grid-template-columns: 1fr 0.85fr 1.45fr 1.6fr; gap: 14px; align-items: start; font-size: 22px; margin-bottom: 4px; }
  .params > div { text-align: center; }
  .params p { margin: 0; }
  .params .lbl { color: #8A8A8A; font-size: 20px; }
  .params .plist { text-align: left; font-size: 24px; line-height: 1.7; align-self: center; }
  .params .lbl + p { margin-top: 6px; }
  section.section { justify-content: center; }
  section.section h1 { font-size: 56px; }
  section.section p { color: #8A8A8A; font-size: 26px; max-width: 85%; }
  section.title h1 { font-size: 58px; }
  .flow { display: flex; align-items: stretch; gap: 10px; font-size: 20px; margin: 10px 0 14px 0; }
  .flow .st { flex: 1; border: 1px solid #F0AC5F; background: rgba(240,172,95,.10); border-radius: 8px; padding: 8px 10px; text-align: center; }
  .flow .st b { display: block; color: #F0AC5F; margin-bottom: 4px; }
  .flow .ar { align-self: center; color: #8A8A8A; font-size: 26px; }
  .flow .fb { flex-basis: 100%; }
  .chip { display: inline-block; font-size: 14px; padding: 1px 8px; border-radius: 10px; margin: 3px 2px 0 2px; background: #2a2a2a; color: #EAEAEA; }
  .chip.pc { background: #3a2530; } .chip.hu { background: #1e3340; }
  .flow.a .st { border-color: #58C4DD; background: rgba(88,196,221,.10); } .flow.a .st b { color: #58C4DD; }
  .lane { font-size: 15px; color: #8A8A8A; margin: 0; }
  .mid { display: flex; gap: 10px; align-items: center; justify-content: center; font-size: 19px; margin: 4px 0; }
  .mid .st { border: 1px solid #83C167; background: rgba(131,193,103,.10); border-radius: 8px; padding: 6px 14px; text-align: center; }
  .mid .st b { color: #83C167; }
  .ph { border: 1px dashed #F7D96F; border-radius: 10px; padding: 14px 22px; margin-top: 10px; background: rgba(247,217,111,.06); }
  .cite { position: absolute; left: 64px; right: 110px; bottom: 16px; font-size: 14px; line-height: 1.3; color: #8A8A8A; border-top: 1px solid #333; padding-top: 6px; }
  .cite p { margin: 0; }
  .tl td:first-child { white-space: nowrap; color: #58C4DD; font-weight: bold; }

  /* Adrian's slides */
  .sim { color: #58C4DD; } .vis { color: #F0AC5F; } .gas { color: #83C167; } .hl { color: #F7D96F; }
  .face { position: absolute; right: 64px; bottom: 40px; width: 190px; height: 190px; border-radius: 50%;
          border: 1px dashed #555; display: flex; align-items: center; justify-content: center; color: #666; font-size: 13px; }
  section.title .sub { font-size: 22px; color: #8A8A8A; margin-top: 18px; }
  section.title .names { font-size: 20px; margin-top: 64px; }
  section.title .tutor { font-size: 17px; color: #8A8A8A; margin-top: 10px; }
  .problem { display: grid; grid-template-columns: 860px 1fr; gap: 34px; }
  .problem video { width: 860px; height: 484px; display: block; }
  .goal h3 { color: #F7D96F; font-size: 25px; margin: 0 0 8px 0; }
  .goal p { font-size: 18px; line-height: 1.35; margin: 0; }
  .top { display: grid; grid-template-columns: 500px 246px 1fr; gap: 34px; }
  .top img { width: 100%; height: 279px; object-fit: cover; display: block; }
  .cap { font-size: 13px; color: #8A8A8A; margin-top: 6px; }
  .cap2 { display: flex; justify-content: space-around; font-size: 13px; color: #8A8A8A; margin-top: 6px; }
  .facts p { font-size: 17px; line-height: 1.3; margin: 0 0 12px 0; color: #CFCFCF; }
  .facts b { display: block; }
  .questions { width: 840px; border-top: 1px solid #333; margin-top: 20px; padding-top: 10px; }
  .questions h3 { font-size: 22px; margin: 0 0 6px 0; color: #fff; }
  .questions li { font-size: 17px; color: #CFCFCF; margin: 4px 0; }
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
  .bottomline { position: absolute; bottom: 44px; left: 64px; right: 64px; font-family: Cambria, Caladea, Georgia, serif; font-size: 23px; color: #F7D96F; }
  .bk td { font-size: 20px; vertical-align: top; }
  .bk th { text-align: left; }
  .owners { position: absolute; bottom: 40px; left: 64px; font-size: 16px; color: #8A8A8A; }
---
<!-- _class: title -->
<!-- _paginate: false -->

<div class="tag">AI in Surgery · WS 26/27 · Kick-off</div>

# Simulating Insufflation

<div class="sub">From the pre-operative CT to the insufflated abdomen, tuned with laparoscopic video</div>

<div class="names">Adrian Nikaeen &nbsp;·&nbsp; Boldizsar Horvath &nbsp;·&nbsp; Daria Rekretiuk &nbsp;·&nbsp; Emilian Denkov</div>
<div class="tutor">Tutor: Maximilian Fehrentz &nbsp;&nbsp;|&nbsp;&nbsp; 27.11.2026</div>

<!--
- The project: simulate how the abdomen changes under insufflation, and use the laparoscope video to make that simulation patient-specific.
-->


<!-- HIDDEN SLIDE (problem statement). To show it again: delete this line and the closing line below, and put "---" back in front of "# Problem statement".

# Problem statement

- Before laparoscopy the abdomen is **insufflated with CO₂**.
- The **abdominal wall lifts** and the **organs shift by centimetres**.
- The **pre-op CT** was taken **before** that: it no longer matches the patient on the table.
- In patients there is **no post-insufflation CT**: we don't know the insufflated anatomy.

<div class="box"><strong>Our idea:</strong> simulate the insufflation from the pre-op CT, and use the laparoscopic video to make it patient-specific.</div>

[notes:
- Insufflation inflates the abdomen with gas so the surgeon has room to work. The wall lifts and the organs move by centimetres.
- Everything we know about the patient comes from the CT taken before that, so it shows the wrong shape.
- And in patients nobody takes a second CT after insufflation, so the real insufflated anatomy is unknown.
]

END OF HIDDEN SLIDE -->

---
<div class="tag">Problem</div>

# Insufflation reshapes the abdomen

<div class="problem">
<video src="assets/insufflation.mp4" poster="assets/insufflation_poster.png" autoplay muted playsinline></video>
<div class="goal">
<h3>Our goal</h3>
<p>Predict the insufflated anatomy from the pre-op CT, then make it patient-specific with the laparoscope video.</p>
</div>
</div>

<!--
- Surgery is planned on the pre-operative CT, which is taken without gas.
- In the OR a Veress needle goes in at the umbilicus and CO2 is blown into the gap between the abdominal wall and the organs. Then the needle comes out and the first trocar keeps the pressure at 12 to 15 mmHg.
- The wall lifts by several centimetres. The organs are pushed down. The back lies on the table and stays fixed.
- So the pre-op CT (dashed line) no longer matches the patient. Planned trocar positions and wall vessels are off.
- And in patients nobody takes a second CT after insufflation, so the real insufflated anatomy is unknown. (Only for our pigs we have one.)
- Our goal: simulate the insufflation from the pre-op CT, and use the laparoscope video to make it patient-specific.
-->

---
# Motivation

<div class="small">
</div>

**Why simulate?**
- **Predict the insufflated anatomy** from the pre-op CT, where no second scan exists.
- **Keep navigation and planning valid:** CT-based overlays and port placement after insufflation.
- **Tool-tissue interaction:**

<!--

-->

---
<div class="tag">Starting point &amp; research questions</div>

# Where we start, where we go

<div class="top">
<div>
<img src="assets/newton_sim.png" alt="Interactive insufflation simulator in NVIDIA Newton">
<div class="cap"><b>Where we start:</b> interactive insufflation simulator in NVIDIA Newton</div>
</div>
<div>
<img src="assets/ct_pair.png" alt="Pre-op CT vs. simulated at 12 mmHg">
<div class="cap2"><span>pre-op CT</span><span>simulated, 12 mmHg</span></div>
</div>
<div class="facts">
<p><b>What exists</b>A pressure-driven soft-tissue simulation of the abdomen in Newton, with many open issues.</p>
<p><b class="hl">Ground truth</b>The real post-insufflation CTs of our 16&nbsp;pigs.</p>
<p><b class="gas">Where we go</b>A simulation that approximates the real insufflation.</p>
</div>
</div>

<div class="questions">

### Questions to answer

- How does soft-tissue simulation work, and which methods are relevant?
- How far can we get modelling tissue properties, attachment points and the abdominal wall, using only our existing semantics and agents?

</div>

<!--
- Starting point: Max's interactive insufflation simulator in NVIDIA Newton. A pressure-driven soft-tissue skeleton exists, with many open issues.
- Example: a human pre-op CT and the simulated state at 12 mmHg.
- Ground truth for us: the real post-insufflation CTs of the 16 pigs.
- Questions: how does soft-tissue simulation work and which methods matter? How far do we get with tissue properties, attachment points and the abdominal wall using only the segmentations and agents we already have?
- Transition: the next slides show how Bano et al. 2012 did this, which is our starting baseline.
-->

---
# Literature: FEM simulation and DejaVu

<span class="muted">Pair A</span>

<div class="ph">

**Placeholder for Pair A's slide**

- How FEM works (high level → the maths)
- DejaVu: simulation set up and combined with a real surgical image [1]
- Material point method vs. FEM, EndoGSim as an example

</div>

<div class="cite">

[1] Haouchine et al., DejaVu: Intra-operative Simulation for Surgical Gesture Rehearsal, MICCAI 2017

</div>

---
# Literature: simulating insufflation

<span class="muted">Pair A</span>

<div class="ph">

**Placeholder for Pair A's slide**

- Bano et al.: how pneumoperitoneum is modelled and validated [1]
- Anatomy: where the gas enters, which cavity unfolds, which organs sit inside or behind the peritoneum

</div>

<div class="cite">

[1] Bano et al., Simulation of Pneumoperitoneum for Laparoscopic Surgery Planning, MICCAI 2012

</div>

---
# Literature: from video pixels to the CT

<div class="wide">
<div>

![w:640](assets/graph.png)

$$P_{CT} = R^{\top}\big(Z\,K^{-1}p - t\big)$$

</div>
<div>

- **Optical tracker:** IR stereo camera, sees reflective *marker arrays* (3–4 balls in a known pattern) → their 6 DOF pose
- **Registration:** CT ↔ patient array. Multiply along the graph → *CT → camera*, per frame
- **FoundationStereo [1]:** stereo, zero-shot → **metric** depth (human)
- **Depth Anything 3 [2]:** mono → depth **up to scale**; tracked poses fix the scale (porcine)

</div>
</div>

<div class="cite">

[1] Wen et al., FoundationStereo: Zero-Shot Stereo Matching, CVPR 2025 · [2] Lin et al., Depth Anything 3, arXiv 2025

</div>

<!--
- The optical tracker sees marker arrays on the laparoscope and the patient. With calibration and registration this gives us, every frame, where the camera is in the CT.
- So each pixel becomes a ray in the CT; we only miss the depth along it.
- FoundationStereo gives metric depth from the stereo laparoscope in the human cases. Depth Anything 3 gives depth from mono video, but only up to scale, which we fix with the tracked camera motion on the porcine data.
- The tracker sees only the marker arrays, not the anatomy: the insufflation is invisible to it.

-->

---
# Literature: reconstruction with DA3 and BridgeSplat

<div class="paper">

![w:540](assets/bridgesplat_fig1.png)

</div>

<div class="cols tight">
<div>

**Depth Anything 3 [1]**
- Takes all frames of a video at once and predicts a depth map and a ray map for each; origin + depth × direction gives a 3D point per pixel, so all frames fuse into one point cloud.
- With our tracked poses as input and the scale fixed in mm, that point cloud is the insufflated surface directly in CT coordinates.

</div>
<div>

**BridgeSplat [2]** <span class="muted">(figure above)</span>
- A monocular, non-rigid reconstruction method for laparoscopic video.
- It would be used to register our patient/porcine data for our alignment with the simulation.
- Same setup as our porcine data: **CT + tracked monocular laparoscope video**

</div>
</div>

<div class="cite">

[1] Lin et al., Depth Anything 3: Recovering the Visual Space from Any Views, arXiv 2025 · [2] Fehrentz et al., BridgeSplat: Bidirectionally Coupled CT and Non-Rigid Gaussian Splatting for Deformable Intraoperative Surgical Navigation, MICCAI 2025

</div>

<!--
- BridgeSplat works on exactly our kind of data. It builds a mesh from the CT, attaches Gaussian splats to it, and renders each frame from the tracked pose.
- Since the pose is known and the Gaussians can't leave the mesh, the only way to match the video is to deform the mesh. That deformed mesh is the real tissue shape in CT coordinates.

How BridgeSplat works (briefly):
- Initialisation: segment the CT into a surface mesh and register it rigidly into the tracker frame. Attach flat 3D Gaussians to the mesh triangles: position fixed by barycentric coordinates, rotation fixed to the triangle normal; only the two in-plane scales, opacity and colour are learned.
- First frame: render, find which Gaussians are visible, and pick anchor vertices among them. Each anchor gets a learnable displacement; all other vertices are interpolated from the anchors (the deformation field).
- Every frame: deform the mesh → the Gaussians move with it → render from the tracked pose → compare with the real frame (photometric loss, surgical tools masked out) → gradients flow back to the anchor displacements.
- Regulariser: ARAP (as-rigid-as-possible) lets local patches rotate but not stretch, which keeps the deformation plausible where one camera sees little.
- Result: the fitted deformation is carried back to the CT, so the CT follows the tissue ("bidirectionally coupled").

How Depth Anything 3 works (briefly):
- Input: any number of frames, with or without camera poses. Known poses (our tracking) can be fed in through a camera token.
- Backbone: a plain DINOv2 transformer. The first 2/3 of the layers attend within each image; the last 1/3 alternate between within-image and across all frames. That cross-frame attention is what makes the views consistent with each other.
- Head (dual-DPT): one shared feature reassembly, then two branches: a depth map and a ray map (per pixel the ray origin + direction). 3D point = origin + depth × direction.
- Training: a teacher trained only on synthetic data gives sharp, complete depth; it is aligned to noisy real depth (scale + shift fit) to make pseudo-labels for the multi-view student.
- Catch for us: the depth is only up to scale, so the metric scale comes from the tracked camera motion (or the CT, or stereo).

-->

---
# Proposed solution

<p class="lane">Simulation (Pair A)</p>
<div class="flow a">
<div class="st"><b>Pre-op CT</b><span class="chip pc">porcine</span><span class="chip hu">human</span></div>
<div class="ar">→</div>
<div class="st"><b>FEM insufflation</b>Bano et al. [1]</div>
<div class="ar">→</div>
<div class="st"><b>Simulated surface</b>insufflated, in CT coordinates</div>
</div>

<div class="mid">
<div class="st"><b>⇅ Compare</b> in CT coordinates → <b>tune simulation parameters</b></div>
<div class="ar">→</div>
<div class="st"><b>Evaluate</b> vs. post-insufflation CT <span class="chip pc">porcine</span></div>
</div>

<p class="lane">Video (Pair B)</p>
<div class="flow">
<div class="st"><b>Tracked video</b><span class="chip pc">porcine: mono</span><span class="chip hu">human: stereo</span></div>
<div class="ar">→</div>
<div class="st"><b>Depth</b>DA3 [2] <span class="chip pc">porcine</span><br>FoundationStereo [3] <span class="chip hu">human</span></div>
<div class="ar">→</div>
<div class="st"><b>BridgeSplat [4]</b>deform the CT mesh to match the video</div>
<div class="ar">→</div>
<div class="st"><b>Reconstructed surface</b>in CT coordinates</div>
</div>

<div class="cite">

[1] Bano et al., MICCAI 2012 · [2] Lin et al., Depth Anything 3, arXiv 2025 · [3] Wen et al., FoundationStereo, CVPR 2025 · [4] Fehrentz et al., BridgeSplat, MICCAI 2025

</div>

<!--
- Top: Pair A simulates the insufflation from the pre-op CT, following Bano et al.
- Bottom: we reconstruct the real insufflated surface from the tracked video: depth from DA3 on porcine and FoundationStereo on human, then BridgeSplat deforms the CT mesh to match.
- Both meet in CT coordinates. The mismatch tunes the simulation's parameters, and on the porcine data we evaluate against the real post-insufflation CT, with and without the video refinement.
-->


<!-- HIDDEN SLIDE (old timeline). To show it again: delete this line and the closing line below, and put "---" back in front of "# Project timeline".

# Project timeline

<div class="tl">

| Step | Simulation (Pair A) | Video (Pair B) |
|---|---|---|
| Now | get to know the dataset | get to know the dataset; video ↔ CT visualizer; first DA3 tests, unproject into the CT |
| 1 · Porcine | reproduce Bano et al. [1], benchmark across all 16 pigs | depth per frame (DA3 + scale), checked against the post-insufflation CT |
| 2 · Human | apply to the human cases (qualitative) | stereo depth with FoundationStereo |
| 3 · Refine | ⇄ tune the simulation parameters to the video reconstruction | reconstruct the early minutes of surgery (porcine + human) |
| 4 · Evaluate | porcine: simulation **with vs. without** video refinement against the post-insufflation CT | |

</div>

<div class="warn"><strong>Interface:</strong> agree early on the coordinate frame (CT) and mesh format, so step 3 can start as soon as both sides are ready.</div>

<div class="cite">

[1] Bano et al., Simulation of Pneumoperitoneum for Laparoscopic Surgery Planning, MICCAI 2012

</div>

[notes:
- Right now both pairs get to know the data. On the video side: a video-to-CT visualizer and first DA3 tests.
- Steps 1 and 2 run in parallel: the simulation is reproduced on the pigs and then the humans; depth is built and checked against the porcine post-insufflation CT.
- Step 3 is where the two parts meet. Step 4 measures whether the video refinement helps, on the pigs.
]

END OF HIDDEN SLIDE -->

---
<div class="tag">Timeline &amp; organisation</div>

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

<div class="owners">Owners: Simulation · Adrian, Daria &nbsp;|&nbsp; 3D vision · Boldizsar, Emilian &nbsp;|&nbsp; Interface: shared CT coordinate frame + surface meshes</div>

<!--
- Course frame from Max: pitches mid October, matching, OR visits in November, kick-off presentations now, final presentations mid to late January before exam season.
- We started in early November with the reading.
- December: Bano baseline on one pig, then the benchmark over all 16 pigs. In parallel the vision side builds a video-to-CT visualizer and tests depth estimation.
- January: improve the simulation and try the human cases, reconstruct the first minutes of surgery from video, tune the simulation to it, evaluate with and without video, final presentation.
-->

---
# Conclusion

- **Problem:** insufflation moves the anatomy by centimetres, and in patients there is no post-insufflation CT
- **Simulation:** predict the insufflated anatomy from the pre-op CT, validated on 16 porcine procedures
- **Video:** reconstruct the real insufflated surface in CT coordinates and use it to tune the simulation
- **Goal:** a patient-specific insufflation model, and a first step towards physics simulation + 3D vision for harder cases (tool–tissue interaction, dissection)

<div class="box"><strong>Key question:</strong> does refining the simulation with video bring it closer to the real post-insufflation CT?</div>

<!--
- To sum up: we simulate what we can't scan, and use what we can see to make it patient-specific. The pigs tell us whether that works. Thanks, happy to take questions.
-->

---
<!-- footer: "" -->

# References

<div class="refs">

- Bano, J. et al. Simulation of Pneumoperitoneum for Laparoscopic Surgery Planning. MICCAI 2012.
- Haouchine, N. et al. DejaVu: Intra-operative Simulation for Surgical Gesture Rehearsal. MICCAI 2017.
- Hartley, R., Zisserman, A. Multiple View Geometry in Computer Vision, 2nd ed. Cambridge University Press, 2004.
- Wen, B. et al. FoundationStereo: Zero-Shot Stereo Matching. CVPR 2025. arXiv:2501.09898
- Lin, H. et al. Depth Anything 3: Recovering the Visual Space from Any Views. arXiv:2511.10647, 2025.
- Fehrentz, M. et al. BridgeSplat: Bidirectionally Coupled CT and Non-Rigid Gaussian Splatting for Deformable Intraoperative Surgical Navigation. MICCAI 2025. arXiv:2509.18501
- Kerbl, B. et al. 3D Gaussian Splatting for Real-Time Radiance Field Rendering. ACM TOG (SIGGRAPH) 2023.

</div>


---
<!-- _paginate: false -->
<div class="tag">Backup · Literature · Simulation</div>

# Beyond Bano

<div class="bk">

| | What it does | What is missing for us |
|---|---|---|
| **Bano et al.** <span class="muted">MICCAI 2012</span> | FEM insufflation from the pre-op CT with measured tissue values | No video. Only 2 pigs, one material for all organs |
| **DejaVu** <span class="muted">MICCAI 2017</span> | FEM organ model (SOFA) registered to one laparoscopic frame, deformation rendered into the real image | Manual rigid 3D/2D registration. Insufflation deformation named as open problem |
| **MPM** <span class="muted">e.g. EndoGSim</span> | Material carried by particles, physics on a background grid. No mesh to build | Different trade-off vs. FEM, fits Gaussian splats from video |

</div>

<div class="bottomline">Bano: physics without video &nbsp;·&nbsp; DejaVu: video with rigid registration &nbsp;·&nbsp; <span class="gas">us: physics tuned by video</span></div>

<!--
BACKUP, only if asked how our project differs from the literature.
- Bano (Bano et al.): FEM insufflation from the pre-op CT, but no video and only 2 pigs.
- DejaVu (Haouchine et al.): pre-op mesh + physical model in SOFA, manually registered to a single intra-op image. Its discussion says the registration has to handle the large deformation from insufflation pressure, and that patient-specific parameters are an open challenge. That is our gap.
- MPM: particles instead of a mesh, EndoGSim as an example.
-->
