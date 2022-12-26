import sys
from typing import List

sys.path.insert(0, "./agro_cycle_gan")
from agro_cycle_gan.train import train, Config

"""
Check that it is possible to use the agro_cycle_gan submodule
to train models from outside the platform
"""


def flask_train() -> None:
    train_model(
        dataset="horse2zebra", image_resize=[64, 64], batch_size=10, num_epochs=5
    )


def train_model(
    dataset: str, image_resize: List[int], batch_size: int, num_epochs: int
) -> None:
    config = Config()
    config.image_resize = image_resize
    config.use_dataset = dataset
    config.batch_size = batch_size
    config.num_epochs = num_epochs
    train(config)


if __name__ == "__main__":
    flask_train()
