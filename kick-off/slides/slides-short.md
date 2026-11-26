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

  /* Pair B (3D vision) slides */
  .data { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; align-items: start; margin-top: 12px; }
  .data h3 { color: #F0AC5F; font-size: 26px; margin: 0 0 6px 0; }
  .data .ph { height: 170px; margin: 0 0 8px 0; padding: 10px 18px; display: flex; align-items: center; justify-content: center; text-align: center; font-size: 17px; color: #CFCFCF; }
  .data li { font-size: 21px; margin: 2px 0; }
  .io { display: grid; grid-template-columns: 150px 1fr 1fr; column-gap: 24px; align-items: center; font-size: 19px; line-height: 1.3; }
  .io > div { padding: 7px 4px; border-bottom: 1px solid #333; }
  .io .hd { font-size: 22px; border-bottom: 0; }
  .io .hd b { color: #F0AC5F; font-weight: 400; font-family: Cambria, Caladea, Georgia, serif; font-size: 25px; }
  .io .fig { border-bottom: 0; padding: 0 0 6px 0; }
  .io .fig img { display: block; width: 100%; height: 150px; object-fit: contain; background: #fff; border-radius: 8px; padding: 4px; box-sizing: border-box; }
  .io .lbl { color: #8A8A8A; font-size: 15px; letter-spacing: .06em; text-transform: uppercase; }
  .flow .st.q { border-style: dashed; border-color: #F7D96F; background: rgba(247,217,111,.06); }
  .flow .st.q b { color: #F7D96F; }
  .oq { border: 1px dashed #F7D96F; border-radius: 8px; padding: 6px 16px; background: rgba(247,217,111,.06); font-size: 18px; margin-top: 4px; }
  .oq p { margin: 2px 0; }
  .oq ul { margin: 2px 0; }
  .oq li { margin: 1px 0; }
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
<div class="tag">3D vision · our data</div>

# Two kinds of video: mono pigs, stereo humans

<span class="muted">The simulation predicts the insufflated shape. The video shows the real one, but only what the camera sees. What we can measure depends on the camera.</span>

<div class="data">
<div>

<h3>Porcine · 16 procedures</h3>

<div class="ph">Visual from the cluster: one laparoscope frame, next to the post-insufflation CT surface with the tracked camera path</div>

- **Mono** laparoscope, tracked
- CT **before and after** insufflation
- One camera: depth only **up to scale**
- Ground truth: the post-insufflation CT

</div>
<div>

<h3>Human · 3 cases, more coming</h3>

<div class="ph">Visual from the cluster: one left/right stereo pair, next to the pre-op CT surface with the tracked camera path</div>

- **Stereo** laparoscope, tracked (robotic and conventional)
- Pre-op CT only
- Two cameras: **metric** depth
- No ground truth: qualitative check only

</div>
</div>

<!--
- Transition from the simulation part: the simulation gives a prediction of the insufflated abdomen. The video is our only observation of the real one, inside the patient, but only of the surface the camera sees.
- Porcine: 16 procedures, one camera. From one camera you can't tell a small, near scene from a large, far one, so the depth has no absolute scale. But we have the CT after insufflation, so we can check our reconstruction against the real shape.
- Human: 3 cases so far, stereo. Two cameras a known distance apart give depth in millimetres directly. But there is no CT after insufflation, so we can only check the result qualitatively.
- Both are tracked. The next slide shows what that gives us.
-->

---
<div class="tag">3D vision · from video to the CT</div>

# Putting the video into the CT

<div class="wide">
<div>

<!-- TODO: add or swap in the tracking photo from Max's slides -->
![w:600](assets/graph.png)

$$P_{CT} = R^{\top}\big(Z\,K^{-1}p - t\big)$$

</div>
<div>

1. The **tracker** follows marker arrays on the laparoscope and on the patient
2. With **calibration** and **registration**, that gives the camera pose in the CT for every frame
3. So every pixel is a **ray** in the CT

</div>
</div>

<div class="box">Known: where the camera is and where each pixel looks. <strong>Missing: how far along the ray the tissue is, the depth Z.</strong></div>

<!--
- The optical tracker is an infrared stereo camera. It sees the marker arrays (3 to 4 reflective balls) on the laparoscope and on the patient, and reports their pose.
- Two links are fixed and measured once: hand-eye calibration (marker array to camera tip) and registration (CT to patient array). Two links are tracked every frame. Multiplying along the graph gives the camera pose in the CT:
  T_cam<-CT = T_cam<-lap · T_lap<-trk · T_trk<-pat · T_pat<-CT
- The formula, right to left: p = (u, v, 1) is the pixel. K⁻¹p undoes the lens and gives the ray direction. Z·K⁻¹p walks to depth Z along it, which is the point in camera coordinates in mm. −t and Rᵀ undo the camera pose (Rᵀ = R⁻¹), which gives the point in the CT.
- The tracker sees only the marker arrays, not the tissue. The insufflation is invisible to it, so the depth has to come from the video.
- First practical step: project the post-insufflation CT into the porcine video. If it lines up, the chain is right before any depth network is involved.
-->

---
<div class="tag">3D vision · methods</div>

# Methods: getting the depth

<div class="io">
  <div></div>
  <div class="hd"><b>FoundationStereo</b> [1] <span class="chip hu">human · stereo</span></div>
  <div class="hd"><b>Depth Anything 3</b> [2] <span class="chip pc">porcine · mono</span></div>

  <div></div>
  <div class="fig"><img src="assets/fs_fig2.png" alt="FoundationStereo architecture"></div>
  <div class="fig"><img src="assets/da3_fig2.png" alt="Depth Anything 3 architecture"></div>

  <div class="lbl">Input</div>
  <div>rectified left + right image</div>
  <div>one or many frames, optionally with K and the tracked poses</div>

  <div class="lbl">Output</div>
  <div>disparity d per pixel → depth Z = f·B / d, in mm</div>
  <div>depth + ray per pixel, consistent across frames, scale unknown</div>

  <div class="lbl">How we use it</div>
  <div>unproject with the tracked pose → metric point cloud in the CT</div>
  <div>scale from the tracked camera motion → point cloud in the CT, checked against the post-insufflation CT</div>
</div>

<div class="box"><strong>With these methods today:</strong> the visible surface, per frame, in CT coordinates. <strong>Not yet:</strong> one consistent surface over time, or anything the camera doesn't see.</div>

<div class="cite">

[1] Wen et al., FoundationStereo: Zero-Shot Stereo Matching, CVPR 2025 · [2] Lin et al., Depth Anything 3: Recovering the Visual Space from Any Views, arXiv 2025

</div>

<!--
- Both are pretrained and used as they are, zero-shot. We don't train them.
- FoundationStereo: the same point appears shifted by d pixels between the left and right image. With focal length f and baseline B (distance between the two cameras) the depth is Z = f·B/d, directly in mm. It runs per frame. Figure: features from both images, a cost volume that compares every possible shift, then iterative refinement of the disparity.
- Depth Anything 3: one transformer looks at all frames together, so the depths agree across views. It predicts a depth map and a ray map per frame; a 3D point is ray origin + depth × direction. Our tracked poses can be given as input. From one camera the scale is unknown; the tracked camera motion is in mm, which fixes it.
- Then the same step for both: the formula from the previous slide puts every pixel into the CT.
- What we get today is the surface the camera sees, frame by frame. Turning that into one surface to compare with the simulation is the open question on the next slide.
-->

<!-- BridgeSplat moved to Pair A (supervisor feedback, 25.11). The full explanation is in slides.md, part 4. -->

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
<div class="st"><b>⇅ Compare</b> in CT coordinates, where the camera saw → <b>tune simulation parameters</b></div>
<div class="ar">→</div>
<div class="st"><b>Evaluate</b> vs. post-insufflation CT <span class="chip pc">porcine</span></div>
</div>

<p class="lane">Video (Pair B)</p>
<div class="flow">
<div class="st"><b>Tracked video</b><span class="chip pc">porcine: mono</span><span class="chip hu">human: stereo</span></div>
<div class="ar">→</div>
<div class="st"><b>Depth</b>DA3 [2] <span class="chip pc">porcine</span><br>FoundationStereo [3] <span class="chip hu">human</span></div>
<div class="ar">→</div>
<div class="st q"><b>Reconstruction ?</b>open question, see below</div>
<div class="ar">→</div>
<div class="st"><b>Reconstructed surface</b>in CT coordinates</div>
</div>

<div class="oq">

**Open question, and our main challenge:** how do we turn per-frame depth into one surface to compare with the simulation?
- **Fuse:** unproject all frames with the tracked poses into one point cloud. Simple, but it assumes nothing moves.
- **Build a mesh** from the fused points and compare surface to surface.
- **Fit a mesh:** deform the pre-op CT or the simulated mesh until it matches the depth, as in BridgeSplat [4]. This keeps the correspondence with the simulation.

</div>

<div class="cite">

[1] Bano et al., MICCAI 2012 · [2] Lin et al., Depth Anything 3, arXiv 2025 · [3] Wen et al., FoundationStereo, CVPR 2025 · [4] Fehrentz et al., BridgeSplat, MICCAI 2025

</div>

<!--
- Top: Pair A simulates the insufflation from the pre-op CT, following Bano et al.
- Bottom: we reconstruct the real insufflated surface from the tracked video: depth from DA3 on porcine and FoundationStereo on human, put into the CT with the tracked poses.
- How exactly we get from per-frame depth to one surface is still open. That is the main challenge on our side. Three options: fuse all frames into one point cloud (simple, but the scene changes while the gas comes in); build a mesh from it; or deform a mesh (pre-op CT or the simulated one) to match the depth, as in BridgeSplat, which keeps the vertex-to-vertex correspondence with the simulation.
- Both meet in CT coordinates. The mismatch tunes the simulation's parameters, and on the porcine data we evaluate against the real post-insufflation CT, with and without the video refinement.
- The video only sees part of the surface, so the comparison counts only the region the camera saw. The physics then carries the correction to the parts it can't see (e.g. wall too stiff → lower stiffness → organs behind move too).
- Humans have no post-insufflation CT; the only check there is that the tracked camera must lie inside the gas, not inside tissue.
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

---
<!-- _paginate: false -->
<div class="tag">Backup · 3D vision · beyond our scope</div>

# If it works: what comes later

- **Continuous alignment:** keep the CT-based simulation and the video aligned through the whole surgery, not only at the start
- **Instruments in 3D:** reconstruct the tools from depth + segmentation
- **Tool–tissue interaction:** feed what the tools do to the tissue into the simulation
- **Beyond the visible:** estimate how tissue the camera can't see deforms

<div class="warn"><strong>Our scope:</strong> insufflation only. Depth of the visible surface in CT coordinates, compared with the simulation and, on the pigs, with the post-insufflation CT.</div>

<!--
BACKUP, only if asked where this leads.
- None of this is part of our project. It's where the group wants to go if aligning simulation and video works for insufflation.
- Instruments: depth gives where the tool surface is, segmentation says which pixels are the tool.
- Beyond the visible: the simulation links what the camera sees to what it doesn't, so a correction in the visible part also moves the hidden part.
-->
