class Transaction:
    # 1. This is a Class Variable. It belongs to the class itself, not individual objects.
    _id_counter = 1

    # 2. We add 'trans_id=None' to the parameters. 
    # If it's None, we know it's a new transaction.
    def __init__(self, name, price, date, time, income_type, trans_id=None):
        
        if trans_id is None:
            # It's a new transaction! Assign the current counter value, then increment it.
            self.id = Transaction._id_counter
            Transaction._id_counter += 1
        else:
            # It's an existing transaction being loaded from the CSV.
            self.id = int(trans_id)
            
            # Make sure our counter stays ahead of the loaded IDs to prevent duplicates
            if self.id >= Transaction._id_counter:
                Transaction._id_counter = self.id + 1

        self.name = name
        self.price = price
        self.date = date
        self.time = time
        self.income_type = income_type

    def __str__(self):
        # Update the string representation to include the ID
        return f"[{self.id}] {self.name} | {self.price} | {self.date} | {self.time} | {self.income_type}"