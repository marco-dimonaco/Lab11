from dataclasses import dataclass
from model.go_products import Go_products


@dataclass
class Connessione:
    p1: Go_products
    p2: Go_products
    peso: int
