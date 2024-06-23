from PIL import Image
import gradio as gr
import modules.scripts as scripts
from modules import images
from modules.shared import opts


class Script(scripts.Script):
    print('Pixelator plugin loaded...')

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
                    pixel_size = gr.Slider(minimum=1, maximum=32, step=1, value=6, label="Pixel size", info="1 = No change, recommended values：2-8")

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
