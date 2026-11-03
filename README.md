# AgroCana Pro 🌱📊

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)
[![Status Acadêmico](https://img.shields.io/badge/Status-Ativo-green.svg)](https://github.com/Prof-Juliane/Agrocana-Pro)

Plataforma web acadêmica interativa desenvolvida com Python e Streamlit para exploração de cálculos agronômicos, simulações e visualização de dados referentes à cultura da cana-de-açúcar.

🌐 **Acesse a aplicação online:** [agrocana-pro.onrender.com](https://agrocana-pro.onrender.com)

</div>

---

## ⚠️ Aviso Importante

Os indicadores, séries temporais e arquivos CSV disponibilizados na aplicação possuem caráter **estritamente demonstrativo e didático**. Eles não representam dados oficiais de órgãos governamentais ou de pesquisa (como CONAB ou INMET), nem constituem previsões agronômicas validadas em campo para fins comerciais.

---

## 🎯 Contexto Acadêmico

Este projeto integra as atividades do **Projeto Integrador em Computação IV** (DRP10 - Turma 001), tendo como principal objetivo articular os fundamentos da engenharia de software, modelagem de dados e conceitos agronômicos em uma solução acessível e intuitiva via navegador.

---

## 🚀 Funcionalidades da Plataforma

* **Dashboard Demonstrativo:** Visualização de indicadores-chave e séries históricas de exemplo para Toneladas de Cana por Hectare (**TCH**), Açúcar Total Recuperável (**ATR**) e índices pluviométricos.
* **Simulador Didático:** Aplicação de modelo simplificado para projeção de impacto considerando precipitação acumulada, temperatura média, características de solo e ciclo de corte.
* **Calculadora Agrícola e Financeira:**
  * Estimativa de corretivos de solo (calagem e gessagem) e adubação (NPK).
  * Levantamento simplificado de custos operacionais e margem de rentabilidade.
  * Cálculos e estimativas correlacionadas de TCH e ATR.
* **Gestão Espacial:** Visualização geoespacial interativa com talhões ilustrativos utilizando **Folium**. *(Nota: Os mapas utilizam camadas do OpenStreetMap e Esri, exigindo conexão com a internet para renderização dos tiles).*
* **Repositório de Dados:** Área dedicada com referências técnicas, download de datasets sintéticos em CSV e templates municipais padronizados.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Interface & Visualização:** Streamlit, Pandas, Plotly
* **Mapeamento Geoespacial:** Leaflet.js / Folium
* **Deploy:** Render

---

## 💻 Como Executar o Projeto Localmente

Se desejar clonar e executar a aplicação em sua máquina de desenvolvimento:

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/Prof-Juliane/Agrocana-Pro.git](https://github.com/Prof-Juliane/Agrocana-Pro.git)
   cd Agrocana-Pro
