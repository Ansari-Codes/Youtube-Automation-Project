import argparse
import json
from deapi import DeapiClient

parser = argparse.ArgumentParser()

parser.add_argument(
    "--orientation",
    choices=["landscape", "portrait"],
    required=True
)

parser.add_argument(
    "--prompt",
    required=True
)

args = parser.parse_args()

# Resolution
if args.orientation == "landscape":
    width = 768
    height = 512
else:
    width = 512
    height = 768

client = DeapiClient(
    api_key="YOUR API KEY HERE",
)

try:
    job = client.video.generate(
        prompt=args.prompt,
        negative_prompt="blurry, low quality",
        model="Ltxv_13B_0_9_8_Distilled_FP8",
        width=width,
        height=height,
        steps=1,
        seed=42,
        frames=120,
        fps=30,
    )
    
    result = job.wait()

    if result.status.lower() in ["done", "completed", "success"]:
        print(json.dumps({
            "success": True,
            "url": result.result_url
        }))
    else:
        print(json.dumps({
            "success": False,
            "url": ""
        }))

except Exception as e:
    print(json.dumps({
        "success": False,
        "url": "",
        "error": str(e)
    }))

finally:
    client.close()
