Description
---

PyCED is a library suite making implementation of Command Query
Responsibility Segregation, Event Sourcing and Domain Driven Design a bit easier.


Installation
---

    pip install git+https://github.com/lostwire/pyced.git#egg=pyced
    

Example
===


Defining aggregates
---

```python
import pyced

class UserAccount(pyced.AggregateRoot):
    @pyced.expect_empty
    def create(self, name):
        self.throw('Created', name=name)
    
    @pyced.unpack_event_data
    def apply_Created(self, name)
        self['name'] = name
```

