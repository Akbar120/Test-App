import base64
import importlib
import mimetypes
import os
from pathlib import Path
import subprocess
import sys
from html import escape


THEMES = {
    "Light": {
        "page_background": "#f3f4f6",
        "sidebar_background": "#1f2937",
        "sidebar_text": "#f9fafb",
        "primary_text": "#0f172a",
        "secondary_text": "#1f2937",
        "muted_text": "#64748b",
        "card_background": "#ffffff",
        "card_border": "#e2e8f0",
        "card_shadow": "rgba(15, 23, 42, 0.08)",
        "accent_color": "#2563eb",
        "accent_text": "#ffffff",
        "accent_gradient_start": "#2563eb",
        "accent_gradient_end": "#60a5fa",
        "text_shadow": "rgba(17, 24, 39, 0.18)"
        ,
        "stock_critical_bg": "rgba(248, 113, 113, 0.18)",
        "stock_critical_text": "#b91c1c",
        "stock_low_bg": "rgba(251, 191, 36, 0.2)",
        "stock_low_text": "#b45309",
        "stock_normal_bg": "rgba(134, 239, 172, 0.22)",
        "stock_normal_text": "#065f46"
    },
    "Dark": {
        "page_background": "#111827",
        "sidebar_background": "#0b1120",
        "sidebar_text": "#e5e7eb",
        "primary_text": "#f9fafb",
        "secondary_text": "#e5e7eb",
        "muted_text": "#9ca3af",
        "card_background": "#1f2937",
        "card_border": "#374151",
        "card_shadow": "rgba(0, 0, 0, 0.4)",
        "accent_color": "#22d3ee",
        "accent_text": "#0b1120",
        "accent_gradient_start": "#22d3ee",
        "accent_gradient_end": "#3b82f6",
        "text_shadow": "rgba(0, 0, 0, 0.5)"
        ,
        "stock_critical_bg": "rgba(239, 68, 68, 0.35)",
        "stock_critical_text": "#fecaca",
        "stock_low_bg": "rgba(245, 158, 11, 0.35)",
        "stock_low_text": "#fffbeb",
        "stock_normal_bg": "rgba(16, 185, 129, 0.35)",
        "stock_normal_text": "#ecfdf5"
    },
    "Grey": {
        "page_background": "#f0f1f3",
        "sidebar_background": "#2f3136",
        "sidebar_text": "#e6e7eb",
        "primary_text": "#1f2937",
        "secondary_text": "#374151",
        "muted_text": "#6b7280",
        "card_background": "#ffffff",
        "card_border": "#d1d5db",
        "card_shadow": "rgba(31, 41, 55, 0.10)",
        "accent_color": "#6b7280",
        "accent_text": "#ffffff",
        "accent_gradient_start": "#9ca3af",
        "accent_gradient_end": "#6b7280",
        "text_shadow": "rgba(17, 24, 39, 0.15)"
        ,
        "stock_critical_bg": "rgba(239, 68, 68, 0.20)",
        "stock_critical_text": "#7f1d1d",
        "stock_low_bg": "rgba(245, 158, 11, 0.20)",
        "stock_low_text": "#7c2d12",
        "stock_normal_bg": "rgba(16, 185, 129, 0.22)",
        "stock_normal_text": "#065f46"
    }
}

DEFAULT_THEME = "Light"


def build_theme_css(theme: dict) -> str:
    return f"""
    <style>
        :root {{
            --page-background: {theme['page_background']};
            --sidebar-background: {theme['sidebar_background']};
            --sidebar-text: {theme['sidebar_text']};
            --primary-text: {theme['primary_text']};
            --secondary-text: {theme['secondary_text']};
            --muted-text: {theme['muted_text']};
            --card-background: {theme['card_background']};
            --card-border: {theme['card_border']};
            --card-shadow: {theme['card_shadow']};
            --accent-color: {theme['accent_color']};
            --accent-text: {theme['accent_text']};
            --accent-gradient-start: {theme['accent_gradient_start']};
            --accent-gradient-end: {theme['accent_gradient_end']};
            --text-shadow-color: {theme['text_shadow']};
            --stock-critical-bg: {theme['stock_critical_bg']};
            --stock-critical-text: {theme['stock_critical_text']};
            --stock-low-bg: {theme['stock_low_bg']};
            --stock-low-text: {theme['stock_low_text']};
            --stock-normal-bg: {theme['stock_normal_bg']};
            --stock-normal-text: {theme['stock_normal_text']};
        }}

        div[data-testid="stAppViewContainer"] {{
            background: var(--page-background);
            color: var(--primary-text);
        }}

        section[data-testid="stSidebar"] > div {{
            background: var(--sidebar-background);
        }}

        section[data-testid="stSidebar"] * {{
            color: var(--sidebar-text) !important;
        }}

        /* Highlight the Navigation section in the sidebar */
        section[data-testid="stSidebar"] .stSelectbox > label {{
            font-weight: 700;
            letter-spacing: 0.02em;
            text-shadow: 0 1px 2px var(--text-shadow-color);
        }}

        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[role="combobox"] {{
            background: linear-gradient(135deg, var(--accent-gradient-start), var(--accent-gradient-end));
            color: var(--accent-text) !important;
            border: 1px solid var(--accent-color);
            border-radius: 10px;
            box-shadow: 0 4px 14px var(--card-shadow);
        }}

        section[data-testid="stSidebar"] .stSelectbox div[role="combobox"] * {{
            color: var(--accent-text) !important;
            font-weight: 700;
            text-shadow: 0 1px 1px var(--text-shadow-color);
        }}

        /* Dropdown options readability */
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[role="listbox"] > div {{
            color: var(--primary-text) !important;
        }}
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] div[role="listbox"] > div[aria-selected="true"] {{
            background: rgba(0,0,0,0.06);
            color: var(--accent-color) !important;
            font-weight: 700;
        }}

        .stTabs [data-baseweb="tab-list"] button div p {{
            color: var(--muted-text) !important;
            text-shadow: 0 1px 1px var(--text-shadow-color);
        }}

        .stTabs [aria-selected="true"] div p {{
            color: var(--accent-color) !important;
            text-shadow: 0 1px 1px var(--text-shadow-color);
        }}

        .stButton > button, .stDownloadButton > button {{
            background: linear-gradient(135deg, var(--accent-gradient-start), var(--accent-gradient-end));
            color: var(--accent-text);
            border: none;
            border-radius: 999px;
            padding: 0.6rem 1.4rem;
            font-weight: 600;
            text-shadow: 0 1px 1px var(--text-shadow-color);
        }}

        .stButton > button:hover, .stDownloadButton > button:hover {{
            filter: brightness(0.95);
        }}

        .stMetric label {{
            color: var(--muted-text) !important;
            text-shadow: 0 1px 1px var(--text-shadow-color);
        }}

        .stMetric div[data-testid="stMetricValue"] {{
            color: var(--accent-color) !important;
            text-shadow: 0 1px 1px var(--text-shadow-color);
        }}

        /* Improve visibility for headings and important text */
        h1, h2, h3, h4, h5, h6 {{
            text-shadow: 0 1px 2px var(--text-shadow-color);
        }}

        .product-card .product-name,
        .product-card .product-price,
        .product-card .stock-pill {{
            text-shadow: 0 1px 1px var(--text-shadow-color);
        }}

        /* Sidebar readability */
        section[data-testid="stSidebar"] *:not(input):not(textarea) {{
            text-shadow: 0 1px 1px var(--text-shadow-color);
        }}
    </style>
    """


