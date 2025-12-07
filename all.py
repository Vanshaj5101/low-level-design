# 1. Library Management System
# Problem: Design a system to manage books, members, and borrowing/returning books in a library.

# Solution:

# Classes:
# Book (attributes: ISBN, title, author, status; methods: update_status)
# Member (attributes: member_id, name, borrowed_books; methods: borrow_book, return_book)
# Library (attributes: books, members; methods: add_book, register_member)
# BorrowingService (handles borrow/return logic, fine calculation)
# NotificationService (interface for email/SMS notifications)
# SOLID:
# S: BorrowingService handles borrowing logic, NotificationService handles notifications.
# O: Extend notification types (email, SMS) via polymorphism.
# L: Subtypes of NotificationService (e.g., EmailNotification) are substitutable.
# I: Separate interfaces for borrowing and notifications.
# D: Depend on NotificationService abstraction.
# Design Pattern: Strategy (for notifications), Singleton (for Library).
# python

from abc import ABC, abstractmethod
from enum import Enum


class BookStatus(Enum):
    AVAILABLE = 1
    BORROWED = 2


class Book:
    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.status = BookStatus.AVAILABLE


class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, member, message):
        pass


class EmailNotification(NotificationService):
    def send_notification(self, member, message):
        print(f"Email to {member.name}: {message}")


class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.borrowed_books = []


class BorrowingService:
    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service

    def borrow_book(self, member: Member, book: Book):
        if book.status == BookStatus.AVAILABLE:
            book.status = BookStatus.BORROWED
            member.borrowed_books.append(book)
            self.notification_service.send_notification(
                member, f"Borrowed {book.title}"
            )
            return True
        return False


class Library:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.books = {}
            cls._instance.members = {}
        return cls._instance

    def add_book(self, book: Book):
        self.books[book.isbn] = book


# 2. Parking Lot
# Problem: Design a system to manage parking slots for different vehicle types.

# Solution:

# Classes:
# Vehicle (abstract; attributes: license_plate, type; subtypes: Car, Bike)
# ParkingSlot (attributes: slot_id, vehicle_type, is_occupied)
# ParkingLot (attributes: slots; methods: park_vehicle, remove_vehicle)
# PricingStrategy (interface for pricing; e.g., hourly, daily)
# SOLID:
# S: PricingStrategy handles pricing, ParkingLot manages slots.
# O: Add new vehicle types or pricing strategies without modifying core logic.
# L: Vehicle subtypes are substitutable.
# I: Separate interfaces for parking and pricing.
# D: Depend on PricingStrategy abstraction.
# Design Pattern: Strategy (pricing), Factory (slot allocation).
# python


from abc import ABC, abstractmethod
from enum import Enum


class VehicleType(Enum):
    CAR = 1
    BIKE = 2


class Vehicle(ABC):
    def __init__(self, license_plate, vehicle_type):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type


class Car(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, VehicleType.CAR)


class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, duration):
        pass


class HourlyPricing(PricingStrategy):
    def calculate_fee(self, duration):
        return duration * 5  # $5 per hour


class ParkingSlot:
    def __init__(self, slot_id, vehicle_type):
        self.slot_id = slot_id
        self.vehicle_type = vehicle_type
        self.is_occupied = False
        self.vehicle = None


class ParkingLot:
    def __init__(self, pricing_strategy: PricingStrategy):
        self.slots = {}  # slot_id -> ParkingSlot
        self.pricing_strategy = pricing_strategy

    def add_slot(self, slot: ParkingSlot):
        self.slots[slot.slot_id] = slot

    def park_vehicle(self, vehicle: Vehicle):
        for slot in self.slots.values():
            if not slot.is_occupied and slot.vehicle_type == vehicle.vehicle_type:
                slot.is_occupied = True
                slot.vehicle = vehicle
                return slot.slot_id
        return None


# 3. Amazon (Online Shopping System)
# Problem: Design an e-commerce platform for products, carts, and orders.

# Solution:

# Classes:
# Product (attributes: product_id, name, price, stock)
# Cart (attributes: user_id, items; methods: add_item, remove_item)
# Order (attributes: order_id, items, status; methods: place_order)
# PaymentService (interface for payment methods; e.g., CreditCard, UPI)
# InventoryManager (manages stock levels)
# SOLID:
# S: PaymentService handles payments, InventoryManager handles stock.
# O: Add new payment methods via polymorphism.
# L: Payment methods are substitutable.
# I: Separate interfaces for payment and inventory.
# D: Depend on PaymentService abstraction.
# Design Pattern: Strategy (payment), Observer (order status updates).
# python

from abc import ABC, abstractmethod
from enum import Enum


class OrderStatus(Enum):
    PENDING = 1
    CONFIRMED = 2


class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock


