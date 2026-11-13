---
marp: true
theme: pair-b
paginate: true
math: katex
title: Layout reference (not part of the talk)
---

<!--
Reference deck: one slide per component of the pair-b theme.
Copy the pattern you need into slides.md. Not exported as part of the talk.
-->

<!-- _class: title -->

# Title slide

## Subtitle line

Names · Event · Date

---

<!-- _class: divider -->
<!-- footer: "Part name shown in the footer from here on" -->

# 2 · Section divider

One sentence: what the audience should take away from this part.

---

# Plain content slide

- One idea per slide
- Short bullets; details go into the speaker notes
- Inline math $Z = \frac{f\,B}{d}$ and display math:

$$
C = \sum_{i} c_i\,\alpha_i \prod_{j<i} (1-\alpha_j)
$$

<!-- Speaker notes: everything in a non-directive HTML comment ends up in the notes. -->

---

# Two columns + takeaway box

<div class="cols">
<div>

**Left**

- Text, list or image
- Blank lines around markdown inside `<div>`s

</div>
<div>

**Right**

- Use `cols-wide-left` / `cols-wide-right` for 3:2 / 2:3 splits

</div>
</div>

<div class="takeaway">

**Takeaway:** the box sticks to the bottom of the slide.

</div>

---

# Image + text + citation

<div class="cols-wide-left">
<div>

![w:560](https://placehold.co/560x320?text=figure)

</div>
<div>

- Local images: put them in `assets/` and write `![w:560](assets/fig.png)`
- Cite figures from papers

</div>
</div>

<div class="question">

**Open question:** use this box for things the group should discuss.

</div>

<div class="cite">Figure from: Author et al., Venue Year</div>

---

# Video (manim / project-page clips)

<video src="assets/example.mp4" controls autoplay loop muted width="800"></video>

<span class="muted">Plays in the HTML export. Marp's PPTX export does not embed videos: insert them afterwards (e.g. python-pptx).</span>

---

![bg right:45%](https://placehold.co/600x800?text=full-height+image)

# Background image split

- `![bg right:45%](…)` gives a full-height image on one side
- Use it for big figures or screenshots
