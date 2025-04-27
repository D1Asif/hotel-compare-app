class HotelScraperPipeline:
    def __init__(self):
        self.items = []
        print("Pipeline initialized")  # Debug print

    def process_item(self, item, spider):
        print(f"Processing item in pipeline: {item}")  # Debug print
        self.items.append(item)
        return item

    def close_spider(self, spider):
        print(f"Closing spider, collected {len(self.items)} items")  # Debug print
        print(f"Items collected: {self.items}")  # Debug print
        return self.items 