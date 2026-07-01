# AI keyword filter

Used in Step 4 of the zsxq-daily-blog skill: when filtering raw knowledge-planet
posts to AI-related cases.

A post passes if its body text contains any of the following tokens (case-insensitive):

- `AI`
- `GPT`
- `ChatGPT`
- `Claude`
- `LLM`
- `大模型` (large model)
- `模型` (model, in context of LLM/image gen)
- `agent`, `智能体`
- `prompt`, `提示词`
- `RAG`, `知识库`
- `Seedance`, `Sora`, `Kling`
- `Midjourney`, `Stable\s*Diffusion`
- `Gemini`
- `Claude\s*Code`, `Cursor`, `codex`, `Copilot`
- `ComfyUI`, `lora`, `fine-?tune`, `Embedding`, `向量`

Posts that pass this filter are then ranked by interaction score. Posts that fail
are dropped — they are not AI monetization cases for the AI Lab section.

Posts with bodies that are purely technical help ("how do I run X on Y") should
be dropped even if they contain AI tokens.
