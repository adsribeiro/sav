import streamlit as st
import pandas as pd
import random


def main():
    """
    Main function to handle the Streamlit app logic.
    """

    st.set_page_config(
        page_title="Pet Sales Dashboard",
        page_icon="🐾",
        layout="wide",
    )

    # Initialize session state if not already present
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "new_order_data" not in st.session_state:
        st.session_state.new_order_data = pd.DataFrame(
            columns=[
                "Pedido",
                "Representante",
                "Marca",
                "Produto",
                "Quantidade",
                "Valor Venda",
            ]
        )
    if "show_order_items" not in st.session_state:
        st.session_state.show_order_items = False
    if "new_order_general_info" not in st.session_state:
        st.session_state.new_order_general_info = {}

    if not st.session_state.logged_in:
        show_login_form()
    else:
        show_dashboard()


def show_login_form():
    """
    Displays the login form.
    """
    st.title("Login")
    username = st.text_input("Representante")
    password = st.text_input("Senha", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.rerun()  # Rerun to show the dashboard
        else:
            st.error("Usuário ou senha inválida.")


def show_dashboard():
    """
    Displays the main dashboard with sales metrics.
    """
    # Sidebar for navigation and logout
    with st.sidebar:
        st.title("Navegação")
        selected_page = st.radio(
            "Ir para", ["Home", "Pedidos", "Relatórios", "Diversos"]
        )
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # Sample data (replace with actual data loading)
    data = generate_sample_data()

    # Display content based on selected page
    if selected_page == "Home":
        show_home(data)
    elif selected_page == "Pedidos":
        show_pedidos(data)
    elif selected_page == "Relatórios":
        show_relatorios(data)
    elif selected_page == "Diversos":
        show_diversos()


def show_home(data):
    """
    Displays the home page with KPIs and metrics.
    """
    st.title("Dashboard de Vendas de Produtos Pet")
    st.write("Bem-vindo ao painel de controle de vendas!")

    # KPIs
    total_sales = data["Valor Venda"].sum()
    num_orders = data["Pedido"].nunique()
    avg_order_value = total_sales / num_orders if num_orders > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Vendas Totais", f"R$ {total_sales:,.2f}")
    col2.metric("Número de Pedidos", num_orders)
    col3.metric("Valor Médio do Pedido", f"R$ {avg_order_value:,.2f}")

    # Sales by Representative
    st.subheader("Vendas por Representante")
    sales_by_rep = (
        data.groupby("Representante")["Valor Venda"].sum().sort_values(ascending=False)
    )
    st.bar_chart(sales_by_rep)

    # Sales by Brand
    st.subheader("Vendas por Marca")
    sales_by_brand = (
        data.groupby("Marca")["Valor Venda"].sum().sort_values(ascending=False)
    )
    st.bar_chart(sales_by_brand)

    # Top selling products
    st.subheader("Produtos Mais Vendidos")
    top_products = (
        data.groupby("Produto")["Quantidade"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(top_products)


def show_pedidos(data):
    """
    Display Pedidos
    """
    st.title("Pedidos")

    if st.button("Fazer Pedido"):
        st.session_state.new_order_general_info = {}
        show_new_order_form()

    if (
        not st.session_state.show_order_items
        and len(st.session_state.new_order_data) > 0
    ):
        st.dataframe(st.session_state.new_order_data)
    elif st.session_state.show_order_items:
        show_order_items_form()
    else:
        st.dataframe(data)


def show_new_order_form():
    """
    Display the form to create a new order.
    """

    st.subheader("Novo Pedido - Informações Gerais")

    # Sample data for dropdowns (replace with actual data)
    companies = ["Filial A", "Filial B", "Filial C"]
    clients = ["Cliente 1", "Cliente 2", "Cliente 3"]
    reps = ["Allan", "Luan", "Ana", "Bruno", "Carla"]
    order_types = [
        "Entrada Normal",
        "Entrada de Pedido Bonificação",
        "Entrada de Pedido Amostra Grátis",
    ]
    price_tables = ["Tabela 1", "Tabela 2", "Tabela 3"]
    delivery_types = [
        "Cliente Retira",
        "Roterização",
        "Pedido Agendado/Programado",
        "Liberado/Imediato",
    ]

    company = st.selectbox("Empresa/Filial", companies, key="company")
    client = st.selectbox("Cliente", clients, key="client")
    rep = st.selectbox("Representante", reps, key="rep")
    order_type = st.selectbox("Tipo do Pedido", order_types, key="order_type")
    price_table = st.selectbox("Tabela de Preço", price_tables, key="price_table")
    credit_sac = st.radio("Crédito SAC", ["Sim", "Não"], key="credit_sac")
    delivery_type = st.selectbox("Tipo Entrega", delivery_types, key="delivery_type")

    if st.button("Processar Pedido"):
        st.session_state.new_order_general_info = {
            "Empresa/Filial": company,
            "Cliente": client,
            "Representante": rep,
            "Tipo do Pedido": order_type,
            "Tabela de Preço": price_table,
            "Crédito SAC": credit_sac,
            "Tipo Entrega": delivery_type,
        }
        st.session_state.show_order_items = True
        st.rerun()


def show_order_items_form():
    """
    Display the form to add items to the order.
    """

    st.subheader("Informações do pedido")
    for key, value in st.session_state.new_order_general_info.items():
        st.write(f"{key}: {value}")

    st.subheader("Itens do Pedido")
    products = [
        "Ração Premium",
        "Ração Light",
        "Petiscos",
        "Brinquedos",
        "Shampoo",
        "Areia",
    ]
    new_product = st.selectbox("Produto", products, key="new_product")
    new_quantity = st.number_input(
        "Quantidade", min_value=1, value=1, step=1, key="new_quantity"
    )
    new_price = st.number_input(
        "Preço", min_value=0.01, value=50.00, step=0.01, key="new_price"
    )

    if st.button("Adicionar Item"):
        new_row = pd.DataFrame(
            [
                {
                    "Pedido": len(st.session_state.new_order_data) + 1,
                    "Representante": st.session_state.new_order_general_info[
                        "Representante"
                    ],
                    "Marca": "Marca X",  # Placeholder, replace with actual brand selection
                    "Produto": new_product,
                    "Quantidade": new_quantity,
                    "Valor Venda": new_quantity * new_price,
                }
            ]
        )
        st.session_state.new_order_data = pd.concat(
            [st.session_state.new_order_data, new_row], ignore_index=True
        )
        st.rerun()

    if len(st.session_state.new_order_data) > 0:
        st.dataframe(st.session_state.new_order_data)

    if st.button("Finalizar Pedido"):
        st.success("Pedido Finalizado com Sucesso")
        st.session_state.show_order_items = False
        st.session_state.new_order_data = pd.DataFrame(
            columns=[
                "Pedido",
                "Representante",
                "Marca",
                "Produto",
                "Quantidade",
                "Valor Venda",
            ]
        )
        st.session_state.new_order_general_info = {}
        st.rerun()


def show_relatorios(data):
    """
    Display Relatórios
    """
    st.title("Relatórios")
    st.write("Aqui você pode gerar diversos relatórios!")
    st.dataframe(data)


def show_diversos():
    """
    Display Diversos
    """
    st.title("Diversos")
    st.write("Esta é uma página com informações diversas.")


def authenticate(username, password):
    """
    Checks the username and password against stored credentials.

    Replace this with your actual authentication logic (e.g., database lookup).
    """
    # Replace with your actual credentials or database lookup
    valid_users = {"admin": "admin123", "allan": "123", "luan": "123"}

    if username in valid_users and valid_users[username] == password:
        return True
    else:
        return False


def generate_sample_data():
    """
    Generates sample sales data.
    """
    reps = ["Allan", "Luan", "Ana", "Bruno", "Carla"]
    brands = ["Patas Felizes", "AuAuBom", "MiauDelícia", "PetPower", "NutriPet"]
    products = [
        "Ração Premium",
        "Ração Light",
        "Petiscos",
        "Brinquedos",
        "Shampoo",
        "Areia",
    ]
    data = []
    for i in range(1, 101):
        rep = random.choice(reps)
        brand = random.choice(brands)
        product = random.choice(products)
        quantity = random.randint(1, 10)
        price = random.uniform(20, 200)
        data.append(
            {
                "Pedido": i,
                "Representante": rep,
                "Marca": brand,
                "Produto": product,
                "Quantidade": quantity,
                "Valor Venda": quantity * price,
            }
        )
    return pd.DataFrame(data)


if __name__ == "__main__":
    main()
