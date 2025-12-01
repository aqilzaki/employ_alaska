class CreateStatusPernikahanDTO:
    def __init__(self, data):
        self.nama = data.get("nama")


class UpdateStatusPernikahanDTO:
    def __init__(self, data):
        self.nama = data.get("nama")
