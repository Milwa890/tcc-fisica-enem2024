# -*- coding: utf-8 -*-
"""
Gera as figuras do TCC "Análise de erros nas questões de Física do ENEM 2024".

Este script NÃO lê os microdados. Ele usa as três planilhas que o notebook
TCC_Fisica_ENEM2024_distratores.ipynb grava na pasta processed/:
  - analise_fisica_ENEM2024.xlsx       (Etapa 7: acerto e escolha das alternativas)
  - curvas_distratores_ENEM2024.xlsx   (Etapa 5: curvas por nível de desempenho)
  - tri_parametros_ENEM2024.xlsx       (Etapa 6: parâmetros a, b, c e acerto previsto)

Uso (no Colab, depois de rodar o notebook):
    !python gerar_figuras_tcc.py "/content/drive/MyDrive/TCC Melissa/enem-fisica/processed"
As figuras são salvas em processed/figuras_tcc/.

Figuras geradas (numeração do TCC):
  fig2_fluxo_base_analitica.png         -> Figura 2
  fig3_acerto_por_questao.png           -> Figura 3
  fig4_b_vs_acerto.png                  -> Figura 4
  fig5_previsto_vs_observado.png        -> Figura 5
  fig6_curvas_concepcao_alternativa.png -> Figura 8  (questões 103 e 132)
  fig7_curvas_conhecimento_parcial.png  -> Figura 14 (questões 121 e 91)
  figB1.png, figB2.png                  -> Figuras 15 e 16 (Apêndice B)
"""
import os, sys
PASTA = sys.argv[1] if len(sys.argv) > 1 else "processed"
import pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

an = pd.read_excel(os.path.join(PASTA, "analise_fisica_ENEM2024.xlsx"), sheet_name="Distratores por questão")
cv = pd.read_excel(os.path.join(PASTA, "curvas_distratores_ENEM2024.xlsx"), sheet_name="Regua 2 - acertos CN")
tri = pd.read_excel(os.path.join(PASTA, "tri_parametros_ENEM2024.xlsx"), sheet_name="Parametros e acerto")
OUT = os.path.join(PASTA, "figuras_tcc") + os.sep
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({"font.family": "serif", "font.serif": ["Liberation Serif", "Times New Roman", "DejaVu Serif"],
                     "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#555555", "axes.labelcolor": "#222222", "xtick.color": "#444444",
                     "ytick.color": "#444444", "axes.grid": False})
INK, MUTED, GRID = "#222222", "#666666", "#dddddd"
AREA = {91: "Mecânica", 96: "Mecânica", 119: "Mecânica", 121: "Mecânica",
        103: "Termologia", 122: "Termologia", 129: "Termologia", 130: "Termologia",
        99: "Ondulatória", 101: "Ondulatória", 106: "Ondulatória",
        100: "Óptica Geométrica", 127: "Eletromagnetismo", 131: "Eletromagnetismo", 132: "Eletromagnetismo"}
CAT = {"Mecânica": "#2a78d6", "Termologia": "#eb6834", "Ondulatória": "#1baf7a",
       "Eletromagnetismo": "#eda100", "Óptica Geométrica": "#e87ba4"}
v = an[an.Situacao == "Válida"].copy()
v["Area"] = v.Questao.map(AREA)

# ---------- Figura 2: fluxo da base analítica (mesmo estilo da Figura 1) ----------
def fluxo(steps, fn):
    h = 1.25 * len(steps)
    fig, ax = plt.subplots(figsize=(5.9, h)); ax.axis("off")
    ax.set_xlim(0, 10); ax.set_ylim(0, len(steps) * 2)
    for i, s in enumerate(steps):
        y = (len(steps) - 1 - i) * 2 + 0.4
        ax.add_patch(FancyBboxPatch((0.6, y), 8.8, 1.2, boxstyle="round,pad=0.02,rounding_size=0.12",
                                    fc="#eaf2fa", ec="#1f4e78", lw=1.4))
        ax.text(5, y + 0.6, s, ha="center", va="center", fontsize=11, color="#1f2a36",
                family="DejaVu Sans")
        if i < len(steps) - 1:
            ax.annotate("", xy=(5, y - 0.75), xytext=(5, y), arrowprops=dict(arrowstyle="-|>", color="#1f4e78", lw=1.6))
    plt.savefig(OUT + fn, dpi=200, bbox_inches="tight"); plt.close()
