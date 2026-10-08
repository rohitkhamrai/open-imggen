# Open-Imggen: Z-Image Turbo GGUF Architecture

Welcome to **Open-Imggen**, a hyper-optimized AI image generation pipeline designed to produce 8K cinematic, culturally accurate Hindu devotional artwork with **perfect native text rendering**.

This repository completely bypasses expensive local GPU hardware by utilizing Google Colab's Free Tier (T4 GPU). By compressing the Lumina architecture using GGUF and swapping in the Qwen3 Text Encoder, we achieve **lightning-fast generation speeds** without sacrificing visual fidelity or typography.

---

## ⚡ Unprecedented Speed on Free Hardware

By leveraging the heavily optimized `zimageTurboByStable_xmasQ8.gguf` UNet paired with a 4-bit quantized text encoder, this pipeline achieves generation speeds that normally require an RTX 4090—completely for free on a Google Colab T4 GPU.

![Generation Speed Showcase](gen%20img/speed_showcase.png)
*(Image generation takes mere seconds from prompt to final 8K rendering)*

---

## 🎨 Showcase: Advanced Prompt Engineering Capabilities

This pipeline relies on **Explicit Physical Description** via an automated LLM (Groq Llama 3) to convert abstract Pooja data into raw anatomical and architectural instructions. Because the Z-Image model inherently understands typography, the text is integrated directly into the image diffusion process (no post-processing required).

### 1. Complex Mult-Armed Deities (Maha Navratri Pooja)
**Capability Proved:** Flawless rendering of 8-armed anatomy, specific weapon grips (Trishul, Lotus, Sword), and complex mounts (Lion), completely avoiding the "melting limbs" AI artifact.

![Maha Navratri Showcase](gen%20img/durga_showcase.png)

**The Prompt:**
> A highly detailed, cinematic, premium square devotional image. A photorealistic idol of Goddess Durga seated on a lion. STRICT ANATOMY: She has exactly 4 arms on her left side and 4 arms on her right side (8 arms total). Her upper right hand tightly grips a golden Trishul (trident). Her upper left hand holds a pink lotus. Her lower hands are in blessing poses. She is adorned in a crimson-red silk saree. In the foreground, a blazing Chandi Homa fire burns. The background is a deeply carved stone temple interior with atmospheric smoke. Glowing, elegant English typography reads: "Maha Navratri Pooja", with a subtitle "Divine Protection". Ensure perfect spelling. Extremely high quality, 8k resolution, authentic Indian spiritual aesthetic.

### 2. Complex Human/Fluid Interaction (Maha Rudrabhishekam)
**Capability Proved:** The ability to render human hands interacting with fluids (pouring milk) over a sacred object without the fluid merging into the metal or skin.

![Maha Rudrabhishekam Showcase](gen%20img/rudrabhishekam_showcase.png)

**The Prompt:**
> A highly detailed, cinematic, premium square devotional image. A photorealistic, documentary-style shot of a traditional Hindu priest (Purohit) performing Maha Rudrabhishekam. The priest, wearing a clean white silk dhoti and sacred thread (Janeu), is leaning over a large, ancient black stone Shiva Lingam. With highly detailed, realistic hands, he is pouring a continuous, smooth stream of pure white milk from a traditional brass Kalasha directly over the top of the Lingam. The temple interior is bathed in the moody, warm amber glow of hundreds of brass oil lamps. Hovering magically in the warm ambient smoke between the priest and the foreground is glowing, ethereal golden serif typography that reads: "Maha Rudrabhishekam", with a fine elegant subtitle below reading "Purify the Soul". Extremely high quality, 8k resolution.

### 3. Extremely Fierce / Abstract Iconography (Maha Kali Pooja)
**Capability Proved:** Ability to render fierce, complex divine forms (dark skin, specific weapons, standing on another deity) while retaining cinematic composition and avoiding horror-like distortions.

![Maha Kali Showcase](gen%20img/kali_showcase.png)

**The Prompt:**
> A highly detailed, cinematic, premium square devotional image. A photorealistic idol of the fierce Goddess Kali (Maa Kali). STRICT ANATOMY: She has exactly four arms. Her top right hand holds a curved sword (khadga). Her bottom right hand holds a Trishul. She wears a traditional garland of small skulls. She is stepping her right foot onto the chest of Lord Shiva, who lies on the stone floor. In the foreground, a priest is offering red hibiscus flowers into a fiercely burning Homa fire. Glowing, ethereal blood-red typography reads: "Maha Kali Pooja", with a subtitle "Awaken the Divine". Ensure perfect spelling. Extremely high quality, 8k resolution.

---

## 🚀 How to Run (Google Colab)

1. Open `notebooks/Colab_ComfyUI_Server.ipynb` in Google Colab.
2. Select **Runtime > Run All**.
3. The notebook will automatically apply the Anti-Disconnect script, download all required GGUF models (`z_image_turbo-Q5_K_S.gguf` & `Qwen3-4B-UD-Q6_K_XL.gguf`) via aria2, and launch the ComfyUI web server.
4. Click the **Cloudflare / Localtunnel link** at the bottom of the cell output.
5. Drag and drop the `Pooja_Card_GGUF_Master.json` file into the UI.
6. Enter your prompt and click **Queue Prompt**!

## 🤖 Automated Prompt Generation

Instead of writing prompts manually, use the included Groq LLM script to automatically convert JSON database entries into these highly explicit visual descriptions.

```bash
# Add your Groq API key to .env
python groq_prompt_generator.py
```
