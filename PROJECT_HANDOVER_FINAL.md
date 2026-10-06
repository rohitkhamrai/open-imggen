# DaivBharathi AI Image Generator - Project Handover

This document contains all critical context, architectural decisions, hardware constraints, and hard-learned lessons from building the DaivBharathi image generation pipeline. 

Pass this document to the next AI agent or developer to ensure zero loss of context.

## 1. Project Goal
Build a fully automated, local, free, and hyper-realistic AI image generator for Hindu pooja cards and deities. The system must create flawless background art, perform instructional image editing (e.g., "add pink flowers"), and never generate fake AI text on the images.

## 2. Hardware Constraints (CRITICAL)
- **GPU:** Nvidia Quadro M4000 (8GB VRAM).
- **Rule:** 8GB VRAM is extremely limited for modern Flow-Matching models. You **cannot** load the UNet or CLIP models more than once. All pipelines (Creation and Editing) must share the exact same `UnetLoaderGGUF`, `CLIPLoaderGGUF`, and `VAELoader` nodes.

## 3. The Model Stack
- **Main Generator (UNet):** `z_image_turbo-Q5_K_S.gguf` (Quantized 8-step Flux/Flow-Matching model).
- **Vision/Text Encoder:** `Qwen3-4B-UD-Q6_K_XL.gguf` (Massive multi-modal encoder required for complex instructional edits).
- **Prompt Enhancer:** Local `Llama 3.2` running via `NoLlamaTextEnhancer` node. Intercepts broken user English, expands it into a highly detailed cinematic prompt, and enforces the "DaivBharathi aesthetic" (no text, no watermarks, photorealistic).

## 4. Current Architecture: `Pooja_Card_GGUF_Master.json`
We consolidated everything into one single ComfyUI workflow with two parallel pipelines:
1. **Creation Pipeline (Top):** 
   - `NoLlama` -> `CLIPTextEncode` -> `EmptyLatentImage(1024x1024)` -> `KSampler(8 steps, CFG 1.0, denoise 1.0)`.
2. **Edit Pipeline (Bottom):**
   - `LoadImage` -> `ImageScale(1024x1024)` -> `TextEncodeQwenImage21` -> `ModelSamplingFlux` -> `KSampler / SamplerCustomAdvanced`.

## 5. Major Failures & Lessons Learned (DO NOT REPEAT)

### A. The "Snowy / Bubbly Artifact" Failure (Image-to-Image)
- **What happened:** When trying to edit an image, the output became a horribly distorted, zoomed-in, snowy mess.
- **Why:** We attempted to use a standard `KSampler` with `denoise=0.5`. 
- **The Fix/Lesson:** Z-Image Turbo is a **Flow-Matching** model. Standard Gaussian noise schedules (denoise=0.5) completely destroy the latent space. Furthermore, `TextEncodeQwenImage21` acts as an *Instructional Injector*. It requires the image to be fully reconstructed. **You must use `ModelSamplingFlux`** to fix the physics, and the noise schedule must be heavily customized (using `SamplerCustomAdvanced`, `BasicScheduler` set to 1.0 denoise, and `ExtendIntermediateSigmas`) optimized specifically for an 8-step model.

### B. The Resolution Crash
- **What happened:** Feeding random aspect ratios or non-standard resolutions into `TextEncodeQwenImage21` breaks the UNet.
- **The Fix/Lesson:** Always force the input image through an `ImageScale` node set to exactly `1024x1024` (or `ImageScaleToTotalPixels`) before it hits the Qwen encoder.

### C. The "Gibberish Text" Failure
- **What happened:** The AI kept trying to draw English or Hindi text on the banners, which looked like alien language.
- **The Fix/Lesson:** The AI is strictly banned from generating text. The `NoLlama` agent aggressively injects negative prompts (`text, letters, typography`). All textual overlays, banners, and logos are to be handled by HTML/CSS or external web UI scripts later.

## 6. Next Steps / Strategic Pivot: "The Two-Layer Generator"
We have officially decided to **abandon the 8GB local constraint and the Image-to-Image editing pipeline.** Trying to force an AI to generate background art, understand complex edits, and render perfect text all at once leads to failure and hallucinations. 

Instead, we are adopting a **Two-Layer Architecture** for manual batch processing:

### Phase 1: The Groq Prompt Generator (Local)
- **Tool:** Python + Groq API (Llama-3.3-70B - Free tier)
- **Action:** A script parses the raw Pooja JSON data and converts it into a pure, highly detailed, text-free visual prompt optimized for FLUX.

### Phase 2: The Colab Art Engine (Cloud)
- **Tool:** Google Colab Free Tier (T4 GPU - 16GB VRAM)
- **Action:** Spin up a lightweight ComfyUI or Diffusers pipeline running an NF4 or GGUF Quantized version of **FLUX.1-Dev**. 
- **Goal:** Run the prompts from Phase 1 to batch-generate pristine, 1024x1024 photorealistic background art (zero text).

### Phase 3: The Text Stamper (Local)
- **Tool:** Python + Pillow library
- **Action:** Take the downloaded background images and automatically overlay the exact English text (Pooja Name, Date, 2 bullet points) using DaivBharathi's official fonts, colors, and branding guidelines. 
- **Output:** Web-optimized 600x600px JPEGs/WebPs under 1MB.

*(Note for next agent: Start by building the Groq script or the Colab notebook based on this roadmap).*
