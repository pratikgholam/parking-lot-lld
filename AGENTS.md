# AGENTS.md: parking-lot-lld

This file tells coding agents (and humans) what this project is, why it exists, and how to work on it. Read it fully before making changes.

## 1. Purpose

Build a small, framework-free Python library that models a parking lot, with clean object-oriented design. The code must demonstrate three design patterns (Strategy, Factory, State) in a way a reviewer can read in minutes.

## 2. Why we are building this

This is a learning and portfolio project, not a production parking system.

- **Learn low-level design:** the goal is to understand how patterns solve real design problems (changing pricing rules, creating objects of many types, managing lifecycle states), not to memorize pattern definitions.
- **Show design judgment on GitHub:** a focused repo with tests, a README, and a class diagram signals design skill to recruiters and interviewers more clearly than a large app with no structure.
- **Set up later projects:** the Strategy and State ideas carry into the movie ticketing system. The core domain thinking carries into the leaderboard and other designs.
- **Stay in the backend engineering comfort zone:** the project is plain Python with no web or AI dependencies, so the focus stays on the design itself.

## 3. Scope

### In scope
- Park a vehicle and return a ticket
- Unpark a vehicle by ticket and return a fee
- Assign the nearest free spot that fits the vehicle type
- Three vehicle types: motorcycle, car, large vehicle
- Three spot sizes matching those types (a larger vehicle can use a larger spot; a smaller vehicle cannot use a smaller spot)
- Pricing strategies: hourly, flat rate, and one peak-hour rule
- Availability query: count of free spots per spot type
- Spot states: free, occupied, out of service
- Clear errors for invalid operations

### Out of scope (do not build)
- Web API, database, or persistence (data lives in memory)
- Payments, real-time sensors, cameras, or license plate recognition
- Multiple floors or entry/exit gate hardware simulation (unless added as a later stage)
- Concurrency control or threading (note it in the README as a known limitation)
- Any AI or ML component
- Third-party dependencies beyond the standard library and `pytest`

## 4. Architecture

```
parking_lot/
  __init__.py
  models.py        # VehicleType, SpotType, Vehicle, ParkingSpot, Ticket
  states.py        # SpotState interface and concrete states (Free, Occupied, OutOfService)
  pricing.py       # PricingStrategy interface and implementations
  factory.py       # VehicleFactory, SpotFactory
  lot.py           # ParkingLot: orchestrates parking, unparking, availability
  errors.py        # Domain exceptions
tests/
  test_lot.py
  test_pricing.py
  test_states.py
  test_factory.py
main.py            # Demo: a few park/unpark cycles printed to stdout
README.md
AGENTS.md
pyproject.toml
```

### Domain model
- **VehicleType:** enum (MOTORCYCLE, CAR, LARGE)
- **SpotType:** enum (SMALL, MEDIUM, LARGE)
- **Vehicle:** plate number and vehicle type
- **ParkingSpot:** id, spot type, current state, occupying ticket (if any)
- **Ticket:** id, vehicle, spot id, entry time, exit time (set on unpark)
- **ParkingLot:** owns spots, active tickets, and a pricing strategy

### Patterns and their roles

| Pattern | Where it lives | Why it is here |
|---|---|---|
| **Strategy** | `pricing.py` | Pricing rules change independently of the lot logic. Adding a new rule should not require editing `ParkingLot`. |
| **Factory** | `factory.py` | Creating vehicles and spots from a type string or config should be centralized, so validation and defaults live in one place. |
| **State** | `states.py` | A spot's behavior depends on its state (park only when free, unpark only when occupied, reject when out of service). State objects replace scattered `if` checks. |

Do not add a pattern that has no clear job. Every pattern in the code must map to a row in the table above.

## 5. Rules for coding agents

### Code rules
- Python 3.11 or newer.
- Standard library only in the package. `pytest` is allowed for tests.
- Use `dataclasses` for simple data holders and `enum` for fixed sets of values.
- Use `abc.ABC` and `@abstractmethod` for Strategy and State interfaces.
- Type hints on all public functions and methods.
- No global mutable state. Pass dependencies in through constructors.
- Keep functions small. If a method needs more than about 30 lines, split it.
- Raise domain exceptions from `errors.py` (e.g., `LotFullError`, `TicketNotFoundError`, `SpotOutOfServiceError`). Do not raise bare `Exception` or return `None` to signal errors.
- Names should be domain words (`park`, `unpark`, `ticket`, `spot`), not generic ones (`process`, `handle`, `data`).

### Design rules
- The `ParkingLot` class coordinates; it does not calculate prices or decide spot states directly. Pricing goes through the Strategy, and state checks go through the State objects.
- A new pricing rule must be addable by creating one new class, with no edits to `lot.py`.
- A new vehicle type must be addable through the Factory and the compatibility rule, with minimal edits elsewhere. Document any place that still needs editing.
- Time must be injectable (pass a `clock` callable or a timestamp) so pricing and tests are deterministic. Do not call `datetime.now()` inside pricing logic.

### Testing rules
- Every public method has at least one test for the happy path and one for an error path.
- Pricing strategies are tested with fixed timestamps.
- Tests must not depend on execution order or shared state.
- Run `pytest` before declaring any task done.

### Documentation rules
- README must include: what the project is, how to run it, a class diagram (Mermaid or ASCII), and a "Why this pattern" section for each of the three patterns.
- Each pattern class or module gets a one-paragraph docstring stating its role in the design.
- Known limitations (no concurrency, in-memory only) must be listed in the README.

### Workflow rules
Work in this order. Do not skip ahead:
1. Domain models and basic park/unpark with a simple inline price (no patterns yet). Get tests passing.
2. Refactor pricing into the Strategy pattern.
3. Refactor spot behavior into the State pattern.
4. Add the Factory for vehicle and spot creation.
5. Add the availability query and the demo in `main.py`.
6. Write the README and diagram.

After each step, run tests and summarize what changed in one short paragraph.

### Commit rules
- Small commits, one logical change each.
- Commit messages in the form `<area>: <change>` (e.g., `pricing: add Strategy interface and hourly rule`).

## 6. Things agents must not do

- Do not add frameworks (FastAPI, Django, SQLAlchemy, etc.).
- Do not add a database or file storage.
- Do not add AI, ML, or external API calls.
- Do not delete or weaken existing tests to make them pass. If a test is wrong, explain why in the commit message.
- Do not add a pattern or abstraction that is not needed by a current requirement.
- Do not silently change the public API after tests are written. If a change is needed, update the tests and note it.

## 7. Definition of done

The project is done when all of the following are true:
- `pytest` passes with no skipped tests.
- `python main.py` runs a demo that parks and unparks several vehicles and prints fees.
- Full lot, double unpark, unknown ticket, and out-of-service spot each raise the correct domain error.
- A new pricing rule can be added by creating one class, and the README shows how.
- The README explains each pattern's role, has a class diagram, and lists limitations.
- The owner can explain each design choice and name one thing they would change for a real system.

## 8. Open decisions

Record the decision here when made. Until then, the agent should ask before assuming.

- Exact nearest-spot rule (lowest spot id, or closest to entrance with an entrance position)
- Fee rounding rule (round up to the next hour or charge per minute)
- Whether out-of-service spots can be set through a public method or only in tests
- Peak-hour window definition for the peak pricing strategy