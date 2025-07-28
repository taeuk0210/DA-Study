import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd


def pieplot(df, colname, dropna=True):
    fig, axe = plt.subplots(1, 2, figsize=(10, 5))  # 도넛 2개 가로 배치
    if dropna:
        df[colname] = df[colname].dropna().astype(str)  # 문자열로 변환
        unique_vals = df[colname].unique()
        unique_vals = [v for v in unique_vals if pd.notna(v) and str(v)!='nan']
    else:
        df[colname] = df[colname].astype(str)
        unique_vals = df[colname].dropna().unique()
    colors = sns.color_palette("Set2", len(unique_vals))  # 고유값 수만큼 색상
    palette = dict(zip(sorted(unique_vals), colors))  # 값과 색상 매핑

    for i, label in enumerate(["적합", "부적합"]):
        grouped = df[df["평가결과라벨"] == label].groupby(colname)["업체정보_인증번호"].count()
        grouped = grouped[grouped > 0]  # 0 이상만 사용
        sorted_keys = sorted(grouped.index)  # 정렬된 키
        sorted_keys = [k for k in sorted_keys if k != 'nan']

        # 도넛 차트 그리기
        wedges, texts, autotexts = axe[i].pie(
            grouped[sorted_keys],
            labels=sorted_keys,
            autopct="%1.1f%%",
            colors=[palette[k] for k in sorted_keys],
            wedgeprops={'width': 0.5},  # 도넛 스타일로 변경됨
            
        )
        for text in texts:
            text.set_fontsize(15)  # 라벨 폰트 크기 설정
        for autotext in autotexts:
            x, y = autotext.get_position()  # 기존 위치 좌표
            autotext.set_position((1.3 * x, 1.3 * y))  # 기존보다 바깥쪽으로 이동
            autotext.set_fontsize(15)  # 글씨 크기
            autotext.set_color("black")  # 글씨 색상
            # autotext.set_fontweight("bold")  # 글씨 굵게
        # axe[i].set_title(f"평가결과라벨: {label}")
        
        # 가운데에 label 텍스트 추가
        axe[i].text(0, 0, label, ha='center', va='center', fontsize=15)  # 중심에 텍스트 삽입

    plt.tight_layout()
    plt.show()
    return



def barplot(df, colname):
    fig, axe = plt.subplots(1, 2, figsize=(10,3))
    df[colname] = df[colname].dropna().astype(str)  # 문자열로 변환
    unique_vals = df[colname].unique()
    unique_vals = [v for v in unique_vals if pd.notna(v)]
    colors = sns.color_palette("Set2", len(unique_vals))
    palette = dict(zip(sorted(unique_vals), colors))

    for i, label in enumerate(["적합", "부적합"]):
        grouped = df[df["평가결과라벨"]==label].groupby([colname])[["평가결과라벨", "업체정보_인증번호"]].count().reset_index()
        sns.barplot(data=grouped[grouped[colname] != '-'], x=colname, y="업체정보_인증번호", hue=colname, palette=palette, ax=axe[i])
        axe[i].set_xticks(grouped[colname].values)
        if (type(grouped[colname][0])==type("str") and max([len(c) for c in grouped[colname].unique()]) >= 6):
            axe[i].tick_params(axis='x', rotation=90)
        axe[i].set_xlabel(colname)
        axe[i].set_ylabel("")
        axe[i].set_title(f"평가결과라벨: {label}")
    
        if (axe[i].get_legend() and len(grouped[colname].unique())>10):
            axe[i].get_legend().remove()
    plt.show()
    return

def violinplot(df, colname):
    fig, axe = plt.subplots(1, 1, figsize=(10,3))

    sns.violinplot(x="평가결과라벨", y=colname, data=df, hue="평가결과라벨", palette="Set2", order=["적합", "부적합"], hue_order=["적합", "부적합"], ax=axe)
    axe.set_xlabel(colname)
    plt.grid(True)
    plt.show()
    return

def histplot(df, colname):
    fig, axe = plt.subplots(1, 3, figsize=(15,3))

    colors = sns.color_palette("Set2", 2)
    palette = dict(zip(["적합", "부적합"], colors))

    for i, label in enumerate(["적합", "부적합"]):
        grouped = df.loc[df["평가결과라벨"]==label, ["평가결과라벨", colname]]
        sns.histplot(x=colname, data=grouped, hue="평가결과라벨", palette=palette, ax=axe[i])
        axe[i].set_xlabel(colname)
        axe[i].set_title(f"평가결과라벨: {label}")

    sns.histplot(x=colname, data=df, hue="평가결과라벨", palette=palette, ax=axe[2])
    axe[2].set_xlabel(colname)
    axe[2].set_title(f"적합/부적합 비교")
    plt.show()
    return

def stackedbarplot(df):
    pivot = df.pivot_table(index="평가대상", columns="평가결과라벨", values="업체정보_인증번호", aggfunc="sum", fill_value=0)

    # ▶ 비율로 정규화
    pivot_ratio = pivot.div(pivot.sum(axis=1), axis=0) * 100

    # ▶ 색상코드 수동 지정 (원하는 평가결과라벨만 지정하면 됨)
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
    plt.legend(title="평가결과라벨", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.show()



def pieplot_two(df, colname):

    fig, axe = plt.subplots(1, 2, figsize=(16,8))

    colors = sns.color_palette("Set2", 2)
    palette = dict(zip(["적합", "부적합"], colors))

    for i, label in enumerate(["적합", "부적합"]):
        grouped = df.loc[df["평가결과라벨"]==label, ["평가결과라벨", colname]]
        
        data = pd.DataFrame(grouped["업체정보_제조/급식"].value_counts())
        data = {k:v[0] for k,v in zip(data.index, data.values)}

        # 2 level pie chart
        # 분류
        outer_labels = ['제조', '기타']
        outer_sizes = [data['제조'], sum(v for k, v in data.items() if k != '제조')]

        # 내부용 데이터 (제조 제외)
        inner_labels = [k for k in data if k != '제조']
        inner_sizes = [data[k] for k in inner_labels]

        # 색상
        outer_colors = ['#66c2a5', '#fc8d62']
        inner_colors = plt.cm.Set3.colors[:len(inner_labels)]  # Set3에서 적당히 뽑기

        # 바깥쪽 도넛 (제조 vs 비제조)
        _, _, autotexts_outer = axe[i].pie(outer_sizes,
            radius=1,
            labels=outer_labels,
            # labeldistance=0.75,
            colors=outer_colors,
            wedgeprops=dict(width=0.4, edgecolor='white'),
            autopct='%1.1f%%')
        

        for autotext in autotexts_outer:
            x, y = autotext.get_position()  # 기존 위치 좌표
            autotext.set_position((1.4 * x, 1 * y)) 

        axe[i].legend()

        # 안쪽 도넛 (비제조 항목들)
        _, _, autotexts_inner = axe[i].pie(inner_sizes,
            radius=0.7,
            labels=inner_labels,
            labeldistance=0.75,
            colors=inner_colors,
            wedgeprops=dict(width=0.4, edgecolor='white'),
            autopct='%1.1f%%')
        
        for autotext in autotexts_inner:
            x, y = autotext.get_position()  # 기존 위치 좌표
            autotext.set_position((1 * x, 0.84 * y)) 
        
        axe[i].text(0, 0, label, ha='center', va='center', fontsize=15)
    plt.show()
    return