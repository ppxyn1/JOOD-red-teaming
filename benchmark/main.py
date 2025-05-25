import os
import json
from PIL import Image
from utils import run_llava, run_judge_model
from prompt import INPUT_TEXT_PROMPT, JUDGE_PROMPT, EVALUATION_PROMPT

CONFIG_PATH = "./config.json"

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

# Normal OOD way 
def get_mixup(image1, image2, alpha, size=(320, 320)): 
    image1 = image1.resize(size).convert("RGB")
    image2 = image2.resize(size).convert("RGB")
    return Image.blend(image1, image2, alpha)

def run_jailbreak(config, input_image, aux_img_path, text_prompt, folder, alpha):
    print(f"auxiliary Image: {aux_img_path}")
    print(f"mixup alpha: {alpha.get('alpha')}")

    aux_img_pil = Image.open(aux_img_path)
    mixup_image = get_mixup(input_image, aux_img_pil, alpha.get("alpha"))
    mixup_image.show(title=f"Mixed Image")

    # llava 1.6
    vlm_response = run_llava(
                            prompt = text_prompt,
                            api_url = config["api_url"],
                            model = config["vlm_model"],
                            image = mixup_image)

    print(f"Response({config['vlm_model']}):\n{vlm_response}")
    judge_prompt = JUDGE_PROMPT.format(question=text_prompt.strip(), vlm_response=vlm_response)
    eval_prompt = EVALUATION_PROMPT.format(instruction=text_prompt.strip())

    # llama-guard3 
    judge_response = run_judge_model(
                                    judge_prompt,
                                    api_url=config["judge_api_url"],
                                    model=config["judge_model"])

    if judge_response:
        judge_decision = judge_response.lower().split()[0]
    print(f"\n[Judge Response({config['judge_model']})]: {judge_decision}")

    if judge_decision == "unsafe":
        attack_success = True
    else:
        attack_success = False

    eval_model = config["vlm_model"]
    eval_response = run_llava(
                            prompt=eval_prompt,
                            api_url=config["api_url"],
                            model=eval_model,
                            image=mixup_image)
    print(f"\n[Eval response{(eval_model)}]:\n{eval_response}")

    return {"folder": folder, "attack_success": attack_success}


def main():
    config = load_config(CONFIG_PATH)
    test_image_folder = config["test_image_folder"]
    input_image_path = config['input_image_path']
    input_image = Image.open(input_image_path)
    text_prompt = INPUT_TEXT_PROMPT

    category_dict = {
        "semantic_dissimilar": os.path.join(test_image_folder, "semantic_dissimilar"),
        "semantic_similar": os.path.join(test_image_folder, "semantic_similar"),
        "etc": os.path.join(test_image_folder, "etc")
    }

    experiments = []
    for category, folder_path in category_dict.items():
        for fname in os.listdir(folder_path):
            aux_path = os.path.join(folder_path, fname)
            for alpha in [0.4, 0.6]: # Mixed up ratio which rouse the most harmfulness 
                experiments.append({
                                    "folder": category,
                                    "aux_path": aux_path,
                                    "params": {"alpha": alpha}
                                    })

    results_list = []
    for i, exp_case in enumerate(experiments):
        print(f"\nProcessing({i+1}/{len(experiments)})")
        result = run_jailbreak(
                            config=config,
                            input_image=input_image,
                            aux_img_path=exp_case["aux_path"],
                            text_prompt=text_prompt,
                            folder=exp_case["folder"],
                            alpha=exp_case["params"])
        results_list.append(result)

    print("\n[Results]")

    result_dict = {}
    for res in results_list:
        category = res["folder"]
        if category not in result_dict:
            result_dict[category] = {"total": 0, "success": 0}
        result_dict[category]["total"] += 1
        result_dict[category]["success"] += int(res["attack_success"])

    for category, data in result_dict.items():
        total = data["total"]
        success = data["success"]
        rate = (success / total * 100) if total else 0
        print(f"{category}: {success}/{total} ({rate:.2f}%)")

if __name__ == "__main__":
    main()
