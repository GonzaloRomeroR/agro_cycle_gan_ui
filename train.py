import sys

sys.path.insert(0, "./agro_cycle_gan")
from agro_cycle_gan.train import train, Config


if __name__ == "__main__":
    config = Config()
    config.image_resize = [64, 64]
    config.use_dataset = "horse2zebra"
    config.batch_size = 10
    config.num_epochs = 20
    train(config)
