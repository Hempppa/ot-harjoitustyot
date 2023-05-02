from gamelogic.event_queue import EventQueue
from gamelogic.clock import Clock
import unittest
import time
import pygame

class TestClock(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.clock = Clock()

    def test_wait_time(self):
        start = time.time()
        for i in range(65):
            self.clock.tick(60)
        end = time.time()
        self.assertGreater(end-start, 1)
        self.assertGreater(self.clock.get_ticks(), 1000)

class TestEventQueue(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.event_queue = EventQueue()

    def test_returns_list(self):
        events = self.event_queue.get()
        for event in events:
            self.assertIsInstance(event, pygame.event.Event)
        self.assertEqual(len(self.event_queue.get()), 0)