fluxo(["Taxa de acerto e escolha de cada alternativa", "Integração com os parâmetros da TRI (a, b, c)",
       "Integração com a classificação de Física", "Curvas de escolha das alternativas\npor nível de desempenho",
       "Análises estatísticas e visualizações"], "fig2_fluxo_base_analitica.png")

# ---------- Figura 3: acerto por questão + distrator mais escolhido ----------
s = v.sort_values("Taxa_Acerto_%")
fig, ax = plt.subplots(figsize=(6.3, 5.6))
y = np.arange(len(s))
ax.barh(y, s["Taxa_Acerto_%"], color=[CAT[a] for a in s.Area], height=0.62, zorder=2)
ax.scatter(s["%Distrator_mais_escolhido"], y, marker="D", s=34, facecolor="white", edgecolor=INK, lw=1.2, zorder=3)
for yi, (acc, dis) in enumerate(zip(s["Taxa_Acerto_%"], s["%Distrator_mais_escolhido"])):
    lab = f"{acc:.1f}".replace(".", ",")
    if acc - 4.5 < dis < acc + 0.5:
        ax.text(acc + 0.6, yi, lab, va="center", ha="left", fontsize=8, color=INK, fontweight="bold", zorder=4)
    else:
        ax.text(acc - 0.6, yi, lab, va="center", ha="right", fontsize=8, color="white", fontweight="bold", zorder=4)
ax.axvline(20, color=MUTED, ls=(0, (4, 3)), lw=0.9, zorder=1)
ax.text(20.4, len(s) - 0.35, "escolha aleatória (1 em 5 = 20%)", fontsize=8, color=MUTED, va="bottom")
for yi, (dis, letra) in enumerate(zip(s["%Distrator_mais_escolhido"], s["Distrator_mais_escolhido"])):
    ax.text(dis + 0.9, yi + 0.02, letra, va="center", ha="left", fontsize=8.5, color=INK, fontweight="bold", zorder=4)
ax.set_yticks(y); ax.set_yticklabels([f"Q{q} (gab. {g})" for q, g in zip(s.Questao, s.Gabarito)], fontsize=9)
ax.set_xlim(0, 50); ax.set_xlabel("Porcentagem dos participantes (%)")
ax.xaxis.grid(True, color=GRID, lw=0.6, zorder=0)
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
h = [Patch(color=CAT[a], label=a) for a in CAT] + [Line2D([], [], marker="D", ls="", mfc="white", mec=INK, label="Distrator mais escolhido (letra da alternativa)")]
ax.legend(handles=h, fontsize=8, frameon=False, loc="upper center", bbox_to_anchor=(0.45, -0.13), ncol=3)
plt.tight_layout(); plt.savefig(OUT + "fig3_acerto_por_questao.png", dpi=300); plt.close()

# ---------- Figura 4: b (escala da nota) × acerto, cor = c ----------
fig, ax = plt.subplots(figsize=(6.3, 4.4))
from matplotlib.colors import LinearSegmentedColormap
cm = LinearSegmentedColormap.from_list("b", ["#cde2fb", "#6da7ec", "#2a78d6", "#104281"])
sc = ax.scatter(tri.b_escala_nota, tri["Acerto_observado_%"], c=tri.c, cmap=cm, vmin=0, vmax=0.3,
                s=46, edgecolor=INK, lw=0.7, zorder=3)
