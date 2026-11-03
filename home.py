import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import calculadora_agricola
import modulo_mapas

# Configuração da Página
st.set_page_config(
    page_title="Agrocana-Pro | Demonstração",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

DADOS_TCH = pd.DataFrame(
    {
        "Safra": ["2021/22", "2022/23", "2023/24", "2024/25", "2025/26"],
        "TCH (ton/ha)": [78.2, 81.0, 75.4, 82.1, 84.5],
        "Classificação": ["Ilustrativo — sem fonte oficial"] * 5,
    }
)

DADOS_CLIMATICOS = pd.DataFrame(
    {
        "Mês": ["Out", "Nov", "Dez", "Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set"],
        "Precipitação (mm)": [120, 180, 210, 250, 190, 140, 80, 40, 20, 15, 30, 70],
        "TCH estimado (ton/ha)": [82, 83, 84, 85, 85, 84, 83, 82, 81, 81, 82, 82],
        "Classificação": ["Ilustrativo — sem fonte oficial"] * 12,
    }
)

MODELO_TCH_MUNICIPAL = pd.DataFrame(
    columns=["Município", "UF", "Safra", "TCH (ton/ha)", "ATR (kg/ton)", "Fonte dos dados"]
)

opcao = st.sidebar.selectbox(
    "Navegação",
    [
        "Home",
        "Calculadora Agronômica e Financeira",
        "Gestão Espacial e Talhões",
    ],
)

if opcao == "Calculadora Agronômica e Financeira":
    calculadora_agricola.app()
    st.stop()

if opcao == "Gestão Espacial e Talhões":
    modulo_mapas.app()
    st.stop()

# Estilização CSS Profissional e Moderna (Agrocana-Pro)
st.markdown("""
    <style>
    /* Fundo geral com gradiente verde claro */
    .stApp {
        background-image: linear-gradient(rgba(236, 253, 245, 0.90), rgba(209, 250, 229, 0.90));
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Estilização da Sidebar (Barra Lateral) */
    [data-testid="stSidebar"] {
        background-color: #064e3b;
        color: #ffffff;
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #ecfdf5 !important;
    }

    /* Cards de Métricas (KPIs) com design moderno */
    .stMetric {
        background-color: #ffffff;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border-left: 5px solid #059669;
        border: 1px solid #e5e7eb;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BARRA LATERAL (Navegação e Configurações)
# ---------------------------------------------------------
st.sidebar.title("Agrocana-Pro")
st.sidebar.markdown("*Demonstração de conceitos agrícolas*")
st.sidebar.markdown("---")
st.sidebar.info("💡 Os valores exibidos são ilustrativos e não representam medições ou previsões validadas.")

# ---------------------------------------------------------
# CABEÇALHO PRINCIPAL
# ---------------------------------------------------------
st.title("🌾 Agrocana-Pro: Inteligência Climática e Agrícola")
st.markdown("Demonstração de indicadores, cálculos e visualizações para a cultura da cana-de-açúcar.")

# ---------------------------------------------------------
# ABAS DA APLICAÇÃO
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 Dashboard demonstrativo", "🧮 Simulador didático", "📁 Dados e fontes"])

# =========================================================
# ABA 1: DASHBOARD & INDICADORES
# =========================================================
with tab1:
    st.header("Painel geral — valores ilustrativos")
    st.caption("As séries e métricas desta tela são exemplos estáticos, não dados oficiais ou observações de campo.")

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="TCH demonstrativo mais recente",
            value=f"{DADOS_TCH['TCH (ton/ha)'].iloc[-1]:.1f} ton/ha",
        )
    with col2:
        st.metric(label="ATR de exemplo", value="138.2 kg/ton")
    with col3:
        precipitacao_total = DADOS_CLIMATICOS["Precipitação (mm)"].sum()
        st.metric(label="Precipitação demonstrativa", value=f"{precipitacao_total:,.0f} mm")
    with col4:
        st.metric(label="Estresse hídrico", value="Não calculado")
        
    st.markdown("---")
    
    # Gráficos com Plotly
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        st.subheader("Série demonstrativa de TCH (2021–2026)")
        fig_tch = px.bar(
            DADOS_TCH,
            x="Safra",
            y="TCH (ton/ha)",
            labels={"Safra": "Safra", "TCH (ton/ha)": "TCH (ton/ha)"},
            color_discrete_sequence=["#16a34a"],
        )
        fig_tch.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(
            fig_tch,
            width="stretch",
            alt="Série ilustrativa de produtividade por safra, sem fonte oficial.",
        )
        
    with col_g2:
        st.subheader("Séries mensais de exemplo")
        fig_corr = make_subplots(specs=[[{"secondary_y": True}]])
        fig_corr.add_trace(
            go.Bar(
                x=DADOS_CLIMATICOS["Mês"],
                y=DADOS_CLIMATICOS["Precipitação (mm)"],
                name="Precipitação (mm)",
                marker_color="#60a5fa",
            ),
            secondary_y=False,
        )
        fig_corr.add_trace(
            go.Scatter(
                x=DADOS_CLIMATICOS["Mês"],
                y=DADOS_CLIMATICOS["TCH estimado (ton/ha)"],
                name="TCH estimado (ton/ha)",
                mode="lines+markers",
                line={"color": "#16a34a"},
            ),
            secondary_y=True,
        )
        fig_corr.update_xaxes(title_text="Mês")
        fig_corr.update_yaxes(title_text="Precipitação (mm)", secondary_y=False)
        fig_corr.update_yaxes(title_text="TCH estimado (ton/ha)", secondary_y=True)
        fig_corr.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(
            fig_corr,
            width="stretch",
            alt="Séries mensais ilustrativas de precipitação e TCH, em escalas separadas.",
        )

# =========================================================
# ABA 2: SIMULADOR DIDÁTICO
# =========================================================
with tab2:
    st.header("🧮 Simulador didático de TCH e ATR")
    st.markdown("Ajuste os parâmetros para ver o resultado de uma fórmula simplificada. O cálculo não usa dados observados nem um modelo agronômico calibrado.")
    
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        st.subheader("Parâmetros Climáticos e de Solo")
        precipitacao_sim = st.slider("Precipitação Anual Acumulada (mm)", 800, 2500, 1450, 50)
        temp_media = st.slider("Temperatura Média Anual (°C)", 18.0, 32.0, 24.5, 0.5)
        tipo_solo = st.selectbox("Tipo de Solo Predominante", ["Latossolo Vermelho (Alta Fertilidade)", "Argissolo Vermelho-Amarelo", "Neossolo Quartzarênico"])
        idade_canavial = st.selectbox("Estágio / Corte do Canavial", ["1º Corte (Planta)", "2º Corte", "3º Corte", "4º Corte ou mais"])
        
    with col_s2:
        st.subheader("Resultado da simulação")
        tch_previsto, atr_previsto = calculadora_agricola.estimar_produtividade(
            precipitacao_sim,
            temp_media,
            tipo_solo,
            idade_canavial,
        )
        
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric("TCH demonstrativo", f"{tch_previsto:.1f} ton/ha")
        with res_col2:
            st.metric("ATR demonstrativo", f"{atr_previsto:.1f} kg/ton")
            
        st.markdown("---")
        st.info(
            f"Resultado ilustrativo para solo **{tipo_solo}** e precipitação de "
            f"**{precipitacao_sim} mm**. Não representa uma previsão validada "
            "nem uma avaliação de estresse hídrico."
        )

# =========================================================
# ABA 3: REFERÊNCIAS E AMOSTRAS
# =========================================================
with tab3:
    st.header("📁 Referências e amostras de dados")
    st.markdown(
        "As instituições listadas são referências para consulta; esta demonstração "
        "não está conectada a essas fontes. Os arquivos abaixo são exemplos "
        "ilustrativos, não bases oficiais."
    )
    
    # Tabela de Datasets
    data_datasets = {
        "Dataset": ["Levantamento de Safra - Cana", "Estações Meteorológicas Automáticas", "Zoneamento Agrícola de Risco Climático (ZARC)", "Mapeamento de Áreas Canavieiras (CanaSat)"],
        "Órgão / Fonte": ["CONAB", "INMET", "Embrapa / MAPA", "INPE / Embrapa"],
        "Frequência": ["Mensal", "Horária / Diária", "Anual", "Anual"],
        "Formato": ["CSV / XLSX", "CSV / API", "GeoJSON / PDF", "Shapefile / TIFF"]
    }
    df_repo = pd.DataFrame(data_datasets)
    
    st.dataframe(
        df_repo,
        width="stretch",
        alt="Referências de instituições e formatos de dados agrícolas públicos.",
    )
    
    st.markdown("### 📥 Baixar arquivos CSV demonstrativos")
    col_d1, col_d2, col_d3 = st.columns(3)
    
    with col_d1:
        st.download_button(
            "Baixar TCH demonstrativo",
            data=DADOS_TCH.to_csv(index=False).encode("utf-8-sig"),
            file_name="tch_demonstrativo.csv",
            mime="text/csv",
            help="Série de exemplo; não corresponde a dados oficiais da CONAB.",
        )
    with col_d2:
        st.download_button(
            "Baixar clima demonstrativo",
            data=DADOS_CLIMATICOS.to_csv(index=False).encode("utf-8-sig"),
            file_name="clima_demonstrativo.csv",
            mime="text/csv",
            help="Série de exemplo; não corresponde a observações do INMET.",
        )
    with col_d3:
        st.download_button(
            "Baixar modelo municipal vazio",
            data=MODELO_TCH_MUNICIPAL.to_csv(index=False).encode("utf-8-sig"),
            file_name="modelo_tch_municipal.csv",
            mime="text/csv",
            help="Modelo vazio para preenchimento; não contém medições de municípios.",
        )

# ---------------------------------------------------------
# RODAPÉ
# ---------------------------------------------------------

st.markdown("---")
st.markdown(
    """
    <p style='text-align: center; color: #1e293b; font-size: 14px;'>
    <strong>Agrocana-Pro</strong> — Análise e Previsão de Produtividade de Cana-de-Açúcar com Dados Públicos<br>
    Projeto Integrador em Computação IV - DRP10 - Turma 001<br>
    © 2026 — Todos os direitos reservados.
    </p>
    """, 
    unsafe_allow_html=True
)
