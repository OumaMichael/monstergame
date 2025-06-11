from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

class Player(Base):
    __tablename__ = 'players'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    money = Column(Integer, default=1000)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    monsters = relationship("PlayerMonster", back_populates="player")
    battles_as_player1 = relationship("Battle", foreign_keys="Battle.player1_id", back_populates="player1")
    battles_as_player2 = relationship("Battle", foreign_keys="Battle.player2_id", back_populates="player2")
    trades_sent = relationship("Trade", foreign_keys="Trade.from_player_id", back_populates="from_player")
    trades_received = relationship("Trade", foreign_keys="Trade.to_player_id", back_populates="to_player")

class MonsterSpecies(Base):
    __tablename__ = 'monster_species'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    type = Column(String(20), nullable=False)  # Fire, Water, Grass, Electric, Rock, etc.
    base_hp = Column(Integer, nullable=False)
    base_attack = Column(Integer, nullable=False)
    base_defense = Column(Integer, nullable=False)
    base_speed = Column(Integer, nullable=False)
    rarity = Column(String(20), nullable=False)  # Common, Uncommon, Rare, Epic, Legendary
    description = Column(Text)
    
    # Relationships
    player_monsters = relationship("PlayerMonster", back_populates="species")

class PlayerMonster(Base):
    __tablename__ = 'player_monsters'
    
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    species_id = Column(Integer, ForeignKey('monster_species.id'), nullable=False)
    nickname = Column(String(50))
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    hp = Column(Integer, nullable=False)
    max_hp = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    caught_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    player = relationship("Player", back_populates="monsters")
    species = relationship("MonsterSpecies", back_populates="player_monsters")

class Battle(Base):
    __tablename__ = 'battles'
    
    id = Column(Integer, primary_key=True)
    player1_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    player2_id = Column(Integer, ForeignKey('players.id'))  # Null for wild battles
    winner_id = Column(Integer, ForeignKey('players.id'))
    battle_type = Column(String(20), nullable=False)  # wild, player, gym
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime)
    
    # Relationships
    player1 = relationship("Player", foreign_keys=[player1_id], back_populates="battles_as_player1")
    player2 = relationship("Player", foreign_keys=[player2_id], back_populates="battles_as_player2")

class Trade(Base):
    __tablename__ = 'trades'
    
    id = Column(Integer, primary_key=True)
    from_player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    to_player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    offered_monster_id = Column(Integer, ForeignKey('player_monsters.id'), nullable=False)
    requested_monster_id = Column(Integer, ForeignKey('player_monsters.id'), nullable=False)
    status = Column(String(20), default='pending')  # pending, accepted, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # Relationships
    from_player = relationship("Player", foreign_keys=[from_player_id], back_populates="trades_sent")
    to_player = relationship("Player", foreign_keys=[to_player_id], back_populates="trades_received")

class Achievement(Base):
    __tablename__ = 'achievements'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    requirement_type = Column(String(50), nullable=False)  # catch_count, battle_wins, etc.
    requirement_value = Column(Integer, nullable=False)

class PlayerAchievement(Base):
    __tablename__ = 'player_achievements'
    
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    achievement_id = Column(Integer, ForeignKey('achievements.id'), nullable=False)
    unlocked_at = Column(DateTime, default=datetime.utcnow)

class Item(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    item_type = Column(String(20), nullable=False)  # potion, pokeball, battle, misc
    effect_type = Column(String(30))  # heal, catch_boost, stat_boost, etc.
    effect_value = Column(Integer, default=0)
    price = Column(Integer, nullable=False)
    rarity = Column(String(20), default='Common')
    
    # Relationships
    inventory_items = relationship("PlayerInventory", back_populates="item")

class PlayerInventory(Base):
    __tablename__ = 'player_inventory'
    
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, default=1)
    acquired_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    player = relationship("Player")
    item = relationship("Item", back_populates="inventory_items")

class ItemUsage(Base):
    __tablename__ = 'item_usage'
    
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    monster_id = Column(Integer, ForeignKey('player_monsters.id'))  # Null for non-monster items
    used_at = Column(DateTime, default=datetime.utcnow)
    success = Column(Boolean, default=True)
    
    # Relationships
    player = relationship("Player")
    item = relationship("Item")
    monster = relationship("PlayerMonster")

# Database setup
def create_database():
    engine = create_engine('sqlite:///monster_game.db', echo=False)
    Base.metadata.create_all(engine)
    return engine

def get_session():
    engine = create_database()
    Session = sessionmaker(bind=engine)
    return Session()