off = {100: (6, 6), 103: (6, -10), 119: (6, 4), 121: (-26, -4), 131: (-28, 4), 132: (6, -4), 127: (6, 4),
       101: (6, -10), 122: (6, 2), 91: (6, -8), 96: (6, 4), 99: (6, 4), 106: (6, 4), 130: (6, -8)}
for _, r in tri.iterrows():
    ax.annotate(f"Q{int(r.Questao)}", (r.b_escala_nota, r["Acerto_observado_%"]), textcoords="offset points",
                xytext=off.get(int(r.Questao), (6, 4)), fontsize=8, color=INK)
ax.axhline(20, color=MUTED, ls=(0, (4, 3)), lw=0.9)
ax.text(541, 20.6, "escolha aleatória (1 em 5 = 20%)", fontsize=8, color=MUTED)
cb = fig.colorbar(sc, ax=ax, pad=0.02); cb.set_label("Parâmetro c (acerto ao acaso)", fontsize=9)
cb.ax.tick_params(labelsize=8)
ax.set_xlabel("Dificuldade b na escala da nota (100·b + 500)"); ax.set_ylabel("Taxa de acerto observada (%)")
ax.set_xlim(535, 750); ax.set_ylim(0, 48); ax.yaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
plt.tight_layout(); plt.savefig(OUT + "fig4_b_vs_acerto.png", dpi=300); plt.close()

# ---------- Figura 5: previsto × observado ----------
fig, ax = plt.subplots(figsize=(4.8, 4.6))
ax.plot([0, 48], [0, 48], color=MUTED, ls=(0, (4, 3)), lw=0.9)
ax.scatter(tri["Acerto_previsto_TRI_%"], tri["Acerto_observado_%"], s=40, color="#2a78d6", edgecolor=INK, lw=0.7, zorder=3)
for _, r in tri.iterrows():
    q = int(r.Questao)
    if abs(r.Diferenca_obs_menos_prev_pp) > 1.5 or q in (103, 132, 127):
        ax.annotate(f"Q{q}", (r["Acerto_previsto_TRI_%"], r["Acerto_observado_%"]), textcoords="offset points",
                    xytext=(-24, 2) if q == 119 else (6, -3), fontsize=8, color=INK)
ax.text(34, 31, "previsto = observado", fontsize=8, color=MUTED, rotation=42)
ax.set_xlim(10, 46); ax.set_ylim(10, 46)
ax.set_xlabel("Acerto previsto pelo modelo da TRI (%)"); ax.set_ylabel("Acerto observado (%)")
ax.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
plt.tight_layout(); plt.savefig(OUT + "fig5_previsto_vs_observado.png", dpi=300); plt.close()

# ---------- Figuras 6 e 7: curvas de escolha (régua: acertos nos demais itens de CN) ----------
GAB = dict(zip(v.Questao, v.Gabarito))
DCOL = ["#2a78d6", "#eb6834", "#1baf7a", "#e87ba4"]
DMK = ["o", "s", "^", "v"]
TIT = {103: "Q103 – aquecedor solar", 132: "Q132 – lâmpadas em série", 121: "Q121 – Calvin e o balanço",
       91: "Q91 – zona de deformação"}
def curvas(qs, fn):
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.3), sharey=True)
    for ax, q in zip(axes, qs):
        d = cv[(cv.Questao == q) & (cv.Participantes >= 1000)]
        g = GAB[q]; k = 0; ends = []
        for alt in "ABCDE":
            if alt == g:
                ax.plot(d.Acertos_demais_itens, d[alt], color=INK, lw=2.2, zorder=3)
                ends.append([d[alt].iloc[-1], f"{alt} (gabarito)"])
            else:
                ax.plot(d.Acertos_demais_itens, d[alt], color=DCOL[k], lw=1.2, marker=DMK[k], ms=3, markevery=3)
                ends.append([d[alt].iloc[-1], alt]); k += 1
        ends.sort()
        for i in range(1, len(ends)):
            if ends[i][0] - ends[i-1][0] < 4.5: ends[i][0] = ends[i-1][0] + 4.5
        xe = d.Acertos_demais_itens.iloc[-1] + 0.8
        for yv, lab in ends:
            ax.text(xe, yv, lab, fontsize=7.5, va="center", color=INK)
        ax.set_title(TIT[q], fontsize=9.5, color=INK)
        ax.set_xlim(0, 47); ax.set_ylim(0, 85)
        ax.yaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
        ax.set_xlabel("Acertos nos demais itens de CN", fontsize=9)
    axes[0].set_ylabel("Escolha da alternativa (%)")
    plt.tight_layout(); plt.savefig(OUT + fn, dpi=300); plt.close()
