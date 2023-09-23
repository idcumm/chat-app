def main():
    while True:
        try:
            exec(input())
        except Exception as e:
            print(f"Error({e})")


if __name__ == "__main__":
    main()
