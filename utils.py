def menu(title, options):
    print(f"\n===== {title} =====")
    for k, v in options.items():
        print(f"{k}. {v}")