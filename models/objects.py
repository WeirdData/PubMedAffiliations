class PubMedEntry:

    def __init__(self, data: list):
        self.raw = data
        self.title = data[0]
        self.url = data[1]
        self.authors = [x.strip().replace(".", "") for x in data[2].split(",")]
        self.details = data[3]
        short_details = data[4]
        try:
            self.year = int(short_details.strip()[-4:])
        except ValueError:
            self.year = 0
        self.journal = short_details.strip()[:-4].strip()
        self.resources = data[5]
        self.resources_type = data[6]
        self.identifiers = data[7]
        self.database = data[8]
        self.uid = data[9]
        self.properties = data[10]
