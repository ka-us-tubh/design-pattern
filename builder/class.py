class QueryBuilder:
    def __init__(self):
        self.select_fields = []
        self.from_table = None
        self.where_clause = None
        self.order_by = None
        self.limit_count = None
    
    def select(self, *fields):
        self.select_fields = list(fields)
        return self
    
    def from_table(self, table):
        self.from_table = table
        return self
    
    def where(self, condition):
        self.where_clause = condition
        return self
    
    def order_by(self, field, direction="ASC"):
        self.order_by = f"{field} {direction}"
        return self
    
    def limit(self, count):
        self.limit_count = count
        return self
    
    def build(self):
        query = f"SELECT {','.join(self.select_fields)} FROM {self.from_table}"
        
        if self.where_clause:
            query += f" WHERE {self.where_clause}"
        if self.order_by:
            query += f" ORDER BY {self.order_by}"
        if self.limit_count:
            query += f" LIMIT {self.limit_count}"
        
        return query

# Usage
query = (QueryBuilder()
    .select("id", "name", "email")
    .from_table("users")
    .where("age > 18")
    .order_by("name")
    .limit(10)
    .build())

print(query)