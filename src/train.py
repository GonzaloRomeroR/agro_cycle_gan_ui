def get_train_command(values):
    dataset = values.get("dataset", "")
    epochs = values.get("epochs", "")
    resize_width = values.get("resize_width", "")
    resize_height = values.get("resize_height", "")
    batch_size = values.get("batch_size", "")
    generator = values.get("generator", "")
    discriminator = values.get("discriminator", "")
    tensorboard = values.get("tensorboard", "")
    store_models = values.get("store_models", "")
    metrics = values.get("metrics", "")
    load_models = values.get("load_models", "")
    download_datasets = values.get("download_datasets", "")
    comments = values.get("comments", "")
    db_connection_str = values.get("db_connection_str", "")
    crop_width = values.get("crop_width", "")
    crop_height = values.get("crop_height", "")

    process_list = [
        "python",
        "-u",
        "agro_cycle_gan/train.py",
        dataset,
        "--num_epochs",
        f"{epochs}",
        "--image_resize",
        f"{resize_width}",
        f"{resize_height}",
        "--batch_size",
        f"{batch_size}",
        "--discriminator",
        f"{discriminator}",
        "--generator",
        f"{generator}",
        "--comments",
        f"{comments}",
        "--db_connection_str",
        f"{db_connection_str}",
    ]

    # Checkboxes
    if tensorboard:
        process_list.append("--tensorboard")
    if store_models:
        process_list.append("--store_models")
    if metrics:
        process_list.append("--metrics")
    if load_models:
        process_list.append("--load_models")
    if download_datasets:
        process_list.append("--download_datasets")

    if crop_width and crop_height:
        process_list.append("--crop_size")
        process_list.append(f"{crop_width}")
        process_list.append(f"{crop_height}")

    return process_list
