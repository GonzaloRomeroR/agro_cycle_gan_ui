import sys
from typing import List, Any, Optional

sys.path.insert(0, "./agro_cycle_gan")
from agro_cycle_gan.generate import ImageTransformer


def flask_generate() -> None:
    generate_images(
        origin_path="./images/horse2zebra/test_A/A",
        dest_path="./images_gen/horse2zebra/",
        domain="B",
    )


def generate_images(
    origin_path: str,
    dest_path: str,
    domain: str = "B",
    resize: Any = None,
    image_num: Optional[int] = None,
) -> None:
    image_transformer = ImageTransformer("horse2zebra")
    image_transformer.transform_dataset(
        origin_path,
        dest_path,
        domain,
        resize,
        image_num,
    )


if __name__ == "__main__":
    flask_generate()
