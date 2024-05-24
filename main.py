from infraboard import InfraMonitor


def main():
    app = InfraMonitor(1, 10)
    app.run()


if __name__ == "__main__":
    main()
