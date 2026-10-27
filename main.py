from pathlib import Path
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

diretorio = Path(__file__).resolve().parent
caminho_entrada = (diretorio / "data" / "producao_industrial.csv")
caminho_saida = (diretorio / "outputs")

df = pd.read_csv(caminho_entrada)

#Verificar valores 
df["data"] = pd.to_datetime(df["data"], errors="coerce")

colunas = ["data","maquina","turno","horas_planeadas","tempo_paragem_min","quantidade_produzida","quantidade_defeituosa"]

print("\nValores em falta")
print(df[colunas].isna().sum())

duplicados = df.duplicated(keep=False)

print(f"Linhas duplicadas: {duplicados.sum()}")

if duplicados.any():
    print("\nLinhas duplicadas: ")
    print(df.loc[duplicados].sort_values())
else:
    print("\nNenhuma linha duplicada encontrada. ")

print("========== Visao Geral ===============")
print(df.info())

#Analise de produçao

#1.Quantidade de peças produzidas
total_producao = (df["quantidade_produzida"].sum())
print(f"\nA fabrica produziu um total de {total_producao} peças.")

#2 Peças produzidas por cada maquina
pecas_por_maquina = (df.groupby(["maquina"], as_index=False)["quantidade_produzida"]
                .sum()
                .sort_values("quantidade_produzida", ascending=False)
                .reset_index(drop=True))
print("\n========== TOTAL DE PEÇAS POR MÁQUINA ==========\n")
print(pecas_por_maquina)


#3. Maquina com maior produçao 
melhor_maquina= (df.groupby(["maquina"], as_index=False)["quantidade_produzida"]
                .sum()
                .sort_values("quantidade_produzida", ascending=False)
                .reset_index(drop=True))
print("\n========== MAQUINA COM MAIOR PRODUÇÃO ==========\n")
maior_producao = melhor_maquina.head(1)
print(maior_producao)

#4. Maquina com menor produçao

pior_maquina = (df.groupby(["maquina"], as_index=False)["quantidade_produzida"]
                .sum()
                .sort_values("quantidade_produzida", ascending=True)
                .reset_index(drop=True))

print("\n========== MAQUINA COM PIOR PRODUÇÃO ==========\n")
menor_producao = pior_maquina.head(1)
print(menor_producao)

#5. Peças defeituosas por maquina 
pecas_defeituosas_por_maquina = (df.groupby(["maquina"], as_index=False)["quantidade_defeituosa"]
                .sum()
                .sort_values("quantidade_defeituosa", ascending=False)
                .reset_index(drop=True))
print("\n========== PEÇAS DEFEITUOSAS POR MÁQUINA ==========\n")
print(pecas_defeituosas_por_maquina)

#6. Taxa de defeitos de cada maquina
df_total = df.groupby('maquina').agg(
            quantidade_produzida= ('quantidade_produzida', 'sum'), 
            quantidade_defeituosa = ('quantidade_defeituosa','sum')
            ).reset_index()

df_total['percentagem_defeito'] = (df_total['quantidade_defeituosa'] / df_total['quantidade_produzida']) * 100
df_total = df_total.sort_values(by='maquina')
print("\n========== TAXA DE DEFEITOS POR MÁQUINA ==========\n")
for _, linha in df_total.iterrows():
    print(f"Máquina {linha['maquina']} -> {linha['percentagem_defeito']:.2f}%")


#Análise das paragens das máquinas 
#7 - Tempo de paragem da fabrica
total_paragem = (df["tempo_paragem_min"].sum())
def formatar_tempo(total_paragem):
    horas, minutos = divmod(int(round(total_paragem)), 60)
    return f"{horas} horas {minutos:02d} minutos"

print("\n========== TEMPO TOLTA DE PARAGEM ==========")
print(f"\nO tempo de paragem total da fabrica e de {formatar_tempo(total_paragem)}.")  
#8 - Tempo total de paragem de cada maquina
tempo_maquinas = (df.groupby(["maquina"], as_index=False)["tempo_paragem_min"]
                .sum()
                .sort_values("tempo_paragem_min")
                .reset_index(drop=True))
print("\n========== TEMPO DE PARAGEM POR MAQUINA ==========\n")
print(tempo_maquinas)

#9 - Maquina com maior tempo de paragem

print("\n========== MAQUINA COM MAIOR TEMPO DE PARAGEM ==========\n")
tempo_minimo_maquina = (df.groupby(["maquina"], as_index=False)["tempo_paragem_min"]
                .sum()
                .sort_values("tempo_paragem_min", ascending=False)
                .reset_index(drop=True))
