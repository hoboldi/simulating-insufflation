---
marp: true
math: mathjax
paginate: true
size: 16:9
title: "From pixels to 3D"
style: |
  section {
    background: #0e1116;
    color: #e8eaed;
    font-family: "Helvetica Neue", Arial, sans-serif;
    font-size: 26px;
    padding: 50px 64px 40px 64px;
    justify-content: flex-start;
  }
  h1 {
    color: #ffffff;
    font-size: 40px;
    margin-bottom: 18px;
    border-bottom: 3px solid #4aa3ff;
    padding-bottom: 8px;
    display: inline-block;
  }
  h2 { color: #4aa3ff; font-size: 30px; }
  strong { color: #ffffff; }
  em { color: #f0a030; font-style: normal; }
  code { background: #1c2128; color: #e8eaed; }
  table { font-size: 22px; border-collapse: collapse; }
  th { background: #1c2128; color: #4aa3ff; }
  td, th { border: 1px solid #2a2f36; padding: 6px 12px; }
  tr { background: #0e1116 !important; }
  section::after { color: #6b7280; font-size: 16px; }
  footer { color: #6b7280; font-size: 16px; left: 64px; bottom: 14px; }
  .muted { color: #9aa0a6; font-size: 20px; }
  .box { border-left: 4px solid #3ecf8e; padding: 6px 16px; background: #13201b; margin-top: 14px; }
  .warn { border-left: 4px solid #ff6b5a; padding: 6px 16px; background: #221413; margin-top: 14px; }
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
  .params .lbl { color: #9aa0a6; font-size: 20px; }
  .params .plist { text-align: left; font-size: 24px; line-height: 1.7; align-self: center; }
  .params .lbl + p { margin-top: 6px; }
  section.section { justify-content: center; }
  section.section h1 { font-size: 56px; border-bottom: 4px solid #f0a030; }
  section.section p { color: #9aa0a6; font-size: 26px; max-width: 85%; }
  section.title h1 { font-size: 52px; border-bottom: 4px solid #4aa3ff; }
  .flow { display: flex; align-items: stretch; gap: 10px; font-size: 20px; margin: 10px 0 14px 0; }
  .flow .st { flex: 1; border: 1px solid #2a2f36; background: #161b22; border-radius: 8px; padding: 8px 10px; text-align: center; }
  .flow .st b { display: block; color: #4aa3ff; margin-bottom: 4px; }
  .flow .sim { border: 2px dashed #f0a030; background: #1f1a10; }
  .flow .sim b { color: #f0a030; }
  .flow .ar { align-self: center; color: #9aa0a6; font-size: 26px; }
  .flow .fb { flex-basis: 100%; }
  .chip { display: inline-block; font-size: 14px; padding: 1px 8px; border-radius: 10px; margin: 3px 2px 0 2px; background: #2a2f36; color: #e8eaed; }
  .chip.pc { background: #3a2a4a; } .chip.hu { background: #1e3a4a; }
  .flow.a .st { border-color: #f0a030; background: #1f1a10; } .flow.a .st b { color: #f0a030; }
  .lane { font-size: 15px; color: #9aa0a6; margin: 0; }
  .mid { display: flex; gap: 10px; align-items: center; justify-content: center; font-size: 19px; margin: 4px 0; }
  .mid .st { border: 2px solid #3ecf8e; background: #13201b; border-radius: 8px; padding: 6px 14px; text-align: center; }
  .mid .st b { color: #3ecf8e; }
  .ph { border: 2px dashed #f0a030; border-radius: 10px; padding: 14px 22px; margin-top: 10px; background: #1f1a10; }
  .cite { position: absolute; left: 64px; right: 110px; bottom: 16px; font-size: 14px; line-height: 1.3; color: #9aa0a6; border-top: 1px solid #2a2f36; padding-top: 6px; }
  .cite p { margin: 0; }
  .tl td:first-child { white-space: nowrap; color: #4aa3ff; font-weight: bold; }
---
<!-- _class: title -->
<!-- _paginate: false -->

# Simulating insufflation

## Physics simulation meets 3D vision on laparoscope video

<br>

AI in Surgery (CAMP, TUM)

<!--
- The project: simulate how the abdomen changes under insufflation, and use the laparoscope video to make that simulation patient-specific.
-->

---
# Problem statement

<div class="cols">
<div>

- Before laparoscopy the abdomen is **insufflated with CO₂**
- The **abdominal wall lifts** and the **organs shift by centimetres**
- The **pre-op CT** was taken **before** that: it no longer matches the patient on the table
- In patients there is **no post-insufflation CT**: we don't know the insufflated anatomy

</div>
<div>

<div class="box"><strong>Pre-op CT:</strong> what we have. Anatomy at rest, no gas.</div>

<div class="warn"><strong>During surgery:</strong> what we need. Anatomy under insufflation, never scanned in patients.</div>

</div>
</div>

<!--
- Insufflation inflates the abdomen with gas so the surgeon has room to work. The wall lifts and the organs move by centimetres.
- Everything we know about the patient comes from the CT taken before that, so it shows the wrong shape.
- And in patients nobody takes a second CT after insufflation, so the real insufflated anatomy is unknown.
-->

---
# Motivation

<div class="small">

| | Porcine (16 procedures) | Human (3 cases, more coming) |
|---|---|---|
| CT | **pre- and post-insufflation** | pre-op contrast CT only |
| Video | mono, tracked | stereo, tracked (robotic + conventional) |
| Ground truth | post-insufflation CT | none |

</div>

**Why simulate?**
- **Predict the insufflated anatomy** from the pre-op CT, where no second scan exists
- **Keep navigation and planning valid:** CT-based overlays and port placement after insufflation
- **Porcine data:** validate the simulation against the real post-insufflation CT
- **Video:** the only intra-op measurement in patients → makes the simulation **patient-specific**

<!--
- Porcine: 16 procedures with a CT before and after insufflation, so real ground truth. Human: only the pre-op CT, plus tracked stereo video.
- A simulation gives us the insufflated anatomy where we can't scan it. We can check it on the pigs, and in patients the video is our window to adapt it to the individual.
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

- **K:** calibration, once. **[R | t]:** tracking chain, every frame
- A pixel is a ray: only the **depth Z** is missing
- **FoundationStereo [1]:** stereo, zero-shot → **metric** depth (human)
- **Depth Anything 3 [2]:** mono → depth **up to scale**; tracked poses fix the scale (porcine)

<span class="muted">The tracker sees the marker arrays, not the anatomy: insufflation is invisible to it.</span>

</div>
</div>

<div class="cite">

[1] Wen et al., FoundationStereo: Zero-Shot Stereo Matching, CVPR 2025 · [2] Lin et al., Depth Anything 3, arXiv 2025

</div>

<!--
- The optical tracker sees marker arrays on the laparoscope and the patient. With calibration and registration this gives us, every frame, where the camera is in the CT.
- So each pixel becomes a ray in the CT; we only miss the depth along it.
- FoundationStereo gives metric depth from the stereo laparoscope in the human cases. Depth Anything 3 gives depth from mono video, but only up to scale, which we fix with the tracked camera motion on the porcine data.
-->

---
# Literature: BridgeSplat

<div class="paper">

![w:680](assets/bridgesplat_fig1.png)

</div>

- Same setup as our porcine data: **CT + tracked monocular laparoscope video** [1]
- Gaussians are **bound to the CT mesh**, the pose comes from tracking → only the **mesh deformation** is optimised, by matching rendered and real frames

<div class="cite">

[1] Fehrentz et al., BridgeSplat: Bidirectionally Coupled CT and Non-Rigid Gaussian Splatting for Deformable Intraoperative Surgical Navigation, MICCAI 2025

</div>

<!--
- BridgeSplat works on exactly our kind of data. It builds a mesh from the CT, attaches Gaussian splats to it, and renders each frame from the tracked pose.
- Since the pose is known and the Gaussians can't leave the mesh, the only way to match the video is to deform the mesh. That deformed mesh is the real tissue shape in CT coordinates.
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

---
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

<!--
- Right now both pairs get to know the data. On the video side: a video-to-CT visualizer and first DA3 tests.
- Steps 1 and 2 run in parallel: the simulation is reproduced on the pigs and then the humans; depth is built and checked against the porcine post-insufflation CT.
- Step 3 is where the two parts meet. Step 4 measures whether the video refinement helps, on the pigs.
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
