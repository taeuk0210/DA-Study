import pandas as pd


def get_dataframe():
    df_cert_comp = pd.read_csv("./data/HACCP_조사평가_2024_인증원_축산물_업체정보.csv")
    df_cert_eval = [
        pd.read_csv("./data/HACCP_조사평가_2024_인증원_축산물_1차평가.csv"),
        pd.read_csv("./data/HACCP_조사평가_2024_인증원_축산물_2차평가.csv"),
    ]
    df_loc1_comp = pd.read_csv("./data/HACCP_조사평가_2024_지방청_축산물_업체정보.csv")
    df_loc1_eval = [
        pd.read_csv("./data/HACCP_조사평가_2024_지방청_축산물_1차평가.csv"),
        pd.read_csv("./data/HACCP_조사평가_2024_지방청_축산물_2차평가.csv"),
        pd.read_csv("./data/HACCP_조사평가_2024_지방청_축산물_3차평가.csv"),
        pd.read_csv("./data/HACCP_조사평가_2024_지방청_축산물_4차평가.csv"),
    ]
    df_loc2_comp = pd.read_csv("./data/HACCP_조사평가_2024_지방청_식품_업체정보.csv")
    df_loc2_eval = [
        pd.read_csv("./data/HACCP_조사평가_2024_지방청_식품_1차평가.csv"),
        pd.read_csv("./data/HACCP_조사평가_2024_지방청_식품_2차평가.csv"),
        pd.read_csv("./data/HACCP_조사평가_2024_지방청_식품_3차평가.csv"),
        pd.read_csv("./data/HACCP_조사평가_2024_지방청_식품_4차평가.csv"),
    ]
    
    info_columns = [
    "인증번호", "업체명", "규모", "평가대상", "적용품목", "의무/자율", "최초인증일", "인증시작일", "인증만료일", "관할청", "인증유지여부"
]

    df_cert_comp = df_cert_comp[[
        '인증번호', '업체명', '규모', '24년대상', '적용품목', '의무/자율', '최초인증일자', '인증시작일', '인증만기일', '지원', '인증유지여부'
    ]]
    df_loc1_comp = df_loc1_comp[[
        '인증번호', '업소명', '규모', '★조사평가대상(현재)', '유형', '의무/자율', '최초인증일', '인증시작일', '인증만료일', '관할지역', '취소내용(반납,만료,인증취소)'
    ]]
    df_loc2_comp = df_loc2_comp[[
        '인증번호', '업체명', '규모', '평가대상(확정)', '식품종,군', '의무/자율', '최초인증', '인증일', '만료일', '관할청', '취소내용'
    ]]

    df_cert_comp.columns = info_columns
    df_loc1_comp.columns = info_columns
    df_loc2_comp.columns = info_columns

    df_cert_comp["인증주체"] = "인증원"
    df_cert_comp["카테고리"] = "축산물"
    df_loc1_comp["인증주체"] = "지방청"
    df_loc1_comp["카테고리"] = "축산물"
    df_loc2_comp["인증주체"] = "지방청"
    df_loc2_comp["카테고리"] = "식품"

    df_info = pd.concat([
        df_cert_comp, df_loc1_comp, df_loc2_comp
    ], axis=0)
    df_info = df_info[~df_info["인증번호"].isna()]
    
    eval_columns = ['인증번호', '총점', '평가일', '평가결과']

    dfs = []

    for i, df in enumerate(df_cert_eval):
        df = df[['인증번호', '총점', '심사일', '최종심사결과']]
        df.columns = eval_columns
        df["평가차수"] = f"{i+1}차"
        df["인증주체"] = "인증원"
        df["카테고리"] = "축산물"

        dfs.append(df)
    for i, df in enumerate(df_loc1_eval):
        df = df[['인증번호', f'총점({i+1}차)', f'평가일({i+1}차)', f'평가결과({i+1}차)']]
        df.columns = eval_columns
        df["평가차수"] = f"{i+1}차"
        df["인증주체"] = "지방청"
        df["카테고리"] = "축산물"
        dfs.append(df)

    for i, df in enumerate(df_loc2_eval):
        df = df[['인증번호', f'총점({i+1}차)', f'평가일({i+1}차)' if i>0 else '평가일', f'평가결과및불능사유({i+1}차)']]
        df.columns = eval_columns
        df["평가차수"] = f"{i+1}차"
        df["인증주체"] = "지방청"
        df["카테고리"] = "식품"
        dfs.append(df)

    df_eval = pd.concat(dfs, axis=0)
    df_eval = df_eval[~df_eval["평가결과"].isna()]

    return df_info.merge(df_eval, on=["인증번호", "인증주체", "카테고리"], how="right")