maior_tempo_paragem = tempo_minimo_maquina.head(1)
print(maior_tempo_paragem)

#10 - Maquina com menor tempo de paragem
print("\n========== MAQUINA COM MENOR TEMPO DE PARAGEM ==========\n")
menor_tempo_producao = tempo_maquinas.head(1)
print(menor_tempo_producao)
#11 - Percetagem de tempo de paragem ao tempo planeado por maquina 
df_tempo = df.groupby('maquina').agg(
            horas_planeadas= ('horas_planeadas', 'sum'), 
            horas_paragem = ('tempo_paragem_min','sum')
            ).reset_index()

df_tempo['minutos_planeados'] = df_tempo['horas_planeadas'] * 60
df_tempo['percentagem_paragem'] = (df_tempo['horas_paragem'] / df_tempo['minutos_planeados']) * 100
df_tempo = df_tempo.sort_values(by='maquina')
print("\n========== TAXA DE PARAGEM POR MAQUINA ==========\n")
for _, linha in df_tempo.iterrows():
    paragem = formatar_tempo(linha['horas_paragem'])
    planeado = formatar_tempo(linha['minutos_planeados'])
    print(f"Máquina {linha['maquina']} -> {linha['percentagem_paragem']:.2f}%" f"\n(paragem: {paragem} de {planeado} planeados)")

# Analise de turnos 
#12 - Quantidade de total de peças produzidas por turno
pecas_por_turno = (df.groupby("turno", as_index=False)['quantidade_produzida']
                   .sum()
                   .sort_values('quantidade_produzida', ascending=False)
                   .reset_index(drop=True)
                   )
print("\n========== PEÇAS PRODUZIDAS POR TURNO ==========\n")
for _, linha in pecas_por_turno.iterrows():
    print(f"Turno {linha['turno']} -> {linha['quantidade_produzida']} peças")

#13 - Indentificar o turno com maior e menor produçao
print("\n========== TURNO COM MENOR PRODUÇAO ==========\n")
turno_menor_producao = pecas_por_turno.iloc[-1]
print(f"Turno {turno_menor_producao['turno']} -> {turno_menor_producao['quantidade_produzida']} peças")
print("\n========== TURNO COM MAIOR PRODUÇAO ==========\n")
turno_maior_producao = pecas_por_turno.iloc[0]
print(f"Turno {turno_maior_producao['turno']} -> {turno_maior_producao['quantidade_produzida']} peças")

#14 - Peças defeituosas por turno 
pecas_defeituosas_por_turno = (df.groupby(['turno'], as_index=False)['quantidade_defeituosa']
                                .sum()
                                .sort_values('quantidade_defeituosa', ascending=False)
                                .reset_index(drop=True)
                                 )
print("\n========== PEÇAS DEFEITUOSAS POR TURNO ==========\n")
print(pecas_defeituosas_por_turno)

#15 - Taxa de defeitos por turno 
df_total_paragem = df.groupby('turno').agg(
            quantidade_produzida= ('quantidade_produzida', 'sum'), 
            quantidade_defeituosa = ('quantidade_defeituosa','sum')
            ).reset_index()

df_total_paragem['percentagem_defeito'] = (df_total_paragem['quantidade_defeituosa'] / df_total_paragem['quantidade_produzida']) * 100
df_total_paragem = df_total_paragem.sort_values(by='turno')
print("\n========== TAXA DE DEFEITOS POR TURNO ==========\n")
for _, linha in df_total_paragem.iterrows():
    print(f"Turno {linha['turno']} -> {linha['percentagem_defeito']:.2f}%")

#16 - Tempo de paragem de cada turno 
paragem_por_turno = (df.groupby(['turno'], as_index=False)['tempo_paragem_min']
                     .sum()
                     .sort_values(['tempo_paragem_min'], ascending=True)
                     .reset_index(drop=True)
                     )
print("\n========== PARAGEM POR TURNO ==========\n")
for _, linha in paragem_por_turno.iterrows():
    paragem = formatar_tempo(linha['tempo_paragem_min'])
    print(f"Turno {linha['turno']} -> {paragem} ")

#17 - Indentificar o turno com mais tempo de paragem comparada as horas planeadas
df_tempo_paragem = df.groupby('turno').agg(
            tempo_planeado = ('horas_planeadas', 'sum'), 
            tempo_paragem = ('tempo_paragem_min','sum')
            ).reset_index()

df_tempo_paragem['minutos_planeados'] = df_tempo_paragem['tempo_planeado'] * 60
df_tempo_paragem['percentagem_paragem'] = (df_tempo_paragem['tempo_paragem'] / df_tempo_paragem['minutos_planeados']) * 100
df_tempo_paragem = df_tempo_paragem.sort_values(by='percentagem_paragem', ascending=False)
print("\n========== TURNO COM MAIOR TEMPO DE PARAGEM ==========\n")