def _ensure_package(package_name: str, import_name: str | None = None):
    module_name = import_name or package_name
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:  # pragma: no cover - dependency bootstrap
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return importlib.import_module(module_name)


st = _ensure_package("streamlit")  # pyright: ignore[reportMissingImports]
pd = _ensure_package("pandas")  # pyright: ignore[reportMissingImports]
px = _ensure_package("plotly", "plotly.express")
go = _ensure_package("plotly", "plotly.graph_objects")
relativedelta_module = _ensure_package("python-dateutil", "dateutil.relativedelta")
relativedelta = relativedelta_module.relativedelta  # pyright: ignore[attr-defined]


if __name__ == "__main__":
    script_arg = sys.argv[0] if sys.argv else ""
    is_direct_invocation = bool(script_arg) and Path(script_arg).resolve() == Path(__file__).resolve()
    if os.getenv("STREAMLIT_AUTORUN") != "1" and is_direct_invocation:
        os.environ["STREAMLIT_AUTORUN"] = "1"
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(Path(__file__).resolve()),
                *sys.argv[1:],
            ],
            check=False,
        )
        sys.exit(result.returncode)
from datetime import datetime, timedelta
from database import init_db, get_db, Product, Sale, PurchaseOrder
from sqlalchemy import func  # pyright: ignore[reportMissingImports]
import io
import os

init_db()

st.set_page_config(page_title="Business Inventory Manager", layout="wide")

if "selected_theme" not in st.session_state:
    st.session_state.selected_theme = DEFAULT_THEME

theme_names = list(THEMES.keys())
if st.session_state.selected_theme not in THEMES:
    st.session_state.selected_theme = DEFAULT_THEME
selected_theme_index = theme_names.index(st.session_state.selected_theme)

header_col1, header_col_search, header_col2 = st.columns([2, 5, 1])

