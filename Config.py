if __name__ == "__main__":
    try:
        load_environment()
        app_config = get_app_config()
        run_application(app_config)
    except ValueError as e:
        print(f"Configuration Error: {e}")
        exit(1)
