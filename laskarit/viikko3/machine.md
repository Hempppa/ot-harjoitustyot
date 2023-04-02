sequenceDiagram
    Main->>+Machine: kone = Machine()
    Machine->>+FuelTank: self.tank = FuelTank()
    FuelTank-->>-Machine
    Machine->>+FuelTank: self.tank.fill(40)
    FuelTank-->>-Machine
    Machine->>+Engine: self.engine = Engine(self.tank)
    Engine-->>-Machine
    Machine-->>-Main
    Main->>+Machine: kone.drive()
    Machine->>+Engine: self.engine.start()
    Engine->>+FuelTank: self.tank.consume(5)
    FuelTank-->>-Engine
    Engine-->>-Machine
    Machine->>+Engine: self.engine.is_running()
    Engine-->>-Machine: True
    Machine->>+Engine: self.engine.use_energy()
    Engine->>+FuelTank: self.fuel_tank.consume(10)
    FuelTank-->>-Engine
    Engine-->>-Machine
    Machine-->>-Main