class PaymentService(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass


class CreditCardPayment(PaymentService):
    def process_payment(self, amount):
        print(f"Processed ${amount} via Credit Card")
        return True


class Cart:
    def __init__(self, user_id):
        self.user_id = user_id
        self.items = {}  # product_id -> quantity

    def add_item(self, product: Product, quantity: int):
        if product.stock >= quantity:
            self.items[product.product_id] = (
                self.items.get(product.product_id, 0) + quantity
            )
            return True
        return False


class Order:
    def __init__(self, order_id, cart: Cart, payment_service: PaymentService):
        self.order_id = order_id
        self.items = cart.items
        self.status = OrderStatus.PENDING
        self.payment_service = payment_service

    def place_order(self):
        total = sum(product.price * qty for product, qty in self.items.items())
        if self.payment_service.process_payment(total):
            self.status = OrderStatus.CONFIRMED
            return True
        return False


# 4. Stack Overflow
# Problem: Design a Q&A platform for users to post questions, answers, and comments.

# Solution:

# Classes:
# User (attributes: user_id, name, reputation)
# Question (attributes: question_id, title, content, tags, user)
# Post (abstract; attributes: post_id, content, user; subtypes: Question, Answer)
# Answer (attributes: answer_id, content, question, user)
# Comment (attributes: comment_id, content, user)
# Vote (attributes: vote_id, type, user, entity)
# SearchService (interface for searching questions)
# SOLID:
# S: SearchService handles search, Vote handles voting.
# O: Add new search algorithms via polymorphism.
# L: Search implementations are substitutable.
# I: Separate interfaces for voting and searching.
# D: Depend on SearchService abstraction.
# Design Pattern: Strategy (search), Composite (questions/answers/comments).
# python


from abc import ABC, abstractmethod
from enum import Enum


class VoteType(Enum):
    UPVOTE = 1
    DOWNVOTE = 2


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.reputation = 0


class Post:
    def __init__(self, post_id, content, user: User):
        self.post_id = post_id
        self.content = content
        self.user = user
        self.votes = []
        self.comments = []


class Question(Post):
    def __init__(self, question_id, title, content, user: User, tags):
        super().__init__(question_id, content, user)
        self.title = title
        self.tags = tags
        self.answers = []


class Answer(Post):
    def __init__(self, answer_id, content, question: Question, user: User):
        super().__init__(answer_id, content, user)
        self.question = question


class SearchService(ABC):
    @abstractmethod
    def search_questions(self, query, tags):
        pass


class KeywordSearch(SearchService):
    def search_questions(self, query, tags):
        # Simplified search logic
        return [question for question in questions if query in question.title]


class StackOverflow:
    def __init__(self, search_service: SearchService):
        self.questions = {}
        self.users = {}
        self.search_service = search_service

    def post_question(self, question: Question):
        self.questions[question.question_id] = question


# 5. Movie Ticket Booking System (BookMyShow)
# Problem: Design a system to book movie tickets for theaters.

# Solution:

# Classes:
# Movie (attributes: movie_id, title, duration)
# Theater (attributes: theater_id, name, screens)
# Screen (attributes: screen_id, seats, showtimes)
# Showtime (attributes: showtime_id, movie, time, available_seats)
# Booking (attributes: booking_id, user, seats, showtime)
# PaymentService (interface for payments)
# SOLID:
# S: PaymentService handles payments, Booking handles reservations.
# O: Add new payment methods or seat types.
# L: Payment methods are substitutable.
# I: Separate interfaces for booking and payment.
# D: Depend on PaymentService abstraction.
# Design Pattern: Strategy (payment), Factory (seat allocation).
# python


from abc import ABC, abstractmethod
from enum import Enum

# --- Enums and Basic Classes ---


class SeatStatus(Enum):
    AVAILABLE = 1
    BOOKED = 2


class Seat:
    def __init__(self, seat_id, seat_type="standard"):
        self.seat_id = seat_id
        self.type = seat_type  # e.g., 'standard', 'premium'


class Movie:
    def __init__(self, movie_id, title, duration):
        self.movie_id = movie_id
        self.title = title
        self.duration = duration


# --- Theater, Screen, Showtime ---


class Theater:
    def __init__(self, theater_id, name):
        self.theater_id = theater_id
        self.name = name
        self.screens = []  # List of Screen objects


class Screen:
    def __init__(self, screen_id):
        self.screen_id = screen_id
        self.seats = []  # List of Seat objects
        self.showtimes = []  # List of Showtime objects


class Showtime:
    def __init__(self, showtime_id, movie: Movie, screen: Screen, time):
        self.showtime_id = showtime_id
        self.movie = movie
        self.screen = screen
        self.time = time
        # Track available seats by seat_id for this showtime
        self.available_seats = set(seat.seat_id for seat in screen.seats)


# --- Payment Strategy Pattern ---


class PaymentService(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass


# Example payment method
class CreditCardPayment(PaymentService):
    def process_payment(self, amount):
        # Implement payment logic here
        return True


# --- Booking ---


class Booking:
    def __init__(
        self,
        booking_id,
        user_id,
        showtime: Showtime,
        seat_ids,
        payment_service: PaymentService,
    ):
        self.booking_id = booking_id
        self.user_id = user_id
        self.showtime = showtime
        self.seat_ids = seat_ids  # List of seat IDs to book
        self.payment_service = payment_service

    def _calculate_total(self):
        # For simplicity, assume $10 per seat
        return len(self.seat_ids) * 10

    def confirm_booking(self):
        # Check seat availability
        if not set(self.seat_ids).issubset(self.showtime.available_seats):
            return False
        # Process payment
        total = self._calculate_total()
        if self.payment_service.process_payment(total):
            # Mark seats as booked for this showtime
            self.showtime.available_seats -= set(self.seat_ids)
            return True
        return False


# 6. ATM
# Problem: Design an ATM system for withdrawals, deposits, and balance inquiries.

# Solution:

# Classes:
# Account (attributes: account_id, balance)
# Card (attributes: card_id, account)
# ATM (attributes: atm_id, cash_dispenser; methods: authenticate, withdraw, deposit)
# Transaction (abstract; subtypes: Withdrawal, Deposit)
# CashDispenser (manages cash inventory)
# SOLID:
# S: CashDispenser handles cash, Transaction handles operations.
# O: Add new transaction types (e.g., Transfer).
# L: Transaction subtypes are substitutable.
# I: Separate interfaces for authentication and transactions.
# D: Depend on Transaction abstraction.
# Design Pattern: Template Method (transaction processing), Singleton (ATM).


from abc import ABC, abstractmethod


class Transaction(ABC):
    def __init__(self, transaction_id, amount):
        self.transaction_id = transaction_id
        self.amount = amount

    @abstractmethod
    def execute(self, account):
        pass


class Withdrawal(Transaction):
    def execute(self, account):
        if account.balance >= self.amount:
            account.balance -= self.amount
            return True
        return False


class Account:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance


class CashDispenser:
    def __init__(self):
        self.cash = 10000  # Initial cash

    def dispense(self, amount):
        if self.cash >= amount:
            self.cash -= amount
            return True
        return False


class ATM:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.cash_dispenser = CashDispenser()
        return cls._instance

    def withdraw(self, account: Account, amount):
        transaction = Withdrawal("TX1", amount)
        if transaction.execute(account) and self.cash_dispenser.dispense(amount):
            return True
        return False


# 7. Airline Management System
# Problem: Design a system to manage flights, bookings, and passengers.

# Solution:

# Classes:
# Flight (attributes: flight_id, origin, destination, seats)
# Passenger (attributes: passenger_id, name)
# Booking (attributes: booking_id, flight, passenger, seat)
# Seat (attributes: seat_id, status)
# PaymentService (interface for payments)
# SOLID:
# S: PaymentService handles payments, Booking handles reservations.
# O: Add new seat types or payment methods.
# L: Payment methods are substitutable.
# I: Separate interfaces for booking and payment.
# D: Depend on PaymentService abstraction.
# Design Pattern: Strategy (payment), Factory (seat allocation).


from abc import ABC, abstractmethod
from enum import Enum


class SeatStatus(Enum):
    AVAILABLE = 1
    BOOKED = 2


class Flight:
    def __init__(self, flight_id, origin, destination):
        self.flight_id = flight_id
        self.origin = origin
        self.destination = destination
        self.seats = {}


class Seat:
    def __init__(self, seat_id):
        self.seat_id = seat_id
        self.status = SeatStatus.AVAILABLE


class Passenger:
    def __init__(self, passenger_id, name):
        self.passenger_id = passenger_id
        self.name = name


class PaymentService(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass


class Booking:
    def __init__(
        self,
        booking_id,
        flight: Flight,
        passenger: Passenger,
        seat: Seat,
        payment_service: PaymentService,
    ):
        self.booking_id = booking_id
        self.flight = flight
        self.passenger = passenger
        self.seat = seat
        self.payment_service = payment_service

    def confirm_booking(self):
        if (
            self.seat.status == SeatStatus.AVAILABLE
            and self.payment_service.process_payment(100)
        ):
            self.seat.status = SeatStatus.BOOKED
            return True
        return False


# 8. Blackjack and a Deck of Cards
# Problem: Design a Blackjack game with a deck of cards.

# Solution:

# Classes:
# Card (attributes: suit, rank, value)
# Deck (attributes: cards; methods: shuffle, deal)
# Player (attributes: name, hand, score)
# Game (attributes: players, deck; methods: start, hit, stand)
# SOLID:
# S: Deck handles cards, Game handles rules.
# O: Add new card types or game variants.
# L: Card types are substitutable.
# I: Separate interfaces for deck and game logic.
# D: Depend on Deck abstraction.
# Design Pattern: Factory (card creation), State (game phases).


from enum import Enum
import random


class Suit(Enum):
    HEARTS = 1
    DIAMONDS = 2


class Rank(Enum):
    ACE = 1
    KING = 13


class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank
        self.value = min(10, rank.value) if rank != Rank.ACE else 11


class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop() if self.cards else None


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0

    def add_card(self, card: Card):
        self.hand.append(card)
        self.score += card.value


class Blackjack:
    def __init__(self):
        self.deck = Deck()
        self.players = [Player("Player"), Player("Dealer")]

    def start(self):
        for _ in range(2):
            for player in self.players:
                player.add_card(self.deck.deal())


# 9. Hotel Management System
# Problem: Design a system to manage hotel rooms, bookings, and payments.

# Solution:

# Classes:
# Room (attributes: room_id, type, price, status)
# Guest (attributes: guest_id, name)
# Booking (attributes: booking_id, room, guest, dates)
# PaymentService (interface for payments)
# Hotel (attributes: rooms, bookings)
# SOLID:
# S: PaymentService handles payments, Booking handles reservations.
# O: Add new room types or payment methods.
# L: Payment methods are substitutable.
# I: Separate interfaces for booking and payment.
# D: Depend on PaymentService abstraction.
# Design Pattern: Strategy (payment), Factory (room allocation).


from abc import ABC, abstractmethod
from enum import Enum


class RoomStatus(Enum):
    AVAILABLE = 1
    BOOKED = 2


class Room:
    def __init__(self, room_id, room_type, price):
        self.room_id = room_id
        self.room_type = room_type
        self.price = price
        self.status = RoomStatus.AVAILABLE


class Guest:
    def __init__(self, guest_id, name):
        self.guest_id = guest_id
        self.name = name


class PaymentService(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass


class Booking:
    def __init__(
        self, booking_id, room: Room, guest: Guest, payment_service: PaymentService
    ):
        self.booking_id = booking_id
        self.room = room
        self.guest = guest
        self.payment_service = payment_service

    def confirm_booking(self):
        if (
            self.room.status == RoomStatus.AVAILABLE
            and self.payment_service.process_payment(self.room.price)
        ):
            self.room.status = RoomStatus.BOOKED
            return True
        return False


# 10. Restaurant Management System
# Problem: Design a system to manage restaurant tables, orders, and payments.

# Solution:

# Classes:
# Table (attributes: table_id, capacity, status)
# Menu (attributes: items; methods: add_item)
# Order (attributes: order_id, table, items, status)
# PaymentService (interface for payments)
# Restaurant (attributes: tables, menu, orders)
# SOLID:
# S: PaymentService handles payments, Order handles orders.
# O: Add new payment methods or menu items.
# L: Payment methods are substitutable.
# I: Separate interfaces for orders and payments.
# D: Depend on PaymentService abstraction.
# Design Pattern: Strategy (payment), Factory (table allocation).


from abc import ABC, abstractmethod
from enum import Enum


class TableStatus(Enum):
    AVAILABLE = 1
    OCCUPIED = 2


class Table:
    def __init__(self, table_id, capacity):
        self.table_id = table_id
        self.capacity = capacity
        self.status = TableStatus.AVAILABLE


class MenuItem:
    def __init__(self, item_id, name, price):
        self.item_id = item_id
        self.name = name
        self.price = price


class PaymentService(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass


class Order:
    def __init__(self, order_id, table: Table, items, payment_service: PaymentService):
        self.order_id = order_id
        self.table = table
        self.items = items
        self.payment_service = payment_service

    def complete_order(self):
        total = sum(item.price for item in self.items)
        if self.payment_service.process_payment(total):
            self.table.status = TableStatus.AVAILABLE
            return True
        return False


# 11. Chess
# Problem: Design a chess game with board, pieces, and rules.

# Solution:

# Classes:
# Piece (abstract; attributes: color, position; subtypes: King, Queen, etc.)
# Board (attributes: squares; methods: move_piece, get_piece)
# Player (attributes: color, pieces)
# Game (attributes: board, players, turn; methods: make_move, checkmate)
# SOLID:
# S: Piece handles moves, Game handles rules.
# O: Add new piece types or rule variants.
# L: Piece subtypes are substitutable.
# I: Separate interfaces for moves and game state.
# D: Depend on Piece abstraction.
# Design Pattern: Strategy (move validation), State (game phases).


from abc import ABC, abstractmethod
from enum import Enum


class Color(Enum):
    WHITE = 1
    BLACK = 2


class Piece(ABC):
    def __init__(self, color: Color, position):
        self.color = color
        self.position = position

    @abstractmethod
    def is_valid_move(self, new_position, board):
        pass


class King(Piece):
    def is_valid_move(self, new_position, board):
        # Simplified: one square in any direction
        dx, dy = abs(new_position[0] - self.position[0]), abs(
            new_position[1] - self.position[1]
        )
        return dx <= 1 and dy <= 1


class Board:
    def __init__(self):
        self.squares = {}  # (x, y) -> Piece

    def move_piece(self, piece: Piece, new_position):
        if piece.is_valid_move(new_position, self):
            self.squares.pop(piece.position, None)
            piece.position = new_position
            self.squares[new_position] = piece
            return True
        return False


class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player(Color.WHITE), Player(Color.BLACK)]
        self.turn = Color.WHITE


# 12. Online Stock Brokerage System
# Problem: Design a system to trade stocks and manage portfolios.

# Solution:

# Classes:
# Stock (attributes: ticker, price)
# User (attributes: user_id, portfolio, balance)
# Order (attributes: order_id, user, stock, quantity, type; subtypes: BuyOrder, SellOrder)
# Portfolio (attributes: holdings)
# TradingService (handles order execution)
# SOLID:
# S: TradingService handles trades, Portfolio manages holdings.
# O: Add new order types or trading strategies.
# L: Order subtypes are substitutable.
# I: Separate interfaces for trading and portfolio management.
# D: Depend on Order abstraction.
# Design Pattern: Strategy (order execution), Observer (price updates).


from abc import ABC, abstractmethod
from enum import Enum


class OrderType(Enum):
    BUY = 1
    SELL = 2


class Stock:
    def __init__(self, ticker, price):
        self.ticker = ticker
        self.price = price


class Order(ABC):
    def __init__(self, order_id, user, stock: Stock, quantity):
        self.order_id = order_id
        self.user = user
        self.stock = stock
        self.quantity = quantity

    @abstractmethod
    def execute(self):
        pass


class BuyOrder(Order):
    def execute(self):
        total = self.stock.price * self.quantity
        if self.user.balance >= total:
            self.user.balance -= total
            self.user.portfolio.add_holding(self.stock, self.quantity)
            return True
        return False


class Portfolio:
    def __init__(self):
        self.holdings = {}  # ticker -> quantity

    def add_holding(self, stock: Stock, quantity):
        self.holdings[stock.ticker] = self.holdings.get(stock.ticker, 0) + quantity


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.portfolio = Portfolio()
        self.balance = 10000  # Initial balance


# 13. LinkedIn
# Problem: Design a professional networking platform for users, connections, and posts.

# Solution:

# Classes:
# User (attributes: user_id, name, connections, posts)
# Connection (attributes: user1, user2, status)
# Post (attributes: post_id, content, user)
# NotificationService (interface for notifications)
# Network (attributes: users, connections)
# SOLID:
# S: NotificationService handles notifications, Network manages connections.
# O: Add new notification types or post formats.
# L: Notification types are substitutable.
# I: Separate interfaces for notifications and connections.
# D: Depend on NotificationService abstraction.
# Design Pattern: Observer (notifications), Graph (connections).


from abc import ABC, abstractmethod
from enum import Enum


class ConnectionStatus(Enum):
    PENDING = 1
    ACCEPTED = 2


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.connections = set()
        self.posts = []


class Post:
    def __init__(self, post_id, content, user: User):
        self.post_id = post_id
        self.content = content
        self.user = user


class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, user, message):
        pass


class Network:
    def __init__(self, notification_service: NotificationService):
        self.users = {}
        self.notification_service = notification_service

    def add_connection(self, user1: User, user2: User):
        connection = Connection(user1, user2, ConnectionStatus.PENDING)
        self.notification_service.send_notification(
            user2, f"Connection request from {user1.name}"
        )
        return connection


# 14. Cricinfo (Sports Website)
# Problem: Design a sports website for live scores, match details, and player stats.

# Solution:

# Classes:
# Match (attributes: match_id, teams, status, score)
# Team (attributes: team_id, name, players)
# Player (attributes: player_id, name, stats)
# ScoreUpdateService (interface for live updates)
# Commentary (attributes: comment_id, text, match)
# SOLID:
# S: ScoreUpdateService handles updates, Match manages state.
# O: Add new update channels or stats.
# L: Update services are substitutable.
# I: Separate interfaces for scores and commentary.
# D: Depend on ScoreUpdateService abstraction.
# Design Pattern: Observer (score updates), Facade (match details).


from abc import ABC, abstractmethod
from enum import Enum


class MatchStatus(Enum):
    LIVE = 1
    FINISHED = 2


class Team:
    def __init__(self, team_id, name):
        self.team_id = team_id
        self.name = name
        self.players = []


class Match:
    def __init__(self, match_id, team1: Team, team2: Team):
        self.match_id = match_id
        self.teams = [team1, team2]
        self.status = MatchStatus.LIVE
        self.score = {team1.team_id: 0, team2.team_id: 0}


class ScoreUpdateService(ABC):
    @abstractmethod
    def update_score(self, match: Match, team: Team, runs):
        pass


class LiveScoreUpdate(ScoreUpdateService):
    def update_score(self, match: Match, team: Team, runs):
        match.score[team.team_id] += runs
        print(f"Updated score: {team.name} {match.score[team.team_id]}")


# 15. Facebook (Social Network)
# Problem: Design a social network for users, posts, and friendships.

# Solution:

# Classes:
# User (attributes: user_id, name, friends, posts)
# Post (attributes: post_id, content, user, likes)
# Friendship (attributes: user1, user2, status)
# NotificationService (interface for notifications)
# SOLID:
# S: NotificationService handles notifications, User manages posts.
# O: Add new post types or notification channels.
# L: Notification types are substitutable.
# I: Separate interfaces for posts and friendships.
# D: Depend on NotificationService abstraction.
# Design Pattern: Observer (notifications), Graph (friendships).


from abc import ABC, abstractmethod
from enum import Enum


class FriendshipStatus(Enum):
    PENDING = 1
    ACCEPTED = 2


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.friends = set()
        self.posts = []


class Post:
    def __init__(self, post_id, content, user: User):
        self.post_id = post_id
        self.content = content
        self.user = user
        self.likes = set()


class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, user, message):
        pass


class SocialNetwork:
    def __init__(self, notification_service: NotificationService):
        self.users = {}
        self.notification_service = notification_service

    def add_friend(self, user1: User, user2: User):
        friendship = Friendship(user1, user2, FriendshipStatus.PENDING)
        self.notification_service.send_notification(
            user2, f"Friend request from {user1.name}"
        )
        return friendship


# 16. Cab Booking (Uber)
# Problem: Design a cab booking system for riders and drivers.

# Solution:

# Classes:
# Rider (attributes: rider_id, name, location)
# Driver (attributes: driver_id, name, location, status)
# Trip (attributes: trip_id, rider, driver, status, fare)
# PricingStrategy (interface for fare calculation)
# MatchingService (matches riders to drivers)
# SOLID:
# S: PricingStrategy handles fares, MatchingService handles matching.
# O: Add new pricing or matching algorithms.
# L: Pricing strategies are substitutable.
# I: Separate interfaces for pricing and matching.
# D: Depend on PricingStrategy abstraction.
# Design Pattern: Strategy (pricing), Factory (driver matching).


from abc import ABC, abstractmethod
from enum import Enum


class TripStatus(Enum):
    REQUESTED = 1
    ONGOING = 2


class Rider:
    def __init__(self, rider_id, name, location):
        self.rider_id = rider_id
        self.name = name
        self.location = location


class Driver:
    def __init__(self, driver_id, name, location):
        self.driver_id = driver_id
        self.name = name
        self.location = location
        self.is_available = True


class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fare(self, distance):
        pass


class DistanceBasedPricing(PricingStrategy):
    def calculate_fare(self, distance):
        return distance * 2  # $2 per km


class Trip:
    def __init__(
        self, trip_id, rider: Rider, driver: Driver, pricing_strategy: PricingStrategy
    ):
        self.trip_id = trip_id
        self.rider = rider
        self.driver = driver
        self.status = TripStatus.REQUESTED
        self.pricing_strategy = pricing_strategy

    def start_trip(self, distance):
        self.status = TripStatus.ONGOING
        self.fare = self.pricing_strategy.calculate_fare(distance)
        self.driver.is_available = False


# 17. Chatting
# Problem: Design a chat application for users and messages.

# Solution:

# Classes:
# User (attributes: user_id, name, chats)
# Chat (attributes: chat_id, participants, messages)
# Message (attributes: message_id, content, sender, timestamp)
# NotificationService (interface for notifications)
# SOLID:
# S: NotificationService handles notifications, Chat manages messages.
# O: Add new message types or notification channels.
# L: Notification types are substitutable.
# I: Separate interfaces for chats and notifications.
# D: Depend on NotificationService abstraction.
# Design Pattern: Observer (notifications), Composite (chat structure).


from abc import ABC, abstractmethod
from datetime import datetime


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.chats = []


class Message:
    def __init__(self, message_id, content, sender: User):
        self.message_id = message_id
        self.content = content
        self.sender = sender
        self.timestamp = datetime.now()


class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, user, message):
        pass


class Chat:
    def __init__(
        self, chat_id, participants, notification_service: NotificationService
    ):
        self.chat_id = chat_id
        self.participants = participants
        self.messages = []
        self.notification_service = notification_service

    def send_message(self, message: Message):
        self.messages.append(message)
        for participant in self.participants:
            if participant != message.sender:
                self.notification_service.send_notification(
                    participant, f"New message: {message.content}"
                )


# 18. Calendar
# Problem: Design a calendar system for events and reminders.

# Solution:

# Classes:
# User (attributes: user_id, name, calendar)
# Event (attributes: event_id, title, time, participants)
# Reminder (attributes: reminder_id, event, time)
# NotificationService (interface for reminders)
# SOLID:
# S: NotificationService handles reminders, Event manages details.
# O: Add new reminder types or event formats.
# L: Notification types are substitutable.
# I: Separate interfaces for events and reminders.
# D: Depend on NotificationService abstraction.
# Design Pattern: Observer (reminders), Factory (event creation).


from abc import ABC, abstractmethod
from datetime import datetime


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.events = []


class Event:
    def __init__(self, event_id, title, time, participants):
        self.event_id = event_id
        self.title = title
        self.time = time
        self.participants = participants


class NotificationService(ABC):
    @abstractmethod
    def send_reminder(self, user, event):
        pass


class Calendar:
    def __init__(self, notification_service: NotificationService):
        self.events = {}
        self.notification_service = notification_service

    def add_event(self, event: Event):
        self.events[event.event_id] = event
        for participant in event.participants:
            self.notification_service.send_reminder(participant, event)


# 19. Blog Site
# Problem: Design a blogging platform for posts and comments.

# Solution:

# Classes:
# User (attributes: user_id, name, posts)
# Post (attributes: post_id, title, content, author)
# Comment (attributes: comment_id, content, user, post)
# NotificationService (interface for notifications)
# SOLID:
# S: NotificationService handles notifications, Post manages content.
# O: Add new comment types or notification channels.
# L: Notification types are substitutable.
# I: Separate interfaces for posts and comments.
# D: Depend on NotificationService abstraction.
# Design Pattern: Observer (notifications), Composite (post-comment hierarchy).


from abc import ABC, abstractmethod


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.posts = []


class Post:
    def __init__(self, post_id, title, content, author: User):
        self.post_id = post_id
        self.title = title
        self.content = content
        self.author = author
        self.comments = []


class Comment:
    def __init__(self, comment_id, content, user: User, post: Post):
        self.comment_id = comment_id
        self.content = content
        self.user = user
        self.post = post


class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, user, message):
        pass