pior = df_tempo_paragem.iloc[0]
print(f"Turno com mais paragem: {pior['turno']} ({formatar_tempo(pior['tempo_paragem'])})\n")


#Análise da evolução diária da produção
#18 - quantidade de peças produzidas por dia 
df["Data"] = df["data"].dt.to_period("D").astype(str)

producao_dia = (df.groupby(["Data"], as_index=False)["quantidade_produzida"] 
                 .sum() .sort_values("Data", ascending=True) 
                 .reset_index(drop=True))
print("\n========== QUANTIDADE DE PEÇAS POR DIA ==========\n")
print(producao_dia)

#19 - o dia com mais produçao
print("\n========== DIA COM MAIS PEÇAS PRODUZIDAS ==========\n")
melhor = producao_dia.loc[producao_dia["quantidade_produzida"].idxmax()]
print("Dia com mais peças produzidas: "
      f"{melhor['Data']} -> {int(melhor['quantidade_produzida'])} peças\n")
    
#20 - o dia com menor produçao
print("\n========== DIA COM MENOS PEÇAS PRODUZIDAS ==========\n")
menor = producao_dia.loc[producao_dia["quantidade_produzida"].idxmin()]
print("Dia com menos peças produzidas: "
      f"{menor['Data']} -> {int(menor['quantidade_produzida'])} peças\n")

#21 - quantidade de peças defeituosas por dia 
defeituosas_por_dia = (df.groupby(["Data"], as_index=False)["quantidade_defeituosa"] 
                 .sum() .sort_values("Data", ascending=True) 
                 .reset_index(drop=True))
print("\n========== QUANTIDADE DE PEÇAS DEFEITUOSAS POR DIA ==========\n")
print(defeituosas_por_dia) 
#22 - taxa de defeitos diaria 
defeitos = df.groupby(['Data']).agg(
            quantidade_produzida= ('quantidade_produzida', 'sum'), 
            quantidade_defeituosa = ('quantidade_defeituosa','sum')
            ).reset_index()

defeitos['percentagem_defeito'] = (defeitos['quantidade_defeituosa'] / defeitos['quantidade_produzida']) * 100
defeitos = defeitos.sort_values(by='Data')
print("\n========== TAXA DE DEFEITOS POR DIA ==========\n")
for _, linha in defeitos.iterrows():
    print(f"Dia {linha['Data']} -> {linha['percentagem_defeito']:.2f}%")
#23 - dia com maior taxa de paragem
df_paragem_dia = df.groupby('Data').agg(
            tempo_planeado = ('horas_planeadas', 'sum'), 
            tempo_paragem = ('tempo_paragem_min','sum')
            ).reset_index()

df_paragem_dia['minutos_planeados'] = df_paragem_dia['tempo_planeado'] * 60
df_paragem_dia['percentagem_paragem'] = (df_paragem_dia['tempo_paragem'] / df_paragem_dia['minutos_planeados']) * 100

df_paragem_dia = df_paragem_dia.sort_values(by='tempo_paragem', ascending=False)
print("\n========== DIA COM MAIOR TEMPO DE PARAGEM ==========\n")

paragem_dia = df_paragem_dia.iloc[0]
print(f"Dia com mais tempo de paragem: {paragem_dia['Data']} "
      f"({formatar_tempo(paragem_dia['tempo_paragem'])})\n")

#Graficos
#24 - Grafico da produçao por maquina
plt.figure(figsize=(12, 5))
plt.title("PRODUÇÃO POR MAQUINA")
sns.barplot(x='maquina', y='quantidade_produzida', data=pecas_por_maquina).set(xlabel='Maquina',ylabel='Quantidade Produzida')
plt.savefig( caminho_saida / "Produção por máquina.png", dpi=300, bbox_inches="tight")
plt.close()

#25 - Grafico de taxa de defeitos por maquina
plt.figure(figsize=(12, 5)) 
plt.title("TAXA DE DEFEITOS POR MAQUINA")
sns.barplot(x='maquina', y='percentagem_defeito',data=df_total).set(xlabel="Maquina",ylabel='Taxa de defeitos (%)')
plt.savefig( caminho_saida / "Taxa de defeitos por máquina.png", dpi=300, bbox_inches="tight")
plt.close()

