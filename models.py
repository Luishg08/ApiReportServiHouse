from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint, DECIMAL
)
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Order(Base):
    __tablename__ = "Order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_number = Column(String, nullable=False)
    delivery_id = Column(Integer, ForeignKey("Delivery.id"))
    final_address_id = Column(Integer, ForeignKey("Location.id"))
    state = Column(String, default="PENDING")
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    stockTransactions = relationship("StockTransaction", back_populates="order")
    delivery = relationship("Delivery", back_populates="orders")
    final_address = relationship("Location", foreign_keys=[final_address_id], back_populates="orders")

class Stock(Base):
    __tablename__ = "Stock"
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer)
    product_id = Column(String, ForeignKey("Product.id"))
    storage_id = Column(String, ForeignKey("Storage.id"))
    dispatcher_id = Column(Integer, ForeignKey("Dispatcher.id"), nullable=True)
    min_amount = Column(Integer, nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    stockTransactions = relationship("StockTransaction", back_populates="stock")
    product = relationship("Product", back_populates="stock")
    storage = relationship("Storage", back_populates="stock")
    dispatcher = relationship("Dispatcher", back_populates="stock")
    __table_args__ = (UniqueConstraint('product_id', 'storage_id', name='_product_storage_uc'),)

class StockTransaction(Base):
    __tablename__ = "StockTransaction"
    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer)
    stock_id = Column(Integer, ForeignKey("Stock.id"))
    order_id = Column(Integer, ForeignKey("Order.id"))
    restock = Column(Boolean, default=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    order = relationship("Order", back_populates="stockTransactions")
    stock = relationship("Stock", back_populates="stockTransactions")

class Delivery(Base):
    __tablename__ = "Delivery"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=True)
    full_name = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey("Location.id"))
    orders = relationship("Order", back_populates="delivery")
    location = relationship("Location", back_populates="deliveries")

class Location(Base):
    __tablename__ = "Location"
    id = Column(Integer, primary_key=True, autoincrement=True)
    altitude = Column(String)
    latitude = Column(String)
    static = Column(Boolean)
    address = Column(String)
    city = Column(String)
    department = Column(String)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    orders = relationship("Order", back_populates="final_address", foreign_keys='Order.final_address_id')
    deliveries = relationship("Delivery", back_populates="location")
    storages = relationship("Storage", back_populates="location")
    __table_args__ = (UniqueConstraint('latitude', 'altitude', name='_lat_alt_uc'),)

class Product(Base):
    __tablename__ = "Product"
    id = Column(String, primary_key=True)
    name = Column(String)
    category = Column(String)
    description = Column(String)
    price = Column(DECIMAL(10, 2))
    picture = Column(String)
    fragile = Column(Boolean)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    stock = relationship("Stock", back_populates="product")
    providerProducts = relationship("ProviderProduct", back_populates="product")

class Storage(Base):
    __tablename__ = "Storage"
    id = Column(String, primary_key=True)
    name = Column(String)
    manager_id = Column(Integer, ForeignKey("Manager.id"))
    location_id = Column(Integer, ForeignKey("Location.id"))
    capacity = Column(Integer)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    stock = relationship("Stock", back_populates="storage")
    location = relationship("Location", back_populates="storages")
    manager = relationship("Manager", back_populates="storages")

class Manager(Base):
    __tablename__ = "Manager"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=True)
    full_name = Column(String)
    state = Column(String, default="ACTIVE")
    email = Column(String, unique=True)
    phone = Column(String)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    storages = relationship("Storage", back_populates="manager")

class MailTemplates(Base):
    __tablename__ = "MailTemplates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    event = Column(String)
    subject = Column(String)
    body = Column(String)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    isActive = Column(Boolean, default=True)

class MessageTemplates(Base):
    __tablename__ = "MessageTemplate"
    id = Column(Integer, primary_key=True, autoincrement=True)
    event = Column(String)
    text = Column(String)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    isActive = Column(Boolean, default=True)

class Provider(Base):
    __tablename__ = "Provider"
    id = Column(String, primary_key=True)
    name = Column(String, unique=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    providerProducts = relationship("ProviderProduct", back_populates="provider")

class ProviderProduct(Base):
    __tablename__ = "ProviderProduct"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String, ForeignKey("Product.id"))
    provider_id = Column(String, ForeignKey("Provider.id"))
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    product = relationship("Product", back_populates="providerProducts")
    provider = relationship("Provider", back_populates="providerProducts")
    __table_args__ = (UniqueConstraint('product_id', 'provider_id', name='_product_provider_uc'),)

class Dispatcher(Base):
    __tablename__ = "Dispatcher"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    stock = relationship("Stock", back_populates="dispatcher")