import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd

def barplot(df, colname):
    fig, axe = plt.subplots(1, 2, figsize=(10,3))
    df[colname] = df[colname].astype(str)
    unique_vals = df[colname].dropna().unique()
    colors = sns.color_palette("Set2", len(unique_vals))
    palette = dict(zip(sorted(unique_vals), colors))

    for i, label in enumerate(["적합", "부적합"]):
        grouped= df[df["평가결과"]==label].groupby([colname])[["평가결과", "인증번호"]].count().reset_index()
        sns.barplot(data=grouped, x=colname, y="인증번호", hue=colname, palette=palette, ax=axe[i])
        axe[i].set_xticks(grouped[colname].values)
        if (type(grouped[colname][0])==type("str") and max([len(c) for c in grouped[colname].unique()]) >= 6):
            axe[i].tick_params(axis='x', rotation=90)
        axe[i].set_xlabel(colname)
        axe[i].set_ylabel("")
        axe[i].set_title(f"평가결과: {label}")
    
        if (axe[i].get_legend() and len(grouped[colname].unique())>10):
            axe[i].get_legend().remove()
    plt.show()
    return

def violinplot(df, colname):
    fig, axe = plt.subplots(1, 1, figsize=(10,3))

    sns.violinplot(x="평가결과", y=colname, data=df, hue="평가결과", palette="Set2", order=["적합", "부적합"], hue_order=["적합", "부적합"], ax=axe)
    axe.set_xlabel(colname)
    plt.grid(True)
    plt.show()
    return

def histplot(df, colname):
    fig, axe = plt.subplots(1, 3, figsize=(15,3))

    colors = sns.color_palette("Set2", 2)
    palette = dict(zip(["적합", "부적합"], colors))

    for i, label in enumerate(["적합", "부적합"]):
        grouped = df.loc[df["평가결과"]==label, ["평가결과", colname]]
        sns.histplot(x=colname, data=grouped, hue="평가결과", palette=palette, ax=axe[i])
        axe[i].set_xlabel(colname)
        axe[i].set_title(f"평가결과: {label}")

    sns.histplot(x=colname, data=df, hue="평가결과", palette=palette, ax=axe[2])
    axe[2].set_xlabel(colname)
    axe[2].set_title(f"적합/부적합 비교")
    plt.show()
    return

def stackedbarplot(df):
    pivot = df.pivot_table(index="평가대상", columns="평가결과", values="인증번호", aggfunc="sum", fill_value=0)

    # ▶ 비율로 정규화
    pivot_ratio = pivot.div(pivot.sum(axis=1), axis=0) * 100

    # ▶ 색상코드 수동 지정 (원하는 평가결과만 지정하면 됨)
    custom_colors = {
        "적합종결": "#90D1CA",
        "적합": "#90D1CA",
        "자체평가완료": "#129990",

        "부적합": "#096B68",
        "부적합종결": "#096B68",
        "미보완종결": "#F49BAB",
        "인증취소": "#FFE1E0",
        "취소예정": "#2A4759",

        "평가불능":"#FFFBDE",
        "심사불가": "#FFFBDE",
        "만료": "#7F55B1",
        "반납": "#9B7EBD",
        "기타":"#FF9F00",
        "소재지이전/규모전환":"#CB0404",
        "폐업":"#4ED7F1"
    }

    # ▶ 그래프 그리기
    ax = pivot_ratio.plot(kind="bar", stacked=True, figsize=(8, 6), color=[custom_colors.get(col, "#BBBBBB") for col in pivot.columns])

    # ▶ 스타일
    plt.ylabel("비율 (%)")
    plt.xlabel("평가대상")
    plt.legend(title="평가결과", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.show()
