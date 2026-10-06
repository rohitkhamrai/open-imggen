# Daiv Bharathi: Sacred Image Generation Pipeline (Local MVP)

## 1. Vision & Goal
**Objective:** Build a local, automated image generation pipeline to produce highly authentic, sacred Hindu ritual imagery (pooja setups, temple altars, murtis) for the Daiv Bharathi catalog.
**Core Challenge:** The pipeline must run entirely locally on heavily constrained legacy hardware while preserving 100% iconographic accuracy of sacred deities (no AI hallucinations of mudras, ayudhas, or faces).
**Target Output:** 3 to 5 jaw-dropping, production-ready catalog cards (768x1152) to serve as a Proof of Concept (POC) to secure management approval for a future cloud GPU budget.

## 2. Hardware Constraints & Environment
* **OS:** Ubuntu Server
* **GPU:** NVIDIA Quadro M4000 (Maxwell Architecture `sm_52`, 8GB VRAM, No Tensor Cores).
* **Memory Limits:** Extremely strict. The 8GB limit dictates the entire software architecture.

## 3. Tech Stack & Architecture
* **Engine:** ComfyUI (Headless/Server Mode).
* **Launch Flags:** `python main.py --lowvram --fp32-vae --listen 0.0.0.0 --port 8188` (Mandatory for the M4000 to prevent OOM and black-image errors).
* **Base Model:** Juggernaut XL (SDXL architecture fine-tuned for photorealism, lighting, and textures).
* **Style Adapter:** IP-Adapter Plus (SDXL) - Used to enforce the brand's warm, cinematic temple lighting.
* **Compositing:** Layering and masking nodes (e.g., `ComfyUI-Inpaint-Nodes`, `Image Composite Masked`).
* **Decoding:** `VAE Decode (Tiled)` with a tile size of 512 is mandatory.

## 4. The MVP Scope (Generative Compositing Workflow)
The pipeline explicitly avoids generating deities from scratch. The workflow is:
1. **Background Generation:** SDXL generates a high-quality temple/pooja background using IP-Adapter Plus for brand style.
2. **Deity Compositing:** A clean, human-segmented PNG cutout of the sacred murti is pasted onto the generated background.
3. **Ambient Inpainting:** A low-denoise inpaint pass (0.20 - 0.25) is run *only* along the feathered outer edge of the deity to cast shadows, reflections, and smoke.
4. **Pixel Protection:** The original deity PNG is pasted back over the final result to guarantee zero pixel degradation of the sacred iconography.

## 5. Strict Agent Rules & Guardrails
* **NO INSIGHTFACE:** Do not install or configure InsightFace, FaceID, or InstantID. They violate commercial licensing and fail on non-human murtis.
* **NO FP16/BF16 FORCES:** Do not attempt to force standard FP16 or BF16 compute on the Maxwell GPU. 
* **NO CLOUD DEPENDENCIES:** This MVP must run 100% locally on the Ubuntu server. Do not write scripts for AWS, RunPod, or Lambda Labs.
* **AGENT EXECUTION RULE:** Before running any bash scripts or pip installs that alter the Ubuntu server environment, output the planned command to the terminal and wait for user confirmation.

## 6. Execution Plan (Agent Instructions)
**Agent Task 1: Environment Setup**
* Verify PyTorch CUDA compatibility with the `sm_52` Maxwell architecture.
* Clone the ComfyUI repository to the workspace.
* Create a `requirements.txt` or setup script to install ComfyUI dependencies, ensuring PyTorch versions match the CUDA limits.
* Install ComfyUI-Manager via git clone into `custom_nodes`.

**Agent Task 2: Pipeline Scaffolding**
* Generate a bash script (`download_models.sh`) to download:
  - Juggernaut XL (`.safetensors`) to `/models/checkpoints/`
  - SDXL VAE to `/models/vae/`
  - IP-Adapter Plus SDXL models to `/models/ipadapter/`
  - CLIP Vision models to `/models/clip_vision/`

**Agent Task 3: Workflow Generation**
* Author a Python script or JSON file that constructs the ComfyUI node wiring for the Generative Compositing Workflow described in Section 4.