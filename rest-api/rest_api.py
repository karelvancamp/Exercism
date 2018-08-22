from collections import defaultdict
from datetime import datetime as dt
import json

class Person(object):
    """Object to display balance of a person as a dict/json"""
    def __init__(self, name, balance):
        
        self.name = name
        self.owes = {k:-v for k,v in balance.items() if v < 0}
        self.owed_by = {k:v for k,v in balance.items() if v > 0}
        self.balance = sum(balance.values())
        
class RestAPI(object):
    """Object used for both bookkeeping iou's and rest calls"""
    def __init__(self, database=None):
        
        # maintains ledger of all historic transations
        self.ledger = []
        
        # recalculated each time a record is added to the ledger
        ## balance per user (owes & owed)'''
        self.balance = {}
        ## list of unique users'''
        self.users = set()

        # dict unpacking ~= working with JSON's as inputs for defs
        self.add_database(**database)
    
    # Utils
      
    def add_user(self, name, owes = {}, owed_by = {}, balance = 0):
        """Creates ledger records for new users
        Doens't delete old debts if user already exists
        """
        # Datetime stam transaction, out scope for exercise but common sense
        now = str(dt.now())
        # Create new user with no debts
        if not balance:
            self.ledger.append((name, name, 0, now ))
        # generates ledger records based on json in
        else:
            for key,value in owed_by.items():
                self.ledger.append((name, key, value, now ))
                
    def add_database(self, users):
        """Create ledger records for initial users in class database input"""
        for user in users:
            self.add_user(**user)
        # trigger recalc ledger
        self.balance_ledger()
                
    def add_iou(self, lender, borrower, amount):
        """Add a IOU record to the ledger"""
        self.ledger.append((lender, borrower, amount, str(dt.now()) ))
        
    def balance_ledger(self):
        """Recaculates the balance per user
        and updates the list of users"""
        # not performance optimal
        self.balance = defaultdict(lambda: defaultdict(int))
        for owed, owes, amount, dt in self.ledger:
            self.balance[owed][owes] += amount
            self.balance[owes][owed] -= amount
        self.users = set(self.balance.keys())

    def balance_person(self, name):
        """Returns the balance of a person according to API specs"""
        return Person(name, self.balance[name]).__dict__

    # API
    
    ## API.Get
    
    def get_all(self):
        """Return the balance of all persons
        even if they have no debts or credit"""
        return [self.balance_person(name) 
                for name in self.users]
    
    def get_one(self, users):
        """Return the balance of a specific person"""
        return [self.balance_person(users)]
        
    def get(self, url, payload=None):
        """Get endpoint"""
        if not payload:
            answer =  self.get_all()
        else:
            answer = self.get_one(**json.loads(payload)) 
        # output as JSON string
        return json.dumps({'users':answer})
    
    ## API.Post
    
    def post_add(self, user):
        """Add a user and update balance"""
        self.add_user(user)
        self.balance_ledger()
        return self.balance_person(user)
    
    def post_iou(self, lender, borrower, amount):
        """Add an IOU records and update balance"""
        self.add_iou(lender, borrower, amount)
        self.balance_ledger()
        # Due to test case test_lender_has_negative_balance
        # Order of list not defined in api specifications
        a,b = sorted([borrower, lender]) 
        return {'users': [self.balance_person(a), 
                          self.balance_person(b)] }

    def post(self, url, payload=None):
        """Post endpoint"""
        payl = json.loads(payload)
        if url == '/add':
            answer = self.post_add(**payl)
        if url == '/iou':
            answer = self.post_iou(**payl)
        # output as JSON string
        return json.dumps(answer)