with header_col1:
    st.markdown(
        """
        <div id="topbar-brand" style="display:flex;align-items:center;gap:8px;">
            <span style="font-size:1.35rem;font-weight:800;letter-spacing:.02em;">Store Manager</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_col_search:
    if "product_search" not in st.session_state:
        st.session_state.product_search = ""
    st.text_input(
        "Search products",
        placeholder="Search by name...",
        key="product_search",
        label_visibility="collapsed",
    )

with header_col2:
    st.markdown(
        """
        <style>
            #theme-toggle button {
                padding: 0.25rem 0.4rem;
                border-radius: 10px;
                min-height: 0;
                line-height: 1;
                font-size: 0.9rem;
            }
            .theme-select [data-baseweb="select"] {
                min-height: 30px;
            }
            .theme-select div[role="combobox"] {
                min-height: 30px;
                padding-top: 2px;
                padding-bottom: 2px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    with st.container():
        st.markdown("<div id='theme-toggle' style='text-align: right;'>", unsafe_allow_html=True)
        if st.button("🎨", key="toggle_theme", help="Cycle theme"):
            current_idx = theme_names.index(st.session_state.selected_theme)
            next_idx = (current_idx + 1) % len(theme_names)
            st.session_state.selected_theme = theme_names[next_idx]
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown(build_theme_css(THEMES[st.session_state.selected_theme]), unsafe_allow_html=True)

st.markdown(
    """
    <style>
        /* Top bar styling */
        div[data-testid="stHorizontalBlock"]:has(#topbar-brand) {
            position: sticky;
            top: 0;
            z-index: 50;
            padding: 8px 0 4px 0;
            background: var(--sidebar-background);
            border-bottom: 1px solid rgba(255,255,255,0.06);
            box-shadow: 0 6px 16px var(--card-shadow);
        }

        /* Search input look */
        div[data-testid="stTextInput"] input {
            border-radius: 999px;
            border: 1px solid var(--card-border);
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);
            padding-left: 14px;
        }

        .product-grid div[data-testid="column"] {
            display: flex;
            flex-direction: column;
        }

        .product-grid div[data-testid="column"] > div {
            flex: 1;
        }

        .product-card {
            display: flex;
            flex-direction: column;
            gap: 10px;
            background: var(--card-background);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 14px;
            box-shadow: 0 6px 20px var(--card-shadow);
            height: 100%;
        }

        .product-card img.product-image {
            width: 100%;
            border-radius: 12px;
            object-fit: cover;
            aspect-ratio: 1 / 1;
        }

        .product-card .image-placeholder {
            position: relative;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--accent-gradient-start), var(--accent-gradient-end));
            width: 100%;
            padding-top: 75%;
            overflow: hidden;
            color: var(--accent-text);
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .product-card .image-placeholder span {
            position: absolute;
        }

        .product-card .product-meta {
            display: flex;
            flex-direction: column;
            gap: 8px;
            flex: 1;
        }

        .product-card .product-name {
            margin: 0;
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--primary-text);
        }

        .product-card .product-price {
            margin: 0;
            font-size: 0.9rem;
            color: var(--secondary-text);
        }

        .product-card .stock-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            border-radius: 999px;
            font-size: 0.85rem;
            font-weight: 500;
        }

        .product-card .stock-pill.critical {
            background: var(--stock-critical-bg);
            color: var(--stock-critical-text);
        }

        .product-card .stock-pill.low {
            background: var(--stock-low-bg);
            color: var(--stock-low-text);
        }

        .product-card .stock-pill.normal {
            background: var(--stock-normal-bg);
            color: var(--stock-normal-text);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

menu = st.sidebar.selectbox(
    "Navigation",
    ["Products", "Add Product", "Manage Products", "Record Sale", "Price Comparison", "Monthly Sales Report", "Sales History", "Purchase Orders", "Financial Dashboard", "Trends & Analytics"]
)

def save_uploaded_image(uploaded_file):
    if uploaded_file is not None:
        upload_dir = Path("uploaded_images")
        upload_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = Path(uploaded_file.name).suffix
        filename = f"{timestamp}_{uploaded_file.name}"
        filepath = upload_dir / filename
        
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return str(filepath)
    return None


def render_product_card(product):
    name = escape(product.name)
    price = f"₹{product.selling_price:.2f}"
    stock_text = f"📦 Stock: {product.current_stock} units"

    if product.current_stock < 10:
        stock_class = "critical"
    elif product.current_stock < 25:
        stock_class = "low"
    else:
        stock_class = "normal"

    image_html = "<div class='image-placeholder'><span>🖼️ No image</span></div>"

    if product.image_url and os.path.exists(product.image_url):
        mime_type, _ = mimetypes.guess_type(product.image_url)
        mime_type = mime_type or "image/jpeg"
        try:
            with open(product.image_url, "rb") as img_file:
                encoded_image = base64.b64encode(img_file.read()).decode()
            image_html = (
                f"<img src='data:{mime_type};base64,{encoded_image}' "
                f"class='product-image' alt='{name}'/>"
            )
        except Exception:
            image_html = "<div class='image-placeholder'><span>🖼️ Image unavailable</span></div>"

    return f"""
        <div class="product-card">
            {image_html}
            <div class="product-meta">
                <p class="product-name">{name}</p>
                <p class="product-price">💰 Price: {price}</p>
                <div class="stock-pill {stock_class}">{stock_text}</div>
            </div>
        </div>
    """


def _month_bounds(year: int, month: int):
    """Return the inclusive start and exclusive end datetime for a calendar month."""
    start = datetime(year, month, 1)
    end = start + relativedelta(months=1)
    return start, end

def add_product(name, buying_price, selling_price, stock, reorder_level=10, image_url=None):
    db = get_db()
    try:
        product = Product(
            name=name,
            buying_price=buying_price,
            selling_price=selling_price,
            current_stock=stock,
            reorder_level=reorder_level,
            image_url=image_url
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        return True
    except Exception as e:
        db.rollback()
        st.error(f"Error adding product: {e}")
        return False
    finally:
        db.close()

def get_all_products():
    db = get_db()
    try:
        products = db.query(Product).all()
        return products
    finally:
        db.close()

def update_product(product_id, name, buying_price, selling_price, stock, reorder_level=10, image_url=None):
    db = get_db()
    try:
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if product:
            product.name = name
            product.buying_price = buying_price
            product.selling_price = selling_price
            product.current_stock = stock
            product.reorder_level = reorder_level
            product.image_url = image_url
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        st.error(f"Error updating product: {e}")
        return False
    finally:
        db.close()

def delete_product(product_id):
    db = get_db()
    try:
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if product:
            db.delete(product)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        st.error(f"Error deleting product: {e}")
        return False
    finally:
        db.close()

def record_sale(product_id, quantity):
    db = get_db()
    try:
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            st.error("Product not found")
            return False
        
        if product.current_stock < quantity:
            st.error(f"Insufficient stock. Available: {product.current_stock}")
            return False
        
        sale = Sale(
            product_id=product_id,
            quantity=quantity,
            sale_price=product.selling_price,
            cost_price=product.buying_price
        )
        
        product.current_stock -= quantity
        
        db.add(sale)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        st.error(f"Error recording sale: {e}")
        return False
    finally:
        db.close()

def get_monthly_sales(year, month):
    db = get_db()
    try:
        start, end = _month_bounds(year, month)
        sales = db.query(Sale).filter(
            Sale.sale_date >= start,
            Sale.sale_date < end
        ).all()
        return sales
    finally:
        db.close()


def get_monthly_stats(year, month):
    db = get_db()
    try:
        start, end = _month_bounds(year, month)
        stats = db.query(
            func.sum(Sale.quantity * Sale.sale_price).label('total_revenue'),
            func.sum(Sale.quantity * (Sale.sale_price - Sale.cost_price)).label('total_profit'),
            func.count(Sale.sale_id).label('total_transactions')
        ).filter(
            Sale.sale_date >= start,
            Sale.sale_date < end
        ).first()

        return {
            'total_revenue': stats.total_revenue or 0,
            'total_profit': stats.total_profit or 0,
            'total_transactions': stats.total_transactions or 0
        }
    finally:
        db.close()

def get_multi_month_stats(months_back=6):
    db = get_db()
    try:
        end_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start_date = end_date - relativedelta(months=months_back - 1)

        monthly_data = []
        current = start_date

        for _ in range(months_back):
            month_start = current
            month_end = month_start + relativedelta(months=1)
            stats = db.query(
                func.sum(Sale.quantity * Sale.sale_price).label('total_revenue'),
                func.sum(Sale.quantity * (Sale.sale_price - Sale.cost_price)).label('total_profit'),
                func.count(Sale.sale_id).label('total_transactions')
            ).filter(
                Sale.sale_date >= month_start,
                Sale.sale_date < month_end
            ).first()

            monthly_data.append({
                'year': month_start.year,
                'month': month_start.month,
                'month_name': month_start.strftime('%b %Y'),
                'revenue': float(stats.total_revenue or 0),
                'profit': float(stats.total_profit or 0),
                'transactions': int(stats.total_transactions or 0)
            })

            current = month_end

        return monthly_data
    finally:
        db.close()

def get_filtered_sales(start_date=None, end_date=None, product_id=None):
    db = get_db()
    try:
        query = db.query(Sale)
        
        if start_date:
            query = query.filter(Sale.sale_date >= start_date)
        if end_date:
            end_datetime = datetime.combine(end_date, datetime.max.time())
            query = query.filter(Sale.sale_date <= end_datetime)
        if product_id:
            query = query.filter(Sale.product_id == product_id)
        
        sales = query.order_by(Sale.sale_date.desc()).all()
        return sales
    finally:
        db.close()

def export_to_csv(dataframe, filename):
    csv = dataframe.to_csv(index=False)
    return csv

def create_purchase_order(product_id, quantity, expected_delivery, cost_per_unit):
    db = get_db()
    try:
        total_cost = quantity * cost_per_unit
        order = PurchaseOrder(
            product_id=product_id,
            quantity=quantity,
            expected_delivery=expected_delivery,
            cost_per_unit=cost_per_unit,
            total_cost=total_cost,
            status="Pending"
        )
        db.add(order)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        st.error(f"Error creating purchase order: {e}")
        return False
    finally:
        db.close()

def receive_purchase_order(order_id):
    db = get_db()
    try:
        order = db.query(PurchaseOrder).filter(PurchaseOrder.order_id == order_id).first()
        if order and order.status == "Pending":
            product = db.query(Product).filter(Product.product_id == order.product_id).first()
            if product:
                product.current_stock += order.quantity
                order.status = "Received"
                db.commit()
                return True
        return False
    except Exception as e:
        db.rollback()
        st.error(f"Error receiving purchase order: {e}")
        return False
    finally:
        db.close()

def get_all_purchase_orders():
    db = get_db()
    try:
        orders = db.query(PurchaseOrder).order_by(PurchaseOrder.order_date.desc()).all()
        return orders
    finally:
        db.close()

def cancel_purchase_order(order_id):
    db = get_db()
    try:
        order = db.query(PurchaseOrder).filter(PurchaseOrder.order_id == order_id).first()
        if order and order.status == "Pending":
            order.status = "Cancelled"
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        st.error(f"Error cancelling purchase order: {e}")
        return False
    finally:
        db.close()

if menu == "Products":
    st.header("📦 Products Overview")
    
    products = get_all_products()
    
    if products:
        tab1, tab2, tab3 = st.tabs(["🖼️ Product Catalog", "📊 Product List", "⚠️ Stock Alerts"])

        with tab1:
            st.subheader("Product Catalog")
            with st.container():
                st.markdown('<div class="product-grid">', unsafe_allow_html=True)
                cols = st.columns(8, gap="small")
                for idx, p in enumerate(products):
                    with cols[idx % len(cols)]:
                        st.markdown(render_product_card(p), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.subheader("Product List")
            product_data = []
            for p in products:
                stock_color = "🔴" if p.current_stock < 10 else "🟡" if p.current_stock < 25 else "🟢"
                product_data.append({
                    'ID': p.product_id,
                    'Product Name': p.name,
                    'Selling Price': f"₹{p.selling_price:.2f}",
                    'Current Stock': p.current_stock,
                    'Status': stock_color
                })

            df = pd.DataFrame(product_data)
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.markdown("""
            **Legend:** 🟢 Adequate (25+) | 🟡 Low (10-24) | 🔴 Critical (<10)
            """)

            export_df = pd.DataFrame([{
                'ID': p.product_id,
                'Product Name': p.name,
                'Selling Price': p.selling_price,
                'Current Stock': p.current_stock
            } for p in products])

            csv = export_to_csv(export_df, "products.csv")
            st.download_button(
                label="📥 Export Products to CSV",
                data=csv,
                file_name=f"products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

        with tab3:
            st.subheader("Stock Alerts")

            critical_stock = [p for p in products if p.current_stock < 10]
            low_stock = [p for p in products if 10 <= p.current_stock < 25]
            normal_stock = [p for p in products if p.current_stock >= 25]

            if critical_stock:
                st.markdown("### 🔴 Critical Stock (Below 10)")
                for p in critical_stock:
                    st.markdown(f"""
                    <div style=\"background-color: #ff4444; padding: 10px; border-radius: 5px; margin: 5px 0; color: white;\">
                        <strong>{p.name}</strong> - Only {p.current_stock} units remaining
                    </div>
                    """, unsafe_allow_html=True)

            if low_stock:
                st.markdown("### 🟡 Low Stock (Below 25)")
                for p in low_stock:
                    st.markdown(f"""
                    <div style=\"background-color: #ffaa00; padding: 10px; border-radius: 5px; margin: 5px 0; color: white;\">
                        <strong>{p.name}</strong> - {p.current_stock} units remaining
                    </div>
                    """, unsafe_allow_html=True)

            if normal_stock:
                st.markdown("### 🟢 Adequate Stock (25+)")
                for p in normal_stock:
                    st.success(f"**{p.name}** - {p.current_stock} units in stock")

            if not critical_stock and not low_stock:
                st.success("✅ All products have adequate stock levels!")
    else:
        st.info("No products available. Add your first product using the 'Add Product' menu.")

elif menu == "Manage Products":
    st.header("🔧 Manage Products")
    
    products = get_all_products()
    
    if products:
        if 'editing_product_id' not in st.session_state:
            st.session_state.editing_product_id = None
        
        st.subheader("📋 All Products - Click Edit to Modify")
        
        for p in products:
            stock_status = "🔴" if p.current_stock < 10 else "🟡" if p.current_stock < 25 else "🟢"
            
            with st.container():
                col1, col2, col3, col4, col5, col6, col7 = st.columns([0.5, 2.5, 1.5, 1.5, 1.2, 1.5, 1.3])
                
                with col1:
                    st.write(stock_status)
                with col2:
                    st.write(f"**{p.name}**")
                with col3:
                    st.write(f"₹{p.buying_price:.2f}")
                with col4:
                    st.write(f"₹{p.selling_price:.2f}")
                with col5:
                    st.write(f"{p.current_stock}")
                with col6:
                    st.write(f"₹{(p.selling_price - p.buying_price):.2f}")
                with col7:
                    if st.button("✏️ Edit", key=f"edit_{p.product_id}", type="primary", use_container_width=True):
                        st.session_state.editing_product_id = p.product_id
                        st.rerun()
                
                if st.session_state.editing_product_id == p.product_id:
                    st.markdown("---")
                    st.markdown(f"### ✏️ Editing: {p.name}")
                    
                    with st.form(f"edit_form_{p.product_id}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            edit_name = st.text_input("Product Name", value=p.name)
                            edit_buying = st.number_input("Buying Price (₹)", value=float(p.buying_price), min_value=0.01, step=0.01)
                            edit_selling = st.number_input("Selling Price (₹)", value=float(p.selling_price), min_value=0.01, step=0.01)
                            edit_stock = st.number_input("Current Stock", value=int(p.current_stock), min_value=0, step=1)
                        
                        with col2:
                            uploaded_image = st.file_uploader("Upload Product Image (optional)", type=['png', 'jpg', 'jpeg', 'gif', 'webp'], key=f"upload_{p.product_id}")
                            
                            if p.image_url and os.path.exists(p.image_url):
                                st.write("Current Image:")
                                st.image(p.image_url, width=200, caption="Current Image")
                            
                            if uploaded_image:
                                st.write("New Image Preview:")
                                st.image(uploaded_image, width=200, caption="New Image")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            submit_edit = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
                        with col2:
                            cancel_edit = st.form_submit_button("❌ Cancel", use_container_width=True)
                        with col3:
                            delete_product_btn = st.form_submit_button("🗑️ Delete", use_container_width=True)
                        
                        if submit_edit:
                            new_image_path = save_uploaded_image(uploaded_image) if uploaded_image else p.image_url
                            if update_product(p.product_id, edit_name, edit_buying, edit_selling, edit_stock, 10, new_image_path):
                                st.success("Product updated successfully!")
                                st.session_state.editing_product_id = None
                                st.rerun()
                        
                        if cancel_edit:
                            st.session_state.editing_product_id = None
                            st.rerun()
                        
                        if delete_product_btn:
                            if delete_product(p.product_id):
                                st.success("Product deleted successfully!")
                                st.session_state.editing_product_id = None
                                st.rerun()
                    
                    st.markdown("---")
                
                st.markdown("<div style='margin: 5px 0;'></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("**Column Headers:** 🔴🟡🟢 Status | Product Name | Buying Price | Selling Price | Stock | Profit/Unit | Actions")
    else:
        st.info("No products available. Add your first product using the 'Add Product' menu.")

elif menu == "Add Product":
    st.header("➕ Add New Product")
    
    with st.form("add_product_form"):
        name = st.text_input("Product Name")
        col1, col2 = st.columns(2)
        with col1:
            buying_price = st.number_input("Buying Price (₹)", min_value=0.01, step=0.01)
        with col2:
            selling_price = st.number_input("Selling Price (₹)", min_value=0.01, step=0.01)
        
        stock = st.number_input("Initial Stock Quantity", min_value=0, step=1)
        
        uploaded_image = st.file_uploader("Upload Product Image (optional)", type=['png', 'jpg', 'jpeg', 'gif', 'webp'])
        
        if uploaded_image:
            st.image(uploaded_image, width=200, caption="Preview")
        
        submit = st.form_submit_button("Add Product")
        
        if submit:
            if name and buying_price and selling_price:
                if selling_price >= buying_price:
                    image_path = save_uploaded_image(uploaded_image) if uploaded_image else None
                    if add_product(name, buying_price, selling_price, stock, 10, image_path):
                        st.success(f"Product '{name}' added successfully!")
                        st.balloons()
                else:
                    st.warning("Selling price should be greater than or equal to buying price for profit!")
            else:
                st.error("Please fill in all required fields")

elif menu == "Record Sale":
    st.header("💰 Record Sale")
    
    products = get_all_products()
    
    if products:
        available_products = [(p.product_id, f"{p.name} (Stock: {p.current_stock}, Price: ₹{p.selling_price:.2f})") for p in products if p.current_stock > 0]
        
        if available_products:
            with st.form("record_sale_form"):
                selected_product = st.selectbox(
                    "Select Product",
                    options=available_products,
                    format_func=lambda x: x[1]
                )
                
                product = next((p for p in products if p.product_id == selected_product[0]), None)
                
                if product:
                    quantity = st.number_input(
                        f"Quantity (Available: {product.current_stock})",
                        min_value=1,
                        max_value=product.current_stock,
                        step=1
                    )
                    
                    st.info(f"Total Sale Amount: ₹{product.selling_price * quantity:.2f}")
                    st.info(f"Profit from this sale: ₹{(product.selling_price - product.buying_price) * quantity:.2f}")
                
                submit = st.form_submit_button("Record Sale")
                
                if submit:
                    if record_sale(selected_product[0], quantity):
                        st.success(f"Sale recorded successfully! {quantity} unit(s) of {product.name} sold.")
                        st.rerun()
        else:
            st.warning("No products available in stock. Please add stock to existing products.")
    else:
        st.info("No products available. Please add products first.")

elif menu == "Price Comparison":
    st.header("💵 Price Comparison Analysis")
    
    products = get_all_products()
    
    if products:
        comparison_data = []
        for p in products:
            profit_per_unit = p.selling_price - p.buying_price
            profit_margin = (profit_per_unit / p.buying_price * 100) if p.buying_price > 0 else 0
            
            comparison_data.append({
                'Product Name': p.name,
                'Buying Price': p.buying_price,
                'Selling Price': p.selling_price,
                'Profit/Unit': profit_per_unit,
                'Profit Margin %': profit_margin,
                'Stock Value (Cost)': p.buying_price * p.current_stock,
                'Stock Value (Retail)': p.selling_price * p.current_stock,
                'Potential Profit': profit_per_unit * p.current_stock
            })
        
        df = pd.DataFrame(comparison_data)
        
        st.subheader("📊 Detailed Price Comparison")
        
        formatted_df = df.copy()
        formatted_df['Buying Price'] = formatted_df['Buying Price'].apply(lambda x: f"₹{x:.2f}")
        formatted_df['Selling Price'] = formatted_df['Selling Price'].apply(lambda x: f"₹{x:.2f}")
        formatted_df['Profit/Unit'] = formatted_df['Profit/Unit'].apply(lambda x: f"₹{x:.2f}")
        formatted_df['Profit Margin %'] = formatted_df['Profit Margin %'].apply(lambda x: f"{x:.2f}%")
        formatted_df['Stock Value (Cost)'] = formatted_df['Stock Value (Cost)'].apply(lambda x: f"₹{x:.2f}")
        formatted_df['Stock Value (Retail)'] = formatted_df['Stock Value (Retail)'].apply(lambda x: f"₹{x:.2f}")
        formatted_df['Potential Profit'] = formatted_df['Potential Profit'].apply(lambda x: f"₹{x:.2f}")
        
        st.dataframe(formatted_df, use_container_width=True, hide_index=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Stock Value (Cost)", f"₹{df['Stock Value (Cost)'].sum():.2f}")
        with col2:
            st.metric("Total Stock Value (Retail)", f"₹{df['Stock Value (Retail)'].sum():.2f}")
        with col3:
            st.metric("Total Potential Profit", f"₹{df['Potential Profit'].sum():.2f}")
        
        st.subheader("📈 Profit Margin Rankings")
        top_margin = df.nlargest(5, 'Profit Margin %')[['Product Name', 'Profit Margin %']]
        for idx, row in top_margin.iterrows():
            st.success(f"**{row['Product Name']}**: {row['Profit Margin %']:.2f}% margin")
    else:
        st.info("No products available for comparison.")

elif menu == "Monthly Sales Report":
    st.header("📅 Monthly Sales Report")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_month = st.selectbox("Select Month", range(1, 13), index=datetime.now().month - 1, format_func=lambda x: datetime(2000, x, 1).strftime('%B'))
    with col2:
        selected_year = st.number_input("Select Year", min_value=2020, max_value=2030, value=datetime.now().year)
    
    sales = get_monthly_sales(selected_year, selected_month)
    
    if sales:
        sales_data = []
        export_monthly_data = []
        db = get_db()
        try:
            for sale in sales:
                product = db.query(Product).filter(Product.product_id == sale.product_id).first()
                product_name = product.name if product else "Unknown"
                
                revenue = sale.quantity * sale.sale_price
                profit = sale.quantity * (sale.sale_price - sale.cost_price)
                
                sales_data.append({
                    'Date': sale.sale_date.strftime('%Y-%m-%d %H:%M'),
                    'Product': product_name,
                    'Quantity': sale.quantity,
                    'Unit Price': f"₹{sale.sale_price:.2f}",
                    'Revenue': f"₹{revenue:.2f}",
                    'Profit': f"₹{profit:.2f}"
                })
                
                export_monthly_data.append({
                    'Date': sale.sale_date.strftime('%Y-%m-%d %H:%M'),
                    'Product': product_name,
                    'Quantity': sale.quantity,
                    'Unit Price': sale.sale_price,
                    'Revenue': revenue,
                    'Profit': profit
                })
        finally:
            db.close()
        
        df = pd.DataFrame(sales_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        export_monthly_df = pd.DataFrame(export_monthly_data)
        
        csv_monthly = export_to_csv(export_monthly_df, "monthly_sales.csv")
        st.download_button(
            label="📥 Export Monthly Report to CSV",
            data=csv_monthly,
            file_name=f"monthly_sales_{datetime(2000, selected_month, 1).strftime('%B')}_{selected_year}.csv",
            mime="text/csv"
        )
        
        st.subheader("📊 Monthly Summary")
        stats = get_monthly_stats(selected_year, selected_month)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Revenue", f"₹{stats['total_revenue']:.2f}")
        with col2:
            st.metric("Total Profit", f"₹{stats['total_profit']:.2f}")
        with col3:
            st.metric("Total Transactions", stats['total_transactions'])
        
        if stats['total_revenue'] > 0:
            profit_percentage = (stats['total_profit'] / stats['total_revenue']) * 100
            st.info(f"Overall Profit Margin: {profit_percentage:.2f}%")
    else:
        st.info(f"No sales recorded for {datetime(2000, selected_month, 1).strftime('%B')} {selected_year}")

elif menu == "Sales History":
    st.header("📜 Detailed Sales History")
    
    st.subheader("🔍 Filter Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=30),
            max_value=datetime.now()
        )
    
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now(),
            max_value=datetime.now()
        )
    
    with col3:
        products = get_all_products()
        product_options = [("all", "All Products")] + [(p.product_id, p.name) for p in products]
        selected_product = st.selectbox(
            "Select Product",
            options=product_options,
            format_func=lambda x: x[1]
        )
    
    product_filter = None if selected_product[0] == "all" else selected_product[0]
    
    if st.button("Apply Filters", type="primary"):
        st.session_state.filter_applied = True
    
    if 'filter_applied' not in st.session_state:
        st.session_state.filter_applied = True
    
    if st.session_state.filter_applied:
        sales = get_filtered_sales(
            start_date=datetime.combine(start_date, datetime.min.time()),
            end_date=end_date,
            product_id=product_filter
        )
        
        if sales:
            sales_data = []
            total_revenue = 0
            total_profit = 0
            total_quantity = 0
            
            db = get_db()
            try:
                for sale in sales:
                    product = db.query(Product).filter(Product.product_id == sale.product_id).first()
                    product_name = product.name if product else "Unknown"
                    
                    revenue = sale.quantity * sale.sale_price
                    profit = sale.quantity * (sale.sale_price - sale.cost_price)
                    
                    total_revenue += revenue
                    total_profit += profit
                    total_quantity += sale.quantity
                    
                    sales_data.append({
                        'Sale ID': sale.sale_id,
                        'Date & Time': sale.sale_date.strftime('%Y-%m-%d %H:%M:%S'),
                        'Product': product_name,
                        'Quantity': sale.quantity,
                        'Unit Price': f"₹{sale.sale_price:.2f}",
                        'Cost Price': f"₹{sale.cost_price:.2f}",
                        'Revenue': f"₹{revenue:.2f}",
                        'Profit': f"₹{profit:.2f}"
                    })
            finally:
                db.close()
            
            st.subheader("📊 Sales Records")
            df = pd.DataFrame(sales_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            db_export = get_db()
            try:
                export_sales_data = []
                for sale in sales:
                    product = db_export.query(Product).filter(Product.product_id == sale.product_id).first()
                    product_name = product.name if product else "Unknown"
                    export_sales_data.append({
                        'Sale ID': sale.sale_id,
                        'Date & Time': sale.sale_date.strftime('%Y-%m-%d %H:%M:%S'),
                        'Product ID': sale.product_id,
                        'Product': product_name,
                        'Quantity': sale.quantity,
                        'Unit Price': sale.sale_price,
                        'Cost Price': sale.cost_price,
                        'Revenue': sale.quantity * sale.sale_price,
                        'Profit': sale.quantity * (sale.sale_price - sale.cost_price)
                    })
                export_sales_df = pd.DataFrame(export_sales_data)
            finally:
                db_export.close()
            
            csv_sales = export_to_csv(export_sales_df, "sales_history.csv")
            st.download_button(
                label="📥 Export Sales History to CSV",
                data=csv_sales,
                file_name=f"sales_history_{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            st.subheader("📈 Summary Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Sales", len(sales))
            with col2:
                st.metric("Total Items Sold", total_quantity)
            with col3:
                st.metric("Total Revenue", f"₹{total_revenue:.2f}")
            with col4:
                st.metric("Total Profit", f"₹{total_profit:.2f}")
            
            if total_revenue > 0:
                profit_margin = (total_profit / total_revenue) * 100
                st.info(f"📊 Average Profit Margin: {profit_margin:.2f}%")
            
            db = get_db()
            try:
                product_breakdown = db.query(
                    Product.name,
                    func.sum(Sale.quantity).label('total_quantity'),
                    func.sum(Sale.quantity * Sale.sale_price).label('total_revenue'),
                    func.sum(Sale.quantity * (Sale.sale_price - Sale.cost_price)).label('total_profit')
                ).join(Sale).filter(
                    Sale.sale_date >= datetime.combine(start_date, datetime.min.time()),
                    Sale.sale_date <= datetime.combine(end_date, datetime.max.time())
                )
                
                if product_filter:
                    product_breakdown = product_breakdown.filter(Sale.product_id == product_filter)
                
                product_breakdown = product_breakdown.group_by(Product.name).all()
                
                if product_breakdown and len(product_breakdown) > 1:
                    st.subheader("🏆 Product Performance Breakdown")
                    
                    breakdown_data = []
                    for name, qty, rev, prof in product_breakdown:
                        breakdown_data.append({
                            'Product': name,
                            'Units Sold': qty,
                            'Revenue': f"₹{rev:.2f}",
                            'Profit': f"₹{prof:.2f}"
                        })
                    
                    breakdown_df = pd.DataFrame(breakdown_data)
                    st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
            finally:
                db.close()
        else:
            st.info("No sales found for the selected filters.")

elif menu == "Purchase Orders":
    st.header("📦 Purchase Order Management")
    
    tab1, tab2 = st.tabs(["Create Purchase Order", "View Purchase Orders"])
    
    with tab1:
        st.subheader("➕ Create New Purchase Order")
        
        products = get_all_products()
        if products:
            with st.form("create_po_form"):
                product_options = [(p.product_id, f"{p.name} (Current Stock: {p.current_stock})") for p in products]
                selected_product = st.selectbox(
                    "Select Product",
                    options=product_options,
                    format_func=lambda x: x[1]
                )
                
                product = next((p for p in products if p.product_id == selected_product[0]), None)
                
                if product:
                    st.info(f"Current Stock: {product.current_stock} | Reorder Level: {product.reorder_level}")
                    if product.current_stock <= product.reorder_level:
                        st.warning(f"⚠️ This product needs restocking!")
                
                col1, col2 = st.columns(2)
                with col1:
                    quantity = st.number_input("Order Quantity", min_value=1, step=1, value=50)
                with col2:
                    cost_per_unit = st.number_input("Cost Per Unit ($)", min_value=0.01, step=0.01, value=float(product.buying_price) if product else 0.01)
                
                expected_delivery = st.date_input(
                    "Expected Delivery Date",
                    value=datetime.now() + timedelta(days=7),
                    min_value=datetime.now()
                )
                
                total_cost = quantity * cost_per_unit
                st.info(f"Total Order Cost: ₹{total_cost:.2f}")
                
                submit = st.form_submit_button("Create Purchase Order")
                
                if submit:
                    if create_purchase_order(selected_product[0], quantity, datetime.combine(expected_delivery, datetime.min.time()), cost_per_unit):
                        st.success(f"Purchase order created successfully!")
                        st.balloons()
                        st.rerun()
        else:
            st.info("No products available. Add products first before creating purchase orders.")
    
    with tab2:
        st.subheader("📋 All Purchase Orders")
        
        orders = get_all_purchase_orders()
        
        if orders:
            col1, col2, col3 = st.columns(3)
            with col1:
                pending_orders = [o for o in orders if o.status == "Pending"]
                st.metric("Pending Orders", len(pending_orders))
            with col2:
                received_orders = [o for o in orders if o.status == "Received"]
                st.metric("Received Orders", len(received_orders))
            with col3:
                cancelled_orders = [o for o in orders if o.status == "Cancelled"]
                st.metric("Cancelled Orders", len(cancelled_orders))
            
            status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Received", "Cancelled"])
            
            filtered_orders = orders if status_filter == "All" else [o for o in orders if o.status == status_filter]
            
            if filtered_orders:
                order_data = []
                db = get_db()
                try:
                    for order in filtered_orders:
                        product = db.query(Product).filter(Product.product_id == order.product_id).first()
                        product_name = product.name if product else "Unknown"
                        
                        order_data.append({
                            'Order ID': order.order_id,
                            'Product': product_name,
                            'Quantity': order.quantity,
                            'Cost/Unit': f"₹{order.cost_per_unit:.2f}",
                            'Total Cost': f"₹{order.total_cost:.2f}",
                            'Order Date': order.order_date.strftime('%Y-%m-%d'),
                            'Expected Delivery': order.expected_delivery.strftime('%Y-%m-%d') if order.expected_delivery else "N/A",
                            'Status': order.status
                        })
                finally:
                    db.close()
                
                df = pd.DataFrame(order_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                st.subheader("🔧 Manage Orders")
                
                pending_orders_list = [o for o in filtered_orders if o.status == "Pending"]
                if pending_orders_list:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Receive Order**")
                        order_to_receive = st.selectbox(
                            "Select Order to Receive",
                            options=[(o.order_id, f"Order #{o.order_id}") for o in pending_orders_list],
                            format_func=lambda x: x[1]
                        )
                        
                        if st.button("Mark as Received", type="primary"):
                            if receive_purchase_order(order_to_receive[0]):
                                st.success("Order received and stock updated!")
                                st.rerun()
                    
                    with col2:
                        st.write("**Cancel Order**")
                        order_to_cancel = st.selectbox(
                            "Select Order to Cancel",
                            options=[(o.order_id, f"Order #{o.order_id}") for o in pending_orders_list],
                            format_func=lambda x: x[1],
                            key="cancel_select"
                        )
                        
                        if st.button("Cancel Order", type="secondary"):
                            if cancel_purchase_order(order_to_cancel[0]):
                                st.success("Order cancelled successfully!")
                                st.rerun()
                else:
                    st.info("No pending orders to manage.")
            else:
                st.info(f"No {status_filter.lower()} orders found.")
        else:
            st.info("No purchase orders created yet.")

elif menu == "Financial Dashboard":
    st.header("💼 Financial Dashboard")
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    st.subheader(f"Current Month: {datetime.now().strftime('%B %Y')}")
    
    current_stats = get_monthly_stats(current_year, current_month)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Monthly Revenue", f"₹{current_stats['total_revenue']:.2f}")
    with col2:
        st.metric("Monthly Profit", f"₹{current_stats['total_profit']:.2f}")
    with col3:
        st.metric("Transactions", current_stats['total_transactions'])
    with col4:
        if current_stats['total_revenue'] > 0:
            margin = (current_stats['total_profit'] / current_stats['total_revenue']) * 100
            st.metric("Profit Margin", f"{margin:.2f}%")
        else:
            st.metric("Profit Margin", "0.00%")
    
    products = get_all_products()
    if products:
        st.subheader("📦 Current Inventory Overview")
        
        total_stock_value_cost = sum(p.buying_price * p.current_stock for p in products)
        total_stock_value_retail = sum(p.selling_price * p.current_stock for p in products)
        potential_profit = total_stock_value_retail - total_stock_value_cost
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Inventory Value (Cost)", f"₹{total_stock_value_cost:.2f}")
        with col2:
            st.metric("Inventory Value (Retail)", f"₹{total_stock_value_retail:.2f}")
        with col3:
            st.metric("Potential Profit in Stock", f"₹{potential_profit:.2f}")
        
        st.subheader("📊 Performance Analysis")
        
        if current_stats['total_profit'] > 0:
            st.success(f"✅ Profitable Month: ₹{current_stats['total_profit']:.2f} profit")
        elif current_stats['total_profit'] < 0:
            st.error(f"❌ Loss Month: ₹{abs(current_stats['total_profit']):.2f} loss")
        else:
            st.info("No profit or loss this month")
        
        db = get_db()
        try:
            month_start, month_end = _month_bounds(current_year, current_month)
            top_products = db.query(
                Product.name,
                func.sum(Sale.quantity).label('total_sold'),
                func.sum(Sale.quantity * (Sale.sale_price - Sale.cost_price)).label('product_profit')
            ).join(Sale).filter(
                Sale.sale_date >= month_start,
                Sale.sale_date < month_end
            ).group_by(Product.name).order_by(func.sum(Sale.quantity * (Sale.sale_price - Sale.cost_price)).desc()).limit(5).all()

            if top_products:
                st.subheader("🏆 Top Performing Products This Month")
                for idx, (name, sold, profit) in enumerate(top_products, 1):
                    st.write(f"{idx}. **{name}** - {sold} units sold, ₹{profit:.2f} profit")
        finally:
            db.close()
    else:
        st.info("No inventory data available.")

elif menu == "Trends & Analytics":
    st.header("📈 Trends & Analytics")
    
    st.subheader("Multi-Month Performance Comparison")
    
    months_options = {"3 Months": 3, "6 Months": 6, "12 Months": 12, "24 Months": 24}
    selected_period = st.selectbox("Select Period", list(months_options.keys()), index=1)
    
    months_back = months_options[selected_period]
    trend_data = get_multi_month_stats(months_back)
    
    if any(d['revenue'] > 0 or d['profit'] > 0 for d in trend_data):
        df_trends = pd.DataFrame(trend_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💰 Revenue Trend")
            fig_revenue = go.Figure()
            fig_revenue.add_trace(go.Scatter(
                x=df_trends['month_name'],
                y=df_trends['revenue'],
                mode='lines+markers',
                name='Revenue',
                line=dict(color='#1f77b4', width=3),
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor='rgba(31, 119, 180, 0.2)'
            ))
            fig_revenue.update_layout(
                xaxis_title="Month",
                yaxis_title="Revenue ($)",
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig_revenue, use_container_width=True)
        
        with col2:
            st.subheader("💵 Profit Trend")
            fig_profit = go.Figure()
            fig_profit.add_trace(go.Scatter(
                x=df_trends['month_name'],
                y=df_trends['profit'],
                mode='lines+markers',
                name='Profit',
                line=dict(color='#2ca02c', width=3),
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor='rgba(44, 160, 44, 0.2)'
            ))
            fig_profit.update_layout(
                xaxis_title="Month",
                yaxis_title="Profit ($)",
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig_profit, use_container_width=True)
        
        st.subheader("📊 Combined Revenue vs Profit")
        fig_combined = go.Figure()
        fig_combined.add_trace(go.Bar(
            x=df_trends['month_name'],
            y=df_trends['revenue'],
            name='Revenue',
            marker_color='#1f77b4'
        ))
        fig_combined.add_trace(go.Bar(
            x=df_trends['month_name'],
            y=df_trends['profit'],
            name='Profit',
            marker_color='#2ca02c'
        ))
        fig_combined.update_layout(
            xaxis_title="Month",
            yaxis_title="Amount ($)",
            barmode='group',
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_combined, use_container_width=True)
        
        st.subheader("📉 Profit Margin Trend")
        df_trends['profit_margin'] = df_trends.apply(
            lambda x: (x['profit'] / x['revenue'] * 100) if x['revenue'] > 0 else 0,
            axis=1
        )
        
        fig_margin = go.Figure()
        fig_margin.add_trace(go.Scatter(
            x=df_trends['month_name'],
            y=df_trends['profit_margin'],
            mode='lines+markers',
            name='Profit Margin %',
            line=dict(color='#ff7f0e', width=3),
            marker=dict(size=8)
        ))
        fig_margin.update_layout(
            xaxis_title="Month",
            yaxis_title="Profit Margin (%)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_margin, use_container_width=True)
        
        st.subheader("📈 Key Insights")
        col1, col2, col3, col4 = st.columns(4)
        
        total_revenue = df_trends['revenue'].sum()
        total_profit = df_trends['profit'].sum()
        avg_monthly_revenue = df_trends['revenue'].mean()
        avg_monthly_profit = df_trends['profit'].mean()
        
        with col1:
            st.metric("Total Revenue", f"₹{total_revenue:.2f}")
        with col2:
            st.metric("Total Profit", f"₹{total_profit:.2f}")
        with col3:
            st.metric("Avg Monthly Revenue", f"₹{avg_monthly_revenue:.2f}")
        with col4:
            st.metric("Avg Monthly Profit", f"₹{avg_monthly_profit:.2f}")
        
        best_month = df_trends.loc[df_trends['profit'].idxmax()]
        worst_month = df_trends.loc[df_trends['profit'].idxmin()]
        
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"🏆 **Best Month**: {best_month['month_name']} with ₹{best_month['profit']:.2f} profit")
        with col2:
            if worst_month['profit'] < 0:
                st.error(f"⚠️ **Worst Month**: {worst_month['month_name']} with ₹{abs(worst_month['profit']):.2f} loss")
            else:
                st.info(f"📊 **Lowest Month**: {worst_month['month_name']} with ₹{worst_month['profit']:.2f} profit")
    else:
        st.info("No sales data available for the selected period. Start recording sales to see trends!")

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: Keep your product information updated for accurate financial tracking!")
