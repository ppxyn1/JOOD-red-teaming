# Red-teaming for AI Safety

## Implementation of JOOD

This is a **unofficial experiments** of the paper:   **[Playing the Fool: Jailbreaking LLMs and Multimodal LLMs with Out-of-Distribution Strategy](https://arxiv.org/abs/2503.20823)** [CVPR 2025] 

**Note**: It was  **personal research and experimentation purposes only for study** on jailbreak since there was no material for the paper at the moment(May/20/2025).

---
## About

The paper explored how out-of-distribution (OOD) strategies can jailbreak the safety alignment of vision language multimodal(VLM). This repo tests a simplified version of the paper.

### Test Setup

- **Test Model**: [llava-v1.6-34b-hf](https://huggingface.co/llava-hf/llava-v1.6-34b-hf) 
- **Judge Model**: [llama-Guard-3-8B ](https://huggingface.co/meta-llama/Llama-Guard-3-8B)
- **Benchmark Data**: Tested with an image of Bomb, and child with gun which belong to category 0 and 7 from [advbench-m](https://github.com/abc03570128/Jailbreaking-Attack-against-Multimodal-Large-Language-Model) 

---

## Example Result

> ***Input Image***: Unsafe with OOD perturbation    
> ***Input Text***: Safe 

<div align="center">
  <img src="assets/imgs/mixup_sample0.png" width="150" alt="Prompt and Result Example" />
  <img src="assets/imgs/mixup_sample2.png" width="150" alt="Prompt and Result Example" />
  <br>
    <img src="assets/imgs/result2.png" width="800" alt="Prompt and Result Example" />
      <br>

  <em>Figure: Example of mixed up images and response from LLaVA, judged by Llama Guard3.</em>
</div>


## Setup

```bash
> git clone https://github.com/your-username/playing-the-fool-test.git
```
```bash
> cd JOOD-RED-TEAMING/benchmark
> python main.py
```
> In the repository, models are called with API since limited resources. Set your API of models in ***config.json***.


