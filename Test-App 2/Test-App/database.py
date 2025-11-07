import importlib
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def _ensure_package(package_name: str, import_name: str | None = None):
    module_name = import_name or package_name
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:  # pragma: no cover - dependency bootstrap
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return importlib.import_module(module_name)


_ensure_package("SQLAlchemy", "sqlalchemy")

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

_DEFAULT_DB_PATH = (Path(__file__).resolve().parent / "app.db").resolve()

DATABASE_URL = os.getenv("DATABASE_URL") or f"sqlite:///{_DEFAULT_DB_PATH.as_posix()}"

if DATABASE_URL.startswith("sqlite"):
    _DEFAULT_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
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
