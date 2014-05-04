import random
import unittest
from hsgame.agents.basic_agents import PredictableBot, DoNothingBot
from hsgame.replay import SavedGame
from tests.testing_agents import SpellTestingAgent, MinionPlayingAgent
from tests.testing_utils import generate_game_for

from hsgame.cards import *

__author__ = 'Daniel'

class TestMage(unittest.TestCase):

    def setUp(self):
        random.seed(1857)

    def testArcaneMissiles(self):
        game = generate_game_for(MogushanWarden, ArcaneMissiles, MinionPlayingAgent,SpellTestingAgent)

        game.play_single_turn()
        game.play_single_turn()

        self.assertEqual(27, game.other_player.health)

        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()
        game.play_single_turn()

        self.assertEqual(1, len(game.current_player.minions))
        self.assertEqual("Mogu'shan Warden", game.current_player.minions[0].card.name)

        game.play_single_turn()
        #The random numbers work so that both arcane missiles hit the Warden twice and the other player once
        self.assertEqual(10, game.other_player.health)
        self.assertEqual(3, game.other_player.minions[0].defense)

    def testArcaneMissilesWithSpellPower(self):
        game = SavedGame("tests/replays/card_tests/ArcaneMissilesWithSpellDamage.rep")
        game.start()

        self.assertEqual(1, len(game.current_player.minions))
        self.assertEqual(1, len(game.other_player.minions))
        self.assertEqual(1, game.other_player.minions[0].defense)
        self.assertEqual(2, game.other_player.minions[0].max_defense)
        self.assertEqual(27, game.other_player.health)

        return game

    def testWaterElemental(self):
        game = generate_game_for(WaterElemental, StonetuskBoar, PredictableBot, DoNothingBot)

        for turn in range(0, 11):
            game.play_single_turn()

        self.assertEqual(25, game.other_player.health)
        self.assertFalse(game.other_player.frozen_this_turn)
        self.assertFalse(game.other_player.frozen)
        self.assertEqual(1, len(game.current_player.minions))
        self.assertEqual(3, game.current_player.minions[0].attack_power)
        self.assertEqual(6, game.current_player.minions[0].defense)
        self.assertEqual("Water Elemental", game.current_player.minions[0].card.name)

        game.play_single_turn()
        game.play_single_turn()

        self.assertEqual(22, game.other_player.health)

        # Always false after the end of a turn
        self.assertFalse(game.other_player.frozen_this_turn)
        self.assertTrue(game.other_player.frozen)

    def testIceLance(self):
        game = generate_game_for(IceLance, OasisSnapjaw, SpellTestingAgent, MinionPlayingAgent)
        game.play_single_turn()

        self.assertTrue(game.other_player.frozen)
        self.assertEqual(30, game.other_player.health)

        game.play_single_turn()
        game.play_single_turn()

        self.assertTrue(game.other_player.frozen)
        self.assertEqual(26, game.other_player.health)

        for turn in range(0, 6):
            game.play_single_turn()

        self.assertEqual(1, len(game.other_player.minions))
        self.assertTrue(game.other_player.minions[0].frozen)
        self.assertEqual(7, game.other_player.minions[0].defense)

