from PIL import Image
from modules import scripts_postprocessing, ui_components, images
from modules import scripts as scripts
from modules.shared import opts
import gradio as gr

print("\033[0;32mPixelator Plugin Loading...\033[0m")


# Class built for txt2img & img2img tabs
class Script(scripts.Script):

    def title(self):
        return "Pixelator"

    # Show plug-in interface
    def show(self, is_img2img):
        return scripts.AlwaysVisible

    # Load UI
    def ui(self, is_img2img):
        with gr.Accordion("Pixelator", open=False):
            with gr.Row():
                enabled = gr.Checkbox(label="Enable", value=False)

            with gr.Column():
                with gr.Row():
                    pixel_size = gr.Slider(minimum=1, maximum=32, step=1, value=4, label="Pixel size", info="1 = No change, recommended values：2-8")

        return [enabled, pixel_size]

    # Reading image process
    def postprocess(self, p, processed, enabled, pixel_size):

        # Whether to enable
        if not enabled:
            return

        # Simple pixel alignment
        def process_image(original_image):
            small = original_image.resize((original_image.width // pixel_size, original_image.height // pixel_size),
                                          resample=Image.NEAREST)
            return small.resize((original_image.width, original_image.height), resample=Image.NEAREST)

        # Batch processing
        for i in range(len(processed.images)):
            pixel_image = process_image(processed.images[i])
            processed.images.append(pixel_image)
            images.save_image(pixel_image, p.outpath_samples, "",
                              processed.seed + i, processed.prompt, opts.samples_format, info=processed.info, p=p, suffix=f"-PixelSize-{pixel_size}")

        return processed


# Class built for Extras tab
class ScriptPostprocessingPixelator(scripts_postprocessing.ScriptPostprocessing):
    name = "Pixelator"
    order = 1500

    # Load UI
    def ui(self):
        with ui_components.InputAccordion(False, label="Pixelator") as enable:
            pixel_size = gr.Slider(minimum=1, maximum=32, step=1, value=4, label="Pixel Size", info="1 = No Change, recommended values: 2-8")

        return {
            "enable": enable,
            "pixel_size": pixel_size,
        }

    # Process image from Extras tab
    def process(self, pp: scripts_postprocessing.PostprocessedImage, enable, pixel_size):

        # Run if Enabled, Return otherwise
        if not enable:
            return

        # Process image
        in_image = pp.image
        small_image = in_image.resize((in_image.width // pixel_size, in_image.height // pixel_size), resample=Image.NEAREST)
        images.save_image(small_image, "output\extras-images\pixelated_small", "", "", "", opts.samples_format, info=small_image.info, p=small_image, suffix=f"PixelSize-{pixel_size}")
        out_image = small_image.resize((in_image.width, in_image.height), resample=Image.NEAREST)

        # Set output image and info
        pp.image = out_image
        pp.info["Pixel Size"] = pixel_size


print("\033[0;32mPixelator plugin loaded...\033[0m")