class Blog:
    def __init__(self, notification_service: NotificationService):
        self.posts = {}
        self.notification_service = notification_service

    def add_comment(self, comment: Comment):
        comment.post.comments.append(comment)
        self.notification_service.send_notification(
            comment.post.author, f"New comment: {comment.content}"
        )


# 20. Food Delivery
# Problem: Design a food delivery system for restaurants, orders, and delivery.

# Solution:

# Classes:
# Restaurant (attributes: restaurant_id, name, menu)
# MenuItem (attributes: item_id, name, price)
# Order (attributes: order_id, user, items, status)
# DeliveryAgent (attributes: agent_id, location, status)
# PaymentService (interface for payments)
# SOLID:
# S: PaymentService handles payments, Order manages orders.
# O: Add new payment methods or delivery strategies.
# L: Payment methods are substitutable.
# I: Separate interfaces for orders and delivery.
# D: Depend on PaymentService abstraction.
# Design Pattern: Strategy (payment), Factory (agent assignment).


from abc import ABC, abstractmethod
from enum import Enum


class OrderStatus(Enum):
    PLACED = 1
    DELIVERED = 2


class Restaurant:
    def __init__(self, restaurant_id, name):
        self.restaurant_id = restaurant_id
        self.name = name
        self.menu = []


class MenuItem:
    def __init__(self, item_id, name, price):
        self.item_id = item_id
        self.name = name
        self.price = price


