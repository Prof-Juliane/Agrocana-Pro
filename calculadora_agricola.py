import pandas as pd
import plotly.express as px
import streamlit as st


def estimar_produtividade(
    precipitacao_mm: int,
    temperatura_c: float,
    tipo_solo: str,
    corte: str,
) -> tuple[float, float]:
    tch = 75.0
    if tipo_solo == "Latossolo Vermelho (Alta Fertilidade)":
        tch += 10
    elif tipo_solo == "Argissolo Vermelho-Amarelo":
        tch += 5

    if precipitacao_mm < 1100:
        tch -= 12
    elif precipitacao_mm > 1800:
        tch += 8

    if corte == "1º Corte (Planta)":
        tch += 12
    elif corte == "4º Corte ou mais":
        tch -= 8

    tch = round(tch + (temperatura_c - 24) * 0.5, 1)
    atr = round(130 + (25 - temperatura_c) * 1.2 + (2000 - precipitacao_mm) * 0.002, 1)
    return tch, atr


def app() -> None:
    st.title("🌾 AgroCana Pro - Calculadora Agrícola")
    st.markdown(
        "Ferramenta de suporte à decisão agronômica e financeira "
        "para a cultura da cana-de-açúcar."
    )
    
    modulo = st.sidebar.selectbox(
        "Selecione o módulo",
        [
            "1. Correção e Adubação do Solo",
            "2. Custo de Produção por Hectare",
            "3. Simulador de Rentabilidade (ROI)",
            "4. Estimativa de TCH e ATR",
        ],
        key="calculator_module",
    )
    area_ha = st.sidebar.number_input(
        "Área total da lavoura (hectares)",
        min_value=1.0,
        value=50.0,
        step=5.0,
    )
    
    if modulo == "1. Correção e Adubação do Solo":
        st.header("🧪 Recomendação de Corretivos e Fertilizantes (NPK)")
        col1, col2 = st.columns(2)
    
        with col1:
            st.subheader("Análise de solo atual")
            calcio = st.number_input("Cálcio (Ca) [cmolc/dm³]", min_value=0.0, value=2.5, step=0.1)
            magnesio = st.number_input("Magnésio (Mg) [cmolc/dm³]", min_value=0.0, value=1.0, step=0.1)
            v_atual = st.number_input(
                "Saturação por bases atual (V%)",
                min_value=0.0,
                max_value=100.0,
                value=45.0,
                step=1.0,
            )
            v_desejado = st.number_input(
                "Saturação por bases desejada (V%)",
                min_value=0.0,
                max_value=100.0,
                value=65.0,
                step=1.0,
            )
            prnt = st.number_input(
                "PRNT do calcário (%)",
                min_value=1.0,
                max_value=100.0,
                value=80.0,
                step=1.0,
            )
    
        with col2:
            st.subheader("Expectativa de produtividade")
            tch_esperado = st.number_input(
                "TCH esperado (ton/ha)",
                min_value=40.0,
                value=80.0,
                step=5.0,
            )
    
        if st.button("Calcular insumos de solo"):
            ctc_estimada = (calcio + magnesio) * 2.2
            nc_t_ha = max(0.0, ((v_desejado - v_atual) * ctc_estimada) / prnt)
            gesso_t_ha = 0.5 if calcio < 2.0 else 0.2
            n_kg_ha = tch_esperado * 1.2
            p_kg_ha = tch_esperado * 0.8
            k_kg_ha = tch_esperado * 1.5
    
            st.success("Cálculo realizado com sucesso!")
            m1, m2, m3 = st.columns(3)
            m1.metric(
                "Calcário dolomítico",
                f"{nc_t_ha:.2f} t/ha",
                f"Total: {nc_t_ha * area_ha:.1f} toneladas",
            )
            m2.metric(
                "Gesso agrícola",
                f"{gesso_t_ha:.2f} t/ha",
                f"Total: {gesso_t_ha * area_ha:.1f} toneladas",
            )
            m3.metric("N-P-K (kg/ha)", f"N: {n_kg_ha:.0f} | P: {p_kg_ha:.0f} | K: {k_kg_ha:.0f}")
            st.caption(
                "Recomendações simplificadas para estimativa. Confirme doses com análise "
                "laboratorial e orientação de profissional agronômico."
            )
    
    elif modulo == "2. Custo de Produção por Hectare":
        st.header("💰 Estimativa detalhada de custos por hectare")
        st.markdown("Informe os custos estimados para compor o orçamento operacional da safra.")
    
        col1, col2 = st.columns(2)
        with col1:
            prep_solo = st.number_input("Preparo do solo (R$/ha)", min_value=0.0, value=450.0, step=50.0)
            mudas = st.number_input("Mudas e plantio (R$/ha)", min_value=0.0, value=1800.0, step=100.0)
            tratos = st.number_input("Tratos culturais (R$/ha)", min_value=0.0, value=1200.0, step=100.0)
        with col2:
            colheita = st.number_input("Colheita mecanizada (R$/ha)", min_value=0.0, value=900.0, step=50.0)
            frete = st.number_input("Frete até a usina (R$/ha)", min_value=0.0, value=750.0, step=50.0)
            outros = st.number_input("Outros custos (R$/ha)", min_value=0.0, value=400.0, step=50.0)
    
        custos = [prep_solo, mudas, tratos, colheita, frete, outros]
        custo_total_ha = sum(custos)
        custo_geral_projeto = custo_total_ha * area_ha
        participacoes = [
            (custo / custo_total_ha * 100) if custo_total_ha > 0 else 0.0
            for custo in custos
        ]
    
        st.markdown("---")
        res1, res2 = st.columns(2)
        res1.metric("Custo total por hectare", f"R$ {custo_total_ha:,.2f} / ha")
        res2.metric("Custo total da propriedade", f"R$ {custo_geral_projeto:,.2f}")
    
        df_custos = pd.DataFrame(
            {
                "Etapa Operacional": [
                    "Preparo do solo",
                    "Mudas e plantio",
                    "Tratos culturais",
                    "Colheita",
                    "Frete",
                    "Outros",
                ],
                "Custo (R$/ha)": custos,
                "Participação (%)": participacoes,
            }
        )
        st.markdown("---")
        st.subheader("📊 Análise visual da composição de custos")
        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            if custo_total_ha > 0:
                fig_pizza = px.pie(
                    df_custos,
                    names="Etapa Operacional",
                    values="Custo (R$/ha)",
                    title="Participação percentual por etapa",
                    hole=0.4,
                    color_discrete_sequence=px.colors.sequential.Greens,
                )
                fig_pizza.update_traces(textposition="inside", textinfo="percent+label")
                st.plotly_chart(
                    fig_pizza,
                    width="stretch",
                    alt="Participação percentual de cada etapa no custo por hectare.",
                )
            else:
                st.info("Informe algum custo acima de zero para visualizar a composição percentual.")

        with col_graf2:
            fig_barras = px.bar(
                df_custos,
                x="Etapa Operacional",
                y="Custo (R$/ha)",
                text="Custo (R$/ha)",
                title="Custo absoluto por hectare (R$/ha)",
                color="Etapa Operacional",
                color_discrete_sequence=px.colors.sequential.Aggrnyl,
            )
            fig_barras.update_traces(
                texttemplate="R$ %{text:,.0f}",
                textposition="outside",
            )
            fig_barras.update_layout(xaxis_tickangle=-25, showlegend=False)
            st.plotly_chart(
                fig_barras,
                width="stretch",
                alt="Custos absolutos por hectare em cada etapa operacional.",
            )

        st.dataframe(
            df_custos.style.format(
                {"Custo (R$/ha)": "R$ {:,.2f}", "Participação (%)": "{:.1f}%"}
            ),
            width="stretch",
            alt="Detalhamento de custos por etapa, valor por hectare e participação percentual.",
        )
    
    elif modulo == "3. Simulador de Rentabilidade (ROI)":
        st.header("📈 Simulador de rentabilidade e retorno financeiro")
    
        col1, col2 = st.columns(2)
        with col1:
            tch_sim = st.number_input("Produtividade média estimada (TCH) [ton/ha]", min_value=0.0, value=85.0, step=2.0)
            atr_sim = st.number_input("ATR [kg/t]", min_value=0.0, value=130.0, step=1.0)
        with col2:
            preco_ton = st.number_input(
                "Preço líquido estimado por tonelada de cana (R$/ton)",
                min_value=0.0,
                value=160.0,
                step=5.0,
            )
            custo_ha_sim = st.number_input(
                "Custo total por hectare (R$/ha)",
                min_value=0.0,
                value=5500.0,
                step=100.0,
            )
    
        if st.button("Simular rentabilidade"):
            receita_bruta_ha = tch_sim * preco_ton
            lucro_bruto_ha = receita_bruta_ha - custo_ha_sim
            margem_lucro = (
                (lucro_bruto_ha / receita_bruta_ha) * 100
                if receita_bruta_ha > 0
                else 0.0
            )
            roi = (lucro_bruto_ha / custo_ha_sim) * 100 if custo_ha_sim > 0 else 0.0
    
            st.success("Simulação de safra concluída!")
            r1, r2, r3, r4 = st.columns(4)
            r1.metric("Receita bruta/ha", f"R$ {receita_bruta_ha:,.2f}")
            r2.metric("Lucro líquido/ha", f"R$ {lucro_bruto_ha:,.2f}", delta=f"{margem_lucro:.1f}% de margem")
            r3.metric("ROI estimado", f"{roi:.1f}%")
            r4.metric("Lucro total da área", f"R$ {lucro_bruto_ha * area_ha:,.2f}")
            st.caption(
                f"ATR informado: {atr_sim:.1f} kg/t. O preço por tonelada é aplicado "
                "diretamente e não é recalculado com base no ATR."
            )
    
    elif modulo == "4. Estimativa de TCH e ATR":
        st.header("🌦️ Estimativa de produtividade")
        col1, col2 = st.columns(2)
        with col1:
            area_calculo_ha = st.number_input(
                "Área de cultivo (ha)",
                min_value=0.1,
                value=1.0,
                step=0.5,
            )
            precipitacao_mm = st.slider(
                "Precipitação anual (mm)",
                min_value=800,
                max_value=2500,
                value=1450,
                step=50,
            )
        with col2:
            temperatura_c = st.slider(
                "Temperatura média anual (°C)",
                min_value=18.0,
                max_value=32.0,
                value=24.5,
                step=0.5,
            )
            tipo_solo = st.selectbox(
                "Tipo de solo",
                [
                    "Latossolo Vermelho (Alta Fertilidade)",
                    "Argissolo Vermelho-Amarelo",
                    "Neossolo Quartzarênico",
                ],
            )
    
        corte = st.selectbox(
            "Estágio / corte do canavial",
            ["1º Corte (Planta)", "2º Corte", "3º Corte", "4º Corte ou mais"],
        )
        tch, atr = estimar_produtividade(
            precipitacao_mm,
            temperatura_c,
            tipo_solo,
            corte,
        )
        metric1, metric2, metric3 = st.columns(3)
        metric1.metric("Produtividade (TCH)", f"{tch:.1f} t/ha")
        metric2.metric("Produção estimada", f"{tch * area_calculo_ha:,.1f} t")
        metric3.metric("Qualidade (ATR)", f"{atr:.1f} kg/t")
        st.caption(
            "Estimativa simplificada para simulação; não substitui análise de campo "
            "nem modelo agronômico calibrado para a região."
        )


if __name__ == "__main__":
    st.set_page_config(
        page_title="AgroCana Pro | Calculadora Agr?cola",
        page_icon="??",
        layout="wide",
    )
    app()
