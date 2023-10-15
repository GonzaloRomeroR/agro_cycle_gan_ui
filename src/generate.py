def get_generate_command(values):
    generator = values.get("generator", "")
    images_path = values.get("images_path", "")
    dest_path = values.get("dest_path", "")
    dest_domain = values.get("dest_domain", "")
    image_resize_x = values.get("image_resize_x", "")
    dest_path = values.get("dest_path", "")
    image_resize_y = values.get("image_resize_y", "")

    process_list = [
        "python",
        "-u",
        "agro_cycle_gan/generate.py",
        images_path,
        dest_path,
        "--generator_name",
        generator,
        "--image_resize",
        image_resize_x,
        image_resize_y,
        "--dest_domain",
        dest_domain,
    ]
    return process_list