class PaymentService(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass


class Order:
    def __init__(
        self,
        order_id,
        user_id,
        restaurant: Restaurant,
        items,
        payment_service: PaymentService,
    ):
        self.order_id = order_id
        self.user_id = user_id
        self.restaurant = restaurant
        self.items = items
        self.status = OrderStatus.PLACED
        self.payment_service = payment_service

    def confirm_order(self):
        total = sum(item.price for item in self.items)
        if self.payment_service.process_payment(total):
            self.status = OrderStatus.DELIVERED
            return True
        return False


# 21. Vending Machine
# Problem: Design a vending machine for products and payments.

# Solution:

# Classes:
# Product (attributes: product_id, name, price, stock)
# PaymentService (interface for payments; e.g., Cash, Card)
# VendingMachine (attributes: products, cash; methods: select_product, process_payment)
# Inventory (manages product stock)
# SOLID:
# S: PaymentService handles payments, Inventory manages stock.
# O: Add new payment methods or products.
# L: Payment methods are substitutable.
# I: Separate interfaces for payment and inventory.
# D: Depend on PaymentService abstraction.
# Design Pattern: State (machine states), Strategy (payment).


from abc import ABC, abstractmethod


class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock


class PaymentService(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass


class CashPayment(PaymentService):
    def process_payment(self, amount):
        print(f"Processed ${amount} in cash")
        return True


class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product: Product):
        self.products[product.product_id] = product

    def dispense_product(self, product_id):
        product = self.products.get(product_id)
        if product and product.stock > 0:
            product.stock -= 1
            return True
        return False


class VendingMachine:
    def __init__(self, payment_service: PaymentService):
        self.inventory = Inventory()
        self.payment_service = payment_service
        self.selected_product = None

    def select_product(self, product_id):
        self.selected_product = self.inventory.products.get(product_id)

    def process_payment(self):
        if self.selected_product and self.payment_service.process_payment(
            self.selected_product.price
        ):
            if self.inventory.dispense_product(self.selected_product.product_id):
                return True
        return False


# 22. Traffic Lights
# Problem: Design a traffic light system for intersections.

# Solution:

# Classes:
# TrafficLight (attributes: light_id, state, timer)
# Intersection (attributes: lights, schedule; methods: change_state)
# LightState (enum: RED, GREEN, YELLOW)
# Timer (manages state transitions)
# SOLID:
# S: Timer handles timing, TrafficLight manages state.
# O: Add new light states or schedules.
# L: Light states are substitutable.
# I: Separate interfaces for timing and state changes.
# D: Depend on Timer abstraction.
# Design Pattern: State (light states), Singleton (intersection).


from enum import Enum
from time import sleep


class LightState(Enum):
    RED = 1
    GREEN = 2
    YELLOW = 3


class Timer:
    def __init__(self, duration):
        self.duration = duration

    def wait(self):
        sleep(self.duration)


class TrafficLight:
    def __init__(self, light_id, state: LightState):
        self.light_id = light_id
        self.state = state
        self.timer = Timer(30)  # Default 30s

    def change_state(self, new_state: LightState):
        self.state = new_state
        print(f"Light {self.light_id} is now {self.state}")
        self.timer.wait()


class Intersection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.lights = {}
        return cls._instance

    def add_light(self, light: TrafficLight):
        self.lights[light.light_id] = light

    def change_all_states(self, states):
        for light_id, state in states.items():
            self.lights[light_id].change_state(state)


# 23. Elevator
# Problem: Design an elevator system for a building.

# Solution:

# Classes:
# Elevator (attributes: elevator_id, current_floor, state, requests)
# Request (attributes: floor, direction)
# Building (attributes: elevators, floors)
# Scheduler (interface for request assignment; e.g., NearestElevator)
# SOLID:
# S: Scheduler handles assignments, Elevator manages movement.
# O: Add new scheduling algorithms or elevator types.
# L: Scheduler implementations are substitutable.
# I: Separate interfaces for scheduling and movement.
# D: Depend on Scheduler abstraction.
# Design Pattern: Strategy (scheduling), State (elevator states).


from abc import ABC, abstractmethod
from enum import Enum


class ElevatorState(Enum):
    IDLE = 1
    MOVING = 2


class Request:
    def __init__(self, floor, direction):
        self.floor = floor
        self.direction = direction


class Scheduler(ABC):
    @abstractmethod
    def assign_elevator(self, request, elevators):
        pass


class NearestElevatorScheduler(Scheduler):
    def assign_elevator(self, request, elevators):
        return min(elevators, key=lambda e: abs(e.current_floor - request.floor))


class Elevator:
    def __init__(self, elevator_id, current_floor):
        self.elevator_id = elevator_id
        self.current_floor = current_floor
        self.state = ElevatorState.IDLE
        self.requests = []

    def move_to(self, floor):
        self.state = ElevatorState.MOVING
        self.current_floor = floor
        self.state = ElevatorState.IDLE


class Building:
    def __init__(self, scheduler: Scheduler):
        self.elevators = {}
        self.scheduler = scheduler

    def add_elevator(self, elevator: Elevator):
        self.elevators[elevator.elevator_id] = elevator

    def request_elevator(self, request: Request):
        elevator = self.scheduler.assign_elevator(request, self.elevators.values())
        elevator.requests.append(request)
        elevator.move_to(request.floor)


# 24. Meeting Scheduler
# Problem: Design a system to schedule meetings with rooms and participants.

# Solution:

# Classes:
# User (attributes: user_id, name, calendar)
# Meeting (attributes: meeting_id, time, participants, room)
# Room (attributes: room_id, capacity, schedule)
# NotificationService (interface for notifications)
# Scheduler (finds available rooms and times)
# SOLID:
# S: Scheduler handles scheduling, NotificationService handles notifications.
# O: Add new scheduling algorithms or notification types.
# L: Notification types are substitutable.
# I: Separate interfaces for scheduling and notifications.
# D: Depend on NotificationService abstraction.
# Design Pattern: Strategy (scheduling), Observer (notifications).


from abc import ABC, abstractmethod
from datetime import datetime


class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.schedule = []


class Room:
    def __init__(self, room_id, capacity):
        self.room_id = room_id
        self.capacity = capacity
        self.schedule = []


class Meeting:
    def __init__(self, meeting_id, time, participants, room: Room):
        self.meeting_id = meeting_id
        self.time = time
        self.participants = participants
        self.room = room


class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, user, message):
        pass