curvas([103, 132], "fig6_curvas_concepcao_alternativa.png")
curvas([121, 91], "fig7_curvas_conhecimento_parcial.png")


DCOL = ["#2a78d6", "#eb6834", "#1baf7a", "#e87ba4"]; DMK = ["o", "s", "^", "v"]

# ---------- Figuras 15 e 16 (Apêndice B): curvas das 14 questões ----------
plt.rcdefaults()
plt.rcParams.update({"font.family": "serif", "font.serif": ["Liberation Serif", "DejaVu Serif"], "font.size": 9,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#555555"})
TEMA = {91: "zona de deformação", 96: "centro de massa", 99: "efeito Doppler", 100: "mirascópio",
        101: "nível sonoro", 103: "aquecedor solar", 106: "raios X", 119: "composição de velocidades",
        121: "Calvin e o balanço", 122: "isolamento térmico", 127: "blindagem eletrostática", 130: "ciclo de Otto",
        131: "LED e resistores", 132: "lâmpadas em série"}
def painel(qs, fn):
    rows = (len(qs) + 1) // 2
    fig, axes = plt.subplots(rows, 2, figsize=(6.6, 2.35 * rows), sharex=True, sharey=True)
    for ax, q in zip(axes.flat, qs):
        dd = cv[(cv.Questao == q) & (cv.Participantes >= 1000)].sort_values("Acertos_demais_itens")
        g = GAB[q]; k = 0; ends = []
        for alt in "ABCDE":
            if alt == g:
                ax.plot(dd.Acertos_demais_itens, dd[alt], color=INK, lw=2.0, zorder=3)
                ends.append([dd[alt].iloc[-1], f"{alt} (gab.)"])
            else:
                ax.plot(dd.Acertos_demais_itens, dd[alt], color=DCOL[k], lw=1.1, marker=DMK[k], ms=2.5, markevery=3)
                ends.append([dd[alt].iloc[-1], alt]); k += 1
        ends.sort()
        for i in range(1, len(ends)):
            if ends[i][0] - ends[i-1][0] < 5: ends[i][0] = ends[i-1][0] + 5
        xe = dd.Acertos_demais_itens.iloc[-1] + 0.8
        for yv, lab in ends: ax.text(xe, yv, lab, fontsize=7, va="center", color=INK)
        ax.set_title(f"Q{q} – {TEMA[q]}", fontsize=8.5, color=INK)
        ax.set_xlim(0, 50); ax.set_ylim(0, 102); ax.set_yticks([0,20,40,60,80,100])
        ax.yaxis.grid(True, color=GRID, lw=0.5); ax.set_axisbelow(True)
    for ax in axes.flat[len(qs):]: ax.axis("off")
    for ax in axes[-1]: ax.set_xlabel("Acertos nos demais itens de CN", fontsize=8)
    for ax in axes[:, 0]: ax.set_ylabel("Escolha (%)", fontsize=8)
    plt.tight_layout(); plt.savefig(OUT + fn, dpi=250); plt.close()
painel([91, 96, 99, 100, 101, 103, 106, 119], "figB1.png")
painel([121, 122, 127, 130, 131, 132], "figB2.png")

print("Figuras salvas em", OUT)
