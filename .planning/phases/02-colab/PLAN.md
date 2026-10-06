---
phase: 02-colab
plan: 01
type: execute
wave: 1
depends_on: []
files_modified: [notebooks/Colab_Flux_Art_Engine.ipynb]
autonomous: false
requirements: [PHASE-2]
user_setup:
  - service: google_colab
    why: "GPU execution"

must_haves:
  truths: 
    - "User can upload Groq prompts to Colab"
    - "Colab runs FLUX.1-Dev GGUF model"
    - "Colab generates text-free 1024x1024 images"
    - "User can download generated images"
  artifacts: 
    - path: "notebooks/Colab_Flux_Art_Engine.ipynb"
      provides: "ComfyUI/Diffusers environment setup on free T4"
  key_links: []
---

<objective>
Build Google Colab notebook to run Phase 2 Cloud Art Engine.

Purpose: 8GB local GPU too small. Use free Colab 16GB T4 for FLUX.
Output: `.ipynb` notebook ready for user upload to Google Colab.
</objective>

<tasks>
<task type="auto">
  <name>Task 1: Generate Colab Notebook</name>
  <files>notebooks/Colab_Flux_Art_Engine.ipynb</files>
  <action>Create a Jupyter Notebook containing cells to: 1) Install ComfyUI/Diffusers, 2) Download FLUX.1-Dev GGUF, 3) Accept JSON prompts, 4) Run batch generation, 5) Zip output images.</action>
  <verify>File exists and is valid JSON format for ipynb.</verify>
  <done>Notebook file created locally.</done>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <what-built>Colab notebook created locally</what-built>
  <how-to-verify>Upload `notebooks/Colab_Flux_Art_Engine.ipynb` to Google Colab, connect T4 GPU, run all cells.</how-to-verify>
  <resume-signal>Type "approved" when images generate successfully.</resume-signal>
</task>
</tasks>