class Scheduler:
    def __init__(self, notification_service: NotificationService):
        self.rooms = {}
        self.notification_service = notification_service

    def schedule_meeting(self, meeting: Meeting):
        room = meeting.room
        if not any(m.time == meeting.time for m in room.schedule):
            room.schedule.append(meeting)
            for participant in meeting.participants:
                self.notification_service.send_notification(
                    participant, f"Meeting scheduled at {meeting.time}"
                )
            return True
        return False


# 25. Car Rental
# Problem: Design a car rental system for vehicles, bookings, and payments.

# Solution:

# Classes:
# Vehicle (attributes: vehicle_id, type, price, status)
# Customer (attributes: customer_id, name)
# Booking (attributes: booking_id, vehicle, customer, dates)
# PaymentService (interface for payments)
# RentalService (manages fleet and bookings)
# SOLID:
# S: PaymentService handles payments, RentalService manages bookings.
# O: Add new vehicle types or payment methods.
# L: Payment methods are substitutable.
# I: Separate interfaces for bookings and payments.
# D: Depend on PaymentService abstraction.
# Design Pattern: Strategy (payment), Factory (vehicle allocation).


from abc import ABC, abstractmethod
from enum import Enum


class VehicleStatus(Enum):
    AVAILABLE = 1
    BOOKED = 2


