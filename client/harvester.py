from collector import MetrixCollector

if __name__ == "__main__":
    collector = MetrixCollector("test")
    print(collector.generate_json("127.0.0.1"))