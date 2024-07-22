from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = []
        self._initialize_members()

    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member):
        if 'id' not in member:
            member['id'] = self._generate_id()
        member['last_name'] = self.last_name
        self._members.append(member)

    def delete_member(self, id):
        self._members = [member for member in self._members if member['id'] != id]

    def get_member(self, id):
        return next((member for member in self._members if member['id'] == id), None)

    def get_all_members(self):
        return self._members

    def _initialize_members(self):
        initial_members = [
            {"first_name": "John", "age": 33, "lucky_numbers": [7, 13, 22]},
            {"first_name": "Jane", "age": 35, "lucky_numbers": [10, 14, 3]},
            {"first_name": "Jimmy", "age": 5, "lucky_numbers": [1]}
        ]
        for member in initial_members:
            self.add_member(member)

# Initialize the Jackson family
jackson_family = FamilyStructure('Jackson')