class Vehicle:
    def __init__(self, vehicle_id, vehicle_type, price):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.price = price
        self.status = VehicleStatus.AVAILABLE


class Customer:
    def __init__(self, customer_id, name):
        self.customer_id = customer_id
        self.name = name


class PaymentService(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass


class Booking:
    def __init__(
        self,
        booking_id,
        vehicle: Vehicle,
        customer: Customer,
        payment_service: PaymentService,
    ):
        self.booking_id = booking_id
        self.vehicle = vehicle
        self.customer = customer
        self.payment_service = payment_service

    def confirm_booking(self):
        if (
            self.vehicle.status == VehicleStatus.AVAILABLE
            and self.payment_service.process_payment(self.vehicle.price)
        ):
            self.vehicle.status = VehicleStatus.BOOKED
            return True
        return False


class RentalService:
    def __init__(self):
        self.vehicles = {}
        self.bookings = {}

    def add_vehicle(self, vehicle: Vehicle):
        self.vehicles[vehicle.vehicle_id] = vehicle

    def create_booking(self, booking: Booking):
        if booking.confirm_booking():
            self.bookings[booking.booking_id] = booking
            return True
        return False


"""
FULL SKELETON: System Blueprints with Initializers and Method Stubs
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict, Optional, Any
import threading


# 1. Library Management System
class Book:
    def __init__(self, isbn: str, title: str, author: str, status: str):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.status = status  # 'available'/'borrowed'


class Member:
    def __init__(self, member_id: str, name: str):
        self.member_id = member_id
        self.name = name
        self.borrowed_books: List[Book] = []

    def borrow_book(self, book: Book):
        # stub: add book to borrowed_books
        pass

    def return_book(self, book: Book):
        # stub: remove book from borrowed_books
        pass


class Library:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.books: Dict[str, Book] = {}
        self.members: Dict[str, Member] = {}

    def add_book(self, book: Book):
        # stub: add book to self.books
        pass

    def register_member(self, member: Member):
        # stub: add member to self.members
        pass


class NotificationService(ABC):
    @abstractmethod
    def send_notification(self, member: Member, message: str):
        pass


class EmailNotification(NotificationService):
    def send_notification(self, member: Member, message: str):
        # stub: send email message
        pass


class BorrowingService:
    def __init__(self, notifier: NotificationService):
        self.notifier = notifier

    def process_borrow(self, member: Member, book: Book):
        # stub: update book status and notify
        pass

    def process_return(self, member: Member, book: Book):
        # stub: update book status and notify
        pass


# 2. Parking Lot System
class Vehicle(ABC):
    def __init__(self, vehicle_type: str):
        self.vehicle_type = vehicle_type


class ParkingSlot:
    def __init__(self, slot_id: str, accepted_type: str):
        self.slot_id = slot_id
        self.accepted_type = accepted_type
        self.is_occupied = False


class Level:
    def __init__(self, level_id: str):
        self.level_id = level_id
        self.slots: List[ParkingSlot] = []

    def find_and_occupy(self, vehicle: Vehicle) -> Optional[str]:
        # stub: find available slot and occupy
        pass

    def free_slot(self, slot_id: str):
        # stub: free the given slot
        pass


class ParkingLot:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, pricing_strategy: Any):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, pricing_strategy: Any):
        self.levels: List[Level] = []
        self.pricing_strategy = pricing_strategy

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        # stub: delegate to Level
        pass

    def leave_vehicle(self, slot_id: str):
        # stub: compute fee and free slot
        pass

    def get_available_spots(self) -> Dict[str, int]:
        # stub: tally available per level
        pass


# 3. Online Shopping (Amazon)
class Product:
    def __init__(self, product_id: str, name: str, price: float, stock: int):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock


class Cart:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.items: Dict[str, int] = {}

    def add_item(self, product: Product, qty: int):
        # stub: add/update self.items
        pass

    def checkout(self):
        # stub: create Order
        pass


class Order:
    def __init__(self, order_id: str, user_id: str, items: Dict[str, int]):
        self.order_id = order_id
        self.user_id = user_id
        self.items = items
        self.status = "pending"


class InventoryManager:
    def __init__(self):
        self.stock: Dict[str, int] = {}

    def update_stock(self, product_id: str, delta: int):
        # stub: adjust stock quantity
        pass


class PaymentService:
    def process_payment(self, user_id: str, amount: float) -> bool:
        # stub: handle payment
        pass


class Catalog:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.products: Dict[str, Product] = {}

    def add_product(self, product: Product):
        # stub: add to catalog
        pass

    def search(self, query: str) -> List[Product]:
        # stub: filter products
        return []


# 4. Q&A Platform (StackOverflow)
class QAUser:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.reputation = 0


class Post(ABC):
    def __init__(self, post_id: str, author_id: str, content: str):
        self.post_id = post_id
        self.author_id = author_id
        self.content = content
        self.votes = 0


class Question(Post):
    def __init__(self, post_id: str, author_id: str, content: str, tags: List[str]):
        super().__init__(post_id, author_id, content)
        self.tags = tags
        self.answers: List[Answer] = []


class Answer(Post):
    def __init__(self, post_id: str, author_id: str, content: str, question_id: str):
        super().__init__(post_id, author_id, content)
        self.question_id = question_id


class Comment:
    def __init__(self, comment_id: str, author_id: str, content: str):
        self.comment_id = comment_id
        self.author_id = author_id
        self.content = content


class VoteService:
    def upvote(self, user_id: str, post_id: str):
        # stub
        pass

    def downvote(self, user_id: str, post_id: str):
        # stub
        pass


class ReputationService:
    def adjust(self, user_id: str, delta: int):
        # stub
        pass


class SearchService:
    def search_questions(self, keyword: str) -> List[Question]:
        # stub
        return []


class StackOverflowSystem:
    def __init__(self):
        self.users: Dict[str, QAUser] = {}
        self.questions: Dict[str, Question] = {}
        self.answers: Dict[str, Answer] = {}

    def post_question(self, user_id: str, content: str, tags: List[str]) -> str:
        # stub
        pass

    def post_answer(self, user_id: str, question_id: str, content: str) -> str:
        # stub
        pass

    def comment(self, user_id: str, post_id: str, content: str) -> str:
        # stub
        pass

    def search(self, keyword: str) -> List[Question]:
        # stub
        return []


# 5. Movie Ticket Booking (BookMyShow)
class Movie:
    def __init__(self, movie_id: str, title: str):
        self.movie_id = movie_id
        self.title = title

    def get_showtimes(self) -> List[str]:
        # stub
        pass


class Theater:
    def __init__(self, theater_id: str, name: str):
        self.theater_id = theater_id
        self.name = name

    def add_screen(self, screen_id: str):
        # stub
        pass


class Screen:
    def __init__(self, screen_id: str, seats: int):
        self.screen_id = screen_id
        self.total_seats = seats

    def book_seat(self, seat_no: int) -> bool:
        # stub
        pass


class Showtime:
    def __init__(self, show_id: str, movie: Movie, screen: Screen, time: str):
        self.show_id = show_id
        self.movie = movie
        self.screen = screen
        self.time = time

    def get_available_seats(self) -> List[int]:
        # stub
        pass


class Seat:
    def __init__(self, seat_no: int):
        self.seat_no = seat_no
        self.is_booked = False


class Booking:
    def __init__(self, booking_id: str, user_id: str, show_id: str, seats: List[int]):
        self.booking_id = booking_id
        self.user_id = user_id
        self.show_id = show_id
        self.seats = seats
        self.status = "confirmed"


class PaymentService:
    def process_payment(self, user_id: str, amount: float) -> bool:
        # stub
        pass


# 6. ATM System
class Account:
    def __init__(self, account_id: str, pin: str, balance: float):
        self.account_id = account_id
        self.pin = pin
        self.balance = balance
        self._lock = threading.Lock()

    def verify_pin(self, pin: str) -> bool:
        # stub
        pass


class CashDispenser:
    def __init__(self, bills: Dict[int, int]):
        self.bills = bills
        self._lock = threading.Lock()

    def dispense(self, amount: int) -> Dict[int, int]:
        # stub
        pass


class BankService:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.accounts: Dict[str, Account] = {}

    def authenticate(self, account_id: str, pin: str) -> bool:
        # stub
        pass

    def get_balance(self, account_id: str) -> float:
        # stub
        pass

    def withdraw(self, account_id: str, amount: float) -> bool:
        # stub
        pass

    def deposit(self, account_id: str, amount: float) -> bool:
        # stub
        pass


class TransactionLogger:
    @staticmethod
    def log(tx_type: str, account_id: str, amount: float, success: bool):
        # stub
        pass


class ATM:
    def __init__(self, dispenser: CashDispenser, bank: BankService):
        self.dispenser = dispenser
        self.bank = bank
        self.current_account: Optional[str] = None
        self.authenticated = False

    def insert_card(self, account_id: str):
        # stub
        pass

    def enter_pin(self, pin: str) -> bool:
        # stub
        pass

    def check_balance(self) -> Optional[float]:
        # stub
        pass

    def withdraw(self, amount: float) -> bool:
        # stub
        pass

    def deposit(self, amount: float) -> bool:
        # stub
        pass

    def eject_card(self):
        # stub
        pass


# ... Continue similarly for systems 7 through 33 ...

# End of file