#26 - Grafico de producao por turno
plt.figure(figsize=(12, 5))
plt.title("PRODUÇÃO POR TURNO")
sns.barplot(x='turno', y='quantidade_produzida', data=pecas_por_turno).set(xlabel="Turno",ylabel='Quantidade Produzida')
for i, valor in enumerate(pecas_por_turno['quantidade_produzida']):
    if valor >= 0:
        plt.text(i, valor + 40, str(valor), ha='center', fontsize=7, fontweight='bold')
plt.savefig( caminho_saida / "Produção por turno.png", dpi=300, bbox_inches="tight")
plt.close()

#27 - Grafico Evoluçao diaria da produçao
producao_dia = producao_dia.sort_values("Data").reset_index(drop=True)
producao_dia["Dia"] = pd.to_datetime(producao_dia["Data"]).dt.day

# Localizar o dia de maior e de menor produção
linha_max = producao_dia.loc[producao_dia["quantidade_produzida"].idxmax()]
linha_min = producao_dia.loc[producao_dia["quantidade_produzida"].idxmin()]

plt.figure(figsize=(12, 5))
plt.plot(producao_dia["Dia"], producao_dia["quantidade_produzida"],
         marker="o", markersize=6, color="tab:blue")

# Destacar os dois pontos
plt.scatter(linha_max["Dia"], linha_max["quantidade_produzida"],
            color="green", s=120, zorder=3)
plt.scatter(linha_min["Dia"], linha_min["quantidade_produzida"],
            color="red", s=120, zorder=3)

# Anotar: máximo acima do ponto, mínimo abaixo
plt.annotate(f"Máx: dia {int(linha_max['Dia'])}\n{int(linha_max['quantidade_produzida']):,} peças",
             xy=(linha_max["Dia"], linha_max["quantidade_produzida"]),
             xytext=(0, 8), textcoords="offset points",
             ha="center", fontweight="bold", color="green")

plt.annotate(f"Mín: dia {int(linha_min['Dia'])}\n{int(linha_min['quantidade_produzida']):,} peças",
             xy=(linha_min["Dia"], linha_min["quantidade_produzida"]),
             xytext=(0, -27), textcoords="offset points",
             ha="center", fontweight="bold", color="red")

plt.xticks(producao_dia["Dia"])
plt.title("Evolução diária de produção")
plt.xlabel("Dia do mês")
plt.ylabel("Quantidade produzida")
plt.grid(True, linestyle="--", alpha=0.6)
plt.margins(y=0.15)
plt.savefig( caminho_saida / "Evolução diária da produção.png", dpi=300, bbox_inches="tight")
plt.close()

#28 - Grafico tempo de paragem por maquina
paragem_maquina = (df.groupby("maquina", as_index=False)["tempo_paragem_min"]
                   .sum()
                   .sort_values("maquina"))

paragem_maquina["horas_paragem"] = paragem_maquina["tempo_paragem_min"] / 60

plt.figure(figsize=(8, 5))
plt.bar(paragem_maquina["maquina"], paragem_maquina["horas_paragem"])

for i, horas in enumerate(paragem_maquina["horas_paragem"]):
    plt.text(i, horas + 1, f"{horas:.1f} h", ha="center", fontsize=10, fontweight="bold")

plt.title("Tempo de paragem por máquina")
plt.xlabel("Máquina")
plt.ylabel("Tempo de paragem (horas)")
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.savefig( caminho_saida / "Tempo de paragem por máquina.png", dpi=300, bbox_inches="tight")
plt.close()

#29 - grafico de Produção e paragens diárias
diario = df.groupby("Data").agg(
    quantidade_produzida=("quantidade_produzida", "sum"),
    minutos_paragem=("tempo_paragem_min", "sum")
).reset_index()

diario = diario.sort_values("Data").reset_index(drop=True)
diario["Dia"] = pd.to_datetime(diario["Data"]).dt.day
diario["horas_paragem"] = diario["minutos_paragem"] / 60

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

ax1.plot(diario["Dia"], diario["quantidade_produzida"],
         marker="o", markersize=7, color="tab:blue")
ax1.set_title("Evolução diária da produção")
ax1.set_ylabel("Peças produzidas")
ax1.grid(True, linestyle="--", alpha=0.6)

ax2.plot(diario["Dia"], diario["horas_paragem"],
         marker="o", markersize=7, color="tab:red")
ax2.set_title("Evolução diária do tempo de paragem")
ax2.set_xlabel("Dia do mês")
ax2.set_ylabel("Tempo de paragem (horas)")
ax2.set_xticks(diario["Dia"])
ax2.grid(True, linestyle="--", alpha=0.6)

fig.suptitle("Produção e paragens diárias", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig( caminho_saida / "Produção e paragens diárias.png", dpi=300, bbox_inches="tight")
plt.close()