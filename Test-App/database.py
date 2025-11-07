import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    buying_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    current_stock = Column(Integer, nullable=False, default=0)
    reorder_level = Column(Integer, default=10)
    image_url = Column(String, nullable=True)
    
    sales = relationship("Sale", back_populates="product")
    purchase_orders = relationship("PurchaseOrder", back_populates="product")

class Sale(Base):
    __tablename__ = "sales"
    
    sale_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    sale_date = Column(DateTime, default=datetime.utcnow)
    sale_price = Column(Float, nullable=False)
    cost_price = Column(Float, nullable=False)
    
    product = relationship("Product", back_populates="sales")

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    
    order_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    expected_delivery = Column(DateTime, nullable=True)
    status = Column(String, default="Pending")
    cost_per_unit = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    
    product = relationship("Product", back_populates="purchase_orders")

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise
