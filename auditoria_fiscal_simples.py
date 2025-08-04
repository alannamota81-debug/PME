
import streamlit as st
import pandas as pd
import plotly.express as px

# Carrega o relatório da empresa
arquivo = "Produtos_3227.csv"  # ajuste o nome do arquivo se necessário
df = pd.read_csv(arquivo, encoding='latin1', sep=';', dtype=str)

# Corrige vírgulas para pontos e converte para número
df['Vlr contábil'] = df['Vlr contábil'].str.replace(',', '.').astype(float)
df['NCM'] = df['NCM'].str.replace('.', '').str.strip()

# Base de NCMs Monofásicos e Alíquota Zero (exemplos)
ncm_monofasico = [
    "33051000",  # Shampoo
    "30049069",  # Medicamento
    "22030000",  # Cerveja
    "87032210",  # Automóvel
    "27101259",  # Gasolina
]

ncm_aliq_zero = [
    "10063021",  # Arroz
    "49019900",  # Livros
    "02071400",  # Carne de frango
]

def classificar_ncm(ncm):
    if ncm in ncm_monofasico:
        return "Monofásico"
    elif ncm in ncm_aliq_zero:
        return "Alíquota Zero"
    else:
        return "Tributável"

# Aplica a classificação
df["Classificação Fiscal"] = df["NCM"].apply(classificar_ncm)

# Marca produtos com possíveis erros
def checar_erro(row):
    if row["Classificação Fiscal"] in ["Monofásico", "Alíquota Zero"]:
        return "⚠️ Verificar: Produto pode estar sendo tributado indevidamente"
    return ""

df["Alerta Fiscal"] = df.apply(checar_erro, axis=1)

# Exporta o relatório final
df.to_excel("Relatorio_Auditoria_Fiscal.xlsx", index=False)

print("✅ Auditoria finalizada! Arquivo salvo como 'Relatorio_Auditoria_Fiscal.xlsx'")
st.dataframe(